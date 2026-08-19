# Competition Self-Evaluation — FloodResilience ASEAN

Self-assessment against the official ASEAN DSE 2026 judging criteria
(https://aseandse.org/judging-criteria/). Scores are our **honest estimate**,
not a guarantee. Every claim below is traceable to files in this repository.

Score scale used: 0-10 per category, then weighted by the official category
weight to a hypothetical 0-100. Weakness lists are deliberately candid so the
team knows exactly where to invest before submission.

---

## 1. Problem Definition — weight 10% — est. 7.5/10

### Evidence
- **Context**: documented Yangon flood years (1988, 1991, 1997, 2002, 2004,
  2007, 2008, 2010, 2013, 2014, 2015, 2017, 2019, 2020) with published sources;
  33 DFO-recorded Myanmar flood events (1990-2023) — `data/sac/sac_yangon_flood_events.csv`,
  `data/sac/sac_flood_events_detail.csv`.
- **SDG alignment**: explicit targets — SDG 11.5 (reduce disaster losses),
  11.b (disaster-resilient cities), 13.1 (resilience to climate hazards),
  13.2/13.3 — in `research/competition_requirements.md`, `docs/sac_storyboard.md`
  (Page 3).
- **ASEAN priority alignment**: ASCC Blueprint 2025/2030 resilience & cities;
  ASEAN Digital Masterplan 2026-2030; AADMER (ASEAN Agreement on Disaster
  Management and Emergency Response) — `docs/asean_scalability.md`,
  `docs/sac_storyboard.md`.
- **Relevance**: city-scale analysis of Yangon Region (Myanmar) with national
  census (2014) and MIMU administrative codes.

### Strengths
- Issue is specific, current, and clearly bounded to a member state.
- SDG/ASEAN alignment is explicit and mapped to the official 2026 theme
  ("Navigating Our Future, Together").
- Real flood history is evidence, not assertion.

### Weaknesses
- Context could cite **quantified economic losses** for Yangon floods (we do not
  fabricate numbers; we currently lean on qualitative "recurrent disruption").
- The "why now" case (climate trend evidence) is associative, not causal.

### Improvement needed
- Add one or two fully-cited quantitative anchors to the Problem page (e.g.,
  published damage figures with explicit source) — only if a credible citation
  is found; otherwise keep qualitative framing and say so.

---

## 2. Analysis & Insights — weight 25% — est. 7.0/10

### Evidence
- **Data storytelling**: narrative spine PROBLEM→EVIDENCE→PATTERN→INSIGHT→WHO
  AFFECTED→WHY→SOLUTION→IMPLEMENTATION→IMPACT across a 15-page storyboard
  plan (`docs/sac_storyboard.md`).
- **Visualization plan**: every chart maps to a question; SAC-ready datasets in
  `data/sac/`; chart specs in `docs/sac_visualizations.md`.
- **Accuracy**: full source catalogue (`data/source_catalog.csv`), provenance
  log with SHA-256 (`data/raw/PROVENANCE.csv`), data dictionary
  (`data/data_dictionary.csv`), data-quality report
  (`outputs/reports/data_quality_report.md`), and key insights with metric /
  value / comparison / source / interpretation / limitation
  (`outputs/reports/key_insights.md`).
- **Real-data migration**: population/age structure now come from the **official
  2014 Myanmar Census** (7,360,703 total; township-level), not model estimates;
  flood events from DFO; official MIMU P-codes.

### Strengths
- Every headline number is traceable (e.g., 45 townships, 7.36 M population,
  1,320 schools, 1,178 health facilities, top township Kayan 58.3/100).
- Temporal (547 rainfall months) and spatial (45-township) analysis present.
- Insights engine is automated and self-limiting (`floodresilience/analysis/insights.py`).

### Weaknesses
- Storyboard charts are **specified, not yet built in SAC** — the highest-risk
  deliverable remaining.
- Sensitivity analysis exists (mean rank spread 4.04 across 5 weightings) but
  the storyboard must make this visible.
- Some relationships (rainfall↔flood) are reported as association only; judges
  may probe causality — defense must be crisp.

### Improvement needed
- Build the SAC storyboard exactly to `docs/sac_storyboard.md`.
- Add a small "data integrity" inset on the Data page (provenance + SHA-256).

---

## 3. Relevancy & Impact — weight 20% — est. 7.5/10

### Evidence
- **Significance**: 2,599,370 residents (35.3% of the census population) live in
  the highest-risk quintile; top risk class includes low-lying delta-fringe
  townships (Kayan 58.3, Thongwa 57.4, North Okkalapa 57.2).
- **Scalability**: common (global rasters, CHIRPS, Copernicus DEM, DFO) vs local
  (national census, MIMU) layer split documented in `docs/asean_scalability.md`.
- **Inclusivity**: age-disaggregated vulnerability (children <15, elderly 65+)
  from the census; township-level urban/rural split highlights peri-urban
  exposure.

### Strengths
- Impact is quantified in people and facilities, not vague claims.
- The framework, not the city, is positioned as the product.
- Vulnerable age groups are explicit.

### Weaknesses
- No income/poverty dimension (no credible township-level open data for Yangon —
  documented as a limitation).
- No gender-disaggregated analysis (not available in the census extract used).

### Improvement needed
- Explicitly call out underserved populations (informal settlements, small
  delta townships) in the storyboard even where data is qualitative.
- In the Q&A pack, be ready to state honestly that poverty data is a documented
  data gap, not an oversight.

---

## 4. Viability — weight 15% — est. 7.0/10

### Evidence
- **Implementability**: everything runs on open data + Python + SvelteKit + SAC
  — no exotic hardware or proprietary licenses beyond SAC (provided free).
- **Stakeholder analysis**: `docs/stakeholders.md` covers govt (city, DRM,
  meteorological agency), NGOs/humanitarian orgs, hospitals/schools,
  infrastructure operators, communities.
- **Strategy**: phased roadmap (data foundation → pilot → validation → scale)
  in `docs/implementation_roadmap.md`.

### Strengths
- Feasible with current technology; reproducible pipeline (`pip install -r
  requirements.txt` + `python -m floodresilience.*`).
- Cost assumptions are not fabricated.

### Weaknesses
- No pilot partner or MOU yet (student project).
- Sustained maintenance (data refresh, server hosting) has no owner identified.
- SAC account dependency for the official storyboard.

### Improvement needed
- Name realistic pilot entry points (e.g., YRTC/DRD Yangon, MIMU) as
  *proposed* partners, clearly labeled as proposals.
- Add a maintenance/hosting note (e.g., static hosting + scheduled pipeline)
  to the roadmap.

---

## 5. Innovation — weight 15% — est. 7.5/10

### Evidence
- **Originality**: explainable, sensitivity-tested township-level risk index
  combining CHIRPS + DEM + census + DFO with quantile classes; open and
  reproducible.
- **AI/digital integration**: a random-forest extreme-rainfall classifier
  (F1 0.667, ROC-AUC 0.949 vs majority baseline on strict temporal split) used
  to justify the hazard component — not a decorative chatbot
  (`outputs/reports/model_evaluation.md`).
- **Digital solution**: SvelteKit decision-support prototype with interactive
  map, risk explorer, scenario engine, methodology transparency
  (`src/routes/*`).
- **Scenario engine**: baseline-anchored normalization so sliders genuinely
  change outcomes (`src/lib/scenario.ts`).

### Strengths
- ML is used to answer a real question and is honestly bounded
  (descriptive, not forecasting).
- Prototype is functional and tested (10/10 unit tests).
- Scenario tool is transparent ("illustrative, not a forecast").

### Weaknesses
- The ML contribution is modest (class imbalance; single site).
- No novelty in algorithm choice — innovation is in the *integration and
  transparency*, which must be the pitch angle.
- Maps/charts in the app are not yet matched by equivalent SAC geo visuals.

### Improvement needed
- Frame innovation as "explainable integration + transparency," not "new ML".
- Add a small geoprocessing/automation novelty to pitch (e.g., automated
  reprocessing on new CHIRPS months).

---

## 6. Presentation Delivery — weight 15% — est. 6.5/10

### Evidence
- Structure and narrative are prepared (`docs/sac_storyboard.md`).
- Q&A pack is in `outputs/reports/judge_questions.md` (this deliverable).
- Cover page requirements mapped (title, team, institution, country, SDGs,
  description).

### Weaknesses
- No rehearsal record yet; no polished PDF deck beyond the storyboard plan.
- Prototype deployment URL not published yet.
- 15-page storyboard not yet built in SAC.

### Improvement needed
- Build SAC storyboard, export landscape PDF ≤20 MB, verify all charts legible.
- Deploy prototype to a public URL for the deck/defense.
- Run a mock judge session using `judge_questions.md`.

---

## Roll-up estimate

| Category | Weight | Est. score /10 | Weighted |
|---|---|---|---|
| Problem Definition | 10% | 7.5 | 0.75 |
| Analysis & Insights | 25% | 7.0 | 1.75 |
| Relevancy & Impact | 20% | 7.5 | 1.50 |
| Viability | 15% | 7.0 | 1.05 |
| Innovation | 15% | 7.5 | 1.13 |
| Presentation Delivery | 15% | 6.5 | 0.98 |
| **Total** | 100% | — | **7.16 / 10 (≈72)** |

**Top three priorities to raise the score:**
1. Build the SAC storyboard exactly to the plan (Analysis & Insights + Presentation).
2. Deploy the prototype to a public URL (Presentation + Viability).
3. Rehearse defense from `judge_questions.md` (Presentation).

*This scorecard is self-assessed for internal use and should be revisited after
the SAC storyboard is built.*