"""FloodResilience ASEAN — shared configuration.

All paths, coordinate bounds and constants live here so that every module
uses exactly the same geographic frame and avoids magic numbers.
"""

from __future__ import annotations

import os
from pathlib import Path

# ---------------------------------------------------------------------------
# Project root: the directory containing this package is the repo root.
# ---------------------------------------------------------------------------
ROOT = Path(__file__).resolve().parents[1]

DATA_RAW = ROOT / "data" / "raw"
DATA_INTERMEDIATE = ROOT / "data" / "intermediate"
DATA_PROCESSED = ROOT / "data" / "processed"
DATA_SAC = ROOT / "data" / "sac"

OUTPUTS = ROOT / "outputs"
OUTPUT_CHARTS = OUTPUTS / "charts"
OUTPUT_MAPS = OUTPUTS / "maps"
OUTPUT_TABLES = OUTPUTS / "tables"
OUTPUT_REPORTS = OUTPUTS / "reports"

MODELS_DIR = ROOT / "models"
DOCS = ROOT / "docs"
RESEARCH = ROOT / "research"

for _d in (
    DATA_RAW,
    DATA_INTERMEDIATE,
    DATA_PROCESSED,
    DATA_SAC,
    OUTPUT_CHARTS,
    OUTPUT_MAPS,
    OUTPUT_TABLES,
    OUTPUT_REPORTS,
    MODELS_DIR,
):
    _d.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------------------
# Geographic frame
# ---------------------------------------------------------------------------
# Analysis location: Yangon Region, Myanmar. WGS84 lon/lat bounds padded
# beyond the region so raster zonal statistics and neighbourhood analysis
# still capture boundary context.
YANGON_BBOX = (93.3, 14.0, 96.9, 17.8)  # (west, south, east, north)
YANGON_CENTER = (96.1561, 16.8713)

# Primary source CRS for the raw geospatial files.
CRS_WGS84 = "EPSG:4326"
# Local projected CRS for distances/areas (Yangon lies in UTM zone 47N).
CRS_UTM = "EPSG:32647"
CRS_WEB = "EPSG:3857"  # for interactive map tiles only

# ---------------------------------------------------------------------------
# Source endpoints (kept here so they can be cited and re-verified)
# ---------------------------------------------------------------------------
CHIRPS_COG_BASE = "https://data.chc.ucsb.edu/products/CHIRPS-2.0/global_monthly/cogs"
CHIRPS_START_YEAR = 1981
CHIRPS_END_YEAR = 2026  # inclusive; product is continuous to the present

# Earthdata / GPM (requires login — not used by automated pipeline yet)
GPM_DATASET_URL = "https://disc.gsfc.nasa.gov/datasets/GPM_3IMERGM_07/summary"

# Copernicus DEM 30 m COG tiles covering the Yangon Region bbox (lat 14-18 N,
# lon 93-97 E). Only the tiles actually downloaded under data/raw/dem/ are used
# by the pipeline; the full 1x1 degree set is listed here for documentation.
DEM_TILES = {
    f"lat{l:02d}-{l+1:02d}Nlon{e:03d}-{e+1:03d}E": (
        f"https://s3.eu-central-1.amazonaws.com/copernicus-dem-30m/"
        f"Copernicus_DSM_COG_10_N{l:02d}_00_E{e:03d}_00_DEM/Copernicus_DSM_COG_10_N{l:02d}_00_E{e:03d}_00_DEM.tif"
    )
    for l in range(14, 18)
    for e in range(93, 97)
}

# HDX / geoBoundaries (Myanmar)
GEOBOUNDARIES_ADM1 = "https://github.com/wmgeolab/geoBoundaries/raw/9469f09/releaseData/gbOpen/MMR/ADM1/geoBoundaries-MMR-ADM1_simplified.geojson"
# Myanmar townships are ADM3 (Yangon Region has 45 townships).
GEOBOUNDARIES_ADM3 = "https://github.com/wmgeolab/geoBoundaries/raw/9469f09/releaseData/gbOpen/MMR/ADM3/geoBoundaries-MMR-ADM3_simplified.geojson"
HDX_API = "https://data.humdata.org/api/3/action/package_show?id="

# 2014 Myanmar Population & Housing Census, township level (DoP / MIMU).
# Open Development Myanmar, dataset "2014 Myanmar Census: Household and
# Population Data for Townships". Source: Department of Population, Ministry of
# Labour, Immigration and Population, Myanmar.
CENSUS_TOWNSHIP_URL = (
    "https://data.opendevelopmentmekong.net/dataset/be760472-6224-4d73-b309-"
    "335d732cab93/resource/702f8d11-8301-4661-b7b8-030501a90626/download/"
    "householdpopulationbaseddatasetmimutownshipsabbreviated.csv"
)

# Documented major Yangon flood years (from published records, within the
# CHIRPS 1981+ record). Sources:
#   - PIAHS 386 (2024) RRI flood study: severe Yangon floods 1988, 1991, 1997,
#     2002, 2004, 2007, 2014.
#   - Sritarapipat (2017) urban-growth study: Yangon floods 2008, 2010, 2013,
#     2014, 2015.
#   - OCHA 2017 monsoon update (Yangon among flooded regions).
#   - UNOSAT Sentinel-1 mapping, 2 Aug 2020 (Yangon Region surface water).
# These are CONTEXT flags only — never used as per-township labels.
DOCUMENTED_YANGON_FLOOD_YEARS = [1988, 1991, 1997, 2002, 2004, 2007, 2008, 2010, 2013, 2014, 2015, 2017, 2019, 2020]

# ---------------------------------------------------------------------------
# Misc
# ---------------------------------------------------------------------------
# Where to store any user-provided secrets (Earthdata, etc.). See .env.example.
ENV_FILE = ROOT / ".env"


def load_dotenv() -> None:
    """Load .env if present (keys: EARTHDATA_USERNAME, EARTHDATA_PASSWORD, ...)."""
    try:
        from dotenv import load_dotenv as _load

        _load(ENV_FILE)
    except ImportError:  # pragma: no cover
        pass


def env(key: str, default: str | None = None) -> str | None:
    load_dotenv()
    return os.getenv(key, default)


def ensure_dirs() -> None:
    for _d in (DATA_RAW, DATA_INTERMEDIATE, DATA_PROCESSED, DATA_SAC, OUTPUT_CHARTS, OUTPUT_MAPS, OUTPUT_TABLES, OUTPUT_REPORTS):
        _d.mkdir(parents=True, exist_ok=True)