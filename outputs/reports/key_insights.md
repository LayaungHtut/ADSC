# Key Insights

Automated analytical summary. Each insight reports metric, value, comparison, source, interpretation and limitation.

Generated: 2026-08-17T12:16:31+00:00

## 1. Highest-risk kecamatan
- **Metric**: risk_100
- **Value**: 58.2
- **Comparison**: vs Jakarta mean 43.5
- **Source**: outputs/tables/risk_scores.csv
- **Interpretation**: Cakung (Jakarta Timur) ranks highest under the default hazard-exposure-vulnerability weighting; it combines high population, dense critical facilities and moderate rainfall exposure.
- **Limitation**: Ranking depends on documented weights; see risk_sensitivity.csv.

## 2. Kecamatan with largest population
- **Metric**: pop_est (persons)
- **Value**: 622,072
- **Comparison**: of Jakarta total 10,487,575
- **Source**: sac_population_exposure.csv (Kontur H3, area-weighted)
- **Interpretation**: Cakung hosts the largest resident population among the 42 urban kecamatan.
- **Limitation**: Kontur population is a modeled estimate (Nov 2023), not census.

## 3. Population in highest-risk class
- **Metric**: pop_est (persons)
- **Value**: 3,241,578
- **Comparison**: 30.9% of Jakarta population
- **Source**: risk_scores.csv + sac_population_exposure.csv
- **Interpretation**: A substantial share of Jakarta's population lives in the top risk quintile of kecamatan.
- **Limitation**: Class boundaries are quintiles of the risk score; they are relative, not absolute safety thresholds.

## 4. Elevation gradient (flood-prone lowlands in the north)
- **Metric**: elev_mean_m
- **Value**: min -17.0 m .. max 56.6 m
- **Comparison**: lowest point Pademangan (-17.0 m), highest mean Jagakarsa (56.6 m)
- **Source**: Copernicus DEM 30m, zonal stats
- **Interpretation**: Northern and western coastal kecamatan sit at or below sea level, consistent with documented coastal/pluvial flood exposure.
- **Limitation**: DEM is a surface model (DSM) and does not capture flood depth or drainage.

## 5. Rainfall seasonality
- **Metric**: mean monthly rainfall (mm)
- **Value**: peak month 1 (368.4)
- **Comparison**: wettest months [1, 2, 12, 11], driest [7, 8, 9]
- **Source**: CHIRPS v2.0 monthly, 1981-2026
- **Interpretation**: Rainfall is strongly seasonal; the wet season aligns with documented peak flooding periods (Nov-Mar).
- **Limitation**: Monthly means smooth extreme sub-monthly events that trigger flash floods.

## 6. Long-term rainfall trend
- **Metric**: mm/year (OLS)
- **Value**: 4.9
- **Comparison**: over 1981-2025
- **Source**: CHIRPS v2.0 monthly aggregated annually (bbox mean)
- **Interpretation**: OLS slope is small; no strong linear trend is assumed. Interannual variability dominates.
- **Limitation**: OLS trend over 45 years is sensitive to endpoints; no significance test applied here.

## 7. Documented flood years align with wet years
- **Metric**: annual rainfall (mm)
- **Value**: 2,680.0
- **Comparison**: mean of documented flood years 2,680 vs overall mean 2,407
- **Source**: CHIRPS + documented Jakarta flood years (2002/2007/2013/2020/2025)
- **Interpretation**: On average, years with documented major Jakarta floods were wetter than the 1981-2025 mean, supporting rainfall as a hazard driver.
- **Limitation**: Correlation between rainfall and flood occurrence is not causation; drainage, land subsidence and tides also matter.

## 8. Critical infrastructure concentration
- **Metric**: facilities
- **Value**: 4,685 schools, 780 health facilities
- **Comparison**: within Jakarta's 42 urban kecamatan
- **Source**: HDX school/health facility points (OSM-derived)
- **Interpretation**: Schools and health facilities are spread across all kecamatan, so any flood event threatens public services.
- **Limitation**: OSM-based facility lists may undercount private or informal facilities.

## 9. Recent flood-relevant rainfall intensity
- **Metric**: rfh index (mean, 2022-2026)
- **Value**: 64.3
- **Comparison**: highest in Jakarta Selatan
- **Source**: World Bank / GFDRR subnational rainfall indicators (ADM2)
- **Interpretation**: Southern Jakarta has seen higher recent rainfall-flood index values on the 10-day scale.
- **Limitation**: Indices are at kota level (not kecamatan) and cover only 2022+.
