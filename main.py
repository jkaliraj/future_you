"""FutureYou — Your Digital Work Twin

Multi-agent AI system built on Google ADK that learns how you work
and acts as your digital twin when you're unavailable.

Team: Phantom Ops
"""

import os

# Force ADK to use Vertex AI (ADC auth) instead of Gemini API key
os.environ.setdefault("GOOGLE_GENAI_USE_VERTEXAI", "TRUE")
os.environ.setdefault("GOOGLE_CLOUD_LOCATION", "us-central1")
# GOOGLE_CLOUD_PROJECT must be set in environment or here:
# os.environ.setdefault("GOOGLE_CLOUD_PROJECT", "futureyou-agent")

from fastapi import FastAPI
from api.routes import router

app = FastAPI(
    title="FutureYou API",
    description="Multi-agent productivity assistant — your digital work twin. Team Phantom Ops.",
    version="2.0.0",
)

app.include_router(router)


@app.get("/")
async def root():
    return {
        "name": "FutureYou",
        "team": "Phantom Ops",
        "version": "2.0.0",
        "tagline": "Your AI self, working while you rest.",
        "endpoints": [
            "POST /onboard",
            "POST /activate",
            "POST /trigger-event",
            "POST /deactivate",
            "GET /decisions/{user_id}",
            "GET /profile/{user_id}",
            "POST /decisions/{decision_id}/override",
        ],
    }


@app.get("/health")
async def health():
    return {"status": "healthy"}
