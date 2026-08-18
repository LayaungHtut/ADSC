"""Generate `data/data_dictionary.csv` from the processed kecamatan dataset.

For every column we record: dataset, type, unit, description, source,
transformation, missing percentage (computed from the real data) and known
limitations. Nothing is invented; column metadata is anchored to the pipeline
that created it (floodresilience/analysis/pipeline.py).
"""

from __future__ import annotations

import pandas as pd

from floodresilience.config import DATA_PROCESSED

FEATURES = DATA_PROCESSED / "jakarta_kecamatan_features.csv"

COLUMN_META: dict[str, dict] = {
    "kec_code": {
        "type": "string",
        "unit": "-",
        "description": "Official Indonesian kecamatan (district) code",
        "source": "GeoBoundaries / Alf-Anas admin boundaries",
        "transformation": "stripped, string-cast",
        "limitations": "Official BPS codes; Kepulauan Seribu excluded (2 offshore kecamatan)",
    },
    "kecamatan": {
        "type": "string",
        "unit": "-",
        "description": "Kecamatan name (title case)",
        "source": "GeoBoundaries / Alf-Anas admin boundaries",
        "transformation": "title-cased",
        "limitations": "-",
    },
    "kota": {
        "type": "string",
        "unit": "-",
        "description": "Kota administrasi (municipal area) of DKI Jakarta",
        "source": "GeoBoundaries / Alf-Anas admin boundaries",
        "transformation": "'Kota Administrasi ' prefix removed, title-cased",
        "limitations": "Kepulauan Seribu removed",
    },
    "rain_annual_mean_mm": {
        "type": "float",
        "unit": "mm/year",
        "description": "Mean annual rainfall from the complete-years CHIRPS series",
        "source": "CHIRPS v2.0 monthly (UCSB Climate Hazards Center), 1981-2026",
        "transformation": "zonal mean per kecamatan, complete years only (12 months present)",
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
        "description": "Share of mean annual rainfall falling in wet-season months (Dec-Mar)",
        "source": "CHIRPS v2.0 monthly",
        "transformation": "sum(wet-season monthly means) / sum(all monthly means)",
        "limitations": "Wet-season window (12,1,2,3) is a simplification of the monsoon pattern",
    },
    "rain_extreme_months": {
        "type": "int",
        "unit": "count",
        "description": "Number of months with rainfall >= 95th percentile of the kecamatan series",
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
        "limitations": "-",
    },
    "elev_mean_m": {
        "type": "float",
        "unit": "m",
        "description": "Mean elevation within the kecamatan",
        "source": "Copernicus DEM GLO-30 (30 m DSM)",
        "transformation": "zonal mean over mosaicked DEM tiles",
        "limitations": "DSM includes vegetation/buildings; coastal sea gaps read ~0",
    },
    "elev_min_m": {
        "type": "float",
        "unit": "m",
        "description": "Minimum elevation within the kecamatan",
        "source": "Copernicus DEM GLO-30",
        "transformation": "zonal min",
        "limitations": "Values below 0 indicate below-sea-level terrain",
    },
    "elev_max_m": {
        "type": "float",
        "unit": "m",
        "description": "Maximum elevation within the kecamatan",
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
        "transformation": "area-weighted intersection of H3 hexagons with kecamatan polygon",
        "limitations": "Model estimate, not census",
    },
    "schools": {
        "type": "int",
        "unit": "facilities",
        "description": "Count of school facilities inside the kecamatan",
        "source": "HDX / OSM school facilities (IDN_school_facilities)",
        "transformation": "point-in-polygon count",
        "limitations": "OSM-derived; may undercount private/informal schools",
    },
    "health_facilities": {
        "type": "int",
        "unit": "facilities",
        "description": "Count of health facilities inside the kecamatan",
        "source": "HDX / HOTOSM health facilities",
        "transformation": "point-in-polygon count",
        "limitations": "OSM-derived; may undercount",
    },
    "rfh_mean": {
        "type": "float",
        "unit": "index",
        "description": "Mean rainfall-flood hazard index (recent, 2022+)",
        "source": "World Bank / GFDRR subnational rainfall indicators (ADM2)",
        "transformation": "grouped by kota, mean over time",
        "limitations": "Kota-level only (all kecamatan in a kota share the value)",
    },
    "r1h_mean": {
        "type": "float",
        "unit": "index",
        "description": "Mean 1-hour rainfall index (recent, 2022+)",
        "source": "World Bank / GFDRR subnational rainfall indicators",
        "transformation": "grouped by kota, mean over time",
        "limitations": "Kota-level only",
    },
    "r3h_mean": {
        "type": "float",
        "unit": "index",
        "description": "Mean 3-hour rainfall index (recent, 2022+)",
        "source": "World Bank / GFDRR subnational rainfall indicators",
        "transformation": "grouped by kota, mean over time",
        "limitations": "Kota-level only",
    },
    "rfh_p95": {
        "type": "float",
        "unit": "index",
        "description": "95th percentile of the rainfall-flood hazard index",
        "source": "World Bank / GFDRR subnational rainfall indicators",
        "transformation": "nanpercentile 95 per kota",
        "limitations": "Kota-level only",
    },
    "n_obs": {
        "type": "int",
        "unit": "count",
        "description": "Number of observations contributing to kota rainfall indices",
        "source": "World Bank / GFDRR subnational rainfall indicators",
        "transformation": "count",
        "limitations": "-",
    },
    "child_share": {
        "type": "float",
        "unit": "fraction 0-1",
        "description": "Share of population aged 0-14",
        "source": "WorldPop ADM2 (UN-adjusted, 2020)",
        "transformation": "sum(T_00_04, T_05_09, T_10_14) / T_TL per kota",
        "limitations": "Kota-level only; census-based aggregation",
    },
    "elderly_share": {
        "type": "float",
        "unit": "fraction 0-1",
        "description": "Share of population aged 65+",
        "source": "WorldPop ADM2 (UN-adjusted, 2020)",
        "transformation": "sum(T_65_69, T_70_74, T_75Plus) / T_TL per kota",
        "limitations": "Kota-level only",
    },
    "area_km2": {
        "type": "float",
        "unit": "km²",
        "description": "Kecamatan area",
        "source": "Admin boundaries (geometry)",
        "transformation": "area in EPSG:32748 / 1e6",
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
    rows = []
    for col in df.columns:
        meta = COLUMN_META.get(col, {
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
            "dataset": "jakarta_kecamatan_features",
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