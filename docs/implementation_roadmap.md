# Implementation Roadmap — FloodResilience ASEAN

A phased, realistic path from student prototype to operational decision support.
Deliberately avoids invented budgets: costs are stated only where credible
public benchmarks exist, and are otherwise marked as `PROPOSED ASSUMPTION`.

Status: design document.

---

## Phase 0 — Competition prototype (current)

Already delivered in this repository:

- Jakarta kecamatan risk + exposure datasets (real, public data).
- Reproducible Python pipeline (`floodresilience/`).
- SAC-ready exports (`data/sac/`).
- Interactive SvelteKit prototype (dashboard, risk explorer, map, scenarios).
- Methodology, data provenance, data-quality report, model evaluation.

**Exit criteria**: storyboard submitted; prototype link live; judge Q&A pack
ready.

## Phase 1 — Data foundation (pilot city, e.g. Jakarta)

Objective: turn the prototype into an agreed municipal dataset.

| Work package | Deliverable | Owner suggestion | Dependency |
|---|---|---|---|
| Boundary & code alignment | Official kecamatan/kelurahan codes from BPS | Statistics agency | - |
| Rainfall validation | CHIRPS vs BMKG gauge comparison | Met agency | Gauge data sharing |
| Flood-event validation | Cross-check DFO/GFD extents vs agency records | Disaster agency | Event archives |
| Facility coverage audit | Compare OSM counts vs official registers | City planning dept | Facility registers |
| Vulnerability expansion | District poverty / tenure indicators if released open | Statistics agency | Open data policy |

**Exit criteria**: an audited, versioned city dataset with documented
validation (not just our global-raster baseline).

## Phase 2 — Pilot deployment

Objective: use the tool in a real decision loop with a limited set of users.

| Activity | Detail |
|---|---|
| Stakeholder workshop | City planning + disaster agency + health/education departments review the risk map |
| Use-case integration | Use rankings to shortlist drainage works and pre-positioning sites |
| Feedback loop | Capture corrections; document where the model missed local reality |
| Prototype deployment | Public prototype URL; access control if needed |

**Exit criteria**: one documented decision made using the tool (e.g., priority
list for a flood-prevention programme) and a list of model gaps.

## Phase 3 — Validation & calibration

Objective: rigorous evaluation before any wider rollout.

- Hold-out validation of risk rankings against new flood events.
- Sensitivity analysis review with local hydrologists.
- Update vulnerability layer if better local data becomes available.
- Independent methodological review (university / NGO).

**Exit criteria**: documented accuracy and limits; decisions on which
components are fit for operational use.

## Phase 4 — ASEAN scaling

Objective: replicate the framework in additional ASEAN cities.

- Re-run pipeline for 1-2 additional cities (see `docs/asean_scalability.md`).
- Build a shared open-data catalogue of per-city outputs.
- Publish the framework as open source so other teams/agencies reuse it.
- Engage regional bodies (ASEAN Secretariat, AADMER partners) on adoption.

**Exit criteria**: at least two cities with published, comparable risk
assessments on a shared methodology.

---

## Costs — honest statement

- The competition prototype cost **only team time + free open data + free SAC
  account**. No paid datasets or software were required.
- `PROPOSED ASSUMPTION`: operational phases would need staff time for data
  validation and stakeholder engagement; costs depend entirely on the adopting
  agency and are **not** estimated here to avoid fabrication.
- Open-source reuse keeps marginal cost per new city low (global rasters are
  free; local validation is the main effort).

## Risks

| Risk | Mitigation |
|---|---|
| Data validation depends on agencies | Deliver the framework on global data first; local data is an enhancement, not a blocker |
| Model is relative, not absolute | Communicate quintile-based classes as prioritisation, not safety zones |
| Community mistrust | Transparent methods, plain language, ethics safeguards |
| Scope creep | Strict phase gates; pilot before scaling |
