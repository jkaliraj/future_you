"""Profile builder — loads pre-built profile for hackathon demo."""

import json
from pathlib import Path
from db.firestore import save_profile, get_profile


SEED_PROFILE_PATH = Path(__file__).parent / "seed_profile.json"


def load_seed_profile(user_id: str) -> dict:
    """Load pre-built demo profile from seed_profile.json and save to Firestore.

    For hackathon demo: loads instantly, no real API analysis.
    """
    with open(SEED_PROFILE_PATH, "r") as f:
        profile = json.load(f)

    profile["user_id"] = user_id
    save_profile(user_id, profile)
    return profile


def get_or_create_profile(user_id: str) -> dict:
    """Get existing profile from Firestore, or create from seed if missing."""
    profile = get_profile(user_id)
    if profile:
        return profile
    return load_seed_profile(user_id)
