# MODELING PHASE 5B-1

## 1. Objective

Phase 5B-1 membandingkan baseline classification pada full dataset dengan kontrak fitur, target, split, dan preprocessing yang sama seperti Phase 5A. Status checkpoint ini **PARTIAL**: Logistic Regression dan Decision Tree selesai; Random Forest dihentikan karena bottleneck komputasi; HistGradientBoosting tidak dijalankan karena incompatibility dengan sparse preprocessing.

Tidak ada tuning, SMOTE, oversampling, undersampling, clustering, association mining, forecasting, deployment, atau final model selection.

## 2. Dataset

| Item                  |                   Value |
| --------------------- | ----------------------: |
| Raw rows              |                 513,801 |
| Raw columns           |                      44 |
| Development           | 412,276 rows, 2021–2024 |
| Holdout               |      101,525 rows, 2025 |
| Target                |    `collision_severity` |
| Encoded feature space |      149 sparse columns |

The legacy 10K Random Forest remains contextual only and was not used in this comparison.

## 3. Split

All records from 2021–2024 were used for development/training. All 2025 records were reserved as the final temporal holdout. No 2025 row was used for preprocessing fitting, feature selection, training, or tuning.

## 4. Feature Set

The Phase 4 provisional 18-feature classification set was reused unchanged: `number_of_vehicles`, `speed_limit`, `first_road_class`, `road_type`, `junction_detail`, `junction_control`, `second_road_class`, `pedestrian_crossing`, `light_conditions`, `weather_conditions`, `road_surface_conditions`, `special_conditions_at_site`, `carriageway_hazards`, `urban_or_rural_area`, `trunk_road_flag`, `day_of_week`, derived `month`, and derived `hour`.

Identifiers, target-derived fields, `number_of_casualties`, police attendance, raw `date`, and raw `time` were excluded as established in Phase 5A.

## 5. Preprocessing

The Phase 5A pipeline was reused for every attempted model:

- `number_of_vehicles`: median imputation.
- Other 17 candidate fields: most-frequent imputation followed by `OneHotEncoder(handle_unknown="ignore")`.
- Learned transformations were fitted on development rows only.
- The encoded matrix remained sparse and contained 149 columns.

## 6. Models

| Model                | Configuration                                                                                 | Status                             |
| -------------------- | --------------------------------------------------------------------------------------------- | ---------------------------------- |
| Logistic Regression  | `solver="lbfgs"`, `max_iter=1000`, `random_state=42`                                          | Completed                          |
| Decision Tree        | `max_depth=12`, `min_samples_leaf=20`, `random_state=42`                                      | Completed                          |
| Random Forest        | `n_estimators=300`, `max_depth=15`, `class_weight="balanced"`, `random_state=42`, `n_jobs=-1` | Not completed; resource bottleneck |
| HistGradientBoosting | `random_state=42` compatibility check                                                         | Not run; sparse input rejected     |

Logistic Regression and Decision Tree were retrained with the same Phase 5A contract so their results are directly comparable to the Phase 5A baseline protocol.

## 7. Class Imbalance Strategy

The natural class distribution was preserved for Logistic Regression and Decision Tree. The only controlled imbalance intervention specified in this subphase was `class_weight="balanced"` for Random Forest. No resampling or SMOTE was performed.

## 8. Evaluation Metrics

Metrics include accuracy, macro/weighted precision, recall, and F1, plus per-class precision, recall, and F1. Primary interpretation uses Macro F1, Macro Recall, Fatal Recall, and Fatal F1 before weighted metrics or accuracy.

## 9. Results

| Model                |      Accuracy | Macro Precision |  Macro Recall |      Macro F1 | Weighted Precision | Weighted Recall |   Weighted F1 |  Fatal Recall |      Fatal F1 |
| -------------------- | ------------: | --------------: | ------------: | ------------: | -----------------: | --------------: | ------------: | ------------: | ------------: |
| Logistic Regression  |        0.7371 |          0.3913 |        0.3358 |        0.2907 |             0.6530 |          0.7371 |        0.6316 |        0.0000 |        0.0000 |
| Decision Tree        |        0.7350 |          0.3820 |        0.3388 |        0.3006 |             0.6471 |          0.7350 |        0.6380 |        0.0000 |        0.0000 |
| Random Forest        | NOT COMPLETED |   NOT COMPLETED | NOT COMPLETED | NOT COMPLETED |      NOT COMPLETED |   NOT COMPLETED | NOT COMPLETED | NOT COMPLETED | NOT COMPLETED |
| HistGradientBoosting |       NOT RUN |         NOT RUN |       NOT RUN |       NOT RUN |            NOT RUN |         NOT RUN |       NOT RUN |       NOT RUN |       NOT RUN |

The complete structured metrics for the two completed models are in `results/classification_phase5b_comparison.csv`.

## 10. Confusion Matrices

Label order is `[Fatal, Serious, Slight]`; rows are actual and columns are predicted.

### Logistic Regression

```text
[[    0,    42,  1411],
 [    0,   309, 24882],
 [    0,   360, 74521]]
```

### Decision Tree

```text
[[    0,    93,  1360],
 [    0,   750, 24441],
 [    0,  1010, 73871]]
```

## 11. Minority-Class Analysis

Both completed models have Fatal recall and F1 equal to 0.0000 on the 2025 holdout. Decision Tree has slightly higher Macro F1 (0.3006 versus 0.2907) and Macro Recall (0.3388 versus 0.3358), but neither baseline detects Fatal cases. This confirms that accuracy around 0.735–0.737 is dominated by the Slight class and is not sufficient evidence of useful minority-class performance.

Random Forest was configured with balanced class weights as requested, but no valid result was produced. It must not be ranked or described as better or worse.

## 12. Legacy Baseline Context

The legacy Random Forest used 10,000 records and reported accuracy 0.6385 and Macro F1 0.3862. This is contextual only: its sample, split, preprocessing, and evaluation protocol differ from the current full-dataset temporal holdout. No direct superiority claim is made.

## 13. Computational Notes

The established sparse preprocessing was compatible with Logistic Regression and Decision Tree. HistGradientBoosting rejected the encoded sparse matrix with `TypeError: Sparse data was passed for X, but dense data is required`; dense conversion was not attempted because it could create an unnecessary high-memory matrix.

Random Forest with the specified 300 trees, depth 15, balanced class weights, and `n_jobs=-1` remained responsive after approximately 27 minutes and used approximately 1.08 GB RAM without producing a result or artifact. It was stopped to protect local resources. No dataset reduction or silent configuration change was made.

## 14. Limitations

- The comparison is incomplete because Random Forest did not finish and HistGradientBoosting was incompatible with sparse preprocessing.
- Only the two completed models can be compared numerically.
- Fatal detection remains unsuccessful for both completed clean baselines.
- No controlled class-weight comparison beyond the incomplete Random Forest attempt was performed.
- This is not final model selection and the 2025 holdout must remain protected in future selection work.

## 15. Next Phase

**PHASE 5B-2 – CONTROLLED CLASS IMBALANCE EXPERIMENT:** evaluate an explicitly controlled imbalance strategy for the classification baseline, keeping the same temporal split and leakage-safe preprocessing. Revisit the incomplete Random Forest only if a resource-bounded design is explicitly approved.
