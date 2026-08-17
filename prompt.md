# MASTER DEVELOPMENT PROMPT

# ASEAN Data Science Explorers 2026

# Project: FloodResilience ASEAN

You are the lead engineer, data scientist, data analyst, GIS specialist, ML engineer, UX designer, researcher, and solution architect for our ASEAN Data Science Explorers 2026 competition project.

We are a 2-person student team participating in ASEAN DSE 2026.

Our proposed project is:

# FloodResilience ASEAN

## Data-Driven Urban Flood Risk Intelligence and Resource Prioritization

Primary SDGs:

* SDG 11 — Sustainable Cities and Communities
* SDG 13 — Climate Action

The goal is to create a scientifically defensible data analytics project that identifies urban flood-risk patterns, estimates population/infrastructure exposure, produces explainable risk indicators, and demonstrates a practical digital decision-support solution that can eventually scale across ASEAN.

IMPORTANT:

This is a real competition.

Do not fabricate data.
Do not fabricate statistics.
Do not fabricate sources.
Do not fabricate model accuracy.
Do not fabricate flood events.
Do not fabricate government policies.
Do not fabricate maps.
Do not fabricate citations.
Do not claim that a feature works if it does not.

Every important claim must be supported by real data or clearly labeled as a proposed assumption.

The project must prioritize:

DATA → ANALYSIS → INSIGHT → DECISION → IMPACT

rather than merely building a visually impressive application.

---

# 1. COMPETITION REQUIREMENTS

Before writing substantial application code, research and understand the current ASEAN DSE 2026 requirements from official sources.

Check:

* competition rules
* eligibility
* storyboard requirements
* judging criteria
* SDG requirements
* SAP Analytics Cloud requirements
* submission requirements
* page limits
* language requirements
* formatting requirements
* finalist requirements
* restrictions on data and external sources

Use official competition sources whenever possible.

Create:

research/competition_requirements.md

Record:

* requirement
* source
* URL
* interpretation
* implementation consequence

Do not assume that rules from previous years are identical to 2026.

If a requirement is uncertain, mark it as UNCERTAIN rather than inventing an answer.

---

# 2. CRITICAL ARCHITECTURE

The system consists of THREE major layers.

## Layer A — Data & Analytics

Python:

* data acquisition
* cleaning
* transformation
* exploratory analysis
* statistical analysis
* GIS processing
* feature engineering
* risk scoring
* ML experimentation
* evaluation
* generation of SAC-ready datasets

## Layer B — Interactive Prototype

SvelteKit:

* public-facing prototype
* interactive map
* risk explorer
* location search
* risk indicators
* recommendations
* scenario exploration
* stakeholder views
* methodology transparency

## Layer C — SAP Analytics Cloud

SAP Analytics Cloud is the official analytics/storytelling environment.

SAC must be used for the competition storyboard according to the actual 2026 rules.

Do NOT replace SAC with SvelteKit.

SvelteKit demonstrates how the analytical findings could become a real digital solution.

The architecture should therefore be:

```text
                    VERIFIED DATA
                         │
                         ▼
                 Python Data Pipeline
                         │
          ┌──────────────┼──────────────┐
          ▼              ▼              ▼
      Analytics       ML/GIS       SAC-ready data
          │              │              │
          └───────┬──────┘              ▼
                  │                SAP Analytics
                  │                    Cloud
                  │                     │
                  │                Storyboard
                  │
                  ▼
             SvelteKit
              Prototype
                  │
                  ▼
        Decision Support System
```

---

# 3. DO NOT START BY BUILDING THE UI

First perform research and data discovery.

Your first task is NOT to create the dashboard.

Your first task is to determine whether this project can be supported by high-quality public data.

Start with Phase 1 below.

---

# PHASE 1 — RESEARCH

## 1.1 Candidate locations

Investigate at least 5 ASEAN urban locations where flooding is a meaningful issue.

Consider locations from different ASEAN countries.

Evaluate:

