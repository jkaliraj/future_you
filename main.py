"""FutureYou — Your Digital Work Twin

Multi-agent AI system built on Google ADK that learns how you work
and acts as your digital twin when you're unavailable.

Serves BOTH:
  - ADK Web UI at / (interactive chat with agent graph)
  - REST API at /api/* (programmatic access)

Team: Phantom Ops
"""

import os

# Force ADK to use Vertex AI (ADC auth) instead of Gemini API key
os.environ.setdefault("GOOGLE_GENAI_USE_VERTEXAI", "TRUE")
os.environ.setdefault("GOOGLE_CLOUD_LOCATION", "us-central1")

from google.adk.cli.fast_api import get_fast_api_app
from api.routes import router

# Create the ADK web app (serves UI + agent chat endpoints)
app = get_fast_api_app(
    agents_dir=".",
    web=True,
    host="0.0.0.0",
    port=8080,
    allow_origins=["*"],
)

# Mount our custom REST API under /api
app.include_router(router, prefix="/api")


@app.get("/health")
async def health():
    return {"status": "healthy"}


@app.get("/api")
async def api_root():
    return {
        "name": "FutureYou",
        "team": "Phantom Ops",
        "version": "2.0.0",
        "tagline": "Your AI self, working while you rest.",
        "docs": "Visit / for ADK Web UI, /api/* for REST endpoints",
        "endpoints": [
            "POST /api/onboard",
            "POST /api/activate",
            "POST /api/trigger-event",
            "POST /api/deactivate",
            "GET /api/decisions/{user_id}",
            "GET /api/profile/{user_id}",
            "POST /api/decisions/{decision_id}/override",
        ],
    }
