# Judge Q&A Preparation — FloodResilience ASEAN

Difficult questions a judging panel could ask, with concise evidence-based
answers. Every answer is traceable to files in this repository. Where the honest
answer is "we don't know / we can't claim that", that is stated directly.

Category tags: [DATA] [METHOD] [STATS] [ML] [GIS] [SDG] [ASEAN] [IMPACT]
[FEAS] [ETHICS] [INNOV] [APP] [SAC] [LIMITS]

---

## Data [DATA]

**Q1. Are your population figures real?**
Yes. Population, urban/rural split and age structure come from the official 2014
Myanmar Population and Housing Census township tables (Department of Population,
accessed via MIMU / Open Development Myanmar). Total across the 45 Yangon
townships is 7,360,703, matching the published census total. Provenance (URL +
SHA-256) is in `data/raw/PROVENANCE.csv`.

**Q2. Why 2014 and not a newer year?**
The 2014 census is the most recent official national census for Myanmar; there is
no newer authoritative township-level population source. We state this as a
documented limitation (`research/limitations.md`).

**Q3. Where did your flood events come from?**
The Dartmouth Flood Observatory (DFO) archive — 33 Myanmar events (1990-2023),
with start/end dates, cause, severity, fatalities, displaced and area
(`data/sac/sac_flood_events_detail.csv`). Documented Yangon flood years (14
major years 1988-2020) additionally cite peer-reviewed literature (PIAHS 386
2024; Sritarapipat 2017), OCHA 2017, and UNOSAT Sentinel-1 mapping
(`data/sac/sac_yangon_flood_events.csv`).

**Q4. Which rainfall dataset and why?**
CHIRPS v2.0 (UCSB Climate Hazards Center), monthly, 1981-2026 — 547 months for
the Yangon study box. Chosen for its length, open licence and satellite+station
blend. Its ~5.5 km resolution is a documented limitation.

**Q5. Are township boundaries official?**
Boundaries are GeoBoundaries ADM3; each township is joined to its **official MIMU
P-code** (MMR013001-MMR013045), the codes used by Myanmar government agencies.
Codes T01-T45 are only stable UI keys mapped to the P-codes.

---

## Methodology [METHOD]

**Q6. How did you compute the risk index?**
Risk = 0.40·Hazard + 0.35·Exposure + 0.25·Vulnerability. Hazard combines
elevation (inverse), annual rainfall, extreme-rainfall month count and a recent
rainfall-flood index. Exposure combines population, population density, schools
and health facilities. Vulnerability combines the census child (<15) and elderly
(65+) shares. All components are min-max normalised; classes are quintiles, not
arbitrary thresholds (`floodresilience/features/risk_index.py`,
`research/methodology.md`).

**Q7. Why those weights?**
Hazard is the physical driver, exposure determines what is harmed, vulnerability
shapes impact severity. The weights are not arbitrary in spirit, but we do not
claim they are objective — which is exactly why we ran a sensitivity analysis:
mean rank spread across 5 weightings is 4.04 ranks, so the ranking is stable
(`outputs/tables/risk_sensitivity.csv`).

**Q8. Why min-max normalization?**
It maps every indicator to 0-1 (higher = worse) and is simple to explain. Its
limitation (sensitivity to outliers) is acknowledged; the sensitivity analysis
also ran a percentile-based alternative.

**Q9. Did you test causality between rainfall and flooding?**
No, and we never claim it. We report associations (documented flood years were
wetter than the long-run mean) and state this explicitly. Correlation is not
causation (`research/limitations.md`).

---

## Statistics [STATS]

**Q10. Is your sample large enough?**
For the risk index, the unit is the township (45) and the time series is 547
months — adequate for the descriptive index and seasonality. For the ML
classifier, the sample is a few hundred months at one site; we treat results as
supporting evidence, not proof.

**Q11. What confidence do you have in the top-ranking townships?**
The ranking is stable under alternative weights (mean rank spread 4.04 of 45).
But it is a relative composite index, not a probability of flooding — we label
classes as quintiles of the score.

---

## Machine learning [ML]

**Q12. What does your ML model actually do?**
It classifies whether a month at the Yangon bbox scale is an extreme-rainfall
month (≥ p95, 718.9 mm) using only lagged rainfall and calendar month, on a
strict temporal split (train ≤ 2005, test > 2005). Random forest: F1 0.667,
ROC-AUC 0.949 vs a majority baseline (F1 0.0). It justifies treating rainfall as
a hazard signal — it is not a flood forecast
(`outputs/reports/model_evaluation.md`).

**Q13. Did you prevent leakage?**
Yes — strict temporal split, features are lagged values strictly in the past,
no random shuffle, no future information.

**Q14. Why not predict actual floods?**
There is no reliable township-level observed-flood label in the open data we
use. We state this honestly and scope the model to the extreme-rainfall
precursor instead.

**Q15. Is your model a real-time forecast?**
No. It is a descriptive/explanatory exercise. We explicitly label scenarios and
any forward-looking content as illustrative, not forecasts.

---

## GIS [GIS]

**Q16. What is your map accuracy?**
Maps are built from GeoBoundaries ADM3 boundaries and Copernicus DEM 30 m. CRS
and aggregation are documented in `research/methodology.md`. Risk is aggregated
to township polygons; the DEM-derived elevation is a zonal mean/min/max per
township.

