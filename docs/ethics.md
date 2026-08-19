# Ethics and Privacy — FloodResilience ASEAN

Principles and safeguards for a public-interest data project about urban flood
risk. These are commitments the project actually follows, not aspirations.

Status: living document.

---

## 1. Privacy by design

- **No personal data is collected.** All inputs are aggregate, public datasets:
  gridded rainfall, elevation, modelled population counts, facility point
  locations, and official event archives.
- No names, addresses of individuals, household records, or any personally
  identifiable information are used or stored.
- Population figures are **official 2014 Census township totals** (DoP / MIMU); model-based grid estimates are not used for headline numbers. No household-level census microdata is used.

## 2. Aggregate data only

- Analysis units are administrative districts (kecamatan) and open grid cells.
- Outputs describe *areas*, not individuals. A risk score is attached to a
  district polygon, never to a person or household.

## 3. Vulnerable populations

- Children (<15) and elderly (65+) are included as **aggregate age shares** at
  kota level to reflect coping capacity — the only demographic dimension the
  open data supports reliably.
- The vulnerability component is deliberately lightweight and labelled as a
  proxy. We do not claim it measures poverty or social fragility.
- No inference about any individual resident is ever made.

## 4. Algorithmic fairness and bias

- Risk is a weighted composite; weights are **documented and sensitivity-tested**
  (`research/methodology.md`, `floodresilience/features/risk_index.py`).
- Because quintile classes are relative, every district is compared fairly
  within the same city; no arbitrary thresholds are imposed.
- Known biases are declared: OSM facility counts may undercount informal
  facilities; modelled population may miss some settlements; vulnerability is
  kota-level. These biases favour *under*rating, not overrating, exposure in
  data-poor districts — which is acknowledged, not hidden.

## 5. False alarms and uncertainty

- The tool is a **decision-support prototype, not an early-warning system**.
- Any predictive statement (ML experiment, scenarios) is explicitly labelled:
  "Illustrative scenario — not a forecast."
- Where a value is unknown, the interface shows "data unavailable" rather than a
  fabricated zero (per the project master prompt, section 41).

## 6. Misuse of risk scores

- Risk classes are **prioritisation bands**, not permanent verdicts. Publishing
  them must not stigmatise neighbourhoods or justify disinvestment.
- We frame outputs as resilience-investment targets and require any derivative
  use to keep the same framing.
- Scores must not be used to deny services, insurance, or credit.

## 7. Accessibility and communication

- The prototype uses accessible markup, keyboard navigation, visible focus,
  sufficient contrast, and labels that do not rely on colour alone.
- Plain-language descriptions accompany every chart and metric.

## 8. Data provenance and openness

- Every download is logged with source, timestamp, and SHA-256
  (`data/raw/PROVENANCE.csv`).
- Sources are cited in `data/source_catalog.csv` and the SAC References page.
- The methodology is published so results are auditable and reproducible.

## 9. If we were to scale (future commitment)

- Community consultation before neighbourhood-level publication.
- No collection of sensitive data (income, tenure) without explicit local
  agreement and legal basis.
- Human review before any score is used in a real funding decision.
