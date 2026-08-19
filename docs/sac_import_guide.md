# SAP Analytics Cloud Import Guide

All SAC-ready datasets live in `data/sac/` as CSV. They are exported by
`floodresilience/export/sac.py`. Column names are lowercase with `_` separators;
geographic keys use the official MIMU township P-codes (see below).

> Codes: `tship_code` (`T01`..`T45`) is a stable code derived from boundary
> order, kept for continuity with the web app. `pcode` is the **official MIMU
> township P-code** (`MMR013001`..`MMR013045`). `district` is the Yangon Region
> ADM2 district (East, North, South, West Yangon) with official district codes
> `MMR013D001`..`MMR013D004`.

## Files

### sac_risk_by_area.csv
Main risk dataset — one row per township (45 rows).

| Column | Type | Unit | Description |
|---|---|---|---|
| `tship_code` | string | - | Stable township code (`T01`..`T45`) |
| `township` | string | - | Township name (e.g. Thongwa, Hlaingtharya) |
| `district` | string | - | Yangon district (East, North, South, West) |
| `hazard` | float | 0-1 | Hazard index (elevation + rainfall + extremes) |
| `exposure` | float | 0-1 | Exposure index (population + density + facilities) |
| `vulnerability` | float | 0-1 | Vulnerability index (age composition) |
| `risk` | float | 0-1 | Composite risk = 0.4·hazard + 0.35·exposure + 0.25·vulnerability |
| `risk_100` | float | 0-100 | Risk rescaled for readability |
| `risk_class` | int | 1-5 | Quintile class (5 = highest) |
| `pop_est` | float | persons | **2014 Census** total population (DoP / MIMU) |
| `elev_mean_m` | float | m | Mean elevation from DEM |
| `schools` | int | facilities | Count of school points |
| `health_facilities` | int | facilities | Count of health facility points |
| `area_km2` | float | km² | Area |

### sac_risk_factors.csv
Full indicator set (45 rows, 31 columns) — inputs to the risk index:

- `tship_code`, `township`, `district`, `district_code`, `pcode` — geographic
  keys (`pcode` is the official MIMU township P-code).
- `rain_annual_mean_mm`, `rain_annual_last5_mean_mm`, `rain_wet_season_share`,
  `rain_extreme_months`, `rain_annual_trend_mm_yr`, `rain_annual_trend_pct_yr`,
  `rain_p95_monthly_mm`, `rain_total_months` — CHIRPS-based rainfall indicators.
- `elev_mean_m`, `elev_min_m`, `elev_max_m`, `slope_mean_pct` — DEM indicators.
- `pop_est`, `pop_urban`, `pop_rural`, `pop_density` — **2014 Census**
  population (total, urban, rural, density).
- `schools`, `health_facilities` — critical infrastructure.
- `rfh_mean`, `r1h_mean`, `r3h_mean`, `rfh_p95`, `n_obs` — World Bank / GFDRR
  rainfall-flood indices (10-day scale, district level).
- `child_share`, `elderly_share` — **2014 Census** age shares (0-14 and 65+),
  township level.
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

### sac_flood_events_detail.csv
Per-event DFO records (real observed events, 1990-2023). Columns: `dfo_id`,
`glide_number`, `start_date`, `end_date`, `country`, `main_cause`, `severity`,
`fatalities`, `displaced`, `area_km2`, `source`,
`in_yangon_documented_year`.

### sac_yangon_flood_events.csv
Documented major Yangon flood years with their published source (peer-reviewed
studies, OCHA, UNOSAT) and whether the DFO archive also recorded a Myanmar
event that year. Columns: `year`, `source`, `has_dfo_event_myanmar`.

### sac_population_exposure.csv
Columns: `tship_code`, `township`, `district`, `pop_est`, `area_km2`,
`pop_density`.

### sac_infrastructure_exposure.csv
Columns: `tship_code`, `township`, `district`, `schools`, `health_facilities`,
`pop_est`, `schools_per_100k`, `health_per_100k`.

## Importing in SAC

### Tenant and access

- SAC tenant (ASEAN DSE, AP region): `https://aseandse.ap11.hcs.cloud.sap/`
- Use **Google Chrome** (ideally incognito); credentials are provided by ASEAN
  Foundation. One shared SAC account per team. Team **Zenith** login:
  `tharlunmmt207@gmail.com` (password kept locally in the gitignored `.env`).
