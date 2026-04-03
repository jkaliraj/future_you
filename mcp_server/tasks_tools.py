"""Tasks MCP tools — wraps Google Tasks API as MCP-compatible tools."""

from google.adk.tools import FunctionTool


def list_tasks(
    task_list_id: str = "@default",
    show_completed: bool = False,
    max_results: int = 10,
) -> dict:
    """List tasks from a Google Tasks list.

    Args:
        task_list_id: The task list ID (default for primary list).
        show_completed: Whether to include completed tasks.
        max_results: Maximum number of tasks to return.

    Returns:
        Dictionary with list of tasks.
    """
    return {
        "status": "success",
        "tool": "list_tasks",
        "task_list_id": task_list_id,
        "message": f"Would list up to {max_results} tasks",
        "tasks": [],
    }


def create_task(
    title: str,
    notes: str = "",
    due_date: str = "",
) -> dict:
    """Create a new task in Google Tasks.

    Args:
        title: Task title.
        notes: Task description/notes.
        due_date: Due date in ISO 8601 format.

    Returns:
        Dictionary with created task details.
    """
    return {
        "status": "success",
        "tool": "create_task",
        "title": title,
        "due_date": due_date,
        "message": f"Would create task '{title}'",
    }


def update_task(
    task_id: str,
    title: str = "",
    notes: str = "",
    status: str = "",
) -> dict:
    """Update an existing task.

    Args:
        task_id: The task ID.
        title: New task title (optional).
        notes: New task notes (optional).
        status: New status — "needsAction" or "completed" (optional).

    Returns:
        Dictionary with update status.
    """
    return {
        "status": "success",
        "tool": "update_task",
        "task_id": task_id,
        "message": f"Would update task {task_id}",
    }


def complete_task(
    task_id: str,
) -> dict:
    """Mark a task as completed.

    Args:
        task_id: The task ID to complete.

    Returns:
        Dictionary with completion status.
    """
    return {
        "status": "success",
        "tool": "complete_task",
        "task_id": task_id,
        "message": f"Would mark task {task_id} as completed",
    }


# Export as ADK FunctionTools
list_tasks_tool = FunctionTool(func=list_tasks)
create_task_tool = FunctionTool(func=create_task)
update_task_tool = FunctionTool(func=update_task)
complete_task_tool = FunctionTool(func=complete_task)

tasks_tools = [list_tasks_tool, create_task_tool, update_task_tool, complete_task_tool]
