"""Custom MCP Server — aggregates all Google Workspace tool wrappers.

This is a thin MCP server that wraps Google Workspace APIs (Gmail, Calendar,
Drive, Tasks) into MCP-compatible tools for use with Google ADK agents.
"""

from mcp_server.gmail_tools import gmail_tools
from mcp_server.calendar_tools import calendar_tools
from mcp_server.drive_tools import drive_tools
from mcp_server.tasks_tools import tasks_tools

# All tools available through the custom MCP server
all_tools = gmail_tools + calendar_tools + drive_tools + tasks_tools

__all__ = [
    "all_tools",
    "gmail_tools",
    "calendar_tools",
    "drive_tools",
    "tasks_tools",
]
