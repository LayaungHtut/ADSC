"""FloodResilience ASEAN — Python data & analytics package.

Layers (mirroring the master prompt `src/` layout):
    ingestion      — download / read raw sources
    cleaning       — automated data-quality validation & reporting
    gis            — raster/vector helpers, zonal statistics
    features       — feature engineering incl. the flood risk index
    analysis       — rainfall & exposure analysis
    export         — SAC-ready dataset writers
"""

from floodresilience.config import ensure_dirs

__version__ = "0.1.0"

ensure_dirs()