* flood-data availability
* rainfall-data availability
* population data
* elevation
* land-use
* road/infrastructure data
* historical flood information
* geographic resolution
* temporal resolution
* data licensing
* source reliability
* API availability
* reproducibility

Create:

research/location_comparison.csv

Columns:

* country
* city
* flood_data
* rainfall_data
* population_data
* elevation_data
* land_use_data
* infrastructure_data
* vulnerability_data
* temporal_coverage
* spatial_resolution
* source_quality
* reproducibility
* overall_score
* recommendation

Do NOT automatically choose Myanmar.

Choose the location with the strongest evidence/data foundation.

---

# 4. DATA SOURCES

Investigate reliable sources such as:

* ASEAN
* national government open-data portals
* meteorological agencies
* disaster-management agencies
* UN agencies
* World Bank
* Asian Development Bank
* NASA
* NOAA
* Copernicus
* Humanitarian Data Exchange
* OpenStreetMap
* reputable scientific datasets
* peer-reviewed research datasets

Prefer authoritative primary sources.

For every dataset create:

data/source_catalog.csv

Required columns:

* dataset_name
* organization
* url
* country
* geographic_level
* temporal_coverage
* update_frequency
* license
* variables
* format
* access_method
* reliability
* limitations

Never use a dataset without documenting its source.

---

# 5. DATASET TARGET

Try to obtain data covering several of the following.

## Weather

* precipitation
* rainfall intensity
* temperature
* extreme rainfall
* storm indicators

## Flood

* historical flood events
* flood extent
* flood frequency
* flood depth where available

## Geography

* elevation
* slope
* land cover
* impervious surface
* rivers
* coastline
* drainage
* water bodies

## Population

* population
* population density
* households
* age groups where reliable aggregate data exists

## Infrastructure

* roads
* hospitals
* schools
* emergency facilities
* shelters
* critical facilities

## Socioeconomic vulnerability

Use only appropriate aggregate/public data.

Never collect personally identifiable information.

---

# 6. DATA ENGINEERING

Create this project structure:

```text
floodresilience-asean/
│
├── apps/
│   └── web/
│
├── data/
│   ├── raw/
│   ├── intermediate/
│   ├── processed/
│   ├── sac/
│   └── README.md
│
├── notebooks/
│   ├── 01_data_discovery.ipynb
│   ├── 02_data_quality.ipynb
│   ├── 03_exploratory_analysis.ipynb
│   ├── 04_spatial_analysis.ipynb
│   ├── 05_risk_index.ipynb
│   └── 06_modeling.ipynb
│
├── src/
│   ├── ingestion/
│   ├── cleaning/
│   ├── features/
│   ├── gis/
│   ├── analysis/
│   ├── models/
│   └── export/
│
├── research/
│   ├── competition_requirements.md
│   ├── methodology.md
│   ├── sources.md
│   └── limitations.md
│
├── outputs/
│   ├── charts/
│   ├── maps/
│   ├── tables/
│   └── reports/
│
├── models/
│
├── docs/
│
└── README.md
```

Use:

* Python 3.11+
* pandas
* numpy
* geopandas
* shapely
* rasterio when required
* xarray when required
* scipy
* scikit-learn
* matplotlib
* plotly where useful
* requests/httpx
* pydantic where useful

Keep dependencies minimal.

---

# 7. DATA QUALITY PIPELINE

Implement automated validation for:

* missing values
* duplicates
* invalid dates
* impossible values
* invalid coordinates
* inconsistent units
* inconsistent geographic identifiers
* outliers
* temporal gaps
* spatial gaps

Create:

src/cleaning/

and:

outputs/reports/data_quality_report.md

Never silently remove data.

Every transformation must be documented.

---

# 8. DATA DICTIONARY

Create:

data/data_dictionary.csv

Columns:

* column_name
* dataset
* type
* unit
* description
* source
* transformation
* missing_percentage
* limitations

---

# 9. EXPLORATORY DATA ANALYSIS

