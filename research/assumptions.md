# Assumptions (Phase 1)

These are explicit assumptions proposed for the project. Each will be validated or replaced with observed evidence in Phase 2. None are presented as facts.

| # | Assumption | Label | Validation plan |
|---|---|---|---|
| A1 | Satellite precipitation (GPM IMERG) is a sufficient proxy for city-scale rainfall extremes given no complete gauge archive is guaranteed | PROPOSED ASSUMPTION | Compare against local gauge records for the chosen city where available |
| A2 | Global Flood Database + DFO provide a representative sample of significant flood events (not an exhaustive count) | PROPOSED ASSUMPTION | Cross-check against documented events/news for the city |
| A3 | District/sub-district administrative units are the appropriate decision-making scale | PROPOSED ASSUMPTION | Confirm stakeholder expectations; document alternative grid scale |
| A4 | WorldPop/GHSL population estimates are acceptable proxies for population distribution (they are model-based, not census) | PROPOSED ASSUMPTION | Compare totals to official census totals for the city |
| A5 | OSM coverage of critical facilities is complete enough for exposure estimates in the chosen city | PROPOSED ASSUMPTION | Coverage audit against official facility lists; report % matched |
| A6 | A defensible risk index can be built from the available data even if some vulnerability indicators are unavailable | PROPOSED ASSUMPTION | Sensitivity analysis; report which components could not be populated |
| A7 | Historical patterns (2000–present) are a reasonable baseline for near-term risk under current climate; no claim of future projection | PROPOSED ASSUMPTION | State explicitly in all outputs; do not forecast |
| A8 | The chosen city's flood context is representative enough to pilot a framework intended to scale across ASEAN | PROPOSED ASSUMPTION | Design common vs. local layers (docs/asean_scalability.md) |
| A9 | Myanmar is the team's represented country for competition eligibility; the primary analysis city is chosen by data strength, not by nationality | PROPOSED ASSUMPTION | Verified in competition_requirements.md (Myanmar is eligible) |

## Risks & limitations (Phase 1)

1. **Data resolution:** IMERG is ~11 km; city-scale detail requires CHIRPS + gauge data and careful interpretation.
2. **Flood event coverage:** GFD (2000–2018) and DFO vary in completeness; recent events must be sourced from local records.
3. **Reproducibility:** NASA data requires a free Earthdata account (fine for a team); some national portals may require registration or have unstable URLs.
4. **Vulnerability data:** district-level socioeconomic indicators may be outdated or missing; we will use only aggregate public data (never PII).
5. **OSM completeness:** volunteer data; under-mapped informal settlements could bias exposure estimates — we will document this.
6. **Competition deadlines:** exact 2026 dates are UNCERTAIN — must re-verify on aseandse.org.
7. **SAC access:** the team must register to receive the SAC account; storyboard development depends on it.
8. **Timeline:** full pipeline (data→analysis→SAC→SvelteKit→documentation) is large for a 2-person team; phase discipline is essential.