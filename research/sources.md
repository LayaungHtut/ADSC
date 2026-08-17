# Data Sources — Phase 1 Discovery

This document lists candidate data sources for FloodResilience ASEAN. The full machine-readable catalog is in `data/source_catalog.csv`. Sources marked `VERIFIED` were checked during Phase 1 (2026-08); `TO VERIFY` means the URL/licence must be confirmed before download in Phase 2.

## Core datasets (global, free)

### Rainfall / climate
- **GPM IMERG** (`VERIFIED`) — NASA GES DISC. Half-hourly/daily/monthly precipitation at 0.1° (~11 km), 2000–present. Monthly final product has ~2.5-month latency; daily final has ~2.5-day latency. Requires free NASA Earthdata account. GeoTIFF available via PPS server.
  - https://disc.gsfc.nasa.gov/datasets/GPM_3IMERGM_07/summary
- **CHIRPS** (`VERIFIED`) — UC Santa Barbara Climate Hazards Center. Daily/monthly precipitation 0.05° (~5 km), 1981–present, open access. Good complement to IMERG at finer resolution.
  - https://www.chc.ucsb.edu/data/chirps

### Flood events
- **Global Flood Database (GFD) v1** (`VERIFIED`) — Cloud to Street + Dartmouth Flood Observatory. 913 satellite-mapped flood events (2000–2018), 250 m, includes population exposed per event (GHSL 2000/2015). Free; access via portal or Google Earth Engine (`GLOBAL_FLOOD_DB/MODIS_EVENTS/V1`).
  - https://global-flood-database.cloudtostreet.ai/ and https://developers.google.com/earth-engine/datasets/catalog/GLOBAL_FLOOD_DB_MODIS_EVENTS_V1
- **Dartmouth Flood Observatory (DFO) Flood Archive** (`VERIFIED`) — long-running event catalogue (1985–present), polygons + severity. Good for building a flood-event time series.
  - https://floodobservatory.colorado.edu/

### Elevation
- **Copernicus DEM GLO-30** (`VERIFIED`) — ESA/Copernicus. 30 m DSM (TanDEM-X, 2011–2015), free & open licence. Download via AWS Open Data or OpenTopography.
  - https://registry.opendata.aws/copernicus-dem/ ; https://portal.opentopography.org/raster?opentopoID=OTSDEM.032021.4326.3
- SRTM v4 (90 m) as an alternative/baseline.

### Land cover
- **ESA WorldCover** (`VERIFIED`) — 10 m land cover 2020/2021, 11 classes, CC-BY 4.0. https://esa-worldcover.org/en

### Population
- **WorldPop** (`VERIFIED`) — 100 m (~3 arcsec) population counts per grid cell, 2000–2020 (and 2015–2030 releases), CC-BY 4.0. https://hub.worldpop.org/
- **GHSL** (`VERIFIED` existence) — JRC. Population + built-up area at 30/100 m, decadal 1975–2030. https://ghsl.jrc.ec.europa.eu/

### Infrastructure
- **OpenStreetMap** (`VERIFIED`) — roads, buildings, hospitals, schools, shelters. ODbL. Download via Geofabrik/Overpass API. Completeness is city-dependent.

### Water bodies
- **JRC Global Surface Water** (`VERIFIED` existence) — surface water occurrence/seasonality, 30 m, 1984–2021. https://global-surface-water.appspot.com/

## National / local sources

- **Jakarta Open Data Portal** (`VERIFIED` existence) — data.jakarta.go.id. Local flood reports, population, facilities. Strong for the primary location.
- **BMKG Indonesia** (`VERIFIED` existence) — dataonline.bmkg.go.id, station rainfall.
- **PAGASA Philippines** (`VERIFIED` existence) — pagasa.dost.gov.ph.
- **Thai Meteorological Dept** (`VERIFIED` existence) — tmd.go.th.
- **Malaysia DID / MET Malaysia** (`VERIFIED` existence) — met.gov.my.
- **Vietnam GSO / MONRE** (`VERIFIED` existence) — gso.gov.vn.
- **Myanmar** — DMH (Department of Meteorology and Hydrology) exists but open-data availability is limited (`TO VERIFY`); OSM coverage of Yangon moderate.

## International / regional

- **HDX (OCHA)** (`VERIFIED`) — humanitarian data exchange, flood events, boundaries. https://data.humdata.org/
- **WRI Aqueduct** (`VERIFIED` existence) — modelled flood risk. https://www.wri.org/aqueduct
- **ASEANstats / ASEAN DataM** (`VERIFIED` existence) — https://data.aseanstats.org/
- **GDACS** (`VERIFIED` existence) — disaster alerts. https://www.gdacs.org/

## Licensing summary

- GPM IMERG, SRTM, USGS: US Government work / public domain.
- CHIRPS, WorldPop (base), ESA WorldCover, GHSL, GFD: open licences (CC-BY 4.0 or similar) — attribution required.
- OSM: ODbL — share-alike applies to derived data.
- Copernicus DEM: free & open Copernicus licence (attribution).
- National portals: generally open government data, terms vary.

**Action for Phase 2:** verify each URL resolves, record exact licence terms, and store download provenance in `data/raw/` plus a `PROVENANCE.md`.