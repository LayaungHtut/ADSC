"""Automated data-quality checks for tabular data.

Every check is non-destructive: it reports problems and counts, it never drops
rows silently. The report is written as markdown to
`outputs/reports/data_quality_report.md`.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np
import pandas as pd

from floodresilience.config import OUTPUT_REPORTS


@dataclass
class QCResult:
    dataset: str
    rows: int = 0
    columns: int = 0
    checks: list[dict] = field(default_factory=list)

    def add(self, check: str, status: str, detail: str = "") -> None:
        self.checks.append({"check": check, "status": status, "detail": detail})

    def to_dict(self) -> dict:
        return {
            "dataset": self.dataset,
            "rows": self.rows,
            "columns": self.columns,
            "checks": self.checks,
        }


def run_qc(df: pd.DataFrame, name: str, *, date_col: str | None = None, id_col: str | None = None) -> QCResult:
    res = QCResult(dataset=name, rows=len(df), columns=len(df.columns))

    # Missing values
    missing = df.isna().mean()
    n_missing_cols = int((missing > 0).sum())
    res.add("missing_values", "PASS" if n_missing_cols == 0 else "REVIEW", f"{n_missing_cols} columns have missing values; max rate {missing.max():.1%}")

    # Duplicates
    n_dups = int(df.duplicated().sum())
    res.add("duplicates", "PASS" if n_dups == 0 else "REVIEW", f"{n_dups} duplicate rows")

    # Dates
    if date_col:
        try:
            dt = pd.to_datetime(df[date_col], errors="coerce")
            n_invalid = int(dt.isna().sum())
            res.add("invalid_dates", "PASS" if n_invalid == 0 else "FAIL", f"{n_invalid} invalid dates in {date_col}")
            res.add("date_range", "INFO", f"{dt.min()} .. {dt.max()}")
        except Exception as exc:  # pragma: no cover
            res.add("date_parse", "FAIL", str(exc))

    # Numeric sanity: impossible values (NaN handled above), inf
    numeric = df.select_dtypes(include=[np.number])
    if len(numeric.columns):
        n_inf = int(np.isinf(numeric.to_numpy(dtype="float64")).sum())
        res.add("infinite_values", "PASS" if n_inf == 0 else "FAIL", f"{n_inf} infinite values")

    # Outliers by IQR on numeric columns (reported, not removed)
    outlier_cols: list[str] = []
    for col in numeric.columns:
        s = df[col].dropna()
        if len(s) < 10 or s.nunique() < 5:
            continue
        q1, q3 = s.quantile([0.25, 0.75])
        iqr = q3 - q1
        if iqr == 0:
            continue
        n_out = int(((s < q1 - 3 * iqr) | (s > q3 + 3 * iqr)).sum())
        if n_out > 0:
            outlier_cols.append(f"{col}:{n_out}")
    res.add("outliers_3iqr", "INFO", "; ".join(outlier_cols) if outlier_cols else "none beyond 3x IQR")

    return res


def write_qc_report(results: list[QCResult], out_path: Path | None = None) -> Path:
    out_path = out_path or (OUTPUT_REPORTS / "data_quality_report.md")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Data Quality Report",
        "",
        "Automatically generated from the ingestion pipeline. **No rows are ever deleted**; issues are recorded here for the analyst.",
        "",
        f"Generated: {pd.Timestamp.utcnow().isoformat(timespec='seconds')}",
        "",
    ]
    for res in results:
        lines.append(f"## {res.dataset}")
        lines.append(f"- Rows: {res.rows}, Columns: {res.columns}")
        for c in res.checks:
            lines.append(f"- **{c['check']}**: `{c['status']}` — {c['detail']}")
        lines.append("")
    out_path.write_text("\n".join(lines), encoding="utf-8")
    return out_path


def save_qc_json(results: list[QCResult], out_path: Path | None = None) -> Path:
    out_path = out_path or (OUTPUT_REPORTS / "data_quality_report.json")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps([r.to_dict() for r in results], indent=2), encoding="utf-8")
    return out_path
