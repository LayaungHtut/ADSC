# FloodResilience ASEAN — Competition Storyboard 2026 (Build Pack)

> Page-by-page content and layout spec for the ASEAN DSE 2026 SAC storyboard.
> Follows the design patterns of past winners in `D:/SAC/` (MYANMAR-TEAM-NEXUS
> Problem→Solution→Impact arc; VIETNAM-TEAM-KpoW emotional framing + honesty),
> constrained to the **2026 rules**: landscape PDF, ≤ 20 MB, ≤ 15 pages incl. cover
> and excl. References, cover with the 6 required fields, SAC-generated charts,
> images ≤ 2 MB each, filename `MYANMAR_TEAM_[TEAMNAME].pdf`.
>
> **Honesty rule (non-negotiable):** every figure below is verified in
> `outputs/tables/` and `outputs/reports/`. Nothing is fabricated. SAC charts are
> marked **[BUILD IN SAC]** — do NOT render a page claiming a SAC chart exists
> until it is actually built and exported. Prototype web-app screenshots are
> labelled "prototype".

---

## File delivery

- Filename: `MYANMAR_TEAM_ZENITH.pdf`.
- Orientation: **Landscape**, PDF, ≤ 20 MB total, each embedded image ≤ 2 MB.
- Page count: **15 pages content + References page(s)** (references excluded from limit).
- Charts: generated in **SAC Story (Classic Design Experience)** using datasets from
  `data/sac/*.csv` (see `docs/sac_import_guide.md`, `docs/sac_visualizations.md`).
- Structure shorthand: P = Problem, A = Analysis, S = Solution, I = Implementation, M = Impact.
  The winners interleave these with a horizontal tab bar (`Problem | Solution | Implementation | Impact`)
  on every page for a strong narrative thread.

---

## PAGE 1 — Cover (6 required fields)

**Layout:** Full-bleed hero (dark flood-blue), big title top-left, 6-field box bottom-third,
team member names + roles under the title.

- **(1) Storyboard Title:** "FloodResilience ASEAN — Data-Driven Urban Flood Risk Intelligence for Yangon"
- **(2) Team Name:** Zenith
- **(3) Institution:** University of Information Technology (UIT)
- **(4) Country Represented:** Myanmar
- **(5) SDG(s):** SDG 11 (11.5, 11.b) · SDG 13 (13.1, 13.3)
- **(6) Brief description:** "Using 45 years of satellite rainfall, census and critical-infrastructure
  data in SAP Analytics Cloud, we map flood risk for all 45 Yangon townships — identifying the
  9 highest-risk townships where 2.6 million people live — and deliver a decision-support tool
  for cities across ASEAN."
- **Team strip (NEXUS-style "About Us"):** Thar Lun Myint Myat Tun — Team Leader ·
  La Yaung Htut — Member. Both, University of Information Technology.

**KPI teaser row (small, cited):** 45 townships · 7.4 M people mapped · 2.6 M in highest risk class
· 15-year flood history documented. Source footnote: 2014 Census; CHIRPS 1981–2026; DFO.
*(Mirrors NEXUS cover: title + SDG + institution + team + emails, then "About Us" strip.)*

---

## PAGE 2 — The Problem (P)

**Headline (emotive, KpoW-style):** "When the monsoon arrives, who in Yangon is at risk?"
**Sub-head:** "Floods are a documented, recurring reality — not a hypothetical."

**Copy (4 bullet claims, each with source):**
- 14 documented major flood years in Yangon Region since 1988
  (1988, 1991, 1997, 2002, 2004, 2007, 2008, 2010, 2013, 2014, 2015, 2017, 2019, 2020)
  — PIAHS 2024; Sritarapipat 2017; OCHA 2017; UNOSAT 2020.
- Myanmar records 33 DFO-documented flood events (1990–2023) — one of ASEAN's most flood-affected countries.
- Monsoon rains are extreme and seasonal: peak month July = 698.9 mm mean (CHIRPS 1981–2026).
- Cities concentrate exposure: Yangon Region is home to ~7.4 M people across 45 townships
  (2014 Census, via MIMU).

