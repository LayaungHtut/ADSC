# Limitations (Phase 1)

This file documents known limitations BEFORE data is collected, to keep us honest during analysis.

## Data limitations

1. **Precipitation resolution** — GPM IMERG is ~0.1° (~11 km). City-scale flood causation cannot be resolved at this scale alone; CHIRPS (~5 km) and local gauges are needed. Satellite estimates have lower skill over complex terrain and coastlines.
2. **Flood-extent limitations** — GFD maps only 913 large events (2000–2018) that MODIS could observe; small, frequent, urban flash floods are under-represented. Cloud cover and the 250 m MODIS footprint limit detection.
3. **Population estimates** — WorldPop/GHSL are model-based disaggregations of census data; uncertainty is higher in dense informal settlements.
4. **OSM completeness** — volunteer data; facility counts reflect mapping effort as much as real distribution.
5. **DEM representation** — Copernicus DEM is a Digital Surface Model (includes buildings/vegetation), not bare-earth; important for urban flood hydraulics.
6. **Temporal gap** — GFD stops at 2018; post-2018 events need other sources (DFO, local reports, Flood Hub).

## Methodological limitations

7. Correlation ≠ causation; we will report associations only.
8. Risk indices are inherently model choices (weights, normalization, aggregation); we will run sensitivity analyses and report ranges rather than false precision.
9. ML, if used, classifies *association with historical flooding*, not a forecast; we will not claim real-time prediction.
10. Vulnerability indicators at district level may be coarse or dated.

## Project limitations

11. 2-person team: scope must be contained.
12. SAC storyboard requires actual SAC access (post-registration).
13. Exact 2026 competition deadlines unverified (UNCERTAIN).
14. Myanmar national data access is limited; the project relies on global open datasets, and the analysis city may differ from the team's home country.

## What this means

- We will never display a number we cannot trace to a source.
- Any gap will be shown as "data unavailable," never as a fabricated zero.
- Every map will state its CRS, resolution, aggregation, and source.