import json
from pathlib import Path

DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "schemes.json"

def load_schemes():
    try:
        with DATA_FILE.open(encoding="utf-8-sig") as f:
            data = json.load(f)
        return data if isinstance(data, list) else []
    except (OSError, json.JSONDecodeError):
        return []

def search_schemes(query=""):
    schemes = load_schemes()
    q = (query or "").strip().casefold()
    if not q:
        return schemes
    return [s for s in schemes if q in " ".join([s.get("name", ""), s.get("category", ""), s.get("description", ""), *s.get("eligibility", [])]).casefold()]

def find_scheme(identifier):
    return next((s for s in load_schemes() if s.get("id") == identifier), None)
