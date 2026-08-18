"""Exploratory analysis and output generation.

Produces:
  - outputs/charts/*.png     (rainfall climatology, trend, risk, exposure)
  - outputs/maps/*.png       (risk, population, elevation, rainfall, facilities)
  - outputs/tables/*.csv     (summary tables)
  - data/processed/jakarta_kecamatan_risk.geojson  (map-ready, WGS84)
"""

from __future__ import annotations

import glob
from pathlib import Path

import geopandas as gpd
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import rasterio

from floodresilience.config import (
    DATA_PROCESSED,
    DATA_RAW,
    DATA_INTERMEDIATE,
    OUTPUT_CHARTS,
    OUTPUT_MAPS,
    OUTPUT_TABLES,
    JAKARTA_BBOX,
    CRS_WGS84,
)
from floodresilience.features.risk_index import build_risk_dataset, risk_scores, DEFAULT_WEIGHTS

FEATURES = DATA_PROCESSED / "jakarta_kecamatan_features.csv"
CHIRPS_DIR = DATA_INTERMEDIATE / "rainfall" / "chirps"
DFO = DATA_RAW / "dfo" / "Global_Flood_Records.csv"
BOUNDARY_SRC = DATA_RAW / "boundaries" / "alfanas" / "DKI_Jakarta_kecamatan.geojson"

MAJOR_JAKARTA_FLOOD_YEARS = [2002, 2007, 2013, 2020, 2025]


def load_chirps_annual() -> pd.DataFrame:
    files = sorted(glob.glob(str(CHIRPS_DIR / "chirps_*.tif")))
    rows = []
    for f in files:
        year = int(Path(f).stem.split("_")[1][:4])
        with rasterio.open(f) as ds:
            a = ds.read(1).astype("float64")
        a[a < 0] = np.nan
        rows.append({"year": year, "monthly": float(np.nanmean(a))})
    df = pd.DataFrame(rows)
    return df.groupby("year")["monthly"].sum().reset_index()


def fig_save(fig, name: str) -> None:
    fig.tight_layout()
    fig.savefig(name, dpi=160, bbox_inches="tight")
    plt.close(fig)
    print("wrote", name)


def chart_rainfall_climatology() -> None:
    df = pd.read_csv(FEATURES)
    # Monthly climatology from the kecamatan feature series is not stored;
    # recompute quickly from CHIRPS files (bbox mean per calendar month).
    files = sorted(glob.glob(str(CHIRPS_DIR / "chirps_*.tif")))
    by_month = {m: [] for m in range(1, 13)}
    for f in files:
        m = int(Path(f).stem.split("_")[1][4:6])
        with rasterio.open(f) as ds:
            a = ds.read(1).astype("float64")
        a[a < 0] = np.nan
        by_month[m].append(float(np.nanmean(a)))
    clim = {m: float(np.mean(v)) for m, v in by_month.items() if v}
    months = list(range(1, 13))
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.bar(months, [clim[m] for m in months], color="#2563eb")
    ax.axvspan(11.5, 4.5, color="orange", alpha=0.12, label="Dec-Mar (wet season)")
    ax.set_xticks(months)
    ax.set_xticklabels(["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"])
    ax.set_ylabel("Mean monthly rainfall (mm)")
    ax.set_title("Jakarta rainfall climatology 1981-2026 (CHIRPS v2.0)")
    ax.legend()
    fig_save(fig, OUTPUT_CHARTS / "rainfall_climatology.png")


def chart_rainfall_trend() -> None:
    ann = load_chirps_annual()
    fig, ax = plt.subplots(figsize=(9, 4.5))
    ax.bar(ann["year"], ann["monthly"], color="#93c5fd")
    for y in MAJOR_JAKARTA_FLOOD_YEARS:
        ax.annotate(str(y), (y, ann.loc[ann["year"] == y, "monthly"].values[0]),
                    xytext=(0, 4), textcoords="offset points", ha="center", fontsize=7, color="#dc2626")
    mean = ann["monthly"].mean()
    ax.axhline(mean, color="#1e3a8a", ls="--", lw=1, label=f"1981-2025 mean ({mean:.0f} mm)")
    z = np.polyfit(ann["year"], ann["monthly"], 1)
    ax.plot(ann["year"], np.polyval(z, ann["year"]), color="#dc2626", lw=1.5, label=f"OLS trend ({z[0]:.1f} mm/yr)")
    ax.set_xlabel("Year"); ax.set_ylabel("Annual rainfall (mm)")
    ax.set_title("Jakarta annual rainfall 1981-2026; annotated years = major flood years")
    ax.legend()
    fig_save(fig, OUTPUT_CHARTS / "rainfall_annual_trend.png")


def chart_dfo_indonesia() -> None:
    df = pd.read_csv(DFO)
    df = df[df["Country"].astype(str).str.contains("Indonesia", case=False, na=False)].copy()
    df["Start Date"] = pd.to_datetime(df["Start Date"], errors="coerce")
    df = df.dropna(subset=["Start Date"])
    df["year"] = df["Start Date"].dt.year
    counts = df.groupby("year").size()
    fig, ax = plt.subplots(figsize=(9, 4.5))
    ax.bar(counts.index, counts.values, color="#34d399")
    ax.set_xlabel("Year"); ax.set_ylabel("Flood events in Indonesia (DFO)")
    ax.set_title("Dartmouth Flood Observatory flood events, Indonesia (1985-2023)")
    fig_save(fig, OUTPUT_CHARTS / "dfo_indonesia_flood_events.png")


