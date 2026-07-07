"""
02_clean.py
Clean the Kaggle dataset → launches_clean.csv (Power BI fact table).

What this does:
  1. Merges USSR → Russia for narrative continuity
  2. Maps launch_success (0/1) → readable status labels
  3. Adds Era column (Cold War / Quiet Middle / New Eruption)
  4. Standardises country labels to match the dashboard design
  5. Selects and renames final columns for Power BI

Input:  launches.csv  (root of project folder)
Output: data/launches_clean.csv

Run:
    python 02_clean.py
"""

import pandas as pd
from pathlib import Path

IN_FILE  = Path("launches.csv")
OUT_FILE = Path("data/launches_clean.csv")
OUT_FILE.parent.mkdir(exist_ok=True)

# ── Country standardisation ───────────────────────────────────────────────────
# USSR → Russia (narrative continuity, noted in dashboard footer)
# Japan kept as-is (217 launches, real story worth preserving)
# "Other" → "Others" (match dashboard label)

COUNTRY_MAP = {
    "USSR":   "Russia",
    "Other":  "Others",
}

# ── Status mapping ────────────────────────────────────────────────────────────
# Dataset uses 1 = success, 0 = failure (no partial failures in this source)
def map_status(val) -> str:
    if val == 1:
        return "Success"
    elif val == 0:
        return "Failure"
    return "Unknown"

# ── Era bucketing ─────────────────────────────────────────────────────────────
def assign_era(year: int) -> str:
    if year <= 1991:
        return "Cold War Era"
    elif year <= 2010:
        return "Quiet Middle"
    else:
        return "New Eruption"

# ── Main ──────────────────────────────────────────────────────────────────────
def clean(df: pd.DataFrame) -> pd.DataFrame:

    # 1. Parse date
    df["launch_date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.dropna(subset=["launch_date", "year", "country"])

    # 2. Standardise countries
    df["country"] = df["country"].replace(COUNTRY_MAP)

    # 3. Status
    df["status"] = df["launch_success"].apply(map_status)

    # 4. Era
    df["era"] = df["year"].astype(int).apply(assign_era)

    # 5. Select final columns for Power BI
    final = df[[
        "launch_id",
        "launch_date",
        "year",
        "month",
        "era",
        "country",
        "operator",
        "rocket",
        "launch_site",
        "orbit",
        "status",
        "payload_mass_kg",
        "crewed",
        "booster_reused",
    ]].copy()

    return final.sort_values("launch_date").reset_index(drop=True)


if __name__ == "__main__":
    print(f"Reading {IN_FILE}...")
    raw = pd.read_csv(IN_FILE)
    print(f"  Raw rows: {len(raw)}")

    cleaned = clean(raw)
    cleaned.to_csv(OUT_FILE, index=False)

    print(f"\nClean CSV saved → {OUT_FILE}  ({len(cleaned)} rows)")

    print("\nCountry distribution:")
    print(cleaned["country"].value_counts().to_string())

    print("\nEra distribution:")
    print(cleaned["era"].value_counts().to_string())

    print("\nStatus distribution:")
    print(cleaned["status"].value_counts().to_string())

    print("\nYear range:")
    print(f"  {int(cleaned['year'].min())} – {int(cleaned['year'].max())}")

    print("\nSample rows:")
    print(cleaned.head(5).to_string())
