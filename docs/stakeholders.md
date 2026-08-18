# Stakeholder Model — FloodResilience ASEAN

Who the decision-support tool serves, what each stakeholder provides and
receives, and the implementation dependencies between them.

Status: design document for the competition storyboard and the Viability /
Relevancy & Impact judging categories. No stakeholder costs or guarantees are
asserted.

---

## 1. Stakeholder map

| Stakeholder | Role | Data they can provide | Benefit they receive | Responsibility | Implementation dependency |
|---|---|---|---|---|---|
| City government (DKI Jakarta / other ASEAN cities) | Decision-maker, land-use & infrastructure planner | District budgets, drainage plans, urban plans | Prioritised flood-risk map to target drainage and zoning | Adopt risk rankings into planning; maintain updated boundary/census data | Needs stable open-data releases; political will |
| National disaster-management agency (e.g. BNPB Indonesia, NDMO Myanmar) | Emergency preparedness and response | National flood event records, disaster loss data | Where/who/what is most exposed; seasonal hazard windows | Use exposure maps for preparedness planning and resource pre-positioning | Needs flood-extent validation data sharing |
| National meteorological agency (BMKG / PAGASA / TMD / MET Malaysia) | Hazard data authority | Gauge rainfall, forecasts | Visibility into how their data supports urban risk analytics | Publish/verify rainfall records; validate CHIRPS against gauges | Needs sustained station maintenance and open access |
| Humanitarian & NGO actors (OCHA/HDX, Red Cross, local NGOs) | Response and community support | Community-level vulnerability and needs | Evidence base to target humanitarian programmes | Ground-truth risk hotspots with field observations | Needs field partnerships and ethics safeguards |
| Health facilities & hospitals | Service continuity | Facility locations, capacity | Awareness of facility exposure to inform continuity planning | Prepare flood contingency for exposed facilities | Needs facility registers shared securely |
| Schools & education authorities | Service continuity, safety of children | School locations, census | Visibility of schools in high-risk areas | Include schools in continuity and safety planning | Needs verified school lists |
| Infrastructure operators (water, power, transport) | Critical asset owners | Asset location and condition | Exposure of critical assets to inform hardening | Use exposure layer to prioritise asset protection | Needs asset geodata (may be proprietary) |
| Local communities / residents | End beneficiaries | Local knowledge of flood behaviour | Understand their area's risk and what drives it | Act on preparedness guidance; provide feedback | Needs trust, accessibility, and plain-language communication |
| Researchers / universities | Validation and method review | Independent flood studies | Reusable open framework + data | Scrutinise methodology and publish validations | Needs transparent methods and open data |

## 2. Data flows between stakeholders

```
met agency + satellites (rainfall)
        ↓
global rasters (elevation, population)
        ↓
      [ Python pipeline ]
        ↓
risk + exposure datasets
        ↓
SAC storyboard ──→ judges / decision-makers
        ↓
SvelteKit prototype ──→ city, agencies, NGOs, communities
        ↓
local records ──→ validation loop back into pipeline
```

## 3. Ethical responsibilities (summary)

- Use **aggregate public data only**; no personal data is collected.
- Risk scores are **relative prioritisation tools**, never definitive verdicts
  about a specific household or person.
- Communicate uncertainty; never present modelled risk as an observed fact.
- Avoid stigmatising high-risk neighbourhoods — frame outputs as *resilience
  investment targets*, not as fault.
- Full detail: `docs/ethics.md`.

## 4. Viability argument for the storyboard

The stakeholder model shows:

- **Who acts** on each output (city, agencies, operators, communities).
- **Who supplies** the data needed to make it work.
- **What each actor gains**, which is the incentive for adoption.
- **Sequencing**: the framework can start with globally available data (no
  government cooperation needed) and deepen as local stakeholders join.

This supports the Viability (15%) and Relevancy & Impact (20%) judging
criteria without overclaiming costs or timelines.
