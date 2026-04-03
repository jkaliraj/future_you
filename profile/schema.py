"""Profile data models using Pydantic."""

from pydantic import BaseModel


class ResponseSpeed(BaseModel):
    vip_contacts: str = "within 1 hour"
    colleagues: str = "within 4 hours"
    unknown_senders: str = "next business day"


class CommunicationStyle(BaseModel):
    tone: str = "professional yet warm"
    signature: str = "Best, Alex"
    average_reply_length: str = "3-5 sentences"
    uses_emojis: bool = False
    response_speed: ResponseSpeed = ResponseSpeed()


class CalendarPreferences(BaseModel):
    preferred_meeting_days: list[str] = ["Tuesday", "Wednesday", "Thursday"]
    avoid_times: list[str] = ["Monday 9-11 AM", "Friday after 3 PM"]
    max_meetings_per_day: int = 4
    buffer_between_meetings_mins: int = 15
    focus_blocks: list[str] = ["Daily 10 AM - 12 PM"]
    auto_accept_from: list[str] = []


class DelegationRules(BaseModel):
    reports_and_docs: str = ""
    client_escalations: str = ""
    technical_issues: str = ""


class WorkHours(BaseModel):
    timezone: str = "Asia/Kolkata"
    start: str = "09:00"
    end: str = "18:30"
    active_days: list[str] = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]


class WorkPersonalityProfile(BaseModel):
    user_id: str
    name: str
    profile_version: str = "2.0"
    last_updated: str = ""
    communication_style: CommunicationStyle = CommunicationStyle()
    calendar_preferences: CalendarPreferences = CalendarPreferences()
    delegation_rules: DelegationRules = DelegationRules()
    priority_contacts: list[str] = []
    hard_limits: list[str] = []
    work_hours: WorkHours = WorkHours()
