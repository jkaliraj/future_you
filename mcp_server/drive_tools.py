"""Drive MCP tools — wraps Google Drive API as MCP-compatible tools."""

from google.adk.tools import FunctionTool


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
    return {
        "status": "success",
        "tool": "search_files",
        "query": query,
        "message": f"Would search Drive for '{query}'",
        "files": [],
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
    return {
        "status": "success",
        "tool": "get_file",
        "file_id": file_id,
        "message": f"Would retrieve file {file_id}",
    }


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
    return {
        "status": "success",
        "tool": "share_file",
        "file_id": file_id,
        "shared_with": email,
        "role": role,
        "message": f"Would share file {file_id} with {email} as {role}",
    }


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
    return {
        "status": "success",
        "tool": "create_file",
        "name": name,
        "mime_type": mime_type,
        "message": f"Would create file '{name}'",
    }


# Export as ADK FunctionTools
search_files_tool = FunctionTool(func=search_files)
get_file_tool = FunctionTool(func=get_file)
share_file_tool = FunctionTool(func=share_file)
create_file_tool = FunctionTool(func=create_file)

drive_tools = [search_files_tool, get_file_tool, share_file_tool, create_file_tool]
