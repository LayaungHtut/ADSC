"""Tests for the SAC exports (export.sac) and web data bundle (export.web)."""

from __future__ import annotations

import pandas as pd
import pytest

from floodresilience.config import DATA_SAC
from floodresilience.export.sac import clean_names, export_risk_by_area


def test_clean_names_lowercases_and_underscores() -> None:
    df = pd.DataFrame({"Risk Score ": [1.0], "Pop Est": [2.0]})
    out = clean_names(df)
    assert list(out.columns) == ["risk_score", "pop_est"]


def test_sac_risk_by_area_has_documented_columns() -> None:
    path = DATA_SAC / "sac_risk_by_area.csv"
    if not path.exists():
        pytest.skip("sac exports not generated")
    df = pd.read_csv(path)
    expected = {"kec_code", "kecamatan", "kota", "hazard", "exposure", "vulnerability", "risk", "risk_100", "risk_class"}
    assert expected.issubset(df.columns)
    assert len(df) == 42


@pytest.mark.parametrize(
    "filename,min_rows",
    [
        ("sac_risk_by_area.csv", 1),
        ("sac_rainfall_timeseries.csv", 1),
        ("sac_flood_events.csv", 1),
        ("sac_population_exposure.csv", 1),
        ("sac_infrastructure_exposure.csv", 1),
        ("sac_risk_factors.csv", 1),
    ],
)
def test_sac_files_exist_and_are_populated(filename: str, min_rows: int) -> None:
    path = DATA_SAC / filename
    if not path.exists():
        pytest.skip("sac exports not generated")
    df = pd.read_csv(path)
    assert len(df) >= min_rows
    assert df.columns.notna().all()