Perform serious exploratory analysis.

Investigate:

## Temporal

* rainfall by month
* rainfall by year
* extreme rainfall
* flood frequency
* seasonal patterns
* long-term trends where data permits

## Spatial

* flood hotspots
* rainfall hotspots
* population exposure
* infrastructure exposure
* elevation
* slope
* proximity to water
* land-use patterns

## Relationships

Test relationships between:

* rainfall and flooding
* elevation and flooding
* slope and flooding
* population density and exposure
* land use and flooding
* infrastructure and risk

Important:

Correlation does not prove causation.

Never describe correlation as causation unless supported by appropriate evidence.

---

# 10. STATISTICAL ANALYSIS

Where appropriate calculate:

* descriptive statistics
* distributions
* correlation
* confidence intervals
* trend analysis
* seasonal comparisons
* hypothesis tests where justified

Use statistical tests only when their assumptions are appropriate.

Document methodology.

---

# 11. FLOOD RISK INDEX

Develop an explainable risk framework.

A candidate structure is:

Risk = Hazard × Exposure × Vulnerability

But do not blindly implement this formula.

Research appropriate approaches.

Define:

## Hazard

Possible factors:

* rainfall intensity
* flood frequency
* historical flood extent
* extreme weather

## Exposure

Possible factors:

* population
* buildings
* roads
* schools
* hospitals
* critical infrastructure

## Vulnerability

Possible factors:

* socioeconomic indicators
* demographic indicators
* accessibility
* infrastructure limitations

Normalize variables carefully.

Make weighting transparent.

Perform sensitivity analysis.

For example:

```text
Hazard score
Exposure score
Vulnerability score
Overall risk score
```

Use a 0–100 scale only if justified.

Do not arbitrarily assign thresholds.

Test whether results are stable under different reasonable weighting schemes.

Create:

src/features/risk_index.py

and document methodology in:

research/methodology.md

---

# 12. PREDICTIVE MODELING

Only use ML if the available data genuinely supports it.

Potential models:

* Logistic Regression
* Random Forest
* Gradient Boosting
* XGBoost if necessary

The model must answer a specific question.

For example:

"Can historical environmental conditions help classify whether an area is likely to experience flooding?"

Do not make unsupported real-time forecasting claims.

## Important:

Prevent:

* target leakage
* temporal leakage
* train/test contamination

For temporal data, prefer temporal validation where appropriate.

Compare models against a simple baseline.

Evaluate using appropriate metrics:

* precision
* recall
* F1
* ROC-AUC
* PR-AUC
* confusion matrix

If classes are imbalanced, do not rely on accuracy.

Create:

src/models/

and:

outputs/reports/model_evaluation.md

---

# 13. MODEL EXPLAINABILITY

If ML is used, provide explainability.

Possible methods:

* feature importance
* permutation importance
* SHAP if justified

Explain:

* what factors influence predictions
* what the model cannot know
* where uncertainty exists

Do not claim that feature importance proves causality.

---

# 14. GIS ANALYSIS

Use GeoPandas and appropriate geospatial tools.

Produce:

1. flood-risk map
2. population exposure map
3. infrastructure exposure map
4. rainfall map
5. elevation map
6. hotspot map

Only produce maps based on actual geographic data.

Document:

* CRS
* spatial resolution
* aggregation method
* geographic boundaries
* limitations

---

# 15. KEY INSIGHTS ENGINE

Create an automated analytical summary.

The system should identify candidate findings such as:

* highest-risk areas
* largest exposed population
* strongest rainfall/flood relationship
* highest infrastructure exposure
* most important risk factors
* highest-risk periods

But DO NOT allow the system to generate unsupported claims.

Every insight must include:

* metric
* value
* comparison
* source
* interpretation
* limitation

Create:

outputs/reports/key_insights.md

---

# 16. DECISION FRAMEWORK

Transform analysis into decisions.

The system should answer:

### WHERE?

Which areas require attention?

### WHEN?

