"""Export clean, documented datasets for SAP Analytics Cloud.

All files go to `data/sac/` with clean column names, documented units and
geographic identifiers. Column-level metadata is written to
`docs/sac_import_guide.md` by the caller.
"""

from __future__ import annotations

import glob
from pathlib import Path

import numpy as np
import pandas as pd
import rasterio

from floodresilience.config import DATA_SAC, DATA_PROCESSED, DATA_RAW, DATA_INTERMEDIATE, OUTPUT_TABLES, DOCUMENTED_YANGON_FLOOD_YEARS

FEATURES = DATA_PROCESSED / "yangon_township_features.csv"
RISK = OUTPUT_TABLES / "risk_scores.csv"
DFO = DATA_RAW / "dfo" / "Global_Flood_Records.csv"
CHIRPS_DIR = DATA_INTERMEDIATE / "rainfall" / "chirps_yangon"

# Documented major Yangon flood years (published records). Used only as context
# flags, never as invented district-level data.
DOCUMENTED_FLOOD_YEARS = DOCUMENTED_YANGON_FLOOD_YEARS


def clean_names(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
    return df


def export_risk_by_area() -> pd.DataFrame:
    risk = pd.read_csv(RISK)
    feat = pd.read_csv(FEATURES)
    out = risk.merge(feat[["tship_code", "pop_est", "elev_mean_m", "schools", "health_facilities", "area_km2"]], on="tship_code")
    out = clean_names(out[["tship_code", "township", "district", "hazard", "exposure", "vulnerability", "risk", "risk_100", "risk_class", "pop_est", "elev_mean_m", "schools", "health_facilities", "area_km2"]])
    out.to_csv(DATA_SAC / "sac_risk_by_area.csv", index=False)
    return out


def export_rainfall_timeseries() -> pd.DataFrame:
    files = sorted(glob.glob(str(CHIRPS_DIR / "chirps_*.tif")))
    rows = []
    for f in files:
        yyyymm = Path(f).stem.split("_")[1]
        with rasterio.open(f) as ds:
            a = ds.read(1).astype("float64")
        a[a < 0] = np.nan
        rows.append({"date": f"{yyyymm[:4]}-{yyyymm[4:6]}-01", "rainfall_mm": float(np.nanmean(a))})
    out = pd.DataFrame(rows)
    out["date"] = pd.to_datetime(out["date"])
    out["year"] = out["date"].dt.year
    out["month"] = out["date"].dt.month
    out["month_name"] = out["date"].dt.month_name()
    out["documented_flood_year"] = out["year"].isin(DOCUMENTED_FLOOD_YEARS)
    out = clean_names(out[["date", "year", "month", "month_name", "rainfall_mm", "documented_flood_year"]])
    out.to_csv(DATA_SAC / "sac_rainfall_timeseries.csv", index=False)
    return out


def export_flood_events() -> pd.DataFrame:
    df = pd.read_csv(DFO)
    df = df[df["Country"].astype(str).str.contains("Myanmar", case=False, na=False)].copy()
    df["start_date"] = pd.to_datetime(df["Start Date"], errors="coerce")
    df = df.dropna(subset=["start_date"])
    df["year"] = df["start_date"].dt.year
    annual = df.groupby("year").size().reset_index(name="n_flood_events_myanmar")
    annual["n_flood_events_yangon_documented"] = np.where(annual["year"].isin(DOCUMENTED_FLOOD_YEARS), 1, 0)
    out = clean_names(annual)
    out.to_csv(DATA_SAC / "sac_flood_events.csv", index=False)
    return out


def export_flood_events_detail() -> pd.DataFrame:
    """Per-event DFO records (real observed events, Dartmouth Flood Observatory)."""
    df = pd.read_csv(DFO)
    df = df[df["Country"].astype(str).str.contains("Myanmar|Burma", case=False, na=False)].copy()
    df["start_date"] = pd.to_datetime(df["Start Date"], errors="coerce")
    df["end_date"] = pd.to_datetime(df["End Date"], errors="coerce")
    df = df.dropna(subset=["start_date"])
    rename = {"﹟": "dfo_id", "Glide ﹟": "glide_number"}
    out = df.rename(columns=rename)[
        ["dfo_id", "glide_number", "start_date", "end_date", "Country", "Main Cause", "Severity", "Fatalities", "Displaced", "Area (km²)", "Source"]
    ].copy()
    out.columns = [
        "dfo_id",
        "glide_number",
        "start_date",
        "end_date",
        "country",
        "main_cause",
        "severity",
        "fatalities",
        "displaced",
        "area_km2",
        "source",
    ]
    out["in_yangon_documented_year"] = out["start_date"].dt.year.isin(DOCUMENTED_FLOOD_YEARS).astype(int)
    out = out.sort_values("start_date")
    out.to_csv(DATA_SAC / "sac_flood_events_detail.csv", index=False)
    return out


def export_yangon_flood_events() -> pd.DataFrame:
    """Documented Yangon Region flood events with their published sources.

    Each year listed here corresponds to at least one major flood reported in
    Yangon Region in the peer-reviewed / agency literature (see
    `floodresilience/config.py` DOCUMENTED_YANGON_FLOOD_YEARS for citations).
    """
    docs = [
        ("1988", "PIAHS 386 (2024) RRI flood study"),
        ("1991", "PIAHS 386 (2024) RRI flood study"),
        ("1997", "PIAHS 386 (2024) RRI flood study"),
        ("2002", "PIAHS 386 (2024) RRI flood study"),
        ("2004", "PIAHS 386 (2024) RRI flood study"),
        ("2007", "PIAHS 386 (2024) RRI flood study"),
        ("2008", "Sritarapipat (2017) urban-growth study (incl. Cyclone Nargis)"),
        ("2010", "Sritarapipat (2017) urban-growth study"),
        ("2013", "Sritarapipat (2017) urban-growth study"),
        ("2014", "PIAHS 386 (2024) + Sritarapipat (2017)"),
        ("2015", "Sritarapipat (2017) urban-growth study"),
        ("2017", "OCHA 2017 monsoon update"),
        ("2019", "DFO record + monsoon flooding reports"),
        ("2020", "UNOSAT Sentinel-1 surface-water mapping, Aug 2020"),
    ]
    out = pd.DataFrame(docs, columns=["year", "source"])
    out["has_dfo_event_myanmar"] = out["year"].astype(int).isin(
        export_flood_events_detail()["start_date"].dt.year
    )
    out.to_csv(DATA_SAC / "sac_yangon_flood_events.csv", index=False)
    return out


def export_population_exposure() -> pd.DataFrame:
    feat = pd.read_csv(FEATURES)
    out = feat[["tship_code", "township", "district", "pop_est", "area_km2"]].copy()
    out["pop_density"] = out["pop_est"] / out["area_km2"]
    out = clean_names(out)
    out.to_csv(DATA_SAC / "sac_population_exposure.csv", index=False)
    return out


def export_infrastructure_exposure() -> pd.DataFrame:
    feat = pd.read_csv(FEATURES)
    out = feat[["tship_code", "township", "district", "schools", "health_facilities", "pop_est"]].copy()
    out["schools_per_100k"] = out["schools"] / out["pop_est"] * 100_000
    out["health_per_100k"] = out["health_facilities"] / out["pop_est"] * 100_000
    out = clean_names(out)
    out.to_csv(DATA_SAC / "sac_infrastructure_exposure.csv", index=False)
    return out


def export_risk_factors() -> pd.DataFrame:
    feat = pd.read_csv(FEATURES)
    out = clean_names(feat)
    out.to_csv(DATA_SAC / "sac_risk_factors.csv", index=False)
    return out


def main() -> None:
    print(export_risk_by_area().shape, "sac_risk_by_area.csv")
    print(export_rainfall_timeseries().shape, "sac_rainfall_timeseries.csv")
    print(export_flood_events().shape, "sac_flood_events.csv")
    print(export_flood_events_detail().shape, "sac_flood_events_detail.csv")
    print(export_yangon_flood_events().shape, "sac_yangon_flood_events.csv")
    print(export_population_exposure().shape, "sac_population_exposure.csv")
    print(export_infrastructure_exposure().shape, "sac_infrastructure_exposure.csv")
    print(export_risk_factors().shape, "sac_risk_factors.csv")


if __name__ == "__main__":
    main()
