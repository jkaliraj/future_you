"""Tasks MCP tools — wraps Google Tasks API as MCP-compatible tools.

Demo mode: uses in-memory store so created tasks are retrievable.
In production, replace with real Google Tasks API calls.
"""

from google.adk.tools import FunctionTool
import uuid

# In-memory task store (demo)
_tasks_store: list[dict] = []


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
    if show_completed:
        tasks = _tasks_store[:max_results]
    else:
        tasks = [t for t in _tasks_store if t["status"] != "completed"][:max_results]
    return {
        "status": "success",
        "tool": "list_tasks",
        "count": len(tasks),
        "tasks": tasks,
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
    task = {
        "task_id": f"task_{uuid.uuid4().hex[:6]}",
        "title": title,
        "notes": notes,
        "due_date": due_date,
        "status": "needsAction",
    }
    _tasks_store.append(task)
    return {
        "status": "success",
        "tool": "create_task",
        "message": f"Task created: '{title}'",
        "task": task,
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
    for t in _tasks_store:
        if t["task_id"] == task_id:
            if title:
                t["title"] = title
            if notes:
                t["notes"] = notes
            if status:
                t["status"] = status
            return {"status": "success", "tool": "update_task", "task": t}
    return {"status": "error", "tool": "update_task", "message": f"Task {task_id} not found"}


def complete_task(
    task_id: str,
) -> dict:
    """Mark a task as completed.

    Args:
        task_id: The task ID to complete.

    Returns:
        Dictionary with completion status.
    """
    for t in _tasks_store:
        if t["task_id"] == task_id:
            t["status"] = "completed"
            return {"status": "success", "tool": "complete_task", "message": f"Task '{t['title']}' completed.", "task": t}
    return {"status": "error", "tool": "complete_task", "message": f"Task {task_id} not found"}


# Export as ADK FunctionTools
list_tasks_tool = FunctionTool(func=list_tasks)
create_task_tool = FunctionTool(func=create_task)
update_task_tool = FunctionTool(func=update_task)
complete_task_tool = FunctionTool(func=complete_task)

tasks_tools = [list_tasks_tool, create_task_tool, update_task_tool, complete_task_tool]