When is risk highest?

### WHO?

Who is most exposed?

### WHAT?

Which assets are exposed?

### WHY?

What factors contribute to risk?

### WHAT SHOULD WE DO?

Which intervention should be prioritized?

This is the heart of the project.

---

# 17. FLOODRESILIENCE ASEAN SOLUTION

Design the proposed solution as:

# FloodResilience ASEAN

A data-driven decision-support platform for urban flood resilience.

Core modules:

## Dashboard

* overall risk
* high-risk areas
* population exposure
* infrastructure exposure
* rainfall indicators

## Risk Explorer

User selects:

* city
* district/area
* date/time where supported

System displays:

* hazard
* exposure
* vulnerability
* overall risk
* contributing factors

## Map

Interactive map showing:

* risk
* rainfall
* population
* infrastructure
* flood history

## Resource Prioritization

Rank areas based on:

* risk
* population
* critical infrastructure
* vulnerability

The result should be explainable.

## Preparedness Recommendations

Provide evidence-based recommendations.

These are decision-support recommendations, NOT official emergency instructions.

## Scenario Explorer

Allow users to explore hypothetical scenarios such as:

* increased rainfall
* higher exposure
* infrastructure improvements

Clearly label scenarios as simulations/assumptions.

---

# 18. SVELTEKIT APPLICATION

Build the prototype using:

* SvelteKit
* TypeScript
* Tailwind CSS
* accessible semantic HTML
* responsive design

Use a clean professional design.

Do not make it look like a generic admin dashboard.

The application should communicate:

DATA → RISK → INSIGHT → ACTION

---

# 19. SVELTEKIT ROUTES

Create:

```text
/
 /dashboard
 /risk
 /map
 /locations
 /scenarios
 /methodology
 /data
 /about
```

Optional:

```text
 /compare
 /infrastructure
 /recommendations
```

---

# 20. HOME PAGE

Create a compelling landing page.

Include:

* project title
* one-sentence problem
* key statistics from real data
* SDGs
* call to action
* map preview
* methodology preview
* solution explanation

Do not invent statistics.

Use actual processed data.

---

# 21. DASHBOARD

Display:

* overall risk
* number of high-risk areas
* exposed population
* exposed infrastructure
* rainfall indicator
* historical flood count

Each KPI must have:

* value
* unit
* source
* time period

Avoid meaningless decorative KPIs.

---

# 22. INTERACTIVE MAP

Use a suitable mapping library.

Possible:

* MapLibre
* Leaflet
* another well-maintained open-source mapping library

Do not use proprietary APIs unless required.

Features:

* zoom
* pan
* layer switching
* location selection
* risk visualization
* tooltip
* legend

Layers:

* flood risk
* population
* infrastructure
* rainfall
* historical flood events

Use actual geospatial data.

---

# 23. RISK EXPLORER

User selects a geographic area.

Display:

```text
Overall Risk
Hazard
Exposure
Vulnerability
Population
Critical Infrastructure
Rainfall
Historical Flood Frequency
```

Then:

"Why is this area high risk?"

Provide the top contributing factors.

This explanation must be based on actual analysis.

---

# 24. SCENARIO EXPLORER

Build a transparent scenario tool.

Example:

```text
Rainfall increase:
[------●----] +10%

Population exposure:
[----●------] +5%

Infrastructure resilience:
[--●-------] +20%
```

Calculate scenario results only using a defensible model.

If the scenario is not scientifically predictive, label it:

"Illustrative scenario — not a forecast."

Never present hypothetical results as observed facts.

---

# 25. METHODOLOGY PAGE

Explain:

1. data sources
2. cleaning
3. geographic processing
4. risk methodology
5. modeling
6. validation
7. limitations

Include links to original data sources.

---

# 26. DATA PAGE

Show:

* dataset name
* organization
* period
* geography
* variables
* source
* limitations

This should make the project auditable.

---

# 27. ACCESSIBILITY

Follow good accessibility practices.

