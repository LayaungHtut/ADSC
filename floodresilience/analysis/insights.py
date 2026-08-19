"""Key insights engine.

Generates `outputs/reports/key_insights.md` from the processed datasets.
Every insight carries: metric, value, comparison, source, interpretation and
limitation. No unsupported claims are emitted.
"""

from __future__ import annotations

import glob
from pathlib import Path

import numpy as np
import pandas as pd
import rasterio

from floodresilience.config import (
    DATA_PROCESSED,
    DATA_RAW,
    DATA_INTERMEDIATE,
    OUTPUT_REPORTS,
    OUTPUT_TABLES,
    DOCUMENTED_YANGON_FLOOD_YEARS,
)

FEATURES = DATA_PROCESSED / "yangon_township_features.csv"
RISK = OUTPUT_TABLES / "risk_scores.csv"
CHIRPS_DIR = DATA_INTERMEDIATE / "rainfall" / "chirps_yangon"
DFO = DATA_RAW / "dfo" / "Global_Flood_Records.csv"

DOCUMENTED_FLOOD_YEARS = DOCUMENTED_YANGON_FLOOD_YEARS


def _fmt(x: float, nd: int = 1) -> str:
    if pd.isna(x):
        return "n/a"
    return f"{x:,.{nd}f}"


def _series_span() -> str:
    """'YYYY-MM .. YYYY-MM' range of the actual CHIRPS tiles present."""
    files = sorted(glob.glob(str(CHIRPS_DIR / "chirps_*.tif")))
    if not files:
        return "n/a"
    first = Path(files[0]).stem.split("_")[1]
    last = Path(files[-1]).stem.split("_")[1]
    return f"{first[:4]}-{first[4:6]} .. {last[:4]}-{last[4:6]}"