- Save all work under **Public > Myanmar > Zenith** — files saved elsewhere are
  deleted without notice (per the official training manual).

### Building the models (Modeler)

Follow the official ASEANDSE SAC workflow (SAC Training Manual 2024):

1. Open **Modeler > Model > Start with data**.
2. **Select Source File** → upload a CSV from `data/sac/` ("Use first row as
   column headers" checked). Import may take time; if it stalls, reload from
   **Draft Sources**.
3. In the data-model page, **review SAC's measure/dimension classification** —
   SAC auto-sorts columns and is sometimes wrong. Every numeric column below
   must be a **Measure** (convert via `… > Convert to Measure`), every text
   column a **Dimension**. Set decimal places where needed (e.g., 2).
4. Set **Exception Aggregation** for any running/period-to-date columns to
   `Last` over `date` — only relevant for `sac_rainfall_timeseries.csv` if you
   add cumulative columns. None of the shipped CSVs contains a running total,
   so default `Sum`/`Average` is correct for the rest.
5. Save the model with a clear name, e.g. `FloodResilience_RiskByArea_MM`.

### Measure / dimension map (per file)

| File | Dimensions | Measures (aggregation) | Notes |
|---|---|---|---|
| `sac_risk_by_area.csv` | `tship_code`, `township`, `district` | `hazard`, `exposure`, `vulnerability`, `risk`, `risk_100` (AVG), `risk_class` (**segment/attribute, not measure**), `pop_est` (SUM), `elev_mean_m` (AVG), `schools`, `health_facilities`, `area_km2` | Base risk model |
| `sac_risk_factors.csv` | `tship_code`, `township`, `district`, `district_code`, `pcode` | all numeric indicator columns (SUM/AVG as appropriate) | Full indicator set |
| `sac_rainfall_timeseries.csv` | `date` (**Time**), `year`, `month`, `month_name`, `documented_flood_year` | `rainfall_mm` (AVG/SUM) | Bind `date` as time |
| `sac_flood_events.csv` | `year` | `n_flood_events_myanmar`, `n_flood_events_yangon_documented` (SUM) | |
| `sac_flood_events_detail.csv` | `dfo_id`, `glide_number`, `start_date` (**Time**), `end_date`, `country`, `main_cause`, `severity` (segment), `source`, `in_yangon_documented_year` | `fatalities`, `displaced`, `area_km2` (SUM) | Per-event detail |
| `sac_yangon_flood_events.csv` | `year`, `source`, `has_dfo_event_myanmar` | — (context table; use as text/table) | Documented Yangon years + citations |
| `sac_population_exposure.csv` | `tship_code`, `township`, `district` | `pop_est` (SUM), `area_km2`, `pop_density` | |
| `sac_infrastructure_exposure.csv` | `tship_code`, `township`, `district` | `schools`, `health_facilities` (SUM), `pop_est`, `schools_per_100k`, `health_per_100k` | |

### Creating the storyboard (Stories)

1. **Stories > Create New > Responsive**, and **select Classic Design Experience**
   (mandatory to follow the standard workflow).
2. Save immediately to **Public > Myanmar > [Team folder]**.
3. **Insert tiles** from the models above (Builder panel: set Measures and
   Dimensions). Use **Duplicate** to copy a tile and swap only the measure.
4. Use **Rank > township > Top N** to simplify charts, and **Exclude** aggregate
   members (e.g., "All") that would skew results.
5. Add **Input Controls** (page filters) for `district` and `risk_class` so
   judges can filter live during the demo.
6. Finish in **Styling mode**: consistent risk color ramp (1=green..5=red),
   legible fonts, reduced decimals.

### Geo enrichment

- Upload `data/processed/yangon_township_risk.geojson` (GeoJSON, WGS84) and join
  to the risk model via **`tship_code`** (or `pcode`) for choropleth/bubble maps.

## Provenance & quality

- All numeric values come from public data with documented provenance
  (`data/raw/PROVENANCE.csv`). No values are invented.
- Population and age composition are **official 2014 Myanmar Census** township
  figures (Department of Population, via MIMU), not model estimates.
- Flood events are observed DFO records; documented Yangon years cite their
  published sources.
- Known limits: census is a 2014 vintage; CHIRPS ~5.5 km resolution; OSM
  facility lists may undercount.
