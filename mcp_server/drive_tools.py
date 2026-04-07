"""Drive MCP tools — wraps Google Drive API as MCP-compatible tools.

Demo mode: uses in-memory store so created/shared files are retrievable.
In production, replace with real Google Drive API calls.
"""

from google.adk.tools import FunctionTool
import uuid

# In-memory file store (demo)
_drive_store: list[dict] = [
    {"file_id": "file_q3deck", "name": "Q3 Strategy Deck", "type": "presentation", "shared_with": [], "folder": "Team Shared"},
    {"file_id": "file_budget", "name": "2026 Budget Plan", "type": "spreadsheet", "shared_with": [], "folder": "Finance"},
    {"file_id": "file_onboard", "name": "Onboarding Checklist", "type": "document", "shared_with": [], "folder": "HR"},
    {"file_id": "file_roadmap", "name": "Product Roadmap H2", "type": "document", "shared_with": [], "folder": "Product"},
]


def search_files(
    query: str,
    max_results: int = 5,
) -> dict:
    """Search for files in Google Drive.

    Args:
        query: Search query string (file name, content keywords).
        max_results: Maximum number of files to return.

    Returns:
        Dictionary with matching files.
    """
    matches = [f for f in _drive_store if query.lower() in f["name"].lower()][:max_results]
    return {
        "status": "success",
        "tool": "search_files",
        "query": query,
        "count": len(matches),
        "files": matches,
    }


def get_file(
    file_id: str,
) -> dict:
    """Get metadata and content summary of a Drive file.

    Args:
        file_id: The Google Drive file ID.

    Returns:
        Dictionary with file metadata.
    """
    for f in _drive_store:
        if f["file_id"] == file_id:
            return {"status": "success", "tool": "get_file", "file": f}
    return {"status": "error", "tool": "get_file", "message": f"File {file_id} not found"}


def share_file(
    file_id: str,
    email: str,
    role: str = "reader",
) -> dict:
    """Share a Drive file with a specific user.

    Args:
        file_id: The Google Drive file ID.
        email: Email address of the person to share with.
        role: Permission role — "reader", "writer", or "commenter".

    Returns:
        Dictionary with share status.
    """
    for f in _drive_store:
        if f["file_id"] == file_id:
            f["shared_with"].append({"email": email, "role": role})
            return {"status": "success", "tool": "share_file", "message": f"Shared '{f['name']}' with {email} as {role}.", "file": f}
    return {"status": "error", "tool": "share_file", "message": f"File {file_id} not found"}


def create_file(
    name: str,
    content: str = "",
    mime_type: str = "application/vnd.google-apps.document",
) -> dict:
    """Create a new file in Google Drive.

    Args:
        name: Name of the file to create.
        content: Initial file content.
        mime_type: MIME type of the file.

    Returns:
        Dictionary with created file details.
    """
    f = {
        "file_id": f"file_{uuid.uuid4().hex[:6]}",
        "name": name,
        "type": mime_type,
        "shared_with": [],
        "folder": "My Drive",
    }
    _drive_store.append(f)
    return {
        "status": "success",
        "tool": "create_file",
        "message": f"File '{name}' created.",
        "file": f,
    }


# Export as ADK FunctionTools
search_files_tool = FunctionTool(func=search_files)
get_file_tool = FunctionTool(func=get_file)
share_file_tool = FunctionTool(func=share_file)
create_file_tool = FunctionTool(func=create_file)

drive_tools = [search_files_tool, get_file_tool, share_file_tool, create_file_tool]
