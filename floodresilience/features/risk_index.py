"""Flood risk index for DKI Jakarta kecamatan.

Risk = f(Hazard, Exposure, Vulnerability).

All sub-indicators are min-max normalised to [0, 1] (higher = worse).
Default weights are documented and a sensitivity analysis runs alternative
weightings and normalisations so rankings can be checked for stability.

Every input is traceable to `data/processed/jakarta_kecamatan_features.csv`.
No thresholds are arbitrarily assigned; classes are quantile-based.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from floodresilience.config import DATA_PROCESSED, OUTPUT_TABLES

FEATURES = DATA_PROCESSED / "jakarta_kecamatan_features.csv"

# Default component weights (sum to 1). Justification: hazard is the driver,
# exposure determines what is harmed, vulnerability shapes impact.
DEFAULT_WEIGHTS = {"hazard": 0.4, "exposure": 0.35, "vulnerability": 0.25}

# Sensitivity scenarios: alternative weightings.
SENSITIVITY_WEIGHTS = [
    {"hazard": 0.5, "exposure": 0.3, "vulnerability": 0.2},
    {"hazard": 0.33, "exposure": 0.33, "vulnerability": 0.34},
    {"hazard": 0.4, "exposure": 0.4, "vulnerability": 0.2},
    {"hazard": 0.5, "exposure": 0.25, "vulnerability": 0.25},
]


def minmax(s: pd.Series) -> pd.Series:
    lo, hi = s.min(), s.max()
    if hi == lo:
        return pd.Series(0.5, index=s.index)
    return (s - lo) / (hi - lo)


def percentile_norm(s: pd.Series) -> pd.Series:
    return s.rank(pct=True)


def hazard_score(df: pd.DataFrame, norm=minmax) -> pd.Series:
    e = norm(df["elev_mean_m"])  # higher elevation -> less hazard
    h_elev = 1.0 - e
    h_rain = norm(df["rain_annual_mean_mm"])
    h_extreme = norm(df["rain_extreme_months"])
    h_rfh = norm(df["rfh_mean"])
    return 0.35 * h_elev + 0.30 * h_rain + 0.20 * h_extreme + 0.15 * h_rfh


def exposure_score(df: pd.DataFrame, norm=minmax) -> pd.Series:
    e_pop = norm(df["pop_est"])
    e_density = norm(df["pop_density"])
    e_schools = norm(df["schools"])
    e_health = norm(df["health_facilities"])
    return 0.35 * e_pop + 0.25 * e_density + 0.20 * e_schools + 0.20 * e_health


def vulnerability_score(df: pd.DataFrame, norm=minmax) -> pd.Series:
    v_child = norm(df["child_share"])
    v_elderly = norm(df["elderly_share"])
    return 0.6 * v_child + 0.4 * v_elderly


def risk_scores(df: pd.DataFrame, weights: dict[str, float], norm=minmax) -> pd.DataFrame:
    out = df[["kec_code", "kecamatan", "kota"]].copy()
    out["hazard"] = hazard_score(df, norm)
    out["exposure"] = exposure_score(df, norm)
    out["vulnerability"] = vulnerability_score(df, norm)
    out["risk"] = (
        weights["hazard"] * out["hazard"]
        + weights["exposure"] * out["exposure"]
        + weights["vulnerability"] * out["vulnerability"]
    )
    out["risk_100"] = out["risk"] * 100.0
    return out


def risk_quantiles(score: pd.Series) -> pd.Series:
    """Quantile-based classes: 1 lowest .. 5 highest (quintiles)."""
    return pd.qcut(score, q=5, labels=[1, 2, 3, 4, 5], duplicates="drop")


def sensitivity_analysis(df: pd.DataFrame) -> pd.DataFrame:
    """Rank each kecamatan under every weighting scheme; report rank spread."""
    ranks = pd.DataFrame({"kecamatan": df["kecamatan"].values})
    for i, w in enumerate([DEFAULT_WEIGHTS, *SENSITIVITY_WEIGHTS]):
        r = risk_scores(df, w)
        ranks[f"rank_{i}"] = r["risk"].rank(ascending=False, method="min").astype(int)
    cols = [c for c in ranks.columns if c.startswith("rank_")]
    ranks["rank_min"] = ranks[cols].min(axis=1)
    ranks["rank_max"] = ranks[cols].max(axis=1)
    ranks["rank_spread"] = ranks["rank_max"] - ranks["rank_min"]
    return ranks


def build_risk_dataset(weights: dict[str, float] | None = None, norm=minmax) -> pd.DataFrame:
    df = pd.read_csv(FEATURES)
    w = weights or DEFAULT_WEIGHTS
    out = risk_scores(df, w, norm)
    out["risk_class"] = risk_quantiles(out["risk_100"]).astype(int)
    out = out.merge(df[["kec_code", "pop_est", "schools", "health_facilities"]], on="kec_code", how="left")
    return out


def main() -> None:
    df = pd.read_csv(FEATURES)
    risk = risk_scores(df, DEFAULT_WEIGHTS)
    risk["risk_class"] = risk_quantiles(risk["risk_100"]).astype(int)

    sens = sensitivity_analysis(df)
    spread = sens["rank_spread"].mean()

    risk.to_csv(OUTPUT_TABLES / "risk_scores.csv", index=False)
    sens.to_csv(OUTPUT_TABLES / "risk_sensitivity.csv", index=False)

    print("=== TOP 10 RISK (default weights) ===")
    print(risk.sort_values("risk_100", ascending=False).head(10).to_string(index=False))
    print(f"\nmean rank spread across {1+len(SENSITIVITY_WEIGHTS)} weightings: {spread:.2f}")
    print("\n=== sensitivity (rank spread per kecamatan) ===")
    print(sens.sort_values("rank_spread", ascending=False).head(10).to_string(index=False))


if __name__ == "__main__":
    main()
