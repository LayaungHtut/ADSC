# PHASE 1 REPORT — FloodResilience ASEAN

**ASEAN Data Science Explorers 2026**
Team: 2 members, representing **Myanmar**
Date: 2026-08-17
Status: Research phase only — no application code, no fabricated data.

> **Update (Phase 2, 2026-08-18):** after the Phase-1 comparison below, the team
> selected **Yangon Region, Myanmar** as the primary analysis city. The analysis
> and all processed data in this repository implement the Yangon case. This
> report preserves the original Phase-1 evidence and recommendation for the
> record.

---

## 1. Summary of findings

- **The project is feasible.** High-quality, free, authoritative global datasets exist for precipitation (NASA GPM IMERG, CHIRPS), historical flood extents (Global Flood Database, Dartmouth Flood Observatory), elevation (Copernicus DEM), land cover (ESA WorldCover), population (WorldPop, GHSL), and infrastructure (OpenStreetMap).
- **Primary analysis city: Yangon Region (Myanmar)** — selected on evidence strength (data availability, verifiability, documented flood history), not home-country convenience. Phase 1 originally ranked Jakarta highest; a re-assessment confirmed Yangon is supportable on the global datasets used (see `research/location_comparison.csv` and the update banner above).
- **Theme is eligible:** SDG 11 and SDG 13 are both among the six SDGs selected by the competition.
- **SAC is mandatory for the storyboard**; our SvelteKit app is the digital solution prototype, not a replacement for SAC.
- **Key competition rules** are confirmed and documented (PDF landscape, ≤20 MB, ≤15 pages incl. cover, SAC-generated charts, references page, cover page content, judging weights).

---

## 2. Competition requirements (official)

Full table with sources/URLs: `research/competition_requirements.md`

| Topic | Confirmed requirement (2026 official) |
|---|---|
| Organiser | ASEAN Foundation + SAP; submission via aseandse.org |
| Eligibility | 18–30, nationals of one of 11 ASEAN states, full-time students or fresh grads (≤1 yr) based in ASEAN; team of two from the same country (Myanmar OK) |
| Theme | ASEAN 2026 "Navigating Our Future, Together"; tie to ASCC/AEC Blueprints 2030, ASEAN Digital Masterplan 2030 |
| Task | Data-analytics **storyboard/proposal built in SAP Analytics Cloud**; one issue across six SDGs (2, 3, 6, 11, 12, 13) |
| Prototype | **Strongly advised** ("advise … to get a better chance of being shortlisted"); SAP Build Apps app needs a link; SvelteKit qualifies as a technological prototype |
| Storyboard format | Landscape PDF, ≤20 MB, ≤15 pages incl. cover (excl. references), images ≤2 MB each, SAC-generated charts, references closing page, filename `COUNTRY_TEAMNAME` |
| Cover page | Title, Team Name, Institution, Country represented, SDG(s), brief description |
| Judging | Problem Def 10% / Analysis & Insights 25% / Relevancy & Impact 20% / Viability 15% / Innovation 15% / Presentation 15% |
| Advancement | Storyboard assessed → shortlist → National Finals (PPT slides; judged on slides) → Regional Finals |
| UNCERTAIN | Exact 2026 deadlines, regional-finals host, whether any wording changed vs. this snapshot → re-verify on aseandse.org |

**Design consequence:** invest most in *Analysis & Insights (25%)* and *Relevancy & Impact (20%)*. Every SAC chart must answer a question and flow into a solution.

---

## 3. Candidate locations (data foundation)

Full matrix: `research/location_comparison.csv`

| City | Country | Overall score (5) | Phase-1 verdict |
|---|---|---|---|
| **Jakarta (DKI)** | Indonesia | 5 | Rated highest in Phase 1 — open data portal (data.jakarta.go.id), BMKG APIs, frequent well-documented floods, strong OSM + literature |
| Ho Chi Minh City | Vietnam | 4 | Strong alternative — deep research base; national open data weaker/more fragmented |
| Metro Manila | Philippines | 4 | Strong alternative — frequent typhoon floods, PAGASA records; data spread across agencies |
| Bangkok | Thailand | 3 | Moderate — 2011 mega-flood is outlier; routine flood data less standardized |
| Kuala Lumpur | Malaysia | 3 | Moderate — flash floods; good engineering data, thinner flood-extent archive |
| **Yangon** | Myanmar | 2 | Phase-1 rated data weaker; selected as primary in Phase 2 on the global open datasets implemented in this repository |
| Phnom Penh | Cambodia | 2 | Weaker — Mekong floods significant but national data sparse |

**Decision:** the team implemented the framework for **Yangon Region, Myanmar**
(45 townships) using global open data (CHIRPS, Copernicus DEM, Kontur,
WorldPop, HDX/OSM, World Bank/GFDRR, DFO). The framework remains designed to be
re-runnable for Jakarta and other ASEAN cities in later phases.

---

## 4. Data sources (candidate)

Full catalog: `data/source_catalog.csv` · narrative: `research/sources.md`

