"""Gmail MCP tools — wraps Google Gmail API as MCP-compatible tools."""

from google.adk.tools import FunctionTool
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials


def _get_gmail_service(credentials: Credentials):
    """Build Gmail API service client."""
    return build("gmail", "v1", credentials=credentials)


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
    # In production: use real Gmail API
    # For demo: return simulated data
    return {
        "status": "success",
        "tool": "read_emails",
        "query": query,
        "message": f"Would read up to {max_results} emails matching '{query}'",
        "emails": [],
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
    return {
        "status": "success",
        "tool": "send_email",
        "to": to,
        "subject": subject,
        "message": f"Would send email to {to} with subject '{subject}'",
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
    return {
        "status": "success",
        "tool": "label_email",
        "message_id": message_id,
        "labels": labels,
        "message": f"Would apply labels {labels} to message {message_id}",
    }


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
    return {
        "status": "success",
        "tool": "search_emails",
        "query": query,
        "message": f"Would search for emails matching '{query}'",
        "results": [],
    }


# Export as ADK FunctionTools
read_emails_tool = FunctionTool(func=read_emails)
send_email_tool = FunctionTool(func=send_email)
label_email_tool = FunctionTool(func=label_email)
search_emails_tool = FunctionTool(func=search_emails)

gmail_tools = [read_emails_tool, send_email_tool, label_email_tool, search_emails_tool]
