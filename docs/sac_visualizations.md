# SAC Visualizations — Storyboard Recommendations

These chart designs fit the SAC storyboard for the **FloodResilience ASEAN**
dashboard (ASEAN Data Science Explorers 2026). Each entry lists the SAC chart
type, the dataset and columns to bind, and the message to convey.

## Story 1: The problem scale (exposure)

| Item | Value |
|---|---|
| SAC chart | **Geo map** (background map + bubble / choropleth by `tship_code`) |
| Dataset | `sac_risk_by_area.csv` |
| Measures | `risk_class` (segment/color), `pop_est` (bubble size) |
| Message | Which townships are riskiest and how many people live there |

| Item | Value |
|---|---|
| SAC chart | **Column** (stacked) |
| Dataset | `sac_infrastructure_exposure.csv` |
| Dimensions | `district` |
| Measures | `schools`, `health_facilities` |
| Message | Critical public facilities concentrated in the same high-risk areas |

## Story 2: The hazard signal (rainfall)

| Item | Value |
|---|---|
| SAC chart | **Line** |
| Dataset | `sac_rainfall_timeseries.csv` |
| Dimensions | `date` (time) |
| Measures | `rainfall_mm` |
| Message | Seasonal peak (Jun–Sep monsoon) drives the flood season; wet years align with documented floods |

| Item | Value |
|---|---|
| SAC chart | **Column** (aggregated by `year`) |
| Dataset | `sac_rainfall_timeseries.csv` |
| Dimensions | `year` |
| Measures | `rainfall_mm` (sum), highlight `documented_flood_year` |
| Message | Documented Yangon flood years were wetter than average |

| Item | Value |
|---|---|
| SAC chart | **Bubble / Line** |
| Dataset | `sac_flood_events.csv` |
| Dimensions | `year` |
| Measures | `n_flood_events_myanmar` |
| Message | National flood frequency trend (DFO) |

## Story 3: Risk drivers (decomposition)

| Item | Value |
|---|---|
| SAC chart | **Radar** or **100% stacked column** |
| Dataset | `sac_risk_by_area.csv` |
| Dimensions | `township` (top 10 by `risk_100`) |
| Measures | `hazard`, `exposure`, `vulnerability` |
| Message | Highest-risk townships combine high hazard AND high exposure |

| Item | Value |
|---|---|
| SAC chart | **Scatter plot** |
| Dataset | `sac_risk_by_area.csv` (has both `elev_mean_m` and `risk_100`) |
| Axis X | `elev_mean_m` |
| Axis Y | `risk_100` |
| Color | `district` |
| Message | Low elevation correlates with higher risk (low-lying delta fringe) |

## Story 4: Actionable priorities

| Item | Value |
|---|---|
| SAC chart | **Table** + **Bar** |
| Dataset | `sac_risk_by_area.csv` |
| Dimensions | `township` |
| Measures | `risk_100`, `pop_est`, `schools`, `health_facilities` |
| Message | Priority list for early-warning and infrastructure hardening |

## SAC techniques to apply (from the official SAC Training Manual 2024)

### Input controls (live filtering)
Add a page **Input Control** on the Risk and Exposure pages, dimension =
`district` (East / North / South / West) and `risk_class`. Judges can then
filter to a district live. Resize the control so all options are visible.

### Ranking and exclusion
Use **Rank > township > Top N** (e.g., Top 10 risk) instead of plotting all 45
rows, and **Exclude** the "All/Total" aggregate members so charts stay honest.

### Calculated measures
Create SAC calculated measures where a ratio tells the story better:
- **Share of population in the top risk class** =
  `SUM([sac_risk_by_area.csv:pop_est] WHERE risk_class = 5) /
  SUM([sac_risk_by_area.csv:pop_est])` — 35.3%.
- **Facilities per 100k people** already exist in
  `sac_infrastructure_exposure.csv` (`schools_per_100k`, `health_per_100k`).

### Automatic forecast (clearly labeled as a model exercise)
On the rainfall **Time Series** tile, use **Add > Forecast > Automatic
Forecast**. Label the tile "illustrative model — not a prediction" so judges
cannot mistake the forecast for an observed claim.

### Smart Discovery (AI — key influencers of risk)
Use **Smart Discovery** on the risk model:
- **Target**: `risk_score` (or `risk_100`) — the measure to explain.
- **Entity**: `township` — the dimension whose variation is explained.
- **Expected output**: a Key Influencers page ranking which indicators
  (elevation, rainfall, population density, age shares) most associate with
  higher risk.
- **Honesty rule**: Smart Discovery output is **association, not causation** —
  state this in the tile footnote and in the defense
  (`outputs/reports/judge_questions.md`, Q28).

## Design rules

- Use a single consistent color ramp for `risk_class` (1 = green .. 5 = red).
- Never plot unsupported values; every chart's underlying dataset is in `data/sac/`.
- Add an "About / Methodology" text box referencing the risk formula:
  Risk = 0.4·Hazard + 0.35·Exposure + 0.25·Vulnerability.
