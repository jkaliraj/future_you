"""Firestore client — handles all database operations.

All data is stored in Firestore (profiles, sessions, decisions, events, agent memory).
No Cloud SQL needed.
"""

from google.cloud import firestore

_db = None


def _get_db() -> firestore.Client:
    """Get or create Firestore client (uses ADC)."""
    global _db
    if _db is None:
        _db = firestore.Client()
    return _db


# --- Profile ---

def save_profile(user_id: str, profile: dict) -> None:
    """Save a Work Personality Profile to Firestore."""
    db = _get_db()
    db.collection("users").document(user_id).collection("profile").document("current").set(profile)


def get_profile(user_id: str) -> dict | None:
    """Get the current Work Personality Profile from Firestore."""
    db = _get_db()
    doc = db.collection("users").document(user_id).collection("profile").document("current").get()
    if doc.exists:
        return doc.to_dict()
    return None


def update_profile(user_id: str, updates: dict) -> None:
    """Update specific fields in the user's profile."""
    db = _get_db()
    db.collection("users").document(user_id).collection("profile").document("current").update(updates)


# --- Sessions ---

def save_session(user_id: str, session: dict) -> None:
    """Save a FutureYou session."""
    db = _get_db()
    session_id = session["session_id"]
    db.collection("users").document(user_id).collection("sessions").document(session_id).set(session)


def get_session(user_id: str, session_id: str) -> dict | None:
    """Get a specific session."""
    db = _get_db()
    doc = db.collection("users").document(user_id).collection("sessions").document(session_id).get()
    if doc.exists:
        return doc.to_dict()
    return None


def update_session(user_id: str, session_id: str, updates: dict) -> None:
    """Update a session (e.g., mark as deactivated)."""
    db = _get_db()
    db.collection("users").document(user_id).collection("sessions").document(session_id).update(updates)


# --- Decisions ---

def save_decision(user_id: str, decision: dict) -> None:
    """Save a decision to the decision log."""
    db = _get_db()
    decision_id = decision["decision_id"]
    db.collection("users").document(user_id).collection("decisions").document(decision_id).set(decision)


def get_decisions(user_id: str, session_id: str | None = None) -> list[dict]:
    """Get all decisions for a user, optionally filtered by session."""
    db = _get_db()
    query = db.collection("users").document(user_id).collection("decisions")
    if session_id:
        query = query.where(filter=firestore.FieldFilter("session_id", "==", session_id))
    docs = [doc.to_dict() for doc in query.stream()]
    docs.sort(key=lambda d: d.get("created_at", ""), reverse=True)
    return docs


def override_decision(user_id: str, decision_id: str, correction: str) -> None:
    """Mark a decision as overridden with the correction note."""
    db = _get_db()
    db.collection("users").document(user_id).collection("decisions").document(decision_id).update({
        "human_override": True,
        "correction": correction,
        "status": "overridden",
    })


# --- Events ---

def save_event(user_id: str, event: dict) -> None:
    """Save an incoming event to the event queue."""
    db = _get_db()
    event_id = event["event_id"]
    db.collection("users").document(user_id).collection("events").document(event_id).set(event)


def get_events(user_id: str, status: str = "pending") -> list[dict]:
    """Get events by status."""
    db = _get_db()
    query = (
        db.collection("users").document(user_id).collection("events")
        .where(filter=firestore.FieldFilter("status", "==", status))
    )
    return [doc.to_dict() for doc in query.stream()]


# --- Agent Memory ---

def save_agent_memory(user_id: str, agent_name: str, key: str, value: str) -> None:
    """Save a memory entry for an agent."""
    db = _get_db()
    doc_id = f"{agent_name}_{key}"
    db.collection("users").document(user_id).collection("agent_memory").document(doc_id).set({
        "agent_name": agent_name,
        "memory_key": key,
        "memory_val": value,
    })


def get_agent_memory(user_id: str, agent_name: str, key: str) -> str | None:
    """Get a specific memory entry for an agent."""
    db = _get_db()
    doc_id = f"{agent_name}_{key}"
    doc = db.collection("users").document(user_id).collection("agent_memory").document(doc_id).get()
    if doc.exists:
        return doc.to_dict().get("memory_val")
    return None
