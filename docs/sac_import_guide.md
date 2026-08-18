# SAP Analytics Cloud Import Guide

All SAC-ready datasets live in `data/sac/` as CSV. They are exported by
`floodresilience/export/sac.py`. Column names are lowercase with `_` separators;
geographic keys use the synthetic township codes (see below).

> Codes: `tship_code` is a stable synthetic code (`T01`..`T45`) derived from
> boundary order, not the official MIMU P-code. `district` is the Yangon Region
> ADM2 district (East, North, South, West Yangon). Official district codes
> (`MMR013D001`..`MMR013D004`) are in `sac_risk_factors.csv`.

## Files

### sac_risk_by_area.csv
Main risk dataset — one row per township (45 rows).

| Column | Type | Unit | Description |
|---|---|---|---|
| `tship_code` | string | - | Synthetic township code (`T01`..`T45`) |
| `township` | string | - | Township name (e.g. Thongwa, Hlaingtharya) |
| `district` | string | - | Yangon district (East, North, South, West) |
| `hazard` | float | 0-1 | Hazard index (elevation + rainfall + extremes) |
| `exposure` | float | 0-1 | Exposure index (population + density + facilities) |
| `vulnerability` | float | 0-1 | Vulnerability index (age composition) |
| `risk` | float | 0-1 | Composite risk = 0.4·hazard + 0.35·exposure + 0.25·vulnerability |
| `risk_100` | float | 0-100 | Risk rescaled for readability |
| `risk_class` | int | 1-5 | Quintile class (5 = highest) |
| `pop_est` | float | persons | Modelled resident population (Kontur H3) |
| `elev_mean_m` | float | m | Mean elevation from DEM |
| `schools` | int | facilities | Count of school points |
| `health_facilities` | int | facilities | Count of health facility points |
| `area_km2` | float | km² | Area |

### sac_risk_factors.csv
Full indicator set (45 rows, 28 columns) — inputs to the risk index:

- `tship_code`, `township`, `district`, `district_code` — geographic keys.
- `rain_annual_mean_mm`, `rain_annual_last5_mean_mm`, `rain_wet_season_share`,
  `rain_extreme_months`, `rain_annual_trend_mm_yr`, `rain_annual_trend_pct_yr`,
  `rain_p95_monthly_mm`, `rain_total_months` — CHIRPS-based rainfall indicators.
- `elev_mean_m`, `elev_min_m`, `elev_max_m`, `slope_mean_pct` — DEM indicators.
- `pop_est`, `pop_density` — population.
- `schools`, `health_facilities` — critical infrastructure.
- `rfh_mean`, `r1h_mean`, `r3h_mean`, `rfh_p95`, `n_obs` — World Bank / GFDRR
  rainfall-flood indices (10-day scale, district level).
- `child_share`, `elderly_share` — population age shares (district level).
- `area_km2` — area.

### sac_rainfall_timeseries.csv
Monthly mean rainfall for the Yangon study-area bbox. Columns: `date`, `year`,
`month`, `month_name`, `rainfall_mm`, `documented_flood_year` (True for the
published major Yangon flood years 1988/1991/1997/2002/2004/2007/2008/2010/
2013/2014/2015/2017/2019/2020).

### sac_flood_events.csv
Annual flood event counts from the Dartmouth Flood Observatory (Myanmar rows).
Columns: `year`, `n_flood_events_myanmar`,
`n_flood_events_yangon_documented` (flag = 1 for documented major Yangon
flood years).

### sac_population_exposure.csv
Columns: `tship_code`, `township`, `district`, `pop_est`, `area_km2`,
`pop_density`.

### sac_infrastructure_exposure.csv
Columns: `tship_code`, `township`, `district`, `schools`, `health_facilities`,
`pop_est`, `schools_per_100k`, `health_per_100k`.

## Importing in SAC

1. Use **Import > Data > Local file** and upload the CSV.
2. Set `township` (or `tship_code`) as the Geo dimension key; `district` as
   secondary.
3. Mark `risk_class` as a category/segment, not a measure.
4. For the rainfall time series, set `date` as Time and `rainfall_mm` as Measure.
5. Bind a background map: upload `data/processed/yangon_township_risk.geojson`
   via **Geo Data > Geo Enrichment** using `tship_code` as the join key.

## Provenance & quality

- All numeric values come from public data with documented provenance
  (`data/raw/PROVENANCE.csv`). No values are invented.
- Data-quality report: `outputs/reports/data_quality_report.md`.
- Known limits: vulnerability is district-level; CHIRPS ~5.5 km resolution; OSM
  facility lists may undercount.
