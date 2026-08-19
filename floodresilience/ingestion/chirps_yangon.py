"""Ingestion: CHIRPS v2.0 monthly precipitation for Yangon (Myanmar).

Source: Climate Hazards Center, UC Santa Barbara.
URL base: https://data.chc.ucsb.edu/products/CHIRPS-2.0/global_monthly/cogs/

Myanmar has no country subset, so we window-read the global monthly COGs
(Cloud-Optimized GeoTIFFs) for the Yangon bounding box and write small
clipped GeoTIFFs under `data/intermediate/rainfall/chirps_yangon/`.

Note: the CHC HTTP mirror returns 403 for automated clients, so the COGs are
fetched over FTP (the CHC-preferred method) and window-read from the local
temporary copy. HTTPS windowed reads are kept as a fallback for environments
where the HTTP mirror is reachable.
"""

from __future__ import annotations

import ftplib
import tempfile
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import date
from pathlib import Path

import numpy as np
import rasterio
from rasterio.windows import from_bounds

from floodresilience.config import DATA_INTERMEDIATE, YANGON_BBOX
from floodresilience.provenance import record_download

CHIRPS_COG_BASE = "https://data.chc.ucsb.edu/products/CHIRPS-2.0/global_monthly/cogs"
CHIRPS_FTP_HOST = "ftp.chc.ucsb.edu"
CHIRPS_FTP_DIR = "/pub/org/chc/products/CHIRPS-2.0/global_monthly/cogs"
CHIRPS_START_YEAR = 1981
CHIRPS_END_YEAR = 2026  # inclusive; product is continuous to the present
CHIRPS_MAX_ATTEMPTS = 4
CHIRPS_RETRY_BACKOFF = 2.0  # seconds, multiplied per attempt

OUT_DIR = DATA_INTERMEDIATE / "rainfall" / "chirps_yangon"


def cog_url(year: int, month: int) -> str:
    return f"{CHIRPS_COG_BASE}/chirps-v2.0.{year:04d}.{month:02d}.cog"


def _cog_ftp_url(year: int, month: int) -> str:
    return f"ftp://{CHIRPS_FTP_HOST}{CHIRPS_FTP_DIR}/chirps-v2.0.{year:04d}.{month:02d}.cog"


def _download_ftp(remote: str, dest: Path) -> None:
    with ftplib.FTP(CHIRPS_FTP_HOST) as ftp:
        ftp.login()
        with open(dest, "wb") as fh:
            ftp.retrbinary(f"RETR {remote}", fh.write)


def _clip_cog(src_path: Path) -> tuple[np.ndarray, object, dict]:
    """Window-read one local COG clipped to the Yangon bbox."""
    with rasterio.open(src_path) as src:
        window = from_bounds(*YANGON_BBOX, transform=src.transform)
        window = window.intersection(src.window(*src.bounds))
        profile = src.profile.copy()
        profile.update(driver="GTiff", height=window.height, width=window.width, crs="EPSG:4326")
        data = src.read(1, window=window)
        transform = src.window_transform(window)
    return data, transform, profile


def _read_https(year: int, month: int) -> tuple[np.ndarray, object, dict]:
    url = cog_url(year, month)
    with rasterio.Env(CPL_TIMEOUT=30, CPL_CONNECT_TIMEOUT=30):
        with rasterio.open(url) as src:
            window = from_bounds(*YANGON_BBOX, transform=src.transform)
            window = window.intersection(src.window(*src.bounds))
            profile = src.profile.copy()
            profile.update(driver="GTiff", height=window.height, width=window.width, crs="EPSG:4326")
            data = src.read(1, window=window)
            transform = src.window_transform(window)
    return data, transform, profile


def _read_ftp(year: int, month: int) -> tuple[np.ndarray, object, dict]:
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td) / f"chirps-v2.0.{year:04d}.{month:02d}.cog"
        _download_ftp(f"{CHIRPS_FTP_DIR}/chirps-v2.0.{year:04d}.{month:02d}.cog", tmp)
        return _clip_cog(tmp)


def _window_read(year: int, month: int) -> tuple[np.ndarray, object, dict, str]:
    """Return (data, transform, profile, source_url), trying HTTPS then FTP."""
    try:
        return (*_read_https(year, month), cog_url(year, month))
    except Exception:
        return (*_read_ftp(year, month), _cog_ftp_url(year, month))


def month_range() -> list[tuple[int, int]]:
    today = date.today()
    end = (CHIRPS_END_YEAR, today.month) if today.year >= CHIRPS_END_YEAR else (today.year, today.month)
    out: list[tuple[int, int]] = []
    for year in range(CHIRPS_START_YEAR, today.year + 1):
        for month in range(1, 13):
            if (year, month) <= end:
                out.append((year, month))
    return out


def fetch_month(year: int, month: int, out_dir: Path = OUT_DIR) -> Path | None:
    """Read one global COG clipped to the Yangon bbox. Returns output path or None."""
    out_tif = out_dir / f"chirps_{year:04d}{month:02d}.tif"
    if out_tif.exists():
        return out_tif

    last_exc: Exception | None = None
    for attempt in range(1, CHIRPS_MAX_ATTEMPTS + 1):
        try:
            data, transform, profile, source_url = _window_read(year, month)
            if data is None or data.size == 0:
                return None
            out_dir.mkdir(parents=True, exist_ok=True)
            with rasterio.open(out_tif, "w", **profile) as dst:
                dst.write(data, 1)
                dst.transform = transform
            break
        except Exception as exc:  # noqa: BLE001
            last_exc = exc
            time.sleep(CHIRPS_RETRY_BACKOFF * attempt)
    else:
        print(f"  ERROR {year:04d}{month:02d}: {last_exc} — giving up")
        return None

    record_download(
        out_tif,
        source_url,
        license_note="CHIRPS is public domain for non-commercial use; cite Funk et al. 2015.",
        notes="Window-read from CHIRPS v2.0 global monthly COG for Yangon bbox.",
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
    print(f"downloaded {len(done)} monthly CHIRPS tiles for Yangon")