"""Tests for the data-quality pipeline (cleaning.quality)."""

from __future__ import annotations

import pandas as pd
import pytest

from floodresilience.cleaning.quality import run_qc


def test_qc_passes_clean_data() -> None:
    df = pd.DataFrame({"a": [1, 2, 3], "b": [1.0, 2.0, 3.0]})
    res = run_qc(df, "clean")
    statuses = {c["check"]: c["status"] for c in res.checks}
    assert statuses["missing_values"] == "PASS"
    assert statuses["duplicates"] == "PASS"
    assert statuses["infinite_values"] == "PASS"


def test_qc_flags_missing_values() -> None:
    df = pd.DataFrame({"a": [1, None, 3]})
    res = run_qc(df, "missing")
    statuses = {c["check"]: c["status"] for c in res.checks}
    assert statuses["missing_values"] == "REVIEW"


def test_qc_flags_duplicates() -> None:
    df = pd.DataFrame({"a": [1, 1, 2]})
    res = run_qc(df, "dups")
    statuses = {c["check"]: c["status"] for c in res.checks}
    assert statuses["duplicates"] == "REVIEW"


def test_qc_parses_dates_and_reports_range() -> None:
    df = pd.DataFrame({"month": ["2020-01-01", "2020-02-01", "not-a-date"]})
    res = run_qc(df, "dates", date_col="month")
    statuses = {c["check"]: c["status"] for c in res.checks}
    assert statuses["invalid_dates"] == "FAIL"
    assert statuses["date_range"] == "INFO"


def test_qc_flags_infinite_values() -> None:
    df = pd.DataFrame({"a": [1.0, float("inf"), 3.0]})
    res = run_qc(df, "inf")
    statuses = {c["check"]: c["status"] for c in res.checks}
    assert statuses["infinite_values"] == "FAIL"


def test_qc_never_drops_rows() -> None:
    df = pd.DataFrame({"a": [1, None, None, 4]})
    res = run_qc(df, "nocap")
    assert res.rows == 4
    assert len(df) == 4
