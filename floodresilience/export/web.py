"""Export compact JSON datasets for the SvelteKit prototype.

Writes into `src/lib/data/`:
  - risk.json        : kecamatan risk + geometry (GeoJSON, compact)
  - features.json    : full indicator table (array of objects)
  - rainfall.json    : monthly rainfall series (year, month, rainfall_mm, flood flag)
  - kota.json        : kota-level summary
"""

from __future__ import annotations

import json
from pathlib import Path

import geopandas as gpd
import pandas as pd

from floodresilience.config import DATA_PROCESSED, OUTPUT_TABLES, DATA_INTERMEDIATE

WEB_DATA = Path("src/lib/data")


def _load_rainfall() -> pd.DataFrame:
    rows = []
    import glob

    import numpy as np
    import rasterio

    from floodresilience.config import DATA_INTERMEDIATE

    files = sorted(glob.glob(str(DATA_INTERMEDIATE / "rainfall" / "chirps" / "chirps_*.tif")))
    for f in files:
        yyyymm = Path(f).stem.split("_")[1]
        with rasterio.open(f) as ds:
            a = ds.read(1).astype("float64")
        a[a < 0] = np.nan
        rows.append({"year": int(yyyymm[:4]), "month": int(yyyymm[4:6]), "rainfall_mm": round(float(np.nanmean(a)), 1)})
    return pd.DataFrame(rows)


def main() -> None:
    WEB_DATA.mkdir(parents=True, exist_ok=True)

    gdf = gpd.read_file(DATA_PROCESSED / "jakarta_kecamatan_risk.geojson")
    gdf = gdf.to_crs(4326)
    gdf["geometry"] = gdf.geometry.simplify(tolerance=0.0001, preserve_topology=True)
    geojson = json.loads(gdf.to_json())
    (WEB_DATA / "risk.json").write_text(json.dumps(geojson, separators=(",", ":")), encoding="utf-8")

    features = pd.read_csv(DATA_PROCESSED / "jakarta_kecamatan_features.csv")
    features = features.round(3)
    (WEB_DATA / "features.json").write_text(features.to_json(orient="records"), encoding="utf-8")

    risk_summary = gdf.drop(columns="geometry")
    risk_summary = risk_summary.round(3)
    (WEB_DATA / "risk-summary.json").write_text(risk_summary.to_json(orient="records"), encoding="utf-8")

    rain = _load_rainfall()
    rain = rain[rain["rainfall_mm"].notna()]
    rain["flood_year"] = rain["year"].isin([2002, 2007, 2013, 2020, 2025]).astype(int)
    (WEB_DATA / "rainfall.json").write_text(rain.to_json(orient="records"), encoding="utf-8")

    kota = features.groupby("kota").agg(
        n_kecamatan=("kec_code", "count"),
        pop_est=("pop_est", "sum"),
        schools=("schools", "sum"),
        health_facilities=("health_facilities", "sum"),
    ).reset_index()
    kota = kota.round(1)
    (WEB_DATA / "kota.json").write_text(kota.to_json(orient="records"), encoding="utf-8")

    for f in sorted(WEB_DATA.glob("*.json")):
        print(f.name, f.stat().st_size // 1024, "KB")


if __name__ == "__main__":
    main()