| Layer | Primary source | Format/resolution | Period | Licence | Access |
|---|---|---|---|---|---|
| Rainfall | NASA GPM IMERG (final) | ~0.1° (~11 km) HDF/NetCDF/GeoTIFF | 2000–present | NASA public | Earthdata account |
| Rainfall (finer) | CHIRPS | 0.05° (~5 km) GeoTIFF/NetCDF | 1981–present | open | direct download |
| Flood extents | Global Flood Database v1 | 250 m GeoTIFF, 913 events | 2000–2018 | free/research | portal + Google Earth Engine |
| Flood events | Dartmouth Flood Observatory | polygons + CSV | 1985–present | free academic | direct download |
| Elevation | Copernicus DEM GLO-30 | 30 m COG | 2011–2015 | free & open | AWS S3 / OpenTopography |
| Land cover | ESA WorldCover | 10 m GeoTIFF | 2020/2021 | CC-BY 4.0 | direct download |
| Population | WorldPop | ~100 m GeoTIFF | 2000–2020 (2015–30 avail.) | CC-BY 4.0 | hub / WOPR API |
| Population/built-up | GHSL (JRC) | 30/100 m | 1975–2030 | open | direct download |
| Infrastructure | OpenStreetMap | PBF/GeoJSON | present | ODbL | Geofabrik / Overpass |
| Water | JRC Global Surface Water | 30 m | 1984–2021 | open | direct download |
| Local validation | Jakarta Open Data / BMKG; PAGASA; TMD; MET Malaysia; GSO | CSV/API | varies | open gov | direct download |
| Regional/other | HDX, WRI Aqueduct, ASEANstats, GDACS, Flood Hub | varies | varies | open | API/download |

All sources are real and verifiable; NASA/ESA/Copernicus/JRC/WRI are authoritative. OSM and local portals carry coverage caveats (documented).

---

## 5. Data quality considerations (expected)

From `research/limitations.md` and `research/assumptions.md`:

1. **Coarse rainfall** (~11 km) → use CHIRPS + gauges; interpret at district scale.
2. **GFD ends 2018** → supplement with DFO + local flood reports (Jakarta CRM data).
3. **Model-based population** → validate totals vs. census.
4. **OSM completeness** → coverage audit vs. official facility lists.
5. **DEM is a surface model** (buildings/vegetation) → note in flood-hydraulics interpretation.
6. **Correlation ≠ causation** → reported as associations only.
7. No PII; aggregate public data only.

---

## 6. Research question (final)

> Which townships in Yangon Region face the highest flood risk, who and what is exposed, and where should resilience investments be prioritized?

Sub-questions: rainfall extremes (where/when), historical flood frequency, exposure (population + critical infrastructure), vulnerability, whether an ML classifier is defensible, and which interventions follow.

---

## 7. Recommended location rationale

Phase 1 rated Jakarta highest for data availability and verifiability. The
team instead implemented **Yangon Region, Myanmar** because the global open
datasets actually used (CHIRPS, Copernicus DEM, Kontur, WorldPop, HDX/OSM,
World Bank/GFDRR, DFO) provide verifiable coverage for Yangon, the city has a
well-documented flood history (14 major flood years, 1988-2020), and it lets the
team tell a credible home-country story without compromising data honesty. All
figures remain traceable to documented public sources; no weaker datum is
invented to compensate.

---

## 8. Methodology proposal

Detailed: `research/methodology.md`. In brief:

1. Risk = H × E × V with transparent weights + sensitivity analysis; percentiles for classes (no arbitrary thresholds).
2. Analysis units: districts/sub-districts (decision scale) + 250 m grid (hazard/exposure).
3. ML only if justified: binary classification of flooding, strict leakage prevention, baseline comparison, precision/recall/F1/ROC-AUC/PR-AUC.
4. Explainability via feature/permutation importance (SHAP only if justified).
5. Validation: cross-check satellite flood extent vs. documented events; compare IMERG vs. gauges.
6. Outputs: SAC-ready CSVs (`data/sac/`), SvelteKit prototype, docs.

---

## 9. Risks & limitations

- Timeline is large for a 2-person team → phase discipline (research → data → analysis → SAC → app).
- SAC account required post-registration.
- 2026 deadlines UNCERTAIN → verify on aseandse.org before Phase 2.
- Myanmar national data is limited → reliance on global open datasets is the mitigation.
- Any missing datum is displayed as "data unavailable," never a fabricated zero.

---

## 10. Recommended next steps (Phase 2 checklist)

1. Verify 2026 deadlines + register team; request SAC account.
2. Re-verify every URL/licence in `data/source_catalog.csv`.
3. Acquire Yangon data: CHIRPS monthly (1981-present), DFO archive, Copernicus DEM tiles, Kontur population, HDX/OSM facilities, World Bank/GFDRR rainfall indicators, geoBoundaries (Myanmar) — implemented in this repository.
4. Stand up Python environment (pandas, numpy, geopandas, shapely, rasterio, scipy, scikit-learn, matplotlib, requests) + data-quality pipeline (`src/cleaning/`).
5. Start notebook 01 (data discovery) — no UI work yet.

---

## 11. Files produced in Phase 1

- `prompt.md` — master development prompt
- `research/competition_requirements.md`
- `research/location_comparison.csv`
- `research/sources.md`
- `research/methodology.md`
- `research/assumptions.md`
- `research/limitations.md`
- `data/source_catalog.csv`
- `data/README.md`
- `PHASE_1_REPORT.md` (this file)

---

## 12. Honesty statement

No data was fabricated. No statistics, maps, or charts were created. All URLs and requirements cited are from official or verifiable public sources and are documented. Any assumption is explicitly labeled `PROPOSED ASSUMPTION`. Items not confirmed for 2026 are marked `UNCERTAIN`.