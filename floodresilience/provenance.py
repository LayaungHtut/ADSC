"""Download provenance tracking.

Every file that enters `data/raw/` is recorded in `data/raw/PROVENANCE.csv`
with its URL, retrieval date and SHA-256. This makes the data audit trail
explicit and reproducible.
"""

from __future__ import annotations

import csv
import hashlib
from datetime import datetime, timezone
from pathlib import Path

from floodresilience.config import DATA_RAW

PROVENANCE_FILE = DATA_RAW / "PROVENANCE.csv"
_COLUMNS = ["path", "source_url", "retrieved_utc", "sha256", "license_note", "notes"]
_LOCK = __import__("threading").Lock()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def _load_rows() -> list[dict[str, str]]:
    if not PROVENANCE_FILE.exists():
        return []
    with open(PROVENANCE_FILE, newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def record_download(
    path: Path,
    source_url: str,
    license_note: str = "",
    notes: str = "",
) -> None:
    """Append (or update) a provenance row for a downloaded file."""
    row = {
        "path": str(path),
        "source_url": source_url,
        "retrieved_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "sha256": sha256_file(path),
        "license_note": license_note,
        "notes": notes,
    }
    rows = [r for r in _load_rows() if r.get("path") != str(path)]
    rows.append(row)
    with _LOCK:
        with open(PROVENANCE_FILE, "w", newline="", encoding="utf-8") as fh:
            writer = csv.DictWriter(fh, fieldnames=_COLUMNS)
            writer.writeheader()
            writer.writerows(rows)


def load_provenance() -> list[dict[str, str]]:
    return _load_rows()