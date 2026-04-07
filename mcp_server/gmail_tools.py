"""Gmail MCP tools — wraps Google Gmail API as MCP-compatible tools.

Demo mode: uses in-memory store so sent/labeled emails are trackable.
In production, replace with real Gmail API calls.
"""

from google.adk.tools import FunctionTool
import uuid

# In-memory email store (demo)
_inbox_store: list[dict] = []
_sent_store: list[dict] = []


def read_emails(
    user_id: str = "me",
    max_results: int = 10,
    query: str = "is:unread",
) -> dict:
    """Read emails from the user's Gmail inbox.

    Args:
        user_id: Gmail user ID (default "me" for authenticated user).
        max_results: Maximum number of emails to return.
        query: Gmail search query (e.g. "is:unread", "from:client@company.com").

    Returns:
        Dictionary with list of email summaries.
    """
    emails = _inbox_store[:max_results]
    return {
        "status": "success",
        "tool": "read_emails",
        "query": query,
        "count": len(emails),
        "emails": emails,
        "note": "No unread emails in inbox." if not emails else f"{len(emails)} email(s) found.",
    }


def send_email(
    to: str,
    subject: str,
    body: str,
) -> dict:
    """Send an email via Gmail.

    Args:
        to: Recipient email address.
        subject: Email subject line.
        body: Email body text.

    Returns:
        Dictionary with send status.
    """
    email = {
        "message_id": f"msg_{uuid.uuid4().hex[:6]}",
        "to": to,
        "subject": subject,
        "body": body,
        "status": "sent",
    }
    _sent_store.append(email)
    return {
        "status": "success",
        "tool": "send_email",
        "message": f"Email sent to {to}: '{subject}'",
        "email": email,
    }


def label_email(
    message_id: str,
    labels: list[str],
) -> dict:
    """Apply labels to an email message.

    Args:
        message_id: The Gmail message ID.
        labels: List of label names to apply.

    Returns:
        Dictionary with label status.
    """
    for e in _inbox_store:
        if e.get("message_id") == message_id:
            e["labels"] = labels
            return {"status": "success", "tool": "label_email", "message": f"Labels {labels} applied.", "email": e}
    return {"status": "success", "tool": "label_email", "message": f"Labels {labels} applied to {message_id}."}


def search_emails(
    query: str,
    max_results: int = 5,
) -> dict:
    """Search emails using Gmail search syntax.

    Args:
        query: Gmail search query string.
        max_results: Maximum results to return.

    Returns:
        Dictionary with search results.
    """
    # Search in both inbox and sent
    all_emails = _inbox_store + _sent_store
    matches = [e for e in all_emails if query.lower() in str(e).lower()][:max_results]
    return {
        "status": "success",
        "tool": "search_emails",
        "query": query,
        "count": len(matches),
        "results": matches,
    }


# Export as ADK FunctionTools
read_emails_tool = FunctionTool(func=read_emails)
send_email_tool = FunctionTool(func=send_email)
label_email_tool = FunctionTool(func=label_email)
search_emails_tool = FunctionTool(func=search_emails)

gmail_tools = [read_emails_tool, send_email_tool, label_email_tool, search_emails_tool]
