# FutureYou — Your Digital Work Twin

> **Team: Phantom Ops** | Google ADK Hackathon

A multi-agent AI system built on **Google ADK** and **Gemini 2.5 Flash** that learns how you work and acts as your digital twin when you're unavailable.

## What It Does

FutureYou autonomously handles your emails, meetings, tasks, and documents while you're offline — making real judgment calls based on your learned work patterns, not just sending auto-replies.

## Architecture

- **Commander Agent** (primary) orchestrates 4 specialized sub-agents
- **Inbox Agent** — Gmail operations (classify, reply, forward, flag)
- **Calendar Agent** — Scheduling (accept/decline, find slots, resolve conflicts)
- **Task Agent** — Task management (delegate, escalate, update status)
- **Knowledge Agent** — Drive operations (search, share, summarize docs)

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Agent Framework | Google ADK |
| LLM | Gemini 2.5 Flash |
| API | FastAPI |
| MCP Tools | Custom MCP server wrapping Google Workspace APIs |
| Database | Firestore |
| Deployment | Google Cloud Run |
| Auth | Google OAuth 2.0 |

## Quick Start

```bash
pip install -r requirements.txt
uvicorn main:app --reload --port 8080
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/onboard` | Load user profile |
| POST | `/activate` | Start FutureYou session (dry-run or live) |
| POST | `/trigger-event` | Simulate incoming event |
| POST | `/deactivate` | End session, get summary |
| GET | `/decisions/{user_id}` | View decision log |
| GET | `/profile/{user_id}` | View work personality profile |
| POST | `/decisions/{id}/override` | Override a decision |

## Deploy to Cloud Run

```bash
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/futureyou
gcloud run deploy futureyou --image gcr.io/YOUR_PROJECT_ID/futureyou --platform managed --region us-central1
```

---

*"Your AI self, working while you rest."*
