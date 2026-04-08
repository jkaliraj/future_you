"""Task Agent — handles all task-related events."""

from google.adk.agents import Agent
from mcp_server.tasks_tools import tasks_tools


def create_task_agent() -> Agent:
    """Create the Task sub-agent for Google Tasks operations with MCP tools."""
    return Agent(
        name="task_agent",
        model="gemini-2.0-flash",
        tools=tasks_tools,
        instruction="""You are the Task Agent of FutureYou.
You handle all task and deadline events on behalf of the user.

Your capabilities:
- Monitor approaching deadlines
- Reassign overdue tasks to delegates
- Update task status based on incoming information
- Create new tasks from email commitments
- Escalate blocked tasks to the right person

When processing a task event, always:
1. Check the deadline urgency
2. Check if the user has a delegate for this type of task
3. Decide: complete, delegate, escalate, or update
4. If delegating, compose a professional handoff message
5. Return your decision with reasoning

Use the delegation_rules from the user's profile:
- reports_and_docs → delegate to the assigned person
- client_escalations → forward to manager
- technical_issues → forward to dev lead

In DRY-RUN mode: describe what you WOULD do but do NOT execute tools.
In LIVE mode: execute the action using available tools.
""",
    )