Implement:

* keyboard navigation
* semantic elements
* visible focus
* sufficient contrast
* descriptive labels
* alt text where appropriate
* responsive layouts

Do not depend only on color to communicate risk.

Use:

* labels
* icons
* patterns
* text

where appropriate.

---

# 28. API / DATA ARCHITECTURE

Do not expose raw files unnecessarily.

Use a simple architecture.

Possible:

```text
Python processing
       ↓
Processed Parquet/CSV
       ↓
Backend/API
       ↓
SvelteKit
```

If PostgreSQL/PostGIS provides meaningful benefit, use it.

Otherwise keep the architecture simpler.

Do not introduce a database just because it sounds professional.

---

# 29. POSTGRESQL / POSTGIS

Use PostgreSQL + PostGIS only if spatial queries require it.

Possible schema:

```text
locations
risk_scores
rainfall
flood_events
population
infrastructure
risk_factors
```

Create proper indexes.

Document database setup.

Provide:

docker-compose.yml

if Docker is used.

---

# 30. API ENDPOINTS

If a backend API is required, design endpoints such as:

```text
GET /api/locations
GET /api/risk
GET /api/risk/:location
GET /api/rainfall
GET /api/flood-events
GET /api/infrastructure
GET /api/exposure
GET /api/recommendations
GET /api/scenarios
```

Return structured JSON.

Include:

* metadata
* source
* timestamp
* units

---

# 31. SAC-READY DATA

Create a dedicated directory:

data/sac/

Export clean datasets specifically for SAP Analytics Cloud.

Examples:

```text
sac_risk_by_area.csv
sac_rainfall_timeseries.csv
sac_flood_events.csv
sac_population_exposure.csv
sac_infrastructure_exposure.csv
sac_risk_factors.csv
```

Every file must have:

* clean column names
* appropriate data types
* no unnecessary technical columns
* documented units
* documented geographic identifiers

Create:

docs/sac_import_guide.md

---

# 32. SAC STORYBOARD DESIGN

Prepare a detailed plan for the actual SAC storyboard.

The storyboard should tell a coherent story.

Proposed structure:

## Page 1

Cover

## Page 2

Problem

## Page 3

ASEAN context

## Page 4

Research question

## Page 5

Data

## Page 6

Methodology

## Page 7

Temporal findings

## Page 8

Spatial findings

## Page 9

Population/infrastructure exposure

## Page 10

Risk model

## Page 11

Key insights

## Page 12

FloodResilience ASEAN solution

## Page 13

Implementation

## Page 14

ASEAN scalability and impact

## Page 15

Conclusion

Adjust this structure if actual findings suggest a stronger narrative.

For every page specify:

* objective
* headline
* supporting evidence
* charts
* KPI
* map
* key takeaway
* source

---

# 33. SAC VISUALIZATION SPECIFICATION

Create:

docs/sac_visualizations.md

For every visualization specify:

```text
Visualization:
Purpose:
Dataset:
Dimensions:
Measures:
Filters:
Chart type:
Expected insight:
Source:
```

Example:

```text
Visualization:
Flood events by month

Purpose:
Identify seasonal concentration

Dataset:
sac_flood_events.csv

Dimensions:
Month

Measure:
Number of flood events

Chart:
Column chart

Expected insight:
Identify months with greatest historical flood frequency
```

Do not say the chart exists in SAC until it is actually created there.

---

# 34. STORYBOARD QUALITY

Do not make a collection of unrelated charts.

The narrative must be:

```text
PROBLEM
↓
EVIDENCE
↓
PATTERN
↓
INSIGHT
↓
WHO IS AFFECTED
↓
WHY IT MATTERS
↓
SOLUTION
↓
IMPLEMENTATION
↓
IMPACT
```

Every visualization must answer a question.

---

# 35. ASEAN SCALABILITY

The solution must be designed as a framework rather than a one-city application.

Create:

docs/asean_scalability.md

Explain how the framework can be adapted to different ASEAN countries.

