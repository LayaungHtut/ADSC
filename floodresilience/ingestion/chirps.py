"""Ingestion: CHIRPS v2.0 monthly precipitation (Indonesia subset).

Source: Climate Hazards Center, UC Santa Barbara.
URL base: https://data.chc.ucsb.edu/products/CHIRPS-2.0/indonesia_monthly/bils/

Each monthly archive contains a BIL + HDR pair covering Indonesia
(0.05 deg, EPSG:4326). We download all months, extract, and clip each to
the Jakarta analysis bounding box, saving small GeoTIFFs under
`data/intermediate/rainfall/chirps/`. Provenance is recorded in
`data/raw/PROVENANCE.csv`.

Filenames changed convention in Nov 2016:
  1981-01 .. 2016-10  -> chirps-v2.0_YYYYMM.tar.gz
  2016-11 .. present  -> v2p0chirpsYYYYMM.tar.gz
"""

from __future__ import annotations

import io
import tarfile
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import date
from pathlib import Path

import rasterio
from rasterio.windows import from_bounds

from floodresilience.config import DATA_RAW, DATA_INTERMEDIATE, JAKARTA_BBOX
from floodresilience.provenance import record_download

CHIRPS_BASE = "https://data.chc.ucsb.edu/products/CHIRPS-2.0/indonesia_monthly/bils"
CHIRPS_START_YEAR = 1981
CHIRPS_END_YEAR = 2026  # inclusive; product is continuous to the present

OUT_DIR = DATA_INTERMEDIATE / "rainfall" / "chirps"
RAW_DIR = DATA_RAW / "rainfall" / "chirps"


def archive_name(year: int, month: int) -> str:
    if (year, month) <= (2016, 10):
        return f"chirps-v2.0_{year:04d}{month:02d}.tar.gz"
    return f"v2p0chirps{year:04d}{month:02d}.tar.gz"


def member_names(year: int, month: int) -> tuple[str, str]:
    stem = f"chirps-v2.0_{year:04d}{month:02d}" if (year, month) <= (2016, 10) else f"v2p0chirps{year:04d}{month:02d}"
    return f"{stem}.bil", f"{stem}.hdr"


def month_range() -> list[tuple[int, int]]:
    """Yield (year, month) tuples from start through the current month."""
    today = date.today()
    end = (CHIRPS_END_YEAR, today.month) if today.year >= CHIRPS_END_YEAR else (today.year, today.month)
    out: list[tuple[int, int]] = []
    for year in range(CHIRPS_START_YEAR, today.year + 1):
        for month in range(1, 13):
            if (year, month) <= end:
                out.append((year, month))
    return out


def fetch_month(year: int, month: int, out_dir: Path = OUT_DIR) -> Path | None:
    """Download, extract and clip one month. Returns output GeoTIFF path or None."""
    name = archive_name(year, month)
    bil_name, _hdr_name = member_names(year, month)
    url = f"{CHIRPS_BASE}/{name}"

    out_tif = out_dir / f"chirps_{year:04d}{month:02d}.tif"
    if out_tif.exists():
        return out_tif

    RAW_DIR.mkdir(parents=True, exist_ok=True)
    out_dir.mkdir(parents=True, exist_ok=True)

    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=90) as resp:
            raw = resp.read()
    except urllib.error.HTTPError as exc:  # noqa: F821
        print(f"  HTTP {exc.code} {name} — skipping")
        return None

    with tarfile.open(fileobj=io.BytesIO(raw)) as tar:
        members = tar.getnames()
        if bil_name not in members:
            print(f"  unexpected members {members} for {name} — skipping")
            return None
        local_bil = RAW_DIR / bil_name
        hdr_name = next((m for m in members if m.endswith(".hdr")), None)
        if hdr_name is None:
            print(f"  no .hdr in {name} — skipping")
            return None
        local_hdr = RAW_DIR / hdr_name
        with open(local_bil, "wb") as fh:
            fh.write(tar.extractfile(bil_name).read())
        with open(local_hdr, "wb") as fh:
            fh.write(tar.extractfile(hdr_name).read())

    # Clip to Jakarta bounding box.
    try:
        with rasterio.open(local_bil) as src:
            window = from_bounds(*JAKARTA_BBOX, transform=src.transform)
            window = window.intersection(src.window(*src.bounds))
            profile = src.profile.copy()
            profile.update(driver="GTiff", height=window.height, width=window.width, crs="EPSG:4326")
            data = src.read(1, window=window)
            transform = src.window_transform(window)
        with rasterio.open(out_tif, "w", **profile) as dst:
            dst.write(data, 1)
            dst.transform = transform
    finally:
        local_bil.unlink(missing_ok=True)
        if "local_hdr" in locals():
            local_hdr.unlink(missing_ok=True)
    record_download(
        out_tif,
        url,
        license_note="CHIRPS is public domain for non-commercial use; cite Funk et al. 2015.",
        notes="Clipped from CHIRPS v2.0 Indonesia monthly BIL to Jakarta bbox.",
    )
    return out_tif


def download_all(start_year: int = CHIRPS_START_YEAR, workers: int = 8) -> list[Path]:
    """Download all months in range, in parallel. Returns list of output paths."""
    pairs = month_range()
    results: list[Path] = []
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futs = {pool.submit(fetch_month, y, m): (y, m) for (y, m) in pairs}
        for fut in as_completed(futs):
            res = fut.result()
            if res is not None:
                results.append(res)
    return sorted(results)


if __name__ == "__main__":
    done = download_all()
    print(f"downloaded {len(done)} monthly CHIRPS tiles for Jakarta")