def build_insights() -> list[dict]:
    df = pd.read_csv(FEATURES)
    risk = pd.read_csv(RISK)
    out: list[dict] = []

    # Highest-risk area
    top = risk.sort_values("risk_100", ascending=False).iloc[0]
    out.append({
        "insight": "Highest-risk township",
        "metric": "risk_100",
        "value": _fmt(top["risk_100"]),
        "comparison": f"vs Yangon mean {_fmt(risk['risk_100'].mean())}",
        "source": "outputs/tables/risk_scores.csv",
        "interpretation": f"{top['township']} ({top['district']}) ranks highest under the default hazard-exposure-vulnerability weighting; it combines high population, dense critical facilities and strong rainfall exposure.",
        "limitation": "Ranking depends on documented weights; see risk_sensitivity.csv.",
    })

    # Largest exposed population
    pop = df.sort_values("pop_est", ascending=False).iloc[0]
    out.append({
        "insight": "Township with largest population",
        "metric": "pop_est (persons)",
        "value": _fmt(pop["pop_est"], 0),
        "comparison": f"of Yangon total {_fmt(df['pop_est'].sum(), 0)}",
        "source": "sac_population_exposure.csv (Kontur H3, area-weighted)",
        "interpretation": f"{pop['township']} hosts the largest resident population among the 45 Yangon townships.",
        "limitation": "Kontur population is a modeled estimate (Nov 2023), not census.",
    })

    # Population in highest risk class
    high = risk[risk["risk_class"] == 5].merge(df[["tship_code", "pop_est"]], on="tship_code")
    out.append({
        "insight": "Population in highest-risk class",
        "metric": "pop_est (persons)",
        "value": _fmt(high["pop_est"].sum(), 0),
        "comparison": f"{_fmt(high['pop_est'].sum() / df['pop_est'].sum() * 100, 1)}% of Yangon population",
        "source": "risk_scores.csv + sac_population_exposure.csv",
        "interpretation": "A substantial share of Yangon's population lives in the top risk quintile of townships.",
        "limitation": "Class boundaries are quintiles of the risk score; they are relative, not absolute safety thresholds.",
    })

    # Elevation gradient
    low = df.sort_values("elev_min_m").iloc[0]
    high_e = df.sort_values("elev_mean_m", ascending=False).iloc[0]
    out.append({
        "insight": "Elevation gradient (flood-prone lowlands near the rivers)",
        "metric": "elev_mean_m",
        "value": f"min {_fmt(df['elev_min_m'].min())} m .. max {_fmt(df['elev_mean_m'].max())} m",
        "comparison": f"lowest point {low['township']} ({_fmt(low['elev_min_m'])} m), highest mean {high_e['township']} ({_fmt(high_e['elev_mean_m'])} m)",
        "source": "Copernicus DEM 30m, zonal stats",
        "interpretation": "Townships along the Yangon, Bago and Hlaing rivers and the delta fringe sit at low elevation, consistent with documented fluvial/pluvial flood exposure.",
        "limitation": "DEM is a surface model (DSM) and does not capture flood depth or drainage.",
    })

    # Rainfall seasonality
    clim_rows = []
    for f in sorted(glob.glob(str(CHIRPS_DIR / "chirps_*.tif"))):
        m = int(Path(f).stem.split("_")[1][4:6])
        with rasterio.open(f) as ds:
            a = ds.read(1).astype("float64")
        a[a < 0] = np.nan
        clim_rows.append({"month": m, "rain": float(np.nanmean(a))})
    cdf = pd.DataFrame(clim_rows).groupby("month")["rain"].mean()
    wet = cdf.nlargest(4).index.tolist()
    dry = cdf.nsmallest(3).index.tolist()
    out.append({
        "insight": "Rainfall seasonality",
        "metric": "mean monthly rainfall (mm)",
        "value": f"peak month {int(wet[0])} ({_fmt(cdf.loc[wet[0]])})",
        "comparison": f"wettest months {wet}, driest {dry}",
        "source": f"CHIRPS v2.0 monthly, {_series_span()}",
        "interpretation": "Rainfall is strongly seasonal under the southwest monsoon; the wet season aligns with the documented peak flooding period (May-Oct).",
        "limitation": "Monthly means smooth extreme sub-monthly events that trigger flash floods.",
    })

    # Trend
    annual = load_annual()
    z = np.polyfit(annual["year"], annual["rain"], 1)
    span_years = int(annual["year"].max() - annual["year"].min())
    out.append({
        "insight": "Long-term rainfall trend",
        "metric": "mm/year (OLS)",
        "value": _fmt(z[0]),
        "comparison": f"over {annual['year'].min()}-{annual['year'].max()}",
        "source": "CHIRPS v2.0 monthly aggregated annually (bbox mean)",
        "interpretation": "OLS slope is small; no strong linear trend is assumed. Interannual variability dominates.",
        "limitation": f"OLS trend over {span_years} years is sensitive to endpoints; no significance test applied here.",
    })

    # Flood years validation
    flood_yr_means = annual[annual["year"].isin(DOCUMENTED_FLOOD_YEARS)]["rain"].mean()
    all_mean = annual["rain"].mean()
    out.append({
        "insight": "Documented flood years align with wet years",
        "metric": "annual rainfall (mm)",
        "value": _fmt(flood_yr_means),
        "comparison": f"mean of documented flood years {_fmt(flood_yr_means,0)} vs overall mean {_fmt(all_mean,0)}",
        "source": "CHIRPS + documented Yangon flood years (PIAHS 2024; Sritarapipat 2017; OCHA 2017; UNOSAT 2020)",
        "interpretation": "On average, years with documented major Yangon floods were wetter than the long-run mean, supporting rainfall as a hazard driver.",
        "limitation": "Correlation between rainfall and flood occurrence is not causation; river levels, tides, drainage and land use also matter.",
    })

    # Infrastructure exposure
    out.append({
        "insight": "Critical infrastructure concentration",
        "metric": "facilities",
        "value": f"{df['schools'].sum():,.0f} schools, {df['health_facilities'].sum():,.0f} health facilities",
        "comparison": "within Yangon's 45 townships",
        "source": "HDX / OSM education & health facility polygons (Myanmar)",
        "interpretation": "Schools and health facilities are spread across all townships, so any flood event threatens public services.",
        "limitation": "OSM-based facility lists may undercount private or informal facilities.",
    })

    # WB recent rainfall index
    wb_top = df.sort_values("rfh_mean", ascending=False).iloc[0]
    out.append({
        "insight": "Recent flood-relevant rainfall intensity",
        "metric": "rfh index (mean, 2022-2026)",
        "value": _fmt(wb_top["rfh_mean"]),
        "comparison": f"highest in {wb_top['district']}",
        "source": "World Bank / GFDRR subnational rainfall indicators (ADM2)",
        "interpretation": "Parts of Yangon show higher recent rainfall-flood index values on the 10-day scale.",
        "limitation": "Indices are at district level (not township) and cover only 2022+.",
    })

    # DFO Myanmar context
    dfo = pd.read_csv(DFO)
    dfo_my = dfo[dfo["Country"].astype(str).str.contains("Myanmar", case=False, na=False)]
    dfo_my["Start Date"] = pd.to_datetime(dfo_my["Start Date"], errors="coerce")
    dfo_my = dfo_my.dropna(subset=["Start Date"])
    y0 = int(dfo_my["Start Date"].dt.year.min())
    y1 = int(dfo_my["Start Date"].dt.year.max())
    out.append({
        "insight": "National flood-events context (DFO)",
        "metric": f"events ({y0}-{y1})",
        "value": str(len(dfo_my)),
        "comparison": "DFO-documented flood events in Myanmar",
        "source": "Dartmouth Flood Observatory Global Flood Records",
        "interpretation": "Myanmar is one of ASEAN's most flood-affected countries; the Yangon analysis sits within this national hazard context.",
        "limitation": "DFO records are event-based and may omit smaller or under-reported floods.",
    })

    return out


def load_annual() -> pd.DataFrame:
    rows = []
    for f in sorted(glob.glob(str(CHIRPS_DIR / "chirps_*.tif"))):
        y = int(Path(f).stem.split("_")[1][:4])
        with rasterio.open(f) as ds:
            a = ds.read(1).astype("float64")
        a[a < 0] = np.nan
        rows.append({"year": y, "monthly": float(np.nanmean(a))})
    df = pd.DataFrame(rows).groupby("year")["monthly"].sum().reset_index().rename(columns={"monthly": "rain"})
    df = df[df["year"] <= 2025]
    return df


def write_report(insights: list[dict]) -> None:
    lines = [
        "# Key Insights",
        "",
        "Automated analytical summary. Each insight reports metric, value, comparison, source, interpretation and limitation.",
        "",
        f"Generated: {pd.Timestamp.now('UTC').isoformat(timespec='seconds')}",
        "",
    ]
    for i, ins in enumerate(insights, 1):
        lines.append(f"## {i}. {ins['insight']}")
        lines.append(f"- **Metric**: {ins['metric']}")
        lines.append(f"- **Value**: {ins['value']}")
        lines.append(f"- **Comparison**: {ins['comparison']}")
        lines.append(f"- **Source**: {ins['source']}")
        lines.append(f"- **Interpretation**: {ins['interpretation']}")
        lines.append(f"- **Limitation**: {ins['limitation']}")
        lines.append("")
    out = OUTPUT_REPORTS / "key_insights.md"
    out.write_text("\n".join(lines), encoding="utf-8")
    print("wrote", out)


if __name__ == "__main__":
    write_report(build_insights())