**Chart [BUILD IN SAC]:** "Documented Yangon flood years, 1988–2020" — **scatter/bullet timeline**
using `sac_yangon_flood_events.csv`; dot per year with severity label. Add **Input Control** = region.
**KPI row:** 14 flood years · 33 national events · 698.9 mm July peak.
**Takeaway:** "Flooding in Yangon is frequent, recent and measurable — the only question is where it will hurt most."

---

## PAGE 3 — Why It Matters: SDG & ASEAN Alignment (P/M)

**Headline:** "Not a local data exercise — an ASEAN priority."
**Copy:** Explains mandate: SDG 11.5 (flood loss reduction), 11.b (resilient cities & DRR),
13.1 (resilience to climate hazards), 13.3 (capacity-building).

**Alignment table (mirror NEXUS/KpoW ASCC tables):**

| SDG / ASEAN framework | Target / element | How this project supports it |
|---|---|---|
| SDG 11.5 | Reduce deaths/people affected by disasters | Township-level risk ranking enables pre-season targeting |
| SDG 11.b | Adopt DRR strategies, build resilient cities | Risk model + open web tool = replicable DRR method |
| SDG 13.1 | Resilience to climate-related hazards | Rainfall (1981–2026) drives the hazard layer |
| SDG 13.3 | Build climate capacity | Method & data fully documented; anyone can replicate |
| ASCC Blueprint 2025 B.2 | Equitable access for all | Free, open web tool; no paywall for townships |
| ASCC Blueprint 2025 D.4 | Protect vulnerable groups in climate crises | Exposure layer flags elderly/children (census age structure) |
| AADMER (2013) | ASEAN disaster management & emergency response | Outputs align to national/regional disaster data formats |

**Takeaway:** "The 15-page story answers 25% of the 'Analysis & Insights' criterion, but the alignment
page answers 'Relevancy & Impact'." Source footnote for ASCC/AADMER on the page.

---

## PAGE 4 — Our Question & Approach (A)

**Headline:** "One question, one region, one framework."
**Research question (framed like NEXUS 'Problem' tab):**
> *"Which Yangon townships face the highest flood risk — and which populations, schools and
> health facilities are exposed there?"*

**Approach strip (4 steps):** DATA → HAZARD · EXPOSURE · VULNERABILITY → RISK RANKING →
DECISION SUPPORT. State the full pipeline ran offline (Python) then imported into SAC for exploration.

**Map [BUILD IN SAC]:** Region overview (geoBoundaries + MIMU P-codes MMR013001–045, 45 townships).
**Honesty box (KpoW-style, always visible):**
- "We compute relative, township-level risk — not a flood forecast."
- "All data is open and cited; any township row is traceable to its source."
**Takeaway:** "Clarity of scope = credibility."

---

## PAGE 5 — The Data (A)

**Headline:** "Open data, openly cited. 547 months of rainfall. 7.4 M people."
**Sources table (compact, cited, NEXUS-style 'Dataset: X, URL: y' on every row):**

| Layer | Dataset | Key figure |
|---|---|---|
| Rainfall | CHIRPS v2.0 (UCSB) | 547 monthly obs, 1981-01..2026-07 |
| Hazard inputs | World Bank/GFDRR subnational rainfall indices | 2022+; district level |
| Elevation | Copernicus DEM 30 m | mean −9.2 m (Hlaingtharya) .. 37.5 m (Taikkyi) |
| Flood events | DFO Flood Archive + PIAHS/UNOSAT/OCHA | 14 Yangon years; 33 Myanmar events |
| Population | 2014 Myanmar Census (via MIMU/ODM) | 7,360,703 total; urban/rural; age 0-14 & 65+ |
| Facilities | OSM / HDX education & health polygons | 1,320 schools; 1,178 health facilities |
| Boundaries | geoBoundaries + MIMU | 45 townships, P-codes matched |

**KPI row:** 547 rainfall months · 45 townships · 1,320 schools · 1,178 health facilities.
**Takeaway:** "Every number on every slide traces to an open, cited source — that is our defense for
'Analysis & Insights' and 'Viability'."

---

## PAGE 6 — Method: Transparent, Not a Black Box (A)

