# Data Quality Report

Automatically generated from the ingestion pipeline. **No rows are ever deleted**; issues are recorded here for the analyst.

Generated: 2026-08-17T12:12:08+00:00

## boundaries_kecamatan
- Rows: 42, Columns: 4
- **missing_values**: `PASS` — 0 columns have missing values; max rate 0.0%
- **duplicates**: `PASS` — 0 duplicate rows
- **infinite_values**: `PASS` — 0 infinite values
- **outliers_3iqr**: `INFO` — none beyond 3x IQR

## chirps_monthly_series
- Rows: 547, Columns: 3
- **missing_values**: `PASS` — 0 columns have missing values; max rate 0.0%
- **duplicates**: `PASS` — 0 duplicate rows
- **invalid_dates**: `PASS` — 0 invalid dates in month
- **date_range**: `INFO` — 1981-01-01 00:00:00 .. 2026-07-01 00:00:00
- **infinite_values**: `PASS` — 0 infinite values
- **outliers_3iqr**: `INFO` — kec_0:3; kec_1:3

## dem_zonal
- Rows: 42, Columns: 5
- **missing_values**: `PASS` — 0 columns have missing values; max rate 0.0%
- **duplicates**: `PASS` — 0 duplicate rows
- **infinite_values**: `PASS` — 0 infinite values
- **outliers_3iqr**: `INFO` — none beyond 3x IQR

## kontur_population
- Rows: 42, Columns: 2
- **missing_values**: `PASS` — 0 columns have missing values; max rate 0.0%
- **duplicates**: `PASS` — 0 duplicate rows
- **infinite_values**: `PASS` — 0 infinite values
- **outliers_3iqr**: `INFO` — none beyond 3x IQR

## facilities
- Rows: 42, Columns: 3
- **missing_values**: `PASS` — 0 columns have missing values; max rate 0.0%
- **duplicates**: `PASS` — 0 duplicate rows
- **infinite_values**: `PASS` — 0 infinite values
- **outliers_3iqr**: `INFO` — health_facilities:1
