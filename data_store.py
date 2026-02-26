"""
Persistent storage for candidate screening reports.
Uses a local JSON file so data survives Streamlit reruns and
multiple candidates can be reviewed by the recruiter.
"""

import json
import os
import hashlib
from datetime import datetime
from pathlib import Path

DATA_DIR = Path("data")
DATA_FILE = DATA_DIR / "candidates.json"


def _ensure_data_file():
    """Create data directory and file if they don't exist."""
    DATA_DIR.mkdir(exist_ok=True)
    if not DATA_FILE.exists():
        DATA_FILE.write_text("[]", encoding="utf-8")


def _load_all() -> list:
    """Load all candidate records from disk."""
    _ensure_data_file()
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except (json.JSONDecodeError, Exception):
        return []


def _save_all(records: list):
    """Write all candidate records to disk."""
    _ensure_data_file()
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(records, f, indent=2, default=str)


def generate_candidate_id(profile: dict) -> str:
    """Generate a unique ID from name + email + timestamp."""
    raw = (
        f"{profile.get('email', '')}-"
        f"{profile.get('full_name', '')}-"
        f"{datetime.now().isoformat()}"
    )
    return hashlib.md5(raw.encode()).hexdigest()[:10]


def save_candidate_report(
    candidate_id: str,
    profile: dict,
    answers: list,
    evaluation: dict,
    raw_debug: str = "",
):
    """Save a completed screening report."""
    records = _load_all()

    record = {
        "candidate_id": candidate_id,
        "timestamp": datetime.now().isoformat(),
        "profile": profile,
        "answers": answers,
        "evaluation": evaluation,
        "raw_debug": raw_debug,
        "status": "completed",
    }

    # Replace existing record with same ID (re-screening)
    records = [r for r in records if r.get("candidate_id") != candidate_id]
    records.append(record)

    _save_all(records)
    return record


def get_all_candidates() -> list:
    """Return all candidate records, newest first."""
    records = _load_all()
    records.sort(key=lambda r: r.get("timestamp", ""), reverse=True)
    return records


def get_candidate_by_id(candidate_id: str):
    """Return a single candidate record by ID, or None."""
    records = _load_all()
    for r in records:
        if r.get("candidate_id") == candidate_id:
            return r
    return None


def delete_candidate(candidate_id: str) -> bool:
    """Delete a candidate record. Returns True if found and deleted."""
    records = _load_all()
    new_records = [r for r in records if r.get("candidate_id") != candidate_id]
    if len(new_records) < len(records):
        _save_all(new_records)
        return True
    return False


def get_stats() -> dict:
    """Return summary statistics for the recruiter dashboard."""
    records = _load_all()
    if not records:
        return {
            "total": 0,
            "hire": 0,
            "maybe": 0,
            "reject": 0,
            "avg_score": 0,
        }

    total = len(records)
    hire = sum(
        1 for r in records
        if r.get("evaluation", {}).get("recommendation") == "Hire"
    )
    maybe = sum(
        1 for r in records
        if r.get("evaluation", {}).get("recommendation") == "Maybe"
    )
    reject = sum(
        1 for r in records
        if r.get("evaluation", {}).get("recommendation") == "Reject"
    )

    scores = [
        r.get("evaluation", {}).get("overall_score", 0)
        for r in records
        if r.get("evaluation", {}).get("overall_score")
    ]
    avg_score = round(sum(scores) / len(scores), 1) if scores else 0

    return {
        "total": total,
        "hire": hire,
        "maybe": maybe,
        "reject": reject,
        "avg_score": avg_score,
    }