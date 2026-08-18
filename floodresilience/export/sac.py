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

from floodresilience.config import DATA_SAC, DATA_PROCESSED, DATA_RAW, DATA_INTERMEDIATE, OUTPUT_TABLES

FEATURES = DATA_PROCESSED / "jakarta_kecamatan_features.csv"
RISK = OUTPUT_TABLES / "risk_scores.csv"
DFO = DATA_RAW / "dfo" / "Global_Flood_Records.csv"
CHIRPS_DIR = DATA_INTERMEDIATE / "rainfall" / "chirps"

# Documented major Jakarta flood years (from published disaster records). Used
# only as context flags, never as invented district-level data.
DOCUMENTED_JAKARTA_FLOOD_YEARS = [2002, 2007, 2013, 2020, 2025]


def clean_names(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
    return df


def export_risk_by_area() -> pd.DataFrame:
    risk = pd.read_csv(RISK)
    feat = pd.read_csv(FEATURES)
    out = risk.merge(feat[["kec_code", "pop_est", "elev_mean_m", "schools", "health_facilities", "area_km2"]], on="kec_code")
    out = clean_names(out[["kec_code", "kecamatan", "kota", "hazard", "exposure", "vulnerability", "risk", "risk_100", "risk_class", "pop_est", "elev_mean_m", "schools", "health_facilities", "area_km2"]])
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
    out["documented_flood_year"] = out["year"].isin(DOCUMENTED_JAKARTA_FLOOD_YEARS)
    out = clean_names(out[["date", "year", "month", "month_name", "rainfall_mm", "documented_flood_year"]])
    out.to_csv(DATA_SAC / "sac_rainfall_timeseries.csv", index=False)
    return out


def export_flood_events() -> pd.DataFrame:
    df = pd.read_csv(DFO)
    df = df[df["Country"].astype(str).str.contains("Indonesia", case=False, na=False)].copy()
    df["start_date"] = pd.to_datetime(df["Start Date"], errors="coerce")
    df = df.dropna(subset=["start_date"])
    df["year"] = df["start_date"].dt.year
    annual = df.groupby("year").size().reset_index(name="n_flood_events_indonesia")
    annual["n_flood_events_jakarta_region"] = np.where(annual["year"].isin(DOCUMENTED_JAKARTA_FLOOD_YEARS), 1, 0)
    out = clean_names(annual)
    out.to_csv(DATA_SAC / "sac_flood_events.csv", index=False)
    return out


def export_population_exposure() -> pd.DataFrame:
    feat = pd.read_csv(FEATURES)
    out = feat[["kec_code", "kecamatan", "kota", "pop_est", "area_km2"]].copy()
    out["pop_density"] = out["pop_est"] / out["area_km2"]
    out = clean_names(out)
    out.to_csv(DATA_SAC / "sac_population_exposure.csv", index=False)
    return out


def export_infrastructure_exposure() -> pd.DataFrame:
    feat = pd.read_csv(FEATURES)
    out = feat[["kec_code", "kecamatan", "kota", "schools", "health_facilities", "pop_est"]].copy()
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
    print(export_population_exposure().shape, "sac_population_exposure.csv")
    print(export_infrastructure_exposure().shape, "sac_infrastructure_exposure.csv")
    print(export_risk_factors().shape, "sac_risk_factors.csv")


if __name__ == "__main__":
    main()
