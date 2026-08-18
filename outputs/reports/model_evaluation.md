# Model Evaluation — FloodResilience ASEAN (Jakarta)

## 1. Research question

Can lagged rainfall conditions classify extreme-rainfall months (>= p95) at the Jakarta bbox scale?

## 2. Scope honesty

- A kecamatan-level flood classifier is **not** attempted: there is no reliable per-district flood-occurrence label in the open data used.
- The target is the monthly extreme-rainfall flag (>= p95 of the training-period distribution) at the Jakarta bbox scale — the environmental precursor that drives the hazard component.
- Strict temporal split (train <= 2005, test > 2005). Features are lagged values strictly in the past; no random shuffle, no target leakage.
- Compared against a simple majority-class baseline. Classes are imbalanced; accuracy is therefore not reported as a headline metric.

## 3. Data

- Source: CHIRPS v2.0 monthly, Jakarta bbox mean (535 months total).
- Extreme threshold: 399.3 mm/month (95th percentile of the training period).
- Training rows: 288 (<= 2005), positive rate 4.9%.
- Test rows: 247 (> 2005), positive rate 6.5%.
- Features: calendar month, lagged rainfall (1/2/3/6/12 months), rolling 3- and 6-month prior totals.

## 4. Results (test period)

| Model | Precision | Recall | F1 | ROC-AUC | PR-AUC |
|---|---|---|---|---|---|
| baseline_majority | 0.000 | 0.000 | 0.000 | 0.500 | 0.468 |
| logistic_regression | 0.207 | 0.688 | 0.319 | 0.870 | 0.214 |
| random_forest | 0.318 | 0.438 | 0.368 | 0.892 | 0.262 |

Confusion matrices (rows = actual, cols = predicted):

- **baseline_majority**: [[231, 0], [16, 0]]
- **logistic_regression**: [[189, 42], [5, 11]]
- **random_forest**: [[216, 15], [9, 7]]

## 5. Feature importance (random forest, permutation)

- `rain_lag12`: +0.0924
- `month`: +0.0720
- `rain_lag2`: +0.0172
- `roll6_prev`: +0.0140
- `roll3_prev`: +0.0110
- `rain_lag1`: +0.0072
- `rain_lag6`: -0.0043
- `rain_lag3`: +0.0003

## 6. Interpretation

- A random-forest classifier trained only on lagged rainfall outperforms the majority-class baseline on F1 and (where comparable) ranking metrics, but the advantage is modest.
- This supports the risk-index design choice: rainfall is a *contributing* hazard signal, not a sufficient predictor. The composite hazard index deliberately combines rainfall with elevation and recent rainfall-flood indices.
- Feature importance is a ranking of association, **not** evidence of causation.

## 7. Limitations

- Small sample (a few hundred months), single site (Jakarta bbox).
- Extreme-rainfall months are a proxy for pluvial flood *conditions*, not observed flood extents.
- The CHIRPS bbox mean smooths local heterogeneity.
- No climate-model projections; the model is descriptive, not a forecast.
- Results do not transfer to other cities without retraining and validation.