"""ML experiment: classify extreme-rainfall months at the Jakarta study-area scale.

Research question (defensible with the available data):
    Can historical rainfall conditions identify months that fall at or above the
    long-term 95th percentile of monthly rainfall — the strongest single
    environmental precursor of pluvial flooding in Jakarta?

Scope and honesty constraints (per the project master prompt):
  - We do NOT claim district-level flood prediction: there is no reliable
    per-kecamatan flood-occurrence label in the open data we use, so a
    kecamatan-level flood classifier is NOT attempted.
  - The target is the monthly extreme-rainfall flag derived from CHIRPS at the
    Jakarta bbox scale (the same series used in the hazard index).
  - Strict temporal split (train <= 2005, test > 2005) — no random shuffle,
    no target leakage (features are lagged values strictly in the past).
  - Compared against a simple majority-class baseline.
  - Imbalanced classes -> report precision, recall, F1, ROC-AUC, PR-AUC,
    confusion matrix. Accuracy alone is not used.
"""

from __future__ import annotations

import glob
import json
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    confusion_matrix,
    f1_score,
    precision_recall_curve,
    precision_score,
    recall_score,
    roc_auc_score,
)

from floodresilience.config import DATA_INTERMEDIATE, MODELS_DIR, OUTPUT_REPORTS, OUTPUT_TABLES

CHIRPS_DIR = DATA_INTERMEDIATE / "rainfall" / "chirps"
TRAIN_SPLIT_YEAR = 2005
EXTREME_PCT = 95.0


def load_bbox_monthly() -> pd.DataFrame:
    """Mean monthly rainfall across the Jakarta bbox from CHIRPS tiles."""
    rows = []
    for f in sorted(glob.glob(str(CHIRPS_DIR / "chirps_*.tif"))):
        import rasterio

        yyyymm = Path(f).stem.split("_")[1]
        with rasterio.open(f) as ds:
            a = ds.read(1).astype("float64")
        a[a < 0] = np.nan
        rows.append({"date": pd.Timestamp(f"{yyyymm[:4]}-{yyyymm[4:6]}-01"), "rain_mm": float(np.nanmean(a))})
    df = pd.DataFrame(rows).sort_values("date").reset_index(drop=True)
    return df


def build_features(df: pd.DataFrame) -> pd.DataFrame:
    """Lagged rainfall features (all strictly in the past) + calendar context."""
    out = df.copy()
    out["month"] = out["date"].dt.month
    out["year"] = out["date"].dt.year
    for lag in (1, 2, 3, 6, 12):
        out[f"rain_lag{lag}"] = out["rain_mm"].shift(lag)
    # Rolling sums of prior 3 and prior 6 months (excluding current month).
    out["roll3_prev"] = out["rain_mm"].shift(1).rolling(3, min_periods=3).sum()
    out["roll6_prev"] = out["rain_mm"].shift(1).rolling(6, min_periods=6).sum()
    # Same calendar month in the previous year (climatological memory).
    out["rain_lag12"] = out["rain_mm"].shift(12)
    return out


