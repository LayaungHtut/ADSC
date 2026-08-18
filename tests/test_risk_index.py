"""Tests for the flood-risk index (features.risk_index)."""

from __future__ import annotations

import pandas as pd
import pytest

from floodresilience.features.risk_index import (
    DEFAULT_WEIGHTS,
    hazard_score,
    exposure_score,
    vulnerability_score,
    risk_scores,
    risk_quantiles,
    sensitivity_analysis,
)

MINI = pd.DataFrame(
    {
        "tship_code": ["A", "B", "C"],
        "township": ["Alpha", "Beta", "Gamma"],
        "district": ["X", "X", "Y"],
        "elev_mean_m": [2.0, 10.0, 50.0],
        "rain_annual_mean_mm": [3000.0, 2400.0, 1800.0],
        "rain_extreme_months": [12, 6, 0],
        "rfh_mean": [80.0, 50.0, 20.0],
        "pop_est": [600000.0, 300000.0, 50000.0],
        "pop_density": [20000.0, 10000.0, 1000.0],
        "schools": [200, 100, 10],
        "health_facilities": [60, 30, 2],
        "child_share": [0.3, 0.25, 0.2],
        "elderly_share": [0.1, 0.1, 0.1],
    }
)


def test_scores_are_bounded_zero_one() -> None:
    out = risk_scores(MINI, DEFAULT_WEIGHTS)
    for col in ["hazard", "exposure", "vulnerability", "risk"]:
        assert out[col].between(0, 1).all(), col
    assert out["risk_100"].between(0, 100).all()


def test_low_elevation_and_high_rainfall_give_higher_hazard() -> None:
    h = hazard_score(MINI).reset_index(drop=True)
    assert h.iloc[0] > h.iloc[1] > h.iloc[2]


def test_high_population_and_facilities_give_higher_exposure() -> None:
    e = exposure_score(MINI).reset_index(drop=True)
    assert e.iloc[0] > e.iloc[1] > e.iloc[2]


def test_weights_sum_to_one() -> None:
    assert sum(DEFAULT_WEIGHTS.values()) == pytest.approx(1.0)


def test_quantiles_assign_five_classes() -> None:
    s = pd.Series([10.0, 20.0, 30.0, 40.0, 50.0])
    q = risk_quantiles(s)
    assert set(q.unique()) == {1, 2, 3, 4, 5}


def test_sensitivity_analysis_reports_rank_spread() -> None:
    sens = sensitivity_analysis(MINI)
    assert "rank_spread" in sens.columns
    assert (sens["rank_spread"] >= 0).all()


def test_risk_dataset_contains_population_and_facilities() -> None:
    from floodresilience.features.risk_index import build_risk_dataset
    import pandas as pd

    # build_risk_dataset reads the real processed file; guard against absence.
    try:
        out = build_risk_dataset()
    except FileNotFoundError:
        pytest.skip("processed features not present")
    assert {"pop_est", "schools", "health_facilities"}.issubset(out.columns)
    assert len(out) > 0