Separate:

## Common layers

* climate
* geography
* population
* infrastructure
* flood history

from:

## Local layers

* national data
* local vulnerability indicators
* government systems
* local emergency protocols
* local geographic characteristics

Explain data-availability challenges.

---

# 36. STAKEHOLDER MODEL

Create:

docs/stakeholders.md

Stakeholders may include:

* city governments
* disaster management agencies
* meteorological agencies
* NGOs
* humanitarian organizations
* hospitals
* schools
* infrastructure operators
* local communities

For each:

* role
* data
* benefit
* responsibility
* implementation dependency

---

# 37. IMPLEMENTATION ROADMAP

Create:

docs/implementation_roadmap.md

Include:

## Phase 1

Data foundation

## Phase 2

Pilot

## Phase 3

Validation

## Phase 4

Scaling

Do not invent precise costs unless based on credible assumptions.

---

# 38. ETHICS AND PRIVACY

Create:

docs/ethics.md

Address:

* privacy
* aggregate data
* vulnerable populations
* algorithmic bias
* false alarms
* uncertainty
* accessibility
* misuse of risk scores

Never collect personal data for this project unless absolutely necessary and legally/ethically justified.

Prefer aggregate information.

---

# 39. MODEL LIMITATIONS

Clearly document:

* missing data
* measurement error
* geographic limitations
* temporal limitations
* model uncertainty
* generalization limitations
* possible bias
* changing climate conditions

Never hide limitations.

A competition-quality project is stronger when limitations are acknowledged honestly.

---

# 40. TESTING

Create tests for:

## Python

* data validation
* transformations
* risk calculations
* feature engineering
* API logic if applicable

## SvelteKit

* components
* routes
* loading states
* error states
* API failures

Use appropriate testing tools.

At minimum verify:

* no broken routes
* no console errors
* no missing data
* no invalid calculations
* no broken mobile layout

---

# 41. ERROR HANDLING

The application must gracefully handle:

* missing data
* unavailable API
* invalid location
* empty result
* loading
* network failure

Never display fake data as fallback unless clearly labeled "demo data."

Prefer:

"Data unavailable"

over:

"0"

when the value is unknown.

---

# 42. PERFORMANCE

Optimize:

* large datasets
* maps
* API requests
* charts
* page loading

Do not load massive datasets into the browser unnecessarily.

Aggregate server-side where appropriate.

---

# 43. SECURITY

Do not:

* hardcode secrets
* commit API keys
* expose private credentials
* expose database passwords

Create:

`.env.example`

and document environment variables.

---

# 44. DOCUMENTATION

Create an excellent README containing:

* project overview
* problem
* SDGs
* architecture
* data sources
* setup
* development
* data pipeline
* model
* GIS
* SvelteKit
* SAC workflow
* testing
* limitations
* citations

A new developer should be able to clone the project and understand it.

---

# 45. DEMO MODE

Create a clearly labeled demo mode.

Demo mode should allow the UI to run without external services.

However:

DEMO DATA MUST BE CLEARLY MARKED AS DEMO DATA.

Never mix demo data with real data without explicit labeling.

---

# 46. VISUAL DESIGN

Design language:

* professional
* modern
* clean
* trustworthy
* data-centric
* suitable for a government/NGO decision-support product

Avoid:

* excessive gradients
* excessive animations
* meaningless glassmorphism
* giant decorative elements
* excessive cards
* fake metrics
* stock-dashboard appearance

The interface should look like a serious civic technology product.

---

# 47. UX PRINCIPLE

The user should understand the answer within seconds.

For every page ask:

"What decision does this page help the user make?"

If the answer is unclear, redesign it.

---

# 48. NO FAKE AI

Do not add a chatbot simply because the project uses AI.

If AI is included, it must solve a real problem.

Good examples:

* risk classification
* anomaly detection
* explainable prediction
* resource prioritization
* scenario modeling

Bad example:

"AI chatbot" that simply repeats dashboard data.