**Headline:** "Risk = 0.4·Hazard + 0.35·Exposure + 0.25·Vulnerability — weighted by the data."
**Copy:**
- Weights chosen from the literature (WB/GFDRR risk practice), applied to township-level
  normalized indicators; components are fully documented.
- Quantile classing → 5 risk classes (1 = lowest .. 5 = highest).
- **Robustness:** ±10% sensitivity re-simulation changes townships' class by only
  **4.04 ranks on average** → ranking is stable, not noise.
- **Hazard justification:** an extreme-rainfall month classifier (Random Forest) achieves
  **F1 = 0.667, ROC-AUC = 0.949** — rainfall signals are genuinely predictive of wet-season extremes.

**Chart [BUILD IN SAC]:** "Risk formula" as a **donut/waterfall**: 0.40 Hazard · 0.35 Exposure ·
0.25 Vulnerability (calculated measure, `sac_risk_by_area.csv`).
**Honesty box:** "Weights are transparent and tunable; the sensitivity page lives in the appendix (risk_sensitivity.csv)."
**Takeaway:** "A model the judges can interrogate beats a black box."

---

## PAGE 7 — What the Data Says: Seasonality (A)

**Headline:** "The monsoon is not 'a season' — it is a peak that must be planned for."
**Copy:**
- Peak month **July = 698.9 mm** mean monthly rainfall (CHIRPS 1981–2026); wettest months Jul, Aug, Jun, Sep.
- Documented flood years averaged **2,903 mm/yr vs 2,844 mm/yr long-run mean** — flood years are measurably wetter.
- Long-run OLS trend (+15 mm/yr, 1981–2025) is small; **interannual variability dominates** → don't overclaim climate trend.

**Chart [BUILD IN SAC]:** **Monthly rainfall climatology (bar + line)**, 12 months, with a
calculated measure for wet-season share. Add **Rank Top-N = 6** for wettest months. Optionally
**forecast labeling** on the annual series (clearly labelled "Auto-Forecast" — not claimed as fact).
**KPI row:** 698.9 mm Jul peak · +59 mm flood-year anomaly · 4 wettest months = Jun–Sep.
**Takeaway:** "Seasonality tells us *when*; the risk model tells us *where*."

---

## PAGE 8 — Where It Concentrates: The Risk Map (A/M)

**Headline:** "Five townships you should know before the next monsoon."
**Copy:**
- Highest risk (class 5): **Kayan 58.3 · Thongwa 57.4 · North Okkalapa 57.2 · Thanlyin 53.2 ·
  Hlaingtharya 52.5** (risk index 0–100).
- Low elevation aligns with high risk: the lowest-lying townships sit along the Yangon, Bago and
  Hlaing rivers and the delta fringe (elev_mean −9.2 m .. 37.5 m).

**Charts [BUILD IN SAC]:**
1. **Choropleth risk map** (`sac_risk_by_area.csv`, `risk_100` on geoBoundaries townships) — the hero visual.
2. **Scatter:** elevation vs risk_100 (axis: elevation, color: risk class) to show the lowland-hazard alignment.
3. **Input Controls:** district + risk class (top bar) so presenters can drill Yangon East/North/South/West live.
**Takeaway:** "Geography is the story: the delta fringe is where risk concentrates."

---

## PAGE 9 — Who and What Is Exposed (A/M)

**Headline:** "Risk is not abstract — it is 2.6 M people, 1,320 schools, 1,178 clinics."
**Copy (exposure facts, all verified):**
- **2,599,370 people (35.3% of the region)** live in the highest-risk townships (class 5).
- District population weights: East 2,366,659 · North 2,606,670 · South 1,417,724 · West 969,650
  (total 7,360,703 — urban + rural = total everywhere).
- Schools and health facilities exist in **every** township → no flood event is free of public-service impact.
- Age vulnerability: children (0–14) and elderly (65+) from the 2014 Census age structure enter the
  vulnerability sub-index.

**Charts [BUILD IN SAC]:**
1. **Bar:** population at risk by risk class (5 bars) — highlight class 5 (2.6 M).
2. **Bubble map:** schools & health facilities sized/colored by township risk class.
**KPI row:** 2.60 M at class-5 risk · 35.3% of population · 2,498 facilities mapped.
**Takeaway:** "We count people and services, not just polygons."

