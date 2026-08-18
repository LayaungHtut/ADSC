# SAP Analytics Cloud Import Guide

All SAC-ready datasets live in `data/sac/` as CSV. They are exported by
`floodresilience/export/sac.py`. Column names are lowercase with `_` separators;
geographic keys use official Indonesian administrative codes.

## Files

### sac_risk_by_area.csv
Main risk dataset — one row per kecamatan (42 rows).

| Column | Type | Unit | Description |
|---|---|---|---|
| `kec_code` | string | - | Official kecamatan code, e.g. `31.75.06` |
| `kecamatan` | string | - | Kecamatan name (localized) |
| `kota` | string | - | Kota / municipal area (Jakarta Barat, Timur, Selatan, Utara, Pusat) |
| `hazard` | float | 0-1 | Hazard index (elevation + rainfall + extremes) |
| `exposure` | float | 0-1 | Exposure index (population + density + facilities) |
| `vulnerability` | float | 0-1 | Vulnerability index (age composition) |
| `risk` | float | 0-1 | Composite risk = 0.4·hazard + 0.35·exposure + 0.25·vulnerability |
| `risk_100` | float | 0-100 | Risk rescaled for readability |
| `risk_class` | int | 1-5 | Quintile class (5 = highest) |
| `pop_est` | float | persons | Modelled resident population |
| `elev_mean_m` | float | m | Mean elevation from DEM |
| `schools` | int | facilities | Count of school points |
| `health_facilities` | int | facilities | Count of health facility points |
| `area_km2` | float | km² | Area |

### sac_risk_factors.csv
Full indicator set (42 rows, 27 columns) — inputs to the risk index:

- `rain_annual_mean_mm`, `rain_annual_last5_mean_mm`, `rain_wet_season_share`,
  `rain_extreme_months`, `rain_annual_trend_mm_yr`, `rain_annual_trend_pct_yr`,
  `rain_p95_monthly_mm`, `rain_total_months` — CHIRPS-based rainfall indicators.
- `elev_mean_m`, `elev_min_m`, `elev_max_m`, `slope_mean_pct` — DEM indicators.
- `pop_est`, `pop_density` — population.
- `schools`, `health_facilities` — critical infrastructure.
- `rfh_mean`, `r1h_mean`, `r3h_mean`, `rfh_p95`, `n_obs` — World Bank / GFDRR
  rainfall-flood indices (10-day scale, 2022+).
- `child_share`, `elderly_share` — population age shares.
- `area_km2` — area.

### sac_rainfall_timeseries.csv
Monthly rainfall for the Jakarta study area (547 rows, 1981-01 to 2026-07).
Columns: `date`, `year`, `month`, `month_name`, `rainfall_mm`,
`documented_flood_year` (True for 2002/2007/2013/2020/2025).

### sac_flood_events.csv
Annual flood event counts from the Dartmouth Flood Observatory (39 rows).
Columns: `year`, `n_flood_events_indonesia`, `n_flood_events_jakarta_region`
(flag = 1 for documented major Jakarta flood years).

### sac_population_exposure.csv
Columns: `kec_code`, `kecamatan`, `kota`, `pop_est`, `area_km2`, `pop_density`.

### sac_infrastructure_exposure.csv
Columns: `kec_code`, `kecamatan`, `kota`, `schools`, `health_facilities`,
`pop_est`, `schools_per_100k`, `health_per_100k`.

## Importing in SAC

1. Use **Import > Data > Local file** and upload the CSV.
2. Set `kecamatan` (or `kec_code`) as the Geo dimension key; `kota` as secondary.
3. Mark `risk_class` as a category/segment, not a measure.
4. For the rainfall time series, set `date` as Time and `rainfall_mm` as Measure.
5. Bind a background map: upload `data/processed/jakarta_kecamatan_risk.geojson`
   via **Geo Data > Geo Enrichment** using `kec_code` as the join key.

## Provenance & quality

- All numeric values come from public data with documented provenance
  (`data/raw/PROVENANCE.csv`). No values are invented.
- Data-quality report: `outputs/reports/data_quality_report.md`.
- Known limits: vulnerability is kota-level; CHIRPS ~5.5 km resolution; OSM
  facility lists may undercount.