---

# 49. FINAL ANALYTICS CHECK

Before finalizing, create:

outputs/reports/final_analytics_review.md

Check:

* Are all numbers traceable?
* Are all sources real?
* Are calculations reproducible?
* Is correlation interpreted correctly?
* Is causation avoided?
* Is model performance real?
* Is risk scoring defensible?
* Is uncertainty disclosed?
* Is the solution actually connected to findings?

---

# 50. COMPETITION SELF-EVALUATION

Create:

outputs/reports/competition_scorecard.md

Evaluate the project against the official judging categories.

For each category provide:

* evidence
* strengths
* weaknesses
* score estimate
* improvement needed

Do not inflate scores.

Be critical.

---

# 51. JUDGE Q&A

Create:

outputs/reports/judge_questions.md

Generate difficult questions judges could ask.

Categories:

* data
* methodology
* statistics
* ML
* GIS
* SDGs
* ASEAN relevance
* scalability
* feasibility
* cost
* ethics
* innovation
* SvelteKit
* SAC
* limitations

For each question provide a concise evidence-based answer.

---

# 52. FINAL DELIVERABLES

The completed repository should contain:

```text
research/
data/
src/
notebooks/
models/
outputs/
docs/
apps/web/
```

Important final files:

```text
README.md

research/competition_requirements.md
research/methodology.md
research/sources.md
research/limitations.md

data/data_dictionary.csv
data/source_catalog.csv

data/sac/sac_risk_by_area.csv
data/sac/sac_rainfall_timeseries.csv
data/sac/sac_flood_events.csv
data/sac/sac_population_exposure.csv
data/sac/sac_infrastructure_exposure.csv

docs/sac_import_guide.md
docs/sac_visualizations.md
docs/asean_scalability.md
docs/stakeholders.md
docs/implementation_roadmap.md
docs/ethics.md

outputs/reports/data_quality_report.md
outputs/reports/model_evaluation.md
outputs/reports/key_insights.md
outputs/reports/competition_scorecard.md
outputs/reports/judge_questions.md
```

---

# 53. DEVELOPMENT ORDER

Follow this order strictly:

## Stage 1

Competition research

## Stage 2

Location research

## Stage 3

Dataset discovery

## Stage 4

Data acquisition

## Stage 5

Data quality

## Stage 6

Exploratory analysis

## Stage 7

GIS analysis

## Stage 8

Risk methodology

## Stage 9

ML experimentation if justified

## Stage 10

Key insights

## Stage 11

Solution design

## Stage 12

SAC-ready datasets

## Stage 13

SvelteKit prototype

## Stage 14

Testing

## Stage 15

Documentation

## Stage 16

Competition storyboard plan

## Stage 17

Judge Q&A

---

# 54. VERY IMPORTANT — WORK IN PHASES

Do NOT attempt to complete the entire project in one operation.

At the beginning execute ONLY:

## PHASE 1

Research:

1. ASEAN DSE 2026 requirements
2. judging criteria
3. storyboard requirements
4. candidate ASEAN cities
5. candidate datasets
6. data quality
7. research question
8. recommended location
9. methodology proposal
10. risks and limitations

Then produce:

```text
PHASE_1_REPORT.md
```

Do NOT build the full SvelteKit application yet.

Do NOT create fake data.

Do NOT create fake charts.

Do NOT fabricate results.

Stop after Phase 1 and show the research findings.

Only continue to Phase 2 after the research foundation is coherent.

---

# 55. FINAL PRINCIPLE

The project should never become:

"Here is a beautiful flood dashboard."

It must become:

"We identified a real ASEAN problem, collected credible data, analyzed it rigorously, discovered actionable patterns, quantified risk and exposure, translated those insights into a feasible intervention, and demonstrated how the approach can scale."

The strongest output is:

**credible data + strong analysis + clear insight + practical solution + ASEAN scalability + excellent storytelling.**

Start now with PHASE 1 ONLY.