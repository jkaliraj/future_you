"""Calendar MCP tools — wraps Google Calendar API as MCP-compatible tools.

Demo mode: uses in-memory store so created events are retrievable.
In production, replace with real Google Calendar API calls.
"""

from google.adk.tools import FunctionTool
import uuid

# In-memory event store (demo) — persists during the session
_calendar_store: list[dict] = []


def get_events(
    time_min: str = "",
    time_max: str = "",
    max_results: int = 10,
) -> dict:
    """Get calendar events within a time range.

    Args:
        time_min: Start time in ISO 8601 format.
        time_max: End time in ISO 8601 format.
        max_results: Maximum number of events to return.

    Returns:
        Dictionary with list of calendar events.
    """
    events = _calendar_store[:max_results]
    return {
        "status": "success",
        "tool": "get_events",
        "count": len(events),
        "events": events,
    }


def create_event(
    summary: str,
    start_time: str,
    end_time: str,
    attendees: list[str] | None = None,
    description: str = "",
) -> dict:
    """Create a new calendar event.

    Args:
        summary: Event title.
        start_time: Start time in ISO 8601 format.
        end_time: End time in ISO 8601 format.
        attendees: List of attendee email addresses.
        description: Event description.

    Returns:
        Dictionary with created event details.
    """
    event = {
        "event_id": f"evt_{uuid.uuid4().hex[:6]}",
        "summary": summary,
        "start": start_time,
        "end": end_time,
        "attendees": attendees or [],
        "description": description,
        "status": "confirmed",
    }
    _calendar_store.append(event)
    return {
        "status": "success",
        "tool": "create_event",
        "message": f"Event '{summary}' created: {start_time} to {end_time}",
        "event": event,
    }


def update_event(
    event_id: str,
    summary: str = "",
    start_time: str = "",
    end_time: str = "",
    status: str = "",
) -> dict:
    """Update an existing calendar event.

    Args:
        event_id: The calendar event ID.
        summary: New event title (optional).
        start_time: New start time (optional).
        end_time: New end time (optional).
        status: New status — "confirmed", "tentative", "cancelled" (optional).

    Returns:
        Dictionary with update status.
    """
    for evt in _calendar_store:
        if evt["event_id"] == event_id:
            if summary:
                evt["summary"] = summary
            if start_time:
                evt["start"] = start_time
            if end_time:
                evt["end"] = end_time
            if status:
                evt["status"] = status
            return {"status": "success", "tool": "update_event", "event": evt}
    return {"status": "error", "tool": "update_event", "message": f"Event {event_id} not found"}


def check_availability(
    date: str,
    start_hour: int = 9,
    end_hour: int = 18,
) -> dict:
    """Check available time slots on a given date.

    Args:
        date: Date to check in YYYY-MM-DD format.
        start_hour: Start of working hours (24h format).
        end_hour: End of working hours (24h format).

    Returns:
        Dictionary with available time slots.
    """
    # Find busy slots from in-memory store for this date
    busy = [e for e in _calendar_store if date in e.get("start", "")]
    busy_summaries = [f"{e['summary']} ({e['start']}–{e['end']})" for e in busy]
    total_meetings = len(busy)
    return {
        "status": "success",
        "tool": "check_availability",
        "date": date,
        "meetings_on_date": total_meetings,
        "busy_slots": busy_summaries,
        "note": f"{total_meetings} meeting(s) found. Max allowed: 4/day.",
    }


# Export as ADK FunctionTools
get_events_tool = FunctionTool(func=get_events)
create_event_tool = FunctionTool(func=create_event)
update_event_tool = FunctionTool(func=update_event)
check_availability_tool = FunctionTool(func=check_availability)

calendar_tools = [get_events_tool, create_event_tool, update_event_tool, check_availability_tool]
