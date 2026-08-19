# SAC Build — Literal Step-by-Step (Team Zenith)

Target: build the 12 charts in SAP Analytics Cloud, save screenshots, and regenerate
`MYANMAR_TEAM_ZENITH.pdf` with the SAC charts swapped in.

**Credential reminder:** login saved in `D:\YOUTHsOrg\ADSC\.env` (gitignored).
Everything must be saved under **Public > Myanmar > Zenith** or it gets deleted.

---

## Part A — Login & create your folder (5 min)

1. Open **Google Chrome** (ideally an incognito window).
2. Go to: `https://aseandse.ap11.hcs.cloud.sap/`
3. Enter email `tharlunmmt207@gmail.com` and the password from `.env` (looks like
   `zamwow-xxxx-xxxxx`), then click **Log On**.
4. You should land on the SAP Analytics Cloud home screen.
5. Top-left **menu (hamburger)** → **Browse**.
6. Left panel: expand **Public** → click **Myanmar**.
7. Right panel: **Create Folder** → name it `Zenith` → **OK**.
   From now on, save ALL work inside `Public > Myanmar > Zenith`.

---

## Part B — Import the 8 data files as models (≈ 30 min)

Your data files are in `D:\YOUTHsOrg\ADSC\data\sac\`:

1. Click the **hamburger menu** → **Modeler** → **Model**.
2. Click **+ Start with data** (top-right).
3. **Select Source File** → browse to `data\sac\` → pick
   `sac_risk_by_area.csv` → **Upload**.
   - Check **"Use first row as column headers"** is ticked.
   - If import stalls, go to **Draft Sources** in the left panel and re-upload from there.
4. On the data-model page, **review the columns SAC auto-sorted**:
   - Text columns (`tship_code`, `township`, `district`) must be **Dimension**.
   - Numbers (`hazard`, `exposure`, `vulnerability`, `risk`, `risk_100`, `pop_est`,
     `elev_mean_m`, `schools`, `health_facilities`, `area_km2`) must be **Measure**.
   - `risk_class` must be a **segment/attribute**, NOT a measure — set its type to
     Dimension (it is a label 1–5).
   - To change: click a column → `…` (more) → **Convert to Measure** or **Convert to
     Dimension**.
5. Click **Save** → name it `FloodResilience_RiskByArea_MM` → save into
   `Public > Myanmar > Zenith`.
6. Repeat steps 2–5 for each file below (name suggestions in bold):

| CSV file | Model name | Fix these |
|---|---|---|
| `sac_risk_by_area.csv` | `RiskByArea_MM` | `risk_class` = dimension |
| `sac_risk_factors.csv` | `RiskFactors_MM` | all numeric = measure; `pcode` = dimension |
| `sac_rainfall_timeseries.csv` | `RainfallTS_MM` | set `date` as **Time** dimension; `rainfall_mm` measure |
| `sac_flood_events.csv` | `FloodEvents_MM` | `year` dimension; 2 count columns measures |
| `sac_flood_events_detail.csv` | `FloodEventsDetail_MM` | `start_date` as Time; `severity` dimension |
| `sac_yangon_flood_events.csv` | `YangonFloodYears_MM` | `year` dimension; text columns dimensions |
| `sac_population_exposure.csv` | `PopExposure_MM` | pop numbers measures |
| `sac_infrastructure_exposure.csv` | `InfraExposure_MM` | counts + per-100k measures |

7. (Maps only) Upload the map file: **Modeler → Model → Start with data → select source
   file** → choose `D:\YOUTHsOrg\ADSC\data\processed\yangon_township_risk.geojson` →
   upload → join to `RiskByArea_MM` on `tship_code` (or `pcode`). Save as
   `YangonRisk_Geo`.

---

## Part C — Create the story (10 min)

1. **Hamburger menu** → **Stories** → **Create New** → **Responsive**.
2. A dialog asks for the experience — choose **Classic Design Experience** (mandatory).
3. Click **Save** immediately → navigate to `Public > Myanmar > Zenith` → **Save**.
   Name: `FloodResilience_Story_Myanmar`.

---

## Part D — Build the 12 charts (≈ 60–90 min)

For each chart below: **Insert → Chart** (or **Insert → Map**), pick the model, set the
measures/dimensions, then style. Use **Duplicate** on an existing chart and swap the
measure to save time.

| # | PDF page | Chart to build | Model | Setting |
|---|---|---|---|---|
| 1 | 2 | Scatter/bar over years | `YangonFloodYears_MM` | x = `year`, y = count; add `has_dfo_event_myanmar` color |
| 2 | 4 | Map (choropleth) | `YangonRisk_Geo` | show township boundaries; color by `district` |
| 3 | 6 | Donut / pie | `RiskByArea_MM` | calculated measure = 0.4·hazard + 0.35·exposure + 0.25·vulnerability; or a fixed donut with 3 slices (40/35/25) |
| 4 | 7 | Bar + line combo | `RainfallTS_MM` | x = `month`/`month_name`, y = average `rainfall_mm` |
| 5 | 8 (top) | Choropleth risk map | `YangonRisk_Geo` | color = `risk_100`; **Range** colors green→red |
| 6 | 8 (bottom) | Scatter | `RiskByArea_MM` | x = `elev_mean_m`, y = `risk_100`, color = `risk_class` |
| 7 | 9 | Bar | `RiskByArea_MM` | x = `risk_class`, y = SUM `pop_est` |
| 8 | 10 | Bar (horizontal) | `RiskByArea_MM` | x = `township`, y = `risk_100`; **Rank > township > Top 10**; add stacked H/E/V decomposition |
| 9 | 11 | Histogram / column | `RiskByArea_MM` | x = `risk_100` binned; OR run **Smart Discovery** (see Part E) and screenshot that |
| 10 | 12 | KPI tiles + map | `RiskByArea_MM` | 3 KPI tiles: Top risk (58.3, Kayan), Class-5 pop (2.60 M), Facilities (2,498); plus small risk map |
| 11 | 14 | Stacked bar | `RiskByArea_MM` | x = `district`, stacked segments per `risk_class` (1–5) |
| 12 | 15 | Map highlighting class 5 | `YangonRisk_Geo` | color only `risk_class` = 5 townships, others grey |

### Input controls (do once)
1. **Insert → Input Control → Dropdown**.
2. Add **`district`** and **`risk_class`** filters to the top of the story so judges can
   filter live during the demo.

### Styling (do once)
1. Switch to **Styling mode** (top-right).
2. Set a consistent color ramp: risk class 1 = green … class 5 = red.
3. Reduce decimal places to 1–2 (click the number → format → decimals).
4. Add page headers matching the PDF page titles.

---

## Part E — Smart Discovery (page 11, optional but high-value)

1. Click the risk map chart → **Insert → Smart Discovery** (or right-click → Smart Discovery).
2. In the Smart Discovery panel: **Target** = `risk_100`, **Entity** = `township`.
3. Click **Run** → it finds key influencers of risk.
4. **Screenshot** the result panel (see Part F, name it `smart_discovery.png`).

---

## Part F — Export each chart as a screenshot (≈ 20 min)

1. Click a chart → **…** (chart menu) → **Export as Image** (or **Download as PNG**).
2. Save it to this folder (create it if needed):
   `D:\YOUTHsOrg\ADSC\outputs\storyboard\sac_exports\`
3. Use these EXACT filenames (the PDF generator auto-prefers these over the offline renders):

| # | Save as (in `sac_exports\`) |
|---|---|
| 1 | `flood_years.png` |
| 2 | `region_map.png` |
| 3 | `risk_formula.png` |
| 4 | `climatology.png` |
| 5 | `risk_map.png` |
| 6 | `elev_vs_risk.png` |
| 7 | `pop_by_class.png` |
| 8 | `top10_decomp.png` |
| 9 | `risk_hist.png` (or `smart_discovery.png` — same name will be used for page 11) |
| 10 | `solution_kpis.png` |
| 11 | `district_classes.png` |
| 12 | `class5_map.png` |

4. Keep each PNG ≤ 2 MB (SAC exports are usually well under this). If one is larger,
   reduce the chart resolution or re-screenshot at smaller zoom.

> Note for #9: the generator looks for `risk_hist.png` first. If you only have
> `smart_discovery.png`, rename it to `risk_hist.png` (page 11 uses that slot).

---

## Part G — Regenerate the PDF with SAC charts (2 min)

1. Open a terminal in `D:\YOUTHsOrg\ADSC`.
2. Run:
   ```
   .venv\Scripts\python.exe tools\build_storyboard_pdf.py
   ```
3. The generator prints `PDF written: ...\MYANMAR_TEAM_ZENITH.pdf`.
   - If it used a SAC export, the chart's top-right tag reads **SAC EXPORT**.
   - If a chart is still missing from `sac_exports`, it falls back to the offline render
     and the tag reads **OFFLINE RENDER — replace with SAC export**.
4. Check final size: `outputs\storyboard\MYANMAR_TEAM_ZENITH.pdf` must stay ≤ 20 MB
   (currently ~0.25 MB, so you have huge headroom).

---

## Part H — Export the storyboard PDF from SAC (if required as the deliverable)

The competition also allows exporting the SAC story itself as PDF:
1. Open your story → **File → Export → PDF**.
2. Choose **Landscape**, A4 or A3, all pages.
3. Verify: ≤ 20 MB, ≤ 15 pages + references, images ≤ 2 MB each.
4. Save the exported file as **`MYANMAR_TEAM_ZENITH.pdf`**.
5. Self-check the cover has all 6 required fields, and run through
   `outputs/reports/competition_scorecard.md` once more.

---

## Quick checklist before submission

- [ ] All 12 charts show **SAC EXPORT** tag in the regenerated PDF (or the SAC-exported PDF).
- [ ] Cover: title / Team Zenith / UIT / Myanmar / SDG 11+13 / description all present.
- [ ] File named `MYANMAR_TEAM_ZENITH.pdf`, ≤ 20 MB, landscape, ≤ 15 pages + references.
- [ ] Prototype screenshots (if any) captioned "prototype".
- [ ] Run `docs/delivery_script_5min.md` timing check with the real SAC demo.