"""Generate `data/data_dictionary.csv` from the processed township dataset.

For every column we record: dataset, type, unit, description, source,
transformation, missing percentage (computed from the real data) and known
limitations. Nothing is invented; column metadata is anchored to the pipeline
that created it (floodresilience/analysis/pipeline.py).
"""

from __future__ import annotations

import glob
from pathlib import Path

import pandas as pd

from floodresilience.config import DATA_PROCESSED, DATA_INTERMEDIATE

FEATURES = DATA_PROCESSED / "yangon_township_features.csv"
CHIRPS_DIR = DATA_INTERMEDIATE / "rainfall" / "chirps_yangon"


def _chirps_series_info() -> tuple[int, str]:
    """(month count, 'YYYY-MM .. YYYY-MM' span) from the actual CHIRPS tiles."""
    files = sorted(glob.glob(str(CHIRPS_DIR / "chirps_*.tif")))
    if not files:
        return 0, "n/a"
    first = Path(files[0]).stem.split("_")[1]
    last = Path(files[-1]).stem.split("_")[1]
    span = f"{first[:4]}-{first[4:6]} .. {last[:4]}-{last[4:6]}"
    return len(files), span

COLUMN_META: dict[str, dict] = {
    "tship_code": {
        "type": "string",
        "unit": "-",
        "description": "Stable synthetic township code (derived from boundary order)",
        "source": "geoBoundaries Myanmar ADM3 (45 townships)",
        "transformation": "generated from boundary order, stripped, string-cast",
        "limitations": "Synthetic code, not the official MIMU P-code",
    },
    "township": {
        "type": "string",
        "unit": "-",
        "description": "Township name (title case)",
        "source": "geoBoundaries Myanmar ADM3",
        "transformation": "title-cased",
        "limitations": "-",
    },
    "district": {
        "type": "string",
        "unit": "-",
        "description": "Yangon Region district (ADM2)",
        "source": "geoBoundaries Myanmar ADM2",
        "transformation": "assigned by representative point, title-cased",
        "limitations": "Four districts: East, North, South, West Yangon",
    },
    "district_code": {
        "type": "string",
        "unit": "-",
        "description": "Official Myanmar district (ADM2) code",
        "source": "geoBoundaries Myanmar ADM2",
        "transformation": "stripped, string-cast",
        "limitations": "-",
    },
    "rain_annual_mean_mm": {
        "type": "float",
        "unit": "mm/year",
        "description": "Mean annual rainfall from the complete-years CHIRPS series",
        "source": "CHIRPS v2.0 monthly (UCSB Climate Hazards Center)",
        "transformation": "zonal mean per township, complete years only (12 months present)",
        "limitations": "~5.5 km grid; bbox-level zonal aggregation",
    },
    "rain_annual_last5_mean_mm": {
        "type": "float",
        "unit": "mm/year",
        "description": "Mean annual rainfall over the last 5 complete years",
        "source": "CHIRPS v2.0 monthly",
        "transformation": "mean of last 5 annual totals",
        "limitations": "Only if >=5 complete years available",
    },
    "rain_wet_season_share": {
        "type": "float",
        "unit": "fraction 0-1",
        "description": "Share of mean annual rainfall falling in wet-season months (Jun-Sep)",
        "source": "CHIRPS v2.0 monthly",
        "transformation": "sum(wet-season monthly means) / sum(all monthly means)",
        "limitations": "Wet-season window (6,7,8,9) is a simplification of the monsoon pattern",
    },
    "rain_extreme_months": {
        "type": "int",
        "unit": "count",
        "description": "Number of months with rainfall >= 95th percentile of the township series",
        "source": "CHIRPS v2.0 monthly",
        "transformation": "count of months >= p95",
        "limitations": "Threshold is series-specific (relative, not absolute)",
    },
    "rain_annual_trend_mm_yr": {
        "type": "float",
        "unit": "mm/year",
        "description": "OLS slope of annual rainfall over time",
        "source": "CHIRPS v2.0 monthly",
        "transformation": "np.polyfit degree-1 on complete annual totals",
        "limitations": "Descriptive only; no significance test; endpoint sensitive",
    },
    "rain_annual_trend_pct_yr": {
        "type": "float",
        "unit": "%/year",
        "description": "OLS slope normalized by the annual mean",
        "source": "CHIRPS v2.0 monthly",
        "transformation": "slope / annual_mean * 100",
        "limitations": "Same as trend slope",
    },
    "rain_p95_monthly_mm": {
        "type": "float",
        "unit": "mm/month",
        "description": "95th percentile of monthly rainfall",
        "source": "CHIRPS v2.0 monthly",
        "transformation": "nanpercentile(s, 95)",
        "limitations": "-",
    },
    "rain_total_months": {
        "type": "int",
        "unit": "count",
        "description": "Number of months with valid rainfall in the series",
        "source": "CHIRPS v2.0 monthly",
        "transformation": "count of non-null months",
        "limitations": "CHIRPS series available for Yangon bbox (see rain_annual_mean_mm source)",
    },
    "elev_mean_m": {
        "type": "float",
        "unit": "m",
        "description": "Mean elevation within the township",
        "source": "Copernicus DEM GLO-30 (30 m DSM)",
        "transformation": "zonal mean over mosaicked DEM tiles",
        "limitations": "DSM includes vegetation/buildings; coastal sea gaps read ~0",
    },
    "elev_min_m": {
        "type": "float",
        "unit": "m",
        "description": "Minimum elevation within the township",
        "source": "Copernicus DEM GLO-30",
        "transformation": "zonal min",
        "limitations": "Values below 0 indicate below-sea-level terrain",
    },
    "elev_max_m": {
        "type": "float",
        "unit": "m",
        "description": "Maximum elevation within the township",
        "source": "Copernicus DEM GLO-30",
        "transformation": "zonal max",
        "limitations": "-",
    },
    "slope_mean_pct": {
        "type": "float",
        "unit": "%",
        "description": "Mean terrain slope in percent",
        "source": "Copernicus DEM GLO-30 (derived)",
        "transformation": "gradient-based slope from DEM, zonal mean",
        "limitations": "Percent slope; computed from DSM",
    },
    "pop_est": {
        "type": "float",
        "unit": "persons",
        "description": "Modelled resident population (area-weighted)",
        "source": "Kontur population grid (H3, Nov 2023)",
        "transformation": "area-weighted intersection of H3 hexagons with township polygon",
        "limitations": "Model estimate, not census",
    },
    "schools": {
        "type": "int",
        "unit": "facilities",
        "description": "Count of school facilities inside the township",
        "source": "HDX / OSM school facilities (Myanmar)",
        "transformation": "point-in-polygon count",
        "limitations": "OSM-derived; may undercount private/informal schools",
    },
    "health_facilities": {
        "type": "int",
        "unit": "facilities",
        "description": "Count of health facilities inside the township",
        "source": "HDX / HOTOSM health facilities (Myanmar)",
        "transformation": "point-in-polygon count",
        "limitations": "OSM-derived; may undercount",
    },
    "rfh_mean": {
        "type": "float",
        "unit": "index",
        "description": "Mean rainfall-flood hazard index (recent)",
        "source": "World Bank / GFDRR subnational rainfall indicators (ADM2)",
        "transformation": "grouped by district, mean over time",
        "limitations": "District-level only (all townships in a district share the value)",
    },
    "r1h_mean": {
        "type": "float",
        "unit": "index",
        "description": "Mean 1-hour rainfall index (recent)",
        "source": "World Bank / GFDRR subnational rainfall indicators",
        "transformation": "grouped by district, mean over time",
        "limitations": "District-level only",
    },
    "r3h_mean": {
        "type": "float",
        "unit": "index",
        "description": "Mean 3-hour rainfall index (recent)",
        "source": "World Bank / GFDRR subnational rainfall indicators",
        "transformation": "grouped by district, mean over time",
        "limitations": "District-level only",
    },
    "rfh_p95": {
        "type": "float",
        "unit": "index",
        "description": "95th percentile of the rainfall-flood hazard index",
        "source": "World Bank / GFDRR subnational rainfall indicators",
        "transformation": "nanpercentile 95 per district",
        "limitations": "District-level only",
    },
    "n_obs": {
        "type": "int",
        "unit": "count",
        "description": "Number of observations contributing to district rainfall indices",
        "source": "World Bank / GFDRR subnational rainfall indicators",
        "transformation": "count",
        "limitations": "-",
    },
    "child_share": {
        "type": "float",
        "unit": "fraction 0-1",
        "description": "Share of population aged 0-14",
        "source": "WorldPop ADM2 (UN-adjusted, 2020)",
        "transformation": "sum(T_00_04, T_05_09, T_10_14) / T_TL per district",
        "limitations": "District-level only; census-based aggregation",
    },
    "elderly_share": {
        "type": "float",
        "unit": "fraction 0-1",
        "description": "Share of population aged 65+",
        "source": "WorldPop ADM2 (UN-adjusted, 2020)",
        "transformation": "sum(T_65_69, T_70_74, T_75Plus) / T_TL per district",
        "limitations": "District-level only",
    },
    "area_km2": {
        "type": "float",
        "unit": "km²",
        "description": "Township area",
        "source": "Admin boundaries (geometry)",
        "transformation": "area in EPSG:32647 / 1e6",
        "limitations": "-",
    },
    "pop_density": {
        "type": "float",
        "unit": "persons/km²",
        "description": "Population density",
        "source": "Kontur population grid + geometry",
        "transformation": "pop_est / area_km2",
        "limitations": "Derived from modelled population",
    },
}


