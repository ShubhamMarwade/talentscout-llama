import json
import time
from pathlib import Path

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

def redact_profile(profile: dict) -> dict:
    # For demo: keep as-is or mask email/phone if you want.
    return dict(profile)

def save_screening_record(profile: dict, tech_answers: list):
    record = {
        "ts": int(time.time()),
        "candidate": profile,
        "tech_answers": tech_answers,
    }
    out = DATA_DIR / f"screening_{record['ts']}.json"
    out.write_text(json.dumps(record, indent=2), encoding="utf-8")