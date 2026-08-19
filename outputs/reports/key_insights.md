# Key Insights

Automated analytical summary. Each insight reports metric, value, comparison, source, interpretation and limitation.

Generated: 2026-08-19T00:00:00+00:00 (regenerated after census-data update)

## 1. Highest-risk township
- **Metric**: risk_100
- **Value**: 58.3
- **Comparison**: vs Yangon mean 42.5
- **Source**: outputs/tables/risk_scores.csv
- **Interpretation**: Kayan (South) ranks highest under the default hazard-exposure-vulnerability weighting; it combines high population, dense critical facilities and strong rainfall exposure.
- **Limitation**: Ranking depends on documented weights; see risk_sensitivity.csv.

## 2. Township with largest population
- **Metric**: pop_est (persons)
- **Value**: 687,867
- **Comparison**: of Yangon total 7,360,703
- **Source**: sac_population_exposure.csv (2014 Census, official township totals)
- **Interpretation**: Hlaingtharya hosts the largest resident population among the 45 Yangon townships.
- **Limitation**: Census is 2014 vintage; population may have grown since.

## 3. Population in highest-risk class
- **Metric**: pop_est (persons)
- **Value**: 2,599,370
- **Comparison**: 35.3% of Yangon population
- **Source**: risk_scores.csv + sac_population_exposure.csv
- **Interpretation**: A substantial share of Yangon's population lives in the top risk quintile of townships.
- **Limitation**: Class boundaries are quintiles of the risk score; they are relative, not absolute safety thresholds.

## 4. Elevation gradient (flood-prone lowlands near the rivers)
- **Metric**: elev_mean_m
- **Value**: min -9.2 m .. max 37.5 m
- **Comparison**: lowest point Hlaingtharya (-9.2 m), highest mean Taikkyi (37.5 m)
- **Source**: Copernicus DEM 30m, zonal stats
- **Interpretation**: Townships along the Yangon, Bago and Hlaing rivers and the delta fringe sit at low elevation, consistent with documented fluvial/pluvial flood exposure.
- **Limitation**: DEM is a surface model (DSM) and does not capture flood depth or drainage.

## 5. Rainfall seasonality
- **Metric**: mean monthly rainfall (mm)
- **Value**: peak month 7 (698.9)
- **Comparison**: wettest months [7, 8, 6, 9], driest [1, 2, 12]
- **Source**: CHIRPS v2.0 monthly, 1981-01 .. 2026-07
- **Interpretation**: Rainfall is strongly seasonal under the southwest monsoon; the wet season aligns with the documented peak flooding period (May-Oct).
- **Limitation**: Monthly means smooth extreme sub-monthly events that trigger flash floods.

## 6. Long-term rainfall trend
- **Metric**: mm/year (OLS)
- **Value**: 15.0
- **Comparison**: over 1981-2025
- **Source**: CHIRPS v2.0 monthly aggregated annually (bbox mean)
- **Interpretation**: OLS slope is small; no strong linear trend is assumed. Interannual variability dominates.
- **Limitation**: OLS trend over 44 years is sensitive to endpoints; no significance test applied here.

## 7. Documented flood years align with wet years
- **Metric**: annual rainfall (mm)
- **Value**: 2,903.4
- **Comparison**: mean of documented flood years 2,903 vs overall mean 2,844
- **Source**: CHIRPS + documented Yangon flood years (PIAHS 2024; Sritarapipat 2017; OCHA 2017; UNOSAT 2020)
- **Interpretation**: On average, years with documented major Yangon floods were wetter than the long-run mean, supporting rainfall as a hazard driver.
- **Limitation**: Correlation between rainfall and flood occurrence is not causation; river levels, tides, drainage and land use also matter.

## 8. Critical infrastructure concentration
- **Metric**: facilities
- **Value**: 1,320 schools, 1,178 health facilities
- **Comparison**: within Yangon's 45 townships
- **Source**: HDX / OSM education & health facility polygons (Myanmar)
- **Interpretation**: Schools and health facilities are spread across all townships, so any flood event threatens public services.
- **Limitation**: OSM-based facility lists may undercount private or informal facilities.

## 9. Recent flood-relevant rainfall intensity
- **Metric**: rfh index (mean, 2022-2026)
- **Value**: 87.8
- **Comparison**: highest in South
- **Source**: World Bank / GFDRR subnational rainfall indicators (ADM2)
- **Interpretation**: Parts of Yangon show higher recent rainfall-flood index values on the 10-day scale.
- **Limitation**: Indices are at district level (not township) and cover only 2022+.

## 10. National flood-events context (DFO)
- **Metric**: events (1990-2023)
- **Value**: 33
- **Comparison**: DFO-documented flood events in Myanmar
- **Source**: Dartmouth Flood Observatory Global Flood Records
- **Interpretation**: Myanmar is one of ASEAN's most flood-affected countries; the Yangon analysis sits within this national hazard context.
- **Limitation**: DFO records are event-based and may omit smaller or under-reported floods.
