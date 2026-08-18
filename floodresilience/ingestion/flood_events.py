"""Ingestion: Dartmouth Flood Observatory global flood records (Zenodo)."""

from __future__ import annotations

import pandas as pd

from floodresilience.config import DATA_RAW

# DFO Global Flood Records v0.9.0 (Jan 1985 - Dec 2023), CC0.
DFO_ZENODO_URL = "https://zenodo.org/records/19288171/files/Global_Flood_Records.csv"
DFO_FILE = DATA_RAW / "dfo" / "Global_Flood_Records.csv"

# Country name used by DFO for Indonesia. Validate against actual data.
INDONESIA_NAMES = ("INDONESIA", "INDONESIA (JAKARTA)")


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
    country_names: tuple[str, ...] = INDONESIA_NAMES,
    country_col: str = "country",
) -> pd.DataFrame:
    """Keep events whose country field matches the given names (case-insensitive)."""
    if country_col not in df.columns:
        raise KeyError(f"country column '{country_col}' not in DFO data; have {list(df.columns)}")
    mask = df[country_col].astype(str).str.upper().isin([c.upper() for c in country_names])
    return df[mask].copy()