---

## PAGE 10 — The Risk Model Output (A/M)

**Headline:** "From 45 townships to one prioritized list."
**Copy:** "Ranking every township on the same scale turns raw data into a decision: **which townships
get early-warning, evacuation drills, and drainage investment first.**"
**Chart [BUILD IN SAC]:**
1. **Top-10 horizontal bar** (`risk_100`, Rank Top-N = 10) with class-5 highlights.
2. **Decomposition** (stacked bar): Hazard / Exposure / Vulnerability per top township — shows
   *why* each ranks high (Kayan & Thongwa = hazard+vulnerability; North Okkalapa = exposure+exposure).
3. Optional **Smart Discovery** (target: `risk_100`, entity: `township`) to surface key influencers — run,
   capture, and caption as "SAC Smart Discovery".

**KPI row:** 58.3 top score (Kayan) · 4.04 avg rank shift under sensitivity · 9 townships in class 5.
**Takeaway:** "A prioritized, explainable list — that is what decision-makers asked for."

---

## PAGE 11 — Key Insights (A)

**Headline:** "Four evidence-backed answers to 'so what?'"
**Insight cards (each = claim + source + limitation — KpoW/NEXUS rigor):**
1. **Flood years are wet years.** Documented flood years averaged 2,903 vs 2,844 mm/yr.
   *Limitation:* correlation ≠ causation; rivers/tides/drainage also matter.
2. **Risk follows elevation and the rivers.** Lowest-lying townships dominate class 5.
   *Limitation:* DEM is a surface model; no flood depth.
3. **Exposure is concentrated, services are everywhere.** 35.3% of people in class 5; schools/clinics in all 45.
   *Limitation:* OSM facility lists may undercount private/informal facilities.
4. **The ranking is robust.** Sensitivity shifts rank by only 4.04 on average.
   *Limitation:* ±10% band tested; wider bands remain future work.

**Chart [BUILD IN SAC]:** Smart Discovery key-influencer panel (captured) or the risk-distribution histogram.
**Takeaway:** "Insights are evidence-backed, limitation-aware — exactly what judges score for 'Analysis & Insights'."

---

## PAGE 12 — The Solution (S)

**Headline:** "From analysis to action: FloodResilience ASEAN."
**Copy (honest framing — prototype, not production):**
- A **decision-support platform** (open web prototype, SvelteKit) that turns the SAC risk model into
  township-level answers anyone can use.
- **Modules:** live risk explorer (45 townships) · scenario engine (raise/lower rainfall, exposure,
  vulnerability → see rank change live) · critical-facility locator · data dictionary with citations.

**Prototype screenshots (label clearly):** risk map page, township detail page, scenario slider —
each ≤ 2 MB, captioned "FloodResilience ASEAN prototype (open web build), data = SAC output."

**Chart [BUILD IN SAC]:** A "solution dashboard" page in SAC with the same KPIs (top risk, class-5 pop,
facility count) as a **KPI tile strip + map** — this demonstrates the SAC-native deliverable.
**Takeaway:** "The model only matters if it changes a decision — the tool makes the decision visible."

---

## PAGE 13 — Implementation & Stakeholders (I)

**Headline:** "Who does what, and when."
**Roadmap (phases, NEXUS/KpoW style):**

| Phase | Window | Milestones |
|---|---|---|
| Phase 1 — Pilot | 0–6 months | Validate with Yangon Region DRR office; 5 townships get risk briefs |
| Phase 2 — Scale | 6–18 months | Web tool public; schools/clinics onboarding; monsoon early-warning link |
| Phase 3 — ASEAN | 18–36 months | Replicate pipeline for 2nd city; AADMER/ASCC reporting alignment |

