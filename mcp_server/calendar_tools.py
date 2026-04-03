"""Calendar MCP tools — wraps Google Calendar API as MCP-compatible tools."""

from google.adk.tools import FunctionTool


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
    return {
        "status": "success",
        "tool": "get_events",
        "time_range": f"{time_min} to {time_max}",
        "message": f"Would fetch up to {max_results} events",
        "events": [],
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
    return {
        "status": "success",
        "tool": "create_event",
        "summary": summary,
        "start": start_time,
        "end": end_time,
        "attendees": attendees or [],
        "message": f"Would create event '{summary}' from {start_time} to {end_time}",
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
    return {
        "status": "success",
        "tool": "update_event",
        "event_id": event_id,
        "message": f"Would update event {event_id}",
    }


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
    return {
        "status": "success",
        "tool": "check_availability",
        "date": date,
        "message": f"Would check availability on {date} from {start_hour}:00 to {end_hour}:00",
        "available_slots": [],
    }


# Export as ADK FunctionTools
get_events_tool = FunctionTool(func=get_events)
create_event_tool = FunctionTool(func=create_event)
update_event_tool = FunctionTool(func=update_event)
check_availability_tool = FunctionTool(func=check_availability)

calendar_tools = [get_events_tool, create_event_tool, update_event_tool, check_availability_tool]
