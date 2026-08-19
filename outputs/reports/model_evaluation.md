# Model Evaluation — FloodResilience ASEAN (Yangon)

## 1. Research question

Can lagged rainfall conditions classify extreme-rainfall months (>= p95) at the Yangon bbox scale?

## 2. Scope honesty

- A township-level flood classifier is **not** attempted: there is no reliable per-district flood-occurrence label in the open data used.
- The target is the monthly extreme-rainfall flag (>= p95 of the training-period distribution) at the Yangon bbox scale — the environmental precursor that drives the hazard component.
- Strict temporal split (train <= 2005, test > 2005). Features are lagged values strictly in the past; no random shuffle, no target leakage.
- Compared against a simple majority-class baseline. Classes are imbalanced; accuracy is therefore not reported as a headline metric.

## 3. Data

- Source: CHIRPS v2.0 monthly, Yangon bbox mean (535 months total).
- Extreme threshold: 718.9 mm/month (95th percentile of the training period).
- Training rows: 288 (<= 2005), positive rate 5.2%.
- Test rows: 247 (> 2005), positive rate 10.5%.
- Features: calendar month, lagged rainfall (1/2/3/6/12 months), rolling 3- and 6-month prior totals.

## 4. Results (test period)

| Model | Precision | Recall | F1 | ROC-AUC | PR-AUC |
|---|---|---|---|---|---|
| baseline_majority | 0.000 | 0.000 | 0.000 | 0.500 | 0.447 |
| logistic_regression | 0.433 | 1.000 | 0.605 | 0.951 | 0.512 |
| random_forest | 0.568 | 0.808 | 0.667 | 0.949 | 0.492 |

Confusion matrices (rows = actual, cols = predicted):

- **baseline_majority**: [[221, 0], [26, 0]]
- **logistic_regression**: [[187, 34], [0, 26]]
- **random_forest**: [[205, 16], [5, 21]]

## 5. Feature importance (random forest, permutation)

- `rain_lag12`: +0.0502
- `rain_lag6`: +0.0345
- `month`: +0.0061
- `rain_lag3`: +0.0036
- `roll6_prev`: +0.0016
- `roll3_prev`: -0.0006
- `rain_lag1`: +0.0003
- `rain_lag2`: -0.0003

## 6. Interpretation

- A random-forest classifier trained only on lagged rainfall outperforms the majority-class baseline on F1 and (where comparable) ranking metrics, but the advantage is modest.
- This supports the risk-index design choice: rainfall is a *contributing* hazard signal, not a sufficient predictor. The composite hazard index deliberately combines rainfall with elevation and recent rainfall-flood indices.
- Feature importance is a ranking of association, **not** evidence of causation.

## 7. Limitations

- Small sample (a few hundred months), single site (Yangon bbox).
- Extreme-rainfall months are a proxy for pluvial flood *conditions*, not observed flood extents.
- The CHIRPS bbox mean smooths local heterogeneity.
- No climate-model projections; the model is descriptive, not a forecast.
- Results do not transfer to other cities without retraining and validation.