**Stakeholder map (compact table):** Region DRR office (validates) · Township administrators (decide) ·
MIMU / HDX (data custodians) · schools & clinics (services at risk) · researchers (open method) ·
SAP Analytics Cloud (analytics platform).
**Honesty note:** cost/revenue claims are **not fabricated**; pilot costs depend on host-government
arrangement (mirrors NEXUS's "as available data" caveat).
**Takeaway:** "A plan the user can actually run — no invented budgets."

---

## PAGE 14 — ASEAN Scalability (I/M)

**Headline:** "Built for Yangon. Designed for ASEAN."
**Copy:**
- **Common (reusable) layers:** CHIRPS/GPM rainfall, Copernicus DEM, census, OSM facilities, DFO —
  all exist for every ASEAN country.
- **Local (swap-in) layers:** admin boundaries + P-codes, national census, flood-event catalogues.
- **Replication path (3 steps):** fetch open layers for target city → run the documented pipeline →
  import to SAC and publish the same web tool. Low marginal cost = high viability.

**Chart [BUILD IN SAC]:** "Data availability across ASEAN" **bar** (count of the 5 core layers available
per country) or a **geographic mini-map** of pilot candidate cities.
**Takeaway:** "The 25% 'Viability' criterion: open data + documented method + cloud analytics = repeatable anywhere."

---

## PAGE 15 — Conclusion (M)

**Headline:** "The next monsoon is coming. We now know where it will hurt — and what to do about it."
**Recap strip:** 45 townships ranked · 9 highest-risk identified · 2.6 M people and 2,498 facilities at
risk · robust, transparent, reproducible method.
**Call to action:** "Prioritize early-warning and infrastructure for Kayan, Thongwa, North Okkalapa,
Thanlyin and Hlaingtharya first; replicate the pipeline across ASEAN."
**Thank-you:** "Team Zenith · University of Information Technology · Myanmar — data, method and tool
are open and cited."
*(Mirrors NEXUS closing: mission sentence + thank you.)*

---

## References (closing page — EXCLUDED from 15-page limit)

Full citations (APA), one block per source family (NEXUS groups them: Datasets / Reports / Policy):
1. UCSB Climate Hazards Center. (1981–2026). *CHIRPS v2.0 precipitation.* https://www.chc.ucsb.edu/data/chirps
2. Dartmouth Flood Observatory. *Global Flood Archive.* https://floodobservatory.colorado.edu/
3. Department of Population, Myanmar. (2014). *Myanmar Population and Housing Census (township level).*
   Via MIMU / Open Development Mekong. https://data.opendevelopmentmekong.net/
4. MIMU. *Administrative boundaries & township P-codes (MMR013001–045).* https://themimu.info/
5. geoBoundaries (William & Mary geoLab). *Myanmar ADM boundaries.* https://www.geoboundaries.org/
6. Copernicus Programme / ESA. *Copernicus DEM GLO-30.* https://registry.opendata.aws/copernicus-dem/
7. OpenStreetMap & HDX. *Education & health facility polygons (Myanmar).* https://www.openstreetmap.org/ · https://data.humdata.org/
8. World Bank / GFDRR. *Subnational rainfall indicators (ADM2).* https://www.gfdrr.org/
9. PIAHS. (2024). *Yangon flood events.*; Sritarapipat et al. (2017); OCHA (2017); UNOSAT (2020).
10. ASEAN Secretariat. (2015). *ASEAN Socio-Cultural Community Blueprint 2025.*; (2013). *AADMER.*

Add the tool footnote: "Built with SAP Analytics Cloud (Classic Design Experience); open Python pipeline
(FloodResilience ASEAN) documented in this repository."

---

## Build checklist (do before export)

1. [ ] In SAC: import `data/sac/*.csv`, fix measure/dimension classification, save under
   `Public > Myanmar > [Team folder]` (Classic Design Experience).
2. [ ] Build charts per page spec above; run Smart Discovery; capture screenshots ≤ 2 MB each.
3. [ ] Assemble 15 pages + references in landscape; keep total ≤ 20 MB.
4. [ ] Cover: verify all 6 required fields are present verbatim.
5. [ ] Export as `MYANMAR_TEAM_ZENITH.pdf`.
6. [ ] Self-score vs `outputs/reports/competition_scorecard.md`; prep answers from
   `outputs/reports/judge_questions.md`.
7. [ ] Mark every chart as SAC-generated; label prototype screenshots as "prototype".