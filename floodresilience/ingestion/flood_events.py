"""Ingestion: Dartmouth Flood Observatory global flood records (Zenodo)."""

from __future__ import annotations

import pandas as pd

from floodresilience.config import DATA_RAW

# DFO Global Flood Records v0.9.0 (Jan 1985 - Dec 2023), CC0.
DFO_ZENODO_URL = "https://zenodo.org/records/19288171/files/Global_Flood_Records.csv"
DFO_FILE = DATA_RAW / "dfo" / "Global_Flood_Records.csv"

# Country names used by DFO. Myanmar events appear both alone and inside
# multi-country strings (e.g. "Myanmar,Bangladesh"), so matching uses substring
# rather than exact equality; see filter_events_by_country.
MYANMAR_NAMES = ("MYANMAR", "BURMA")


def load_flood_records() -> pd.DataFrame:
    """Load the raw DFO flood records CSV."""
    if not DFO_FILE.exists():
        raise FileNotFoundError(
            f"DFO records not found at {DFO_FILE}. "
            "Download from " + DFO_ZENODO_URL
        )
    df = pd.read_csv(DFO_FILE)
    return df


def filter_events_by_country(
    df: pd.DataFrame,
    country_names: tuple[str, ...] = MYANMAR_NAMES,
    country_col: str = "Country",
) -> pd.DataFrame:
    """Keep events whose country field contains any of the given names.

    The DFO country field sometimes lists several countries (e.g.
    "Myanmar,Bangladesh"), so we use a case-insensitive substring match.
    """
    if country_col not in df.columns:
        raise KeyError(f"country column '{country_col}' not in DFO data; have {list(df.columns)}")
    mask = df[country_col].astype(str).str.upper().str.contains("|".join(c.upper() for c in country_names), na=False, regex=True)
    return df[mask].copy()