# Data Quality Report

Automatically generated from the ingestion pipeline. **No rows are ever deleted**; issues are recorded here for the analyst.

Generated: 2026-08-18T08:52:22+00:00

## boundaries_township
- Rows: 45, Columns: 5
- **missing_values**: `PASS` — 0 columns have missing values; max rate 0.0%
- **duplicates**: `PASS` — 0 duplicate rows
- **infinite_values**: `PASS` — 0 infinite values
- **outliers_3iqr**: `INFO` — none beyond 3x IQR

## chirps_monthly_series
- Rows: 245, Columns: 3
- **missing_values**: `PASS` — 0 columns have missing values; max rate 0.0%
- **duplicates**: `PASS` — 0 duplicate rows
- **invalid_dates**: `PASS` — 0 invalid dates in month
- **date_range**: `INFO` — 1981-01-01 00:00:00 .. 2001-05-01 00:00:00
- **infinite_values**: `PASS` — 0 infinite values
- **outliers_3iqr**: `INFO` — none beyond 3x IQR

## dem_zonal
- Rows: 45, Columns: 5
- **missing_values**: `PASS` — 0 columns have missing values; max rate 0.0%
- **duplicates**: `PASS` — 0 duplicate rows
- **infinite_values**: `PASS` — 0 infinite values
- **outliers_3iqr**: `INFO` — elev_max_m:2

## kontur_population
- Rows: 45, Columns: 2
- **missing_values**: `PASS` — 0 columns have missing values; max rate 0.0%
- **duplicates**: `PASS` — 0 duplicate rows
- **infinite_values**: `PASS` — 0 infinite values
- **outliers_3iqr**: `INFO` — pop_est:1

## facilities
- Rows: 45, Columns: 3
- **missing_values**: `PASS` — 0 columns have missing values; max rate 0.0%
- **duplicates**: `PASS` — 0 duplicate rows
- **infinite_values**: `PASS` — 0 infinite values
- **outliers_3iqr**: `INFO` — health_facilities:2