def main() -> None:
    df = pd.read_csv(FEATURES)
    n_months, span = _chirps_series_info()
    col_meta = dict(COLUMN_META)
    col_meta["rain_annual_mean_mm"] = {
        **col_meta["rain_annual_mean_mm"],
        "source": f"CHIRPS v2.0 monthly (UCSB Climate Hazards Center), {span}",
    }
    col_meta["rain_total_months"] = {
        **col_meta["rain_total_months"],
        "limitations": f"{n_months} months ({span}) available for Yangon bbox",
    }
    rows = []
    for col in df.columns:
        meta = col_meta.get(col, {
            "type": str(df[col].dtype),
            "unit": "-",
            "description": "Derived / auxiliary column",
            "source": "See pipeline (floodresilience/analysis/pipeline.py)",
            "transformation": "-",
            "limitations": "-",
        })
        missing = float(df[col].isna().mean() * 100)
        rows.append({
            "column_name": col,
            "dataset": "yangon_township_features",
            "type": meta["type"],
            "unit": meta["unit"],
            "description": meta["description"],
            "source": meta["source"],
            "transformation": meta["transformation"],
            "missing_percentage": f"{missing:.2f}",
            "limitations": meta["limitations"],
        })
    out = pd.DataFrame(rows)
    out.to_csv("data/data_dictionary.csv", index=False)
    print(out.to_string(index=False))


if __name__ == "__main__":
    main()
