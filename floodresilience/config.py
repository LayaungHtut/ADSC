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
# Analysis location: DKI Jakarta, Indonesia (chosen in Phase 1 on data strength).
# WGS84 lon/lat bounds. Padded beyond the province so raster zonal statistics
# and neighbourhood analysis still capture boundary context.
JAKARTA_BBOX = (106.55, -6.50, 107.10, -5.95)  # (west, south, east, north)
JAKARTA_CENTER = (106.8456, -6.2088)

# Primary source CRS for the raw geospatial files.
CRS_WGS84 = "EPSG:4326"
# Local projected CRS for distances/areas (Jakarta lies in UTM zone 48S).
CRS_UTM = "EPSG:32748"
CRS_WEB = "EPSG:3857"  # for interactive map tiles only

# ---------------------------------------------------------------------------
# Source endpoints (kept here so they can be cited and re-verified)
# ---------------------------------------------------------------------------
CHIRPS_COG_BASE = "https://data.chc.ucsb.edu/products/CHIRPS-2.0/global_monthly/cogs"
CHIRPS_START_YEAR = 1981
CHIRPS_END_YEAR = 2024  # inclusive; product continues

# Earthdata / GPM (requires login — not used by automated pipeline yet)
GPM_DATASET_URL = "https://disc.gsfc.nasa.gov/datasets/GPM_3IMERGM_07/summary"

# Copernicus DEM 30 m COG tiles covering Jakarta (S06E106, S06E107 and the
# mainland band S07E106, S07E107 — Jakarta city centre lies south of -6.0).
DEM_TILES = {
    "S06E106": "https://s3.eu-central-1.amazonaws.com/copernicus-dem-30m/Copernicus_DSM_COG_10_S06_00_E106_00_DEM/Copernicus_DSM_COG_10_S06_00_E106_00_DEM.tif",
    "S06E107": "https://s3.eu-central-1.amazonaws.com/copernicus-dem-30m/Copernicus_DSM_COG_10_S06_00_E107_00_DEM/Copernicus_DSM_COG_10_S06_00_E107_00_DEM.tif",
    "S07E106": "https://s3.eu-central-1.amazonaws.com/copernicus-dem-30m/Copernicus_DSM_COG_10_S07_00_E106_00_DEM/Copernicus_DSM_COG_10_S07_00_E106_00_DEM.tif",
    "S07E107": "https://s3.eu-central-1.amazonaws.com/copernicus-dem-30m/Copernicus_DSM_COG_10_S07_00_E107_00_DEM/Copernicus_DSM_COG_10_S07_00_E107_00_DEM.tif",
}

# HDX / geoBoundaries
GEOBOUNDARIES_ADM1 = "https://github.com/wmgeolab/geoBoundaries/raw/9469f09/releaseData/gbOpen/IDN/ADM1/geoBoundaries-IDN-ADM1_simplified.geojson"
GEOBOUNDARIES_ADM2 = "https://github.com/wmgeolab/geoBoundaries/raw/9469f09/releaseData/gbOpen/IDN/ADM2/geoBoundaries-IDN-ADM2_simplified.geojson"
HDX_API = "https://data.humdata.org/api/3/action/package_show?id="

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