def chart_risk_distribution() -> None:
    risk = pd.read_csv(OUTPUT_TABLES / "risk_scores.csv")
    top = risk.sort_values("risk_100", ascending=False).head(10)
    fig, ax = plt.subplots(figsize=(9, 4.5))
    ax.barh(top["kecamatan"], top["risk_100"], color="#0f766e")
    ax.invert_yaxis()
    ax.set_xlabel("Risk score (0-100)")
    ax.set_title("Top 10 kecamatan by flood risk (default weights)")
    fig_save(fig, OUTPUT_CHARTS / "top10_risk.png")


def chart_exposure_components() -> None:
    df = pd.read_csv(FEATURES)
    fig, axes = plt.subplots(1, 3, figsize=(13, 4))
    axes[0].hist(df["pop_est"] / 1000, bins=14, color="#6366f1")
    axes[0].set_title("Population (thousands)")
    axes[1].hist(df["schools"], bins=14, color="#f59e0b")
    axes[1].set_title("Schools")
    axes[2].hist(df["health_facilities"], bins=14, color="#ef4444")
    axes[2].set_title("Health facilities")
    fig_save(fig, OUTPUT_CHARTS / "exposure_components.png")


def chart_elevation_vs_risk() -> None:
    risk = pd.read_csv(OUTPUT_TABLES / "risk_scores.csv")
    df = pd.read_csv(FEATURES)
    merged = risk.merge(df[["kec_code", "elev_mean_m"]], on="kec_code")
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.scatter(merged["elev_mean_m"], merged["risk_100"], s=40, color="#2563eb", alpha=0.8)
    ax.set_xlabel("Mean elevation (m)"); ax.set_ylabel("Risk score (0-100)")
    ax.set_title("Low-elevation kecamatan tend to rank higher risk")
    fig_save(fig, OUTPUT_CHARTS / "elevation_vs_risk.png")


def make_risk_geojson() -> None:
    """Merge risk scores into boundary geometries and export GeoJSON for the app."""
    b = gpd.read_file(BOUNDARY_SRC)
    b = b[b["PROVINSI"].str.contains("Jakarta", na=False)].copy()
    b["kec_code"] = b["KODE_KEC"].astype(str).str.strip()
    b["kecamatan"] = b["KECAMATAN"].str.title()
    b["kota"] = b["KAB_KOTA"].str.replace("Kota Administrasi ", "", regex=False).str.title()
    b = b[b["kota"] != "Administrasi Kepulauan Seribu"]
    risk = pd.read_csv(OUTPUT_TABLES / "risk_scores.csv")
    feat = pd.read_csv(FEATURES)
    merged = b.merge(risk, on="kec_code", suffixes=("", "_risk")).merge(
        feat[["kec_code", "pop_est", "elev_mean_m", "schools", "health_facilities"]], on="kec_code"
    )
    merged = merged[["kec_code", "kecamatan", "kota", "hazard", "exposure", "vulnerability", "risk_100", "risk_class", "pop_est", "elev_mean_m", "schools", "health_facilities", "geometry"]]
    merged = merged.rename(columns={"risk_100": "risk_score"})
    merged.to_file(DATA_PROCESSED / "jakarta_kecamatan_risk.geojson", driver="GeoJSON")
    print("wrote", DATA_PROCESSED / "jakarta_kecamatan_risk.geojson")


def make_choropleth_maps() -> None:
    g = gpd.read_file(DATA_PROCESSED / "jakarta_kecamatan_risk.geojson")

    def plot(column, cmap, title, out, log=False):
        fig, ax = plt.subplots(figsize=(7, 7))
        vmin, vmax = g[column].min(), g[column].max()
        g.plot(column=column, cmap=cmap, ax=ax, edgecolor="white", linewidth=0.4,
               legend=True, legend_kwds={"shrink": 0.6}, vmin=vmin, vmax=vmax)
        ax.set_title(title, fontsize=10)
        ax.set_axis_off()
        fig_save(fig, out)

    plot("risk_score", "YlOrRd", "Flood risk score (0-100)", OUTPUT_MAPS / "risk_map.png")
    plot("hazard", "Blues", "Hazard score", OUTPUT_MAPS / "hazard_map.png")
    plot("exposure", "Greens", "Exposure score", OUTPUT_MAPS / "exposure_map.png")
    plot("vulnerability", "Purples", "Vulnerability score", OUTPUT_MAPS / "vulnerability_map.png")


def summary_tables() -> None:
    df = pd.read_csv(FEATURES)
    risk = pd.read_csv(OUTPUT_TABLES / "risk_scores.csv")
    # Kota-level aggregate
    agg = risk.merge(df[["kec_code", "pop_est"]], on="kec_code").groupby("kota").agg(
        kecamatan=("kec_code", "count"),
        pop_total=("pop_est", "sum"),
        mean_risk=("risk_100", "mean"),
    ).reset_index().round(2)
    agg.to_csv(OUTPUT_TABLES / "summary_by_kota.csv", index=False)
    # Exposure summary
    exp = df[["kecamatan", "pop_est", "pop_density", "schools", "health_facilities", "elev_mean_m"]].round(2)
    exp.to_csv(OUTPUT_TABLES / "summary_exposure.csv", index=False)
    print(agg.to_string(index=False))


def main() -> None:
    chart_rainfall_climatology()
    chart_rainfall_trend()
    chart_dfo_indonesia()
    chart_risk_distribution()
    chart_exposure_components()
    chart_elevation_vs_risk()
    make_risk_geojson()
    make_choropleth_maps()
    summary_tables()


if __name__ == "__main__":
    main()
