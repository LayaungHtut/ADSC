# Methodology Proposal — FloodResilience ASEAN (Phase 1 draft)

## 1. Research question

**Primary question:** Which urban districts within our chosen ASEAN city face the highest flood risk, who and what is exposed, and where should resilience investments be prioritized?

**Supporting sub-questions:**
1. What is the spatial and seasonal pattern of rainfall extremes (2000–present)?
2. Where have historical flood events occurred, and with what frequency?
3. Which areas combine high hazard, high population/infrastructure exposure, and high vulnerability?
4. Can historical environmental conditions explain flood occurrence well enough to support a defensible risk index and a simple ML classifier?
5. Which interventions follow from the evidence, and how do they scale across ASEAN?

## 2. Conceptual framework

Risk = f(Hazard, Exposure, Vulnerability), decomposed into explainable sub-indicators:

- **Hazard (H):** rainfall intensity/extremes (GPM IMERG), historical flood frequency/extent (GFD + DFO), elevation/slope/low-lying proximity to water (Copernicus DEM + JRC water).
- **Exposure (E):** population count/density (WorldPop/GHSL), critical infrastructure (OSM: hospitals, schools, shelters, roads), built-up area (GHSL/WorldCover).
- **Vulnerability (V):** aggregate socioeconomic indicators (national statistics by district), age composition where reliable aggregate data exists, infrastructure quality proxies (road density).

Weights will be set **transparently and tested via sensitivity analysis** (equal weights vs. weighting variants). The final index uses a justified normalization (e.g., min–max or rank-based), **not arbitrary thresholds**. Risk categories are described relative to the observed distribution (e.g., percentile bands) and clearly labeled as analytic classes, not engineering flood zones.

## 3. Analytical pipeline

1. **Acquisition** — global rasters (IMERG, GFD, Copernicus DEM, WorldPop, WorldCover, JRC water, OSM) + local validation data.
2. **Cleaning & quality checks** — missing values, duplicates, invalid dates/coords, unit consistency, outlier review. Every transformation documented (see data-quality pipeline in the master prompt).
3. **Exploratory analysis** — monthly/yearly rainfall, extreme rainfall (e.g., 95th percentile thresholds), flood frequency, seasonal patterns, spatial hotspots.
4. **Statistical analysis** — descriptive stats, correlation (rainfall–flood), seasonal comparisons, trend where data permits. Correlations reported as associations, never as causation.
5. **GIS / spatial analysis** — clip to city boundary, define analysis units (districts/sub-districts), compute zonal summaries, produce risk/exposure maps.
6. **Risk index** — normalize indicators, combine H × E × V, run sensitivity analysis.
7. **ML (only if justified)** — binary classification: "does an area/district experience flooding?" using environmental predictors. Strict temporal/data-leakage prevention; baseline comparison; metrics: precision, recall, F1, ROC-AUC, PR-AUC (imbalanced classes).
8. **Explainability** — feature importance / permutation importance; SHAP only if justified.
9. **Key insights** — each insight includes metric, value, comparison, source, interpretation, limitation.
10. **Decision framework** — WHERE/WHEN/WHO/WHAT/WHY/WHAT-TO-DO.
11. **SAC-ready exports** — clean CSVs in `data/sac/`.
12. **Prototype** — SvelteKit decision-support app; clearly-labeled demo mode.

## 4. Analysis unit

- Primary: **administrative districts/sub-districts** (because decision-makers act at this level and vulnerability data exists at district level).
- Secondary: **grid-based** (250 m) for hazard maps and exposure calculations.

## 5. Validation strategy

- Cross-check satellite flood extents against documented events (news/reports) for the chosen city.
- Compare IMERG rainfall to local gauge records (BMKG/PAGASA/TMD etc.) where obtainable.
- Report model performance honestly; do not overstate predictive claims.
- Document all limitations.

## 6. Deliverables mapped to competition judging

- Problem Definition (10%): crisp problem statement + SDG 11/13 targets + ASEAN alignment.
- Analysis & Insights (25%): rigorous EDA/statistics/GIS, SAC charts with narrative.
- Relevancy & Impact (20%): population/infrastructure exposure and resource-prioritization outputs.
- Viability (15%): stakeholder model + implementation roadmap.
- Innovation (15%): transparent risk framework, ML classification (if justified), interactive digital prototype.
- Presentation Delivery (15%): judge Q&A pack.

## 7. Risks to feasibility (mitigation summary)

- Coarse IMERG (~11 km): mitigated by CHIRPS (~5 km) and local gauges; hazard interpretation stays at district scale.
- GFD ends 2018: mitigated by DFO event catalogue + local reports for recent years.
- OSM completeness varies: mitigated by focusing on the primary city (Yangon, where OSM coverage is moderate) and documenting coverage limits.
- Data licensing/attribution: handled in source catalog.
- Myanmar home-team context: the analysis city (Yangon Region) is chosen on data strength and verifiability, not home-country convenience; local national open data is limited, so the analysis relies on global open datasets (see location_comparison.csv).