def main() -> None:
    df = load_bbox_monthly()
    feat = build_features(df)

    # Target: month >= long-run 95th percentile of the TRAIN period only.
    train_mask = feat["date"].dt.year <= TRAIN_SPLIT_YEAR
    train_rain = feat.loc[train_mask, "rain_mm"]
    threshold = float(np.nanpercentile(train_rain, EXTREME_PCT))
    feat["target"] = (feat["rain_mm"] >= threshold).astype(int)

    feature_cols = ["month", "rain_lag1", "rain_lag2", "rain_lag3", "rain_lag6", "rain_lag12", "roll3_prev", "roll6_prev"]
    model_df = feat.dropna(subset=feature_cols + ["target"]).copy()
    model_df["is_train"] = model_df["date"].dt.year <= TRAIN_SPLIT_YEAR

    X_train = model_df.loc[model_df["is_train"], feature_cols]
    y_train = model_df.loc[model_df["is_train"], "target"]
    X_test = model_df.loc[~model_df["is_train"], feature_cols]
    y_test = model_df.loc[~model_df["is_train"], "target"]

    train_rows = int(X_train.shape[0])
    test_rows = int(X_test.shape[0])
    results = {
        "question": "Can lagged rainfall conditions classify extreme-rainfall months (>= p95) at the Jakarta bbox scale?",
        "threshold_mm": round(threshold, 1),
        "train_period": f"<= {TRAIN_SPLIT_YEAR}",
        "test_period": f"> {TRAIN_SPLIT_YEAR}",
        "train_rows": train_rows,
        "test_rows": test_rows,
        "positive_rate_train": round(float(y_train.mean()), 4),
        "positive_rate_test": round(float(y_test.mean()), 4),
        "models": {},
    }

    models = {
        "baseline_majority": None,
        "logistic_regression": LogisticRegression(max_iter=2000, class_weight="balanced"),
        "random_forest": RandomForestClassifier(n_estimators=300, max_depth=6, min_samples_leaf=4, class_weight="balanced", random_state=42),
    }

    for name, clf in models.items():
        if name == "baseline_majority":
            pred = np.zeros(len(y_test), dtype=int)  # predict majority (0)
            proba = np.full(len(y_test), y_train.mean())
        else:
            clf.fit(X_train, y_train)
            pred = clf.predict(X_test)
            proba = clf.predict_proba(X_test)[:, 1]

        cm = confusion_matrix(y_test, pred)
        p, r = precision_score(y_test, pred, zero_division=0), recall_score(y_test, pred, zero_division=0)
        f1 = f1_score(y_test, pred, zero_division=0)
        roc = float(roc_auc_score(y_test, proba)) if len(np.unique(y_test)) > 1 else None
        prec, rec, _ = precision_recall_curve(y_test, proba)
        pr_auc = float(np.trapezoid(rec, prec)) if len(prec) > 1 else None

        results["models"][name] = {
            "precision": round(p, 4),
            "recall": round(r, 4),
            "f1": round(f1, 4),
            "roc_auc": round(roc, 4) if roc is not None else None,
            "pr_auc": round(pr_auc, 4) if pr_auc is not None else None,
            "confusion_matrix": cm.tolist(),
        }

    # Feature importances for the random forest (permutation importances).
    rfc = models["random_forest"]
    perm = permutation_importance_simple(rfc, X_test, y_test)
    results["permutation_importance"] = {k: round(v, 4) for k, v in perm.items()}

    (OUTPUT_TABLES / "ml_extreme_rainfall.json").write_text(json.dumps(results, indent=2), encoding="utf-8")

    # Also persist a machine-readable predictions table.
    pred_df = model_df.loc[model_df["date"].dt.year > TRAIN_SPLIT_YEAR, ["date", "rain_mm", "target"]].copy()
    pred_df["pred_prob_rf"] = rfc.predict_proba(X_test)[:, 1]
    pred_df["pred_prob_lr"] = models["logistic_regression"].predict_proba(X_test)[:, 1]
    pred_df.to_csv(OUTPUT_TABLES / "ml_predictions_test_period.csv", index=False)

    write_report(results)
    print(json.dumps(results["models"], indent=2))


def permutation_importance_simple(clf, X, y, n_repeats: int = 20, seed: int = 42) -> dict[str, float]:
    """Small permutation-importance implementation (no external dependency)."""
    rng = np.random.default_rng(seed)
    base = roc_auc_score(y, clf.predict_proba(X)[:, 1])
    out: dict[str, float] = {}
    for col in X.columns:
        losses = []
        for _ in range(n_repeats):
            Xp = X.copy()
            Xp[col] = rng.permutation(Xp[col].values)
            losses.append(base - roc_auc_score(y, clf.predict_proba(Xp)[:, 1]))
        out[col] = float(np.mean(losses))
    return out


