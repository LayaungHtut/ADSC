# ASEAN Scalability — FloodResilience ASEAN

How the Jakarta proof-of-concept becomes a replicable ASEAN framework.

Status: design document. No data is fabricated; the Jakarta figures cited here
are from the actual processed datasets (see `data/processed/` and
`outputs/reports/key_insights.md`).

---

## 1. Design principle

The project is built as a **framework, not a one-city application**. Every
analytical stage is data-driven and parameterised by city:

```
city config  ->  data pipeline  ->  risk model  ->  SAC-ready datasets  ->  decision tool
```

For Jakarta the parameters are fixed (bbox, admin boundaries, thresholds).
For another ASEAN city, only the configuration layer changes — the code path is
identical. This is what makes the approach scalable.

## 2. The Jakarta recipe (what we validated)

| Layer | Jakarta implementation | Source family |
|---|---|---|
| Boundaries | 42 urban kecamatan (GeoBoundaries / Alf-Anas) | local + global |
| Rainfall | CHIRPS v2.0 monthly, 1981-2026, bbox zonal means | CHIRPS (global) |
| Elevation | Copernicus DEM GLO-30 zonal stats | Copernicus (global) |
| Population | Kontur H3 area-weighted; WorldPop ADM2 age shares | Kontur / WorldPop (global) |
| Infrastructure | HDX school + health facility point counts | HDX / OSM |
| Recent rainfall hazard | World Bank / GFDRR subnational indices | WB / GFDRR |
| Historical flood context | Dartmouth Flood Observatory event archive | DFO |

Every one of these datasets is **global or ASEAN-wide**, meaning the same
acquisition pipeline works for Manila, Bangkok, HCMC, Kuala Lumpur, Yangon or
Phnom Penh.

## 3. Common vs local layers

### Common layers (already validated for Jakarta, portable as-is)

- Climate: CHIRPS / GPM IMERG rainfall (global).
- Geography: Copernicus DEM, ESA WorldCover, JRC water (global).
- Population: WorldPop / GHSL / Kontur (global, model-based).
- Infrastructure: OSM / HDX facility data (global, quality varies).
- Flood history: Global Flood Database (2000-2018) + DFO (1985-present) (global).

### Local layers (must be provided per country)

- National administrative boundaries and official area codes.
- National meteorological agency gauge records (BMKG, PAGASA, TMD, MET Malaysia,
  etc.) for validation.
- National census totals for reconciling modelled population.
- National disaster-management records for flood-event validation.
- Local vulnerability/socioeconomic indicators (poverty, tenure, informal
  settlement extent) where open data permits.
- Local emergency protocols and critical-facility registers.

### Data-availability challenges per country

| Layer | Strength | Weakness |
|---|---|---|
| Indonesia (Jakarta) | open data portal, BMKG, strong OSM | district poverty data restricted |
| Philippines (Manila) | PAGASA, strong OSM, GFD events | data spread across agencies |
| Vietnam (HCMC) | strong research base | national open data fragmented |
| Thailand (Bangkok) | TMD, DID records | routine flood extents less standardised |
| Malaysia (KL) | DID open data | mostly flash floods, thinner extent archive |
| Myanmar (Yangon) | GFD + DFO capture major events | national open data very limited post-2021 |
| Cambodia (Phnom Penh) | Mekong records | sparse national datasets |

The global raster layer set is the **equaliser**: it gives every city a common
baseline. Local layers then sharpen validity, never replace the baseline.

## 4. Replication procedure for a new city

1. Define a city config (`bbox`, admin boundary source, analysis-unit level).
2. Run the shared acquisition script for rainfall / DEM / population /
   infrastructure / flood events.
3. Run zonal statistics (same code as Jakarta).
4. Run the risk index with the documented weights; run the sensitivity analysis.
5. Validate against local records (rainfall gauges, documented flood years).
6. Export SAC-ready CSVs; load into SAC; rebuild the storyboard with local
   figures.
7. Re-generate the SvelteKit prototype data bundle; deploy.

Estimated code reuse: the Python package (`floodresilience/`) is city-agnostic
except for the config module and boundary source. The SvelteKit app renders
whatever `src/lib/data/*.json` contains, so the same UI serves any city.

## 5. Scaling dimensions

- **Geographic scaling**: one city → many cities → national → regional.
- **Analytic scaling**: from kecamatan-level risk to neighbourhood grids where
  finer hazard rasters (GFD, GPM) support it.
- **Temporal scaling**: from static risk maps toward near-real-time rainfall
  screening using CHIRPS/GPM streaming (clearly labelled, not a forecast).
- **Institutional scaling**: from a student prototype toward integration with
  national disaster-management agencies and city governments.

## 6. What does NOT scale automatically (honesty)

- Vulnerability proxies are kota-level for Jakarta and will differ per country.
- OSM completeness varies; facility counts need a coverage audit per city.
- A single flood-risk formula cannot capture local hydrology (tides, drainage,
  subsidence) without local calibration.
- The ML experiment (see `outputs/reports/model_evaluation.md`) is descriptive
  for Jakarta; it must be re-run and re-validated for any other city.

## 7. ASEAN policy alignment

- SDG 11.5 (disasters), SDG 11.b (resilient cities), SDG 13.1 (climate
  resilience) are the anchors.
- The framework aligns with the ASEAN Agreement on Disaster Management and
  Emergency Response (AADMER) and the ASEAN Socio-Cultural Community (ASCC)
  Blueprint 2025/2030 resilience goals.
- A shared, open-data methodology across member states supports comparable risk
  assessments — a contribution beyond any single national system.

---

Every claim above is either a statement of the implemented codebase or labelled
as a design proposal. Nothing here asserts validated results for cities other
than Jakarta.
