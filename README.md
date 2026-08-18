# FloodResilience ASEAN

**Data-driven urban flood risk intelligence and resource prioritization.**

Student project for the **ASEAN Data Science Explorers 2026** competition.
Two-person team representing **Myanmar**. Primary SDGs: **SDG 11** (Sustainable
Cities and Communities) and **SDG 13** (Climate Action).

The analysis city is **Yangon Region, Myanmar** — selected in Phase 1 on evidence
strength (data availability, verifiability, documented flood history), not on
home-country convenience. The framework is designed to replicate across ASEAN
cities (see `docs/asean_scalability.md`).

> Honesty principle: no fabricated data, statistics, sources, model accuracy or
> maps. Every number in this repository is traceable to a documented public
> source or is explicitly labelled `PROPOSED ASSUMPTION`.

---

## 1. Problem

Urban flooding in ASEAN threatens lives, critical infrastructure and economic
activity. Cities need a defensible, data-driven way to know **where** risk is
highest, **who/what** is exposed, **when** hazards peak, and **what** to do
first. This project answers those questions for Yangon and demonstrates how
the method scales across ASEAN.

## 2. Approach

```
VERIFIED DATA → Python pipeline → risk model → SAC storyboard + SvelteKit prototype
```

- **Layer A — Data & analytics (Python):** acquisition, cleaning, GIS zonal
  statistics, risk scoring, ML experimentation, exports.
- **Layer B — Interactive prototype (SvelteKit):** dashboard, risk explorer,
  interactive map, scenario explorer, methodology & data pages.
- **Layer C — SAP Analytics Cloud:** the official competition storyboard
  (mandatory per 2026 rules). SvelteKit is the solution prototype, **not** a
  replacement for SAC.

## 3. Key results (real data)

| Finding | Value | Source |
|---|---|---|
| Townships assessed | 45 townships of Yangon Region | `data/processed/` |
| Modelled population | ~8.32 M (45 townships) | Kontur H3, area-weighted |
| Population in highest risk class | ~31.3% (class 5) | risk scores + population |
| Rainfall months analysed | 245 (1981-2001) | CHIRPS v2.0 |
| Top-ranked township | Thongwa (56.8 / 100) | default weights |
| Elevation range | -9.2 m … 487.5 m (township min/max) | Copernicus DEM 30 m |
| Facilities | 1,320 schools, 1,178 health facilities | HDX/OSM (Myanmar) |
| Documented flood years | 1988, 1991, 1997, 2002, 2004, 2007, 2008, 2010, 2013, 2014, 2015, 2017, 2019, 2020 | PIAHS 386, Sritarapipat 2017, OCHA, UNOSAT |

Full narrative: `outputs/reports/key_insights.md`.

## 4. Risk methodology

Risk = 0.40 · Hazard + 0.35 · Exposure + 0.25 · Vulnerability

- **Hazard:** elevation (inverse), annual rainfall, extreme-rainfall month count,
  recent rainfall-flood index (World Bank/GFDRR).
- **Exposure:** population, density, schools, health facilities.
- **Vulnerability:** children (<15) and elderly (65+) shares (district-level).

All components min-max normalised to [0,1]; classes are quintiles (no arbitrary
thresholds); five weighting schemes are sensitivity-tested. Details:
`research/methodology.md`, `floodresilience/features/risk_index.py`.

## 5. Repository layout

```
data/             raw / intermediate / processed / sac / source_catalog.csv / data_dictionary.csv
docs/             SAC import guide, visualizations, storyboard, scalability, stakeholders, roadmap, ethics
floodresilience/  Python package (ingestion, cleaning, features, gis, analysis, models, export)
models/           trained model artifacts (empty until ML is justified)
notebooks/        notebooks (see below)
outputs/          charts / maps / tables / reports (quality, insights, model evaluation)
research/         competition requirements, location comparison, sources, methodology, assumptions, limitations
src/              SvelteKit app
tests/            Python + SvelteKit tests
```

## 6. Data sources

| Layer | Source | Licence |
|---|---|---|
| Rainfall | CHIRPS v2.0 (UCSB Climate Hazards Center) | free/public |
| Elevation | Copernicus DEM GLO-30 | free & open |
| Population | Kontur H3 (2023); WorldPop ADM2 age shares | CC-BY-like |
| Facilities | HDX / OSM school & health points | ODbL/HDX |
| Rainfall-flood index | World Bank / GFDRR subnational | open |
| Flood events | Dartmouth Flood Observatory | free academic |
| Boundaries | GeoBoundaries Myanmar (ADM1/2/3), MIMU codes | open |

Full catalogue with URLs and limitations: `data/source_catalog.csv`. Download
log with SHA-256: `data/raw/PROVENANCE.csv`.

## 7. Setup — Python pipeline

Requires Python 3.11+.

```sh
python -m venv .venv
.venv\Scripts\activate          # Windows
# source .venv/bin/activate     # macOS/Linux
pip install -r requirements.txt
```

Regenerate all analytics outputs (assumes `data/raw/` is populated):

```sh
.venv\Scripts\python.exe -m floodresilience.analysis.pipeline     # features + QC report
.venv\Scripts\python.exe -m floodresilience.features.risk_index   # risk scores + sensitivity
.venv\Scripts\python.exe -m floodresilience.analysis.insights     # key insights
.venv\Scripts\python.exe -m floodresilience.models.extreme_rainfall  # ML experiment + report
.venv\Scripts\python.exe -m floodresilience.export.sac            # SAC-ready CSVs
.venv\Scripts\python.exe -m floodresilience.export.web            # SvelteKit data bundle
.venv\Scripts\python.exe -m floodresilience.export.data_dictionary  # data dictionary
```

## 8. Setup — SvelteKit prototype

```sh
npm install
npm run dev        # http://localhost:5173
npm run build      # production build
npm run preview    # preview production build
```

Routes: `/` (dashboard), `/risk` (explorer), `/map`, `/scenarios`,
`/locations` (+ per-township), `/methodology`, `/data`, `/about`.

Quality gates:

```sh
npm run check      # svelte-check (types)
npm run lint       # eslint + prettier
npm test           # vitest unit tests
```

## 9. ML experimentation (honest scope)

`floodresilience/models/extreme_rainfall.py` answers a strictly scoped
question: *can lagged rainfall classify extreme-rainfall months (≥ p95) at the
Yangon bbox scale?* It uses a temporal train/test split (train ≤2005, test
>2005), no target leakage, a majority-class baseline, and reports
precision/recall/F1/ROC-AUC/PR-AUC. A township-level flood classifier is
**not** attempted because no reliable per-township flood label exists in the
open data. Full evaluation: `outputs/reports/model_evaluation.md`.

## 10. SAC workflow

1. Import the CSVs in `data/sac/` into SAP Analytics Cloud.
2. Follow `docs/sac_import_guide.md` for columns, types and geo mapping.
3. Build the storyboard per `docs/sac_storyboard.md` and
   `docs/sac_visualizations.md`.
4. Export landscape PDF ≤20 MB, ≤15 pages incl. cover, references closing.

## 11. Testing

- Python: `pytest` for cleaning, risk calculations, exports (see `tests/`).
- SvelteKit: vitest component/unit tests (see `src/lib/**/*.spec.ts` and
  `tests/`).

## 12. Limitations (summary)

- Vulnerability is district-level, not township-level.
- CHIRPS rainfall is ~5.5 km — coarse for intra-township differences.
- No township-level poverty/socioeconomic open data for Yangon.
- Modelled population (Kontur/WorldPop) is an estimate, not a census.
- OSM facility counts may undercount informal facilities.
- Correlations are reported as associations, never causation.

Full: `research/limitations.md`, `research/assumptions.md`, `docs/ethics.md`.

## 13. Competition context

Official 2026 requirements are compiled in `research/competition_requirements.md`
with sources and URLs. Key constraints: SAC storyboard mandatory; six SDGs
(2, 3, 6, 11, 12, 13); landscape PDF ≤20 MB, ≤15 pages incl. cover, images
≤2 MB, SAC-generated charts, references closing page; judging weights
Analysis & Insights 25%, Relevancy & Impact 20%, Problem Definition 10%,
Viability 15%, Innovation 15%, Presentation 15%. Items not confirmed for 2026
are marked `UNCERTAIN` in that file.

## 14. Documentation index

- `PHASE_1_REPORT.md` — research foundation
- `research/methodology.md` — risk model and pipeline
- `docs/sac_storyboard.md` — storyboard plan
- `docs/asean_scalability.md` — ASEAN scaling
- `docs/stakeholders.md` — stakeholder model
- `docs/implementation_roadmap.md` — rollout phases
- `docs/ethics.md` — ethics and privacy
- `outputs/reports/key_insights.md` — analytical findings
- `outputs/reports/data_quality_report.md` — QC results
- `outputs/reports/model_evaluation.md` — ML evaluation

## 15. Acknowledgements

All data is public and attributed in `data/source_catalog.csv` and the SAC
References page. This project is a student submission; it is a decision-support
prototype, not an operational early-warning system.