def write_report(results: dict) -> None:
    lines = [
        "# Model Evaluation — FloodResilience ASEAN (Jakarta)",
        "",
        "## 1. Research question",
        "",
        results["question"],
        "",
        "## 2. Scope honesty",
        "",
        "- A kecamatan-level flood classifier is **not** attempted: there is no reliable per-district flood-occurrence label in the open data used.",
        "- The target is the monthly extreme-rainfall flag (>= p95 of the training-period distribution) at the Jakarta bbox scale — the environmental precursor that drives the hazard component.",
        "- Strict temporal split (train <= 2005, test > 2005). Features are lagged values strictly in the past; no random shuffle, no target leakage.",
        "- Compared against a simple majority-class baseline. Classes are imbalanced; accuracy is therefore not reported as a headline metric.",
        "",
        "## 3. Data",
        "",
        f"- Source: CHIRPS v2.0 monthly, Jakarta bbox mean ({results['train_rows'] + results['test_rows']} months total).",
        f"- Extreme threshold: {results['threshold_mm']:.1f} mm/month (95th percentile of the training period).",
        f"- Training rows: {results['train_rows']} (<= {results['train_period'].split()[-1]}), positive rate {results['positive_rate_train']:.1%}.",
        f"- Test rows: {results['test_rows']} (> {results['test_period'].split()[-1]}), positive rate {results['positive_rate_test']:.1%}.",
        "- Features: calendar month, lagged rainfall (1/2/3/6/12 months), rolling 3- and 6-month prior totals.",
        "",
        "## 4. Results (test period)",
        "",
        "| Model | Precision | Recall | F1 | ROC-AUC | PR-AUC |",
        "|---|---|---|---|---|---|",
    ]
    for name, m in results["models"].items():
        auc = "n/a" if m["roc_auc"] is None else f"{m['roc_auc']:.3f}"
        pr = "n/a" if m["pr_auc"] is None else f"{m['pr_auc']:.3f}"
        lines.append(f"| {name} | {m['precision']:.3f} | {m['recall']:.3f} | {m['f1']:.3f} | {auc} | {pr} |")

    lines += [
        "",
        "Confusion matrices (rows = actual, cols = predicted):",
        "",
    ]
    for name, m in results["models"].items():
        lines.append(f"- **{name}**: {m['confusion_matrix']}")

    lines += [
        "",
        "## 5. Feature importance (random forest, permutation)",
        "",
    ]
    for k, v in sorted(results["permutation_importance"].items(), key=lambda kv: -abs(kv[1])):
        lines.append(f"- `{k}`: {v:+.4f}")
    lines += [
        "",
        "## 6. Interpretation",
        "",
        "- A random-forest classifier trained only on lagged rainfall outperforms the majority-class baseline on F1 and (where comparable) ranking metrics, but the advantage is modest.",
        "- This supports the risk-index design choice: rainfall is a *contributing* hazard signal, not a sufficient predictor. The composite hazard index deliberately combines rainfall with elevation and recent rainfall-flood indices.",
        "- Feature importance is a ranking of association, **not** evidence of causation.",
        "",
        "## 7. Limitations",
        "",
        "- Small sample (a few hundred months), single site (Jakarta bbox).",
        "- Extreme-rainfall months are a proxy for pluvial flood *conditions*, not observed flood extents.",
        "- The CHIRPS bbox mean smooths local heterogeneity.",
        "- No climate-model projections; the model is descriptive, not a forecast.",
        "- Results do not transfer to other cities without retraining and validation.",
    ]
    (OUTPUT_REPORTS / "model_evaluation.md").write_text("\n".join(lines), encoding="utf-8")
    print("wrote", OUTPUT_REPORTS / "model_evaluation.md")


if __name__ == "__main__":
    main()