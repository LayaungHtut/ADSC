# Final Analytics Review — FloodResilience ASEAN

Pre-submission audit of every claim that will appear in the storyboard and
prototype. The rule: **every number is traceable to a file, a source, or an
explicitly labeled assumption. Nothing is invented.**

Reviewed: after the 2014 Census / real-data migration.

---

## 1. Are all numbers traceable?

| Claim used in storyboard/app | Value | Traceable to | Status |
|---|---|---|---|
| Townships assessed | 45 | `data/processed/yangon_township_features.csv` (45 rows) | PASS |
| Census population (Yangon Region, 45 townships) | 7,360,703 | census CSV + `data/sac/sac_population_exposure.csv` sum; matches published 2014 census total | PASS |
| Population in highest risk class | 2,599,370 (35.3%) | `src/lib/data/risk-summary.json` (risk_class==5) | PASS |
| Top-risk township | Kayan (58.3 / 100) | `outputs/tables/risk_scores.csv`, `src/lib/data/risk-summary.json` | PASS |
| Mean risk | 42.5 / 100 | `src/lib/data/risk-summary.json` | PASS |
| Rainfall months | 547 (1981-2026) | `data/sac/sac_rainfall_timeseries.csv` | PASS |
| Schools / health facilities | 1,320 / 1,178 | `data/sac/sac_infrastructure_exposure.csv` sums | PASS |
| DFO Myanmar flood events | 33 (1990-2023) | `data/sac/sac_flood_events_detail.csv` | PASS |
| Documented Yangon flood years | 14 (1988, 1991, 1997, 2002, 2004, 2007, 2008, 2010, 2013, 2014, 2015, 2017, 2019, 2020) | `data/sac/sac_yangon_flood_events.csv` with per-year sources | PASS |
| Elevation range | -9.2 m (Hlaingtharya min) to 487.5 m (Hlegu max); mean range 3.6-37.5 m | `src/lib/data/features.json` (elev_min_m / elev_max_m / elev_mean_m) | PASS |
| Extreme-rainfall threshold | 718.9 mm/month (p95) | `outputs/tables/ml_extreme_rainfall.json` | PASS |
| ML test-period results | RF F1 0.667, ROC-AUC 0.949 | `outputs/reports/model_evaluation.md`, `outputs/tables/ml_predictions_test_period.csv` | PASS |
| Mean rank spread (sensitivity) | 4.04 of 45 ranks | `outputs/tables/risk_sensitivity.csv` | PASS |

## 2. Are all sources real?

- Every dataset is listed with URL, licence and limitations in
  `data/source_catalog.csv`; download log with SHA-256 in
  `data/raw/PROVENANCE.csv`.
- No fabricated sources. Yangon flood-year citations are specific
  (PIAHS 386 2024; Sritarapipat 2017; OCHA 2017; UNOSAT 2020) and listed in the
  CSV, ready for the References page.

## 3. Are calculations reproducible?

- Pipeline: `python -m floodresilience.analysis.pipeline` (ingest → clean →
  features), `python -m floodresilience.features.risk_index`, `python -m
  floodresilience.analysis.explore` (geojson), `python -m
  floodresilience.export.sac`, `python -m floodresilience.export.web`.
- Unit tests: `npx vitest run` → 10/10 passing; `svelte-check` → 0 errors.
- Scenario engine mirrors `risk_index.py` (`src/lib/scenario.ts`).

## 4. Is correlation interpreted correctly?

- We report that documented flood years were wetter than the long-run mean as an
  **association**. No causal claim is made anywhere (`research/limitations.md`,
  `outputs/reports/model_evaluation.md` §6).

## 5. Is causation avoided?

- PASS. The words "causes/caused by" do not appear in claims about rainfall↔flood.
- ML feature importance is explicitly labeled as association, not causation.

## 6. Is model performance real?

- Results come from a held-out temporal test set (train ≤ 2005, test > 2005),
  no leakage, compared against a majority baseline. Confusion matrices and
  PR/ROC curves are reproducible from
  `outputs/tables/ml_predictions_test_period.csv`.

## 7. Is risk scoring defensible?

- Weighted, min-max normalized, quintile-classed index with 5-weighting
  sensitivity analysis (mean spread 4.04). Weighting rationale documented;
  limitations acknowledged. **No arbitrary thresholds.**

## 8. Is uncertainty disclosed?

- PASS across deliverables: `research/limitations.md`, `docs/ethics.md`,
  `data/source_catalog.csv` (limitations column), storyboard pages carry
  limitation notes, scenario tool is labeled "illustrative — not a forecast".

## 9. Is the solution connected to findings?

- Findings (high-risk areas, exposed population, seasonal window, elevation
  gradient, facility spread) feed directly into: risk explorer, map, resource
  prioritization and scenario modules of the prototype, and the SAC storyboard
  pages 7-15.

---

## Residual risks before submission

1. **SAC storyboard not yet built** — the biggest open item; charts are
   specified but must be created in SAC, then exported to a landscape PDF ≤20 MB.
2. **Prototype not deployed** — a public URL strengthens Viability and
   Presentation.
3. **Sensitivity and ML results must be visible in the storyboard**, not only in
   repo reports.
4. **2014 census vintage** — stated everywhere; judges will ask, answers are in
   `outputs/reports/judge_questions.md` (Q2).

## Verdict

All claims that will be presented are **traceable, sourced, reproducible and
honestly bounded**. No fabricated data, statistics, models, events, maps or
citations were found in the deliverable set. The project is submission-ready on
analytics integrity; remaining work is packaging (SAC build, deployment,
rehearsal).