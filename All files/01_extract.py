"""
01_extract.py
Pull all orbital launches from Launch Library 2 API and save a raw CSV.

Features:
  - Saves progress after every page → safe to Ctrl+C and resume
  - Exponential backoff on 429 (65s → 130s → 260s → 300s cap)
  - Resumes from last saved offset automatically

Usage:
    pip install requests pandas
    python 01_extract.py
"""

import requests
import pandas as pd
import time
import json
from pathlib import Path

# ── Config ────────────────────────────────────────────────────────────────────
BASE_URL   = "https://ll.thespacedevs.com/2.2.0/launch/previous/"
PAGE_SIZE  = 100
DELAY      = 2.0        # seconds between successful requests
BACKOFF_BASE = 65       # seconds to wait after first 429
BACKOFF_CAP  = 300      # max wait between retries
PROGRESS_FILE = Path("data/progress.json")
RAW_OUT       = Path("data/raw_launches.csv")
RAW_OUT.parent.mkdir(exist_ok=True)

# ── Helpers ───────────────────────────────────────────────────────────────────
def safe_get(d, *keys, default=None):
    for k in keys:
        if not isinstance(d, dict):
            return default
        d = d.get(k)
    return d if d is not None else default


def flatten_launch(launch: dict) -> dict:
    return {
        "id":            launch.get("id"),
        "mission_name":  launch.get("name"),
        "net":           launch.get("net"),
        "status_name":   safe_get(launch, "status", "name"),
        "status_abbrev": safe_get(launch, "status", "abbrev"),
        "agency_name":   safe_get(launch, "launch_service_provider", "name"),
        "agency_type":   safe_get(launch, "launch_service_provider", "type"),
        "rocket_name":   safe_get(launch, "rocket", "configuration", "name"),
        "pad_name":      safe_get(launch, "pad", "name"),
        "pad_country":   safe_get(launch, "pad", "location", "country_code"),
        "orbit_name":    safe_get(launch, "mission", "orbit", "name"),
        "orbit_abbrev":  safe_get(launch, "mission", "orbit", "abbrev"),
    }


def load_progress() -> tuple[int, list]:
    """Return (starting_offset, already_fetched_rows)."""
    if PROGRESS_FILE.exists() and RAW_OUT.exists():
        state = json.loads(PROGRESS_FILE.read_text())
        existing = pd.read_csv(RAW_OUT).to_dict("records")
        print(f"Resuming from offset {state['offset']} ({len(existing)} rows already saved)")
        return state["offset"], existing
    return 0, []


def save_progress(offset: int, records: list):
    pd.DataFrame(records).to_csv(RAW_OUT, index=False)
    PROGRESS_FILE.write_text(json.dumps({"offset": offset}))


# ── Fetch ─────────────────────────────────────────────────────────────────────
def fetch_all() -> list[dict]:
    start_offset, records = load_progress()

    params = {
        "limit":    PAGE_SIZE,
        "offset":   start_offset,
        "ordering": "net",
        "format":   "json",
    }

    page        = (start_offset // PAGE_SIZE) + 1
    total_count = None

    print("Fetching launches from Launch Library 2 API...")

    while True:
        backoff = BACKOFF_BASE
        while True:
            try:
                resp = requests.get(BASE_URL, params=params, timeout=30)

                if resp.status_code == 429:
                    print(f"\n  ⚠ Rate limited (429). Waiting {backoff}s before retry...")
                    time.sleep(backoff)
                    backoff = min(backoff * 2, BACKOFF_CAP)
                    continue

                resp.raise_for_status()
                break   # success — exit retry loop

            except requests.RequestException as e:
                print(f"\n  ⚠ Request error: {e}. Waiting {backoff}s...")
                time.sleep(backoff)
                backoff = min(backoff * 2, BACKOFF_CAP)

        data        = resp.json()
        total_count = data.get("count", total_count or "?")
        results     = data.get("results", [])

        records.extend(flatten_launch(r) for r in results)

        new_offset = params["offset"] + len(results)
        save_progress(new_offset, records)

        print(f"  Page {page:>3} | {new_offset:>5} / {total_count} launches saved", end="\r")

        if not data.get("next"):
            break

        params["offset"] = new_offset
        page += 1
        time.sleep(DELAY)

    print(f"\nDone. Total records: {len(records)}")
    return records


# ── Main ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    records = fetch_all()

    df = pd.DataFrame(records)
    df.to_csv(RAW_OUT, index=False)

    # Clean up progress file once complete
    if PROGRESS_FILE.exists():
        PROGRESS_FILE.unlink()

    print(f"\nRaw CSV saved → {RAW_OUT}  ({len(df)} rows, {len(df.columns)} columns)")
    print("\nStatus values in dataset:")
    print(df["status_name"].value_counts().to_string())
