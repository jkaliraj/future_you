"""API route definitions for FutureYou."""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from agents.commander import create_commander_agent
from profile.builder import load_seed_profile, get_or_create_profile
from db.firestore import (
    get_profile,
    get_decisions,
    save_decision,
    get_session,
    save_session,
    update_session,
    save_event,
    override_decision,
    update_profile,
)
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
import uuid
from datetime import datetime, timedelta


router = APIRouter()


# --- Request / Response Models ---

class OnboardRequest(BaseModel):
    user_id: str


class ActivateRequest(BaseModel):
    user_id: str
    duration_minutes: int = 180
    mode: str = "dry-run"
    message: str = ""


class DeactivateRequest(BaseModel):
    user_id: str
    session_id: str


class TriggerEventRequest(BaseModel):
    user_id: str
    session_id: str
    event_type: str
    event_data: dict


class OverrideRequest(BaseModel):
    user_id: str
    correction: str
    undo: bool = False


# --- Endpoints ---

@router.post("/onboard")
async def onboard(req: OnboardRequest):
    """Load pre-built profile from Firestore (demo: instant)."""
    profile = load_seed_profile(req.user_id)
    return {"status": "ready", "profile": profile}


@router.post("/activate")
async def activate(req: ActivateRequest):
    """Activate FutureYou session. Mode: 'dry-run' or 'live'."""
    profile = get_profile(req.user_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found. Call /onboard first.")

    session_id = f"sess_{uuid.uuid4().hex[:8]}"
    session = {
        "session_id": session_id,
        "started_at": datetime.utcnow().isoformat(),
        "ended_at": None,
        "status": "active",
        "mode": req.mode,
        "offline_message": req.message,
        "deactivates_at": (datetime.utcnow() + timedelta(minutes=req.duration_minutes)).isoformat(),
    }
    save_session(req.user_id, session)
    return {
        "session_id": session_id,
        "status": "active",
        "mode": req.mode,
        "monitoring": True,
        "deactivates_at": session["deactivates_at"],
    }


@router.post("/trigger-event")
async def trigger_event(req: TriggerEventRequest):
    """Simulate an incoming event. Commander agent processes it and returns a decision."""
    session = get_session(req.user_id, req.session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found.")
    if session.get("status") != "active":
        raise HTTPException(status_code=400, detail="Session is not active.")

    mode = session.get("mode", "dry-run")

    # Save the incoming event
    event_id = f"evt_{uuid.uuid4().hex[:6]}"
    event_record = {
        "event_id": event_id,
        "event_type": req.event_type,
        "event_data": req.event_data,
        "status": "processing",
        "assigned_agent": f"{req.event_type}_agent",
        "created_at": datetime.utcnow().isoformat(),
    }
    save_event(req.user_id, event_record)

    # Run Commander agent
    commander = create_commander_agent(req.user_id)
    session_service = InMemorySessionService()
    runner = Runner(
        agent=commander,
        app_name="futureyou",
        session_service=session_service,
    )

    adk_session = await session_service.create_session(
        app_name="futureyou",
        user_id=req.user_id,
    )

    prompt = f"""Mode: {mode}.
Handle this {req.event_type} event:
{req.event_data}

Remember: if mode is dry-run, describe what you WOULD do but do NOT execute tools.
Provide your decision, action, reasoning, and confidence score."""

    result_text = ""
    async for event in runner.run_async(
        user_id=req.user_id,
        session_id=adk_session.id,
        new_message=prompt,
    ):
        if event.is_final_response():
            result_text = event.content.parts[0].text if event.content and event.content.parts else str(event.content)

    # Save decision
    decision = {
        "decision_id": f"dec_{uuid.uuid4().hex[:6]}",
        "session_id": req.session_id,
        "agent_name": f"{req.event_type}_agent",
        "event_type": req.event_type,
        "event_summary": str(req.event_data),
        "action_taken": result_text,
        "reasoning": "Based on Work Personality Profile",
        "confidence": 0.9,
        "status": "completed",
        "executed": mode == "live",
        "human_override": False,
        "created_at": datetime.utcnow().isoformat(),
    }
    save_decision(req.user_id, decision)

    return {"decision": decision}


@router.post("/deactivate")
async def deactivate(req: DeactivateRequest):
    """End the FutureYou session and return summary."""
    session = get_session(req.user_id, req.session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found.")

    update_session(req.user_id, req.session_id, {
        "status": "deactivated",
        "ended_at": datetime.utcnow().isoformat(),
    })

    decisions = get_decisions(req.user_id, req.session_id)
    summary = {
        "total_decisions": len(decisions),
        "emails_handled": sum(1 for d in decisions if d.get("event_type") == "email"),
        "meetings_handled": sum(1 for d in decisions if d.get("event_type") == "calendar"),
        "tasks_handled": sum(1 for d in decisions if d.get("event_type") == "task"),
        "files_handled": sum(1 for d in decisions if d.get("event_type") == "file"),
        "flagged_for_review": sum(1 for d in decisions if d.get("confidence", 1) < 0.7),
    }
    return {"status": "deactivated", "summary": summary, "decisions": decisions}


@router.get("/decisions/{user_id}")
async def get_decision_log(user_id: str, session_id: str | None = None):
    """Get the decision log for a user, optionally filtered by session."""
    decisions = get_decisions(user_id, session_id)
    return {"decisions": decisions}


@router.get("/profile/{user_id}")
async def get_user_profile(user_id: str):
    """Get the current Work Personality Profile."""
    profile = get_profile(user_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found.")
    return {"profile": profile}


@router.post("/decisions/{decision_id}/override")
async def override(decision_id: str, req: OverrideRequest):
    """Human overrides a decision. Profile updated from correction."""
    override_decision(req.user_id, decision_id, req.correction)
    return {"status": "overridden", "decision_id": decision_id, "profile_updated": True}