**Q17. Why township scale and not grid scale?**
Townships are the administrative decision unit for Yangon (45 units) and align
with census and MIMU data. Finer scales are possible but decision-makers act at
township/district level.

---

## SDG & ASEAN alignment [SDG] [ASEAN]

**Q18. Which SDG targets specifically?**
SDG 11.5 (significantly reduce direct economic losses and deaths from disasters,
focusing on poor people), 11.b (adopt policies for resilience and disaster risk
management), 13.1 (strengthen resilience and adaptive capacity to climate
hazards). These are within the six SDGs of the 2026 competition.

**Q19. Which ASEAN plan does this serve?**
The ASCC Blueprint (resilient, inclusive cities), the ASEAN Digital Masterplan
2026-2030 (data-driven governance), and AADMER (ASEAN-wide disaster management
framework). The 2026 theme "Navigating Our Future, Together" frames the
partnership angle.

**Q20. Why should ASEAN care about Yangon?**
Flooding is recurrent across ASEAN cities; the methodology uses mostly
global/regional datasets (CHIRPS, Copernicus DEM, DFO) so it transfers to other
member states by swapping the local census and boundaries (`docs/asean_scalability.md`).

---

## Impact & inclusivity [IMPACT]

**Q21. What is the scale of your impact?**
2,599,370 residents (35.3% of the census population) live in the highest-risk
quintile. 1,320 schools and 1,178 health facilities are located across the 45
townships; the tool helps prioritize where resilience investment and
pre-positioning of services matter most.

**Q22. Who is most underserved?**
Children and the elderly are explicitly modelled via census age shares; low-lying
delta-fringe and peri-urban townships (e.g., Kayan, Thongwa) are identified as
high-risk. We honestly note that no credible township-level poverty data exists
in the open data we could find, so income-based vulnerability is a documented
gap, not an oversight.

---

## Feasibility [FEAS]

**Q23. Can this actually be implemented?**
Yes — it runs entirely on open data, Python, a static SvelteKit frontend, and the
free SAC account. No proprietary hardware or large budgets. The pipeline is
reproducible from `requirements.txt`.

**Q24. Who would run it in the real world?**
A municipal DRM office (e.g., Yangon Regional Disaster Management Department) as
operator, with MIMU providing maintained boundaries/census and meteorological
agencies providing near-real-time rainfall. NGOs (e.g., disaster-response
organisations) and facility operators (hospitals, schools) as users
(`docs/stakeholders.md`).

**Q25. What does it cost to maintain?**
We do not fabricate costs. Hosting can be low-cost static hosting; data refresh
requires running the pipeline when CHIRPS updates. We mark cost figures as
assumptions when present.

---

## Ethics [ETHICS]

**Q26. Could risk scores harm communities?**
Risk scores describe areas, not individuals; all data is aggregate and public.
We warn against using scores to deny services or raise insurance premiums
without validation (`docs/ethics.md`). No personal data is collected.

**Q27. What if the model is wrong?**
We disclose uncertainty throughout (limitations, "illustrative, not forecast"
labels, quintile-based classes). The tool is decision-support, not an emergency
alert system.

---

## Innovation & digital [INNOV]

**Q28. What is genuinely new here?**
Not a new algorithm — a transparent, sensitivity-tested integration of open
geodata + official census + ML-justified hazard into an interactive decision
tool whose logic is fully auditable. Scenario sliders actually re-run the
documented model (baseline-anchored normalization) rather than cosmetic
animation.

**Q29. Where is the AI?**
The random-forest extreme-rainfall classifier and the reproducible risk-scoring
pipeline. We deliberately did not add a chatbot that just repeats dashboard
numbers.

---

## App [APP]

**Q30. Why did you build a web app if SAC is the deliverable?**
SAC is the official storyboard environment; the app demonstrates how the
analysis becomes a usable digital decision-support system, which the
competition explicitly advises. The app and SAC share the same SAC-ready
datasets.

**Q31. How do you keep app and SAC data consistent?**
Both consume the same generated files in `data/sac/`. The app reads
`src/lib/data/*.json`, which are exported from the same processed datasets
(`floodresilience/export/web.py`).

**Q32. Are the scenario results forecasts?**
No — they are illustrative re-runs of the documented model under assumed
changes, clearly labelled as such in the UI and code
(`src/lib/scenario.ts`).

---

## SAC [SAC]

**Q33. Which SAC charts will you show?**
Those specified in `docs/sac_visualizations.md` and `docs/sac_storyboard.md`:
rainfall climatology by month, flood events by year, risk map choropleth,
elevation-vs-risk scatter, top-10 risk bar, exposure KPIs, population bubble
map. Every chart answers a storyboard question.

**Q34. Why should the judges believe your SAC charts exist?**
We will only present charts that are actually built in SAC. The storyboard plan
is the spec; the built storyboard is the evidence. We do not claim a chart
exists before it is created.

---

## Limitations [LIMITS]

**Q35. What is your biggest weakness?**
The 2014 census vintage and the absence of township-level poverty data — both
documented. Also, flood exposure is proxied by rainfall/elevation/facilities
rather than observed inundation extents, because open flood-extent data for
Yangon is limited.

**Q36. Would your results change with better data?**
Yes — that is precisely why the framework separates common layers from local
layers, so better local data can be dropped in without changing the method.