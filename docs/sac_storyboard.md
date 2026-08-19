# SAC Storyboard Plan — FloodResilience ASEAN

Page-by-page design for the SAP Analytics Cloud storyboard (competition
deliverable). 15 pages max including cover, excluding references, per the
official 2026 storyboard requirement (landscape PDF, ≤20 MB, SAC-generated
charts).

Status: **design plan**. Charts are not yet created in SAC — this document
specifies what to build once the SAC account is available.

Build workflow follows the official **SAC Training Manual 2024**
(`D:/SAC/SAC Training Manual 2024.pdf`): Modeler → import CSV from `data/sac/`
→ fix measure/dimension classification → save model under
`Public > Myanmar > [Team folder]` → Stories > Responsive + **Classic Design
Experience** → insert tiles, input controls, styling. Detailed steps in
`docs/sac_import_guide.md`; chart specs in `docs/sac_visualizations.md`.

References to datasets are the real SAC-ready files in `data/sac/`. Every
number cited is from the actual processed data (see
`outputs/reports/key_insights.md`).

---

## Narrative spine

```
PROBLEM → EVIDENCE → PATTERN → INSIGHT → WHO IS AFFECTED → WHY IT MATTERS
→ SOLUTION → IMPLEMENTATION → IMPACT
```

---

## Page 1 — Cover

- **Objective**: identify the project at a glance.
- **Headline**: FloodResilience ASEAN — Data-Driven Urban Flood Risk
  Intelligence for Yangon.
- **Content (official cover requirements)**: Storyboard Title; Team Name;
  Institution; Country represented (Myanmar); SDG(s) to achieve (SDG 11, SDG
  13); brief description.
- **Charts**: none (cover page). Visual accent only.
- **Key takeaway**: a credible, data-driven approach to urban flood resilience.

## Page 2 — Problem

- **Objective**: why urban flooding is a serious ASEAN problem now.
- **Headline**: Urban floods threaten lives, services and economies across ASEAN.
- **Evidence**: regional flood-event counts from `sac_flood_events.csv`
  (Dartmouth Flood Observatory, 33 Myanmar events 1990-2023); Yangon's
  documented major flood years (1988, 1991, 1997, 2002, 2004, 2007, 2008,
  2010, 2013, 2014, 2015, 2017, 2019, 2020) as context flags.
- **Charts**: line/column of `n_flood_events_myanmar` by year (SAC).
- **KPI**: documented flood years in Yangon; national flood event count.
- **Source**: DFO archive; cited on References page.
- **Key takeaway**: recurrent, severe urban flooding justifies a systematic
  analytical response.

## Page 3 — ASEAN context

- **Objective**: situate the issue within ASEAN priorities.
- **Headline**: Aligned with the ASCC Blueprint and the ASEAN Digital
  Masterplan 2030.
- **Content**: SDG 11.5 / 11.b / 13.1; AADMER alignment; why cities are the
  right scale (population concentration, critical infrastructure).
- **Charts**: none required; clean context graphics allowed (not data charts —
  data charts must be SAC-generated).
- **Source**: aseandse.org theme; SDG targets.
- **Key takeaway**: this project is a concrete contribution to shared ASEAN
  resilience goals.

## Page 4 — Research question

- **Objective**: state the question the analysis answers.
- **Headline**: Which Yangon townships face the highest flood risk, who and
  what is exposed, and where should investments be prioritised?
- **Sub-questions**: where/when are rainfall extremes; historical flood
  frequency; population & infrastructure exposure; vulnerability; can an ML
  classifier be defended; which interventions follow.
- **Charts**: none (text page).
- **Key takeaway**: every later chart answers one of these questions.

## Page 5 — Data

- **Objective**: demonstrate credible, sourced, open data.
- **Headline**: All inputs are public, traceable data.
- **Evidence**: source families — CHIRPS rainfall (1981-present), Copernicus DEM
  30 m, 2014 Myanmar Census (population, age structure, urban/rural, official
  MIMU P-codes), HDX/OSM facilities, World Bank/GFDRR rainfall indices, DFO
  flood archive, official boundaries.
- **Charts**: optional simple count visuals (e.g., number of rainfall months =
  547, townships = 45) as SAC tables/numbers.
- **Source**: `data/source_catalog.csv`; full list on References page.
- **Key takeaway**: the analysis rests on verifiable data — no invented figures.

## Page 6 — Methodology

- **Objective**: explain the risk model transparently.
- **Headline**: Risk = 0.40 · Hazard + 0.35 · Exposure + 0.25 · Vulnerability.
- **Evidence**: component definitions; min-max normalization; quantile classes;
  sensitivity analysis (5 weight schemes).
- **Charts**: simple schematic/table (SAC text + number where appropriate).
- **Source**: `research/methodology.md`; `floodresilience/features/risk_index.py`.
- **Key takeaway**: the ranking is explainable and tested against weighting
  choices.

## Page 7 — Temporal findings

- **Objective**: show the seasonal and multi-year rainfall pattern.
- **Headline**: Rainfall is strongly seasonal — and flood years are wet years.
- **Evidence**: `sac_rainfall_timeseries.csv` (547 months, 1981-2026).
- **Charts**:
  - Line: monthly `rainfall_mm` over time (SAC).
  - Column by `month`: climatology showing the Jun-Sep monsoon peak.
  - Column by `year` with `documented_flood_year` highlight: documented flood
    years were wetter than the long-run mean.
- **Key takeaway**: seasonal hazard windows are identifiable in the data.
- **Note**: correlation is not causation — reported as association only.

## Page 8 — Spatial findings

- **Objective**: show where risk concentrates.
- **Headline**: Low-lying delta-fringe townships rank highest.
- **Evidence**: `sac_risk_by_area.csv`; elevation gradient from below sea level
  (min -9.2 m in Hlaingtharya) to higher ground inland (max mean 37.5 m in
  Taikkyi).
- **Charts**:
  - Geo choropleth by `risk_class` (map).
  - Scatter: `elev_mean_m` vs `risk_100`, colored by `district`.
- **Key takeaway**: hazard (elevation) visibly tracks risk ranking.

## Page 9 — Population & infrastructure exposure

- **Objective**: quantify who and what is at risk.
- **Headline**: ~2.6M people live in the highest-risk class; schools and health
  facilities are spread city-wide.
- **Evidence**: `sac_population_exposure.csv`, `sac_infrastructure_exposure.csv`;
  1,320 schools, 1,178 health facilities across 45 townships; top risk class
  population 2,599,370 (35.3% of the 2014 Census total).
- **Charts**:
  - Geo bubble map: `pop_est` by township (SAC geo).
  - Stacked column: `schools` + `health_facilities` by `district`.
- **Key takeaway**: exposure is concentrated where hazard is high → targeted
  investment is justified.

## Page 10 — Risk model output

- **Objective**: show the composite ranking and its decomposition.
- **Headline**: A transparent, weighted, sensitivity-tested risk index.
- **Evidence**: `sac_risk_by_area.csv`; top-ranked township Kayan (58.3 / 100)
  under default weights.
- **Charts**:
  - Bar: top-10 townships by `risk_100` (SAC).
  - Radar or 100% stacked column: `hazard` / `exposure` / `vulnerability` for
    top-10.
  - Table: full 45-row ranking with `pop_est`, `schools`, `health_facilities`.
- **Key takeaway**: ranking is explainable and stable under alternative weights.

## Page 11 — Key insights

- **Objective**: distil the story into defensible findings.
- **Headline**: Ten evidence-backed insights (seasonality, elevation gradient,
  exposure concentration, flood-year wetness, facility spread, recent rainfall
  intensity, national flood context).
- **Evidence**: `outputs/reports/key_insights.md`.
- **Charts**: supporting SAC charts from Pages 7-10 (reused) or summary KPIs;
  optional **Smart Discovery** "Key Influencers" tile (target `risk_score`,
  entity `township`) backing the driver insights — labeled as association, not
  causation.
- **Key takeaway**: each insight carries a metric, source, interpretation and
  limitation.

## Page 12 — The solution: FloodResilience ASEAN

- **Objective**: present the decision-support product.
- **Headline**: From insight to action — a civic decision-support tool.
- **Content**: risk explorer, interactive map, scenario explorer, resource
  prioritization; screenshot/links to the SvelteKit prototype (clearly labeled
  prototype).
- **Charts**: prototype screenshots (images ≤2 MB each) allowed; not data charts.
- **Key takeaway**: findings become a usable, explainable digital solution.

## Page 13 — Implementation

- **Objective**: show how it becomes real.
- **Headline**: A phased path: data foundation → pilot → validation → scale.
- **Evidence**: `docs/implementation_roadmap.md`; stakeholder model
  (`docs/stakeholders.md`).
- **Charts**: optional simple roadmap graphic (not a data chart).
- **Key takeaway**: viable with current technology and open data; costs not
  fabricated.

## Page 14 — ASEAN scalability

- **Objective**: show the framework generalises across ASEAN.
- **Headline**: One methodology, many cities.
- **Evidence**: `docs/asean_scalability.md`; common (global raster) vs local
  layers; replication procedure.
- **Charts**: optional schematic of common vs local layers.
- **Key takeaway**: Yangon is the validated pilot; the framework is the
  product.

## Page 15 — Conclusion

- **Objective**: close the story.
- **Headline**: Credible data → strong analysis → clear insight → practical
  solution → ASEAN scale.
- **Content**: recap research question, what was found, what we built, who it
  helps, and honest limitations.
- **Key takeaway**: a defensible, reproducible contribution to urban flood
  resilience.

## References page (after Page 15, excluded from the 15-page limit)

- Every dataset and external source with URLs (from `data/source_catalog.csv`
  and `research/sources.md`).
- Include: CHIRPS (Funk et al. 2015), Copernicus DEM, 2014 Myanmar Census
  (DoP / MIMU), HDX/OSM, World Bank/GFDRR, DFO, geoBoundaries/Alf-Anas,
  aseandse.org rules.

---

## Design rules

- One consistent color ramp for `risk_class` (1=green … 5=red) across all maps
  and charts.
- Every data chart is SAC-generated; images are ≤2 MB; PDF ≤20 MB; landscape.
- Every page answers a question and advances the narrative; no decorative KPIs.
- Do not claim any chart exists in SAC until it is actually built there.
