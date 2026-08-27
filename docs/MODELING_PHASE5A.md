# MODELING PHASE 5A

## 1. Objective

Phase 5A membangun baseline classification pertama menggunakan full dataset STATS19. Tujuannya adalah memperoleh reference point yang interpretable sebelum perbandingan algoritma Phase 5B. Ini bukan final model, tuning, balancing experiment, atau deployment.

## 2. Dataset

| Item                   |                Value |
| ---------------------- | -------------------: |
| Raw rows               |              513,801 |
| Raw columns            |                   44 |
| Period                 |            2021–2025 |
| Target                 | `collision_severity` |
| Development rows       |  412,276 (2021–2024) |
| Final temporal holdout |       101,525 (2025) |

The legacy 10K Random Forest remains historical context only and was not used for this training run.

## 3. Feature Set

The provisional 18-feature classification set from `docs/FEATURE_SELECTION.md` was used:

`number_of_vehicles`, `speed_limit`, `first_road_class`, `road_type`, `junction_detail`, `junction_control`, `second_road_class`, `pedestrian_crossing`, `light_conditions`, `weather_conditions`, `road_surface_conditions`, `special_conditions_at_site`, `carriageway_hazards`, `urban_or_rural_area`, `trunk_road_flag`, `day_of_week`, derived `month`, and derived `hour`.

Excluded from predictors were identifiers, target-derived fields, `number_of_casualties`, police attendance, raw `date`, and raw `time`. No unresolved code was relabeled or semantically guessed.

## 4. Target

All three classes were preserved:

| Code | Label   |      Development |         Holdout |
| ---: | ------- | ---------------: | --------------: |
|    1 | Fatal   |    6,100 (1.48%) |   1,453 (1.43%) |
|    2 | Serious |  91,622 (22.22%) | 25,191 (24.81%) |
|    3 | Slight  | 314,554 (76.30%) | 74,881 (73.76%) |

No oversampling, undersampling, SMOTE, or class weighting was applied.

## 5. Train/Holdout Strategy

The temporal split follows the Phase 4 provisional recommendation:

- Development/training: all records from 2021, 2022, 2023, and 2024.
- Final holdout: all records from 2025.
- No 2025 row was used to fit preprocessing, train either model, or select features.
- `random_state=42` was recorded where supported; the temporal split itself is deterministic by year.

## 6. Preprocessing

A scikit-learn `Pipeline` with `ColumnTransformer` was fitted separately for each model:

- Numeric: `number_of_vehicles`, median imputation.
- Categorical: the remaining 17 candidate fields, most-frequent imputation and `OneHotEncoder(handle_unknown="ignore")`.
- Raw `date` and `time` were parsed to derived `month` and `hour` before the split matrices were built.
- All learned preprocessing objects were fitted on development rows only and then applied to the 2025 holdout.
- The transformed development feature space contains 149 columns for the fitted baseline pipeline and remains sparse.

## 7. Class Imbalance

Fatal represents 1.48% of development data and 1.43% of the holdout. The clean baseline keeps the natural distribution. Class-aware metrics, especially Fatal recall and F1, are therefore more informative than accuracy alone.

## 8. Logistic Regression Configuration

`LogisticRegression(solver="lbfgs", max_iter=1000, random_state=42)` was fitted on the sparse encoded development matrix. No hyperparameter search was performed.

## 9. Decision Tree Configuration

The optional second baseline was executed: `DecisionTreeClassifier(max_depth=12, min_samples_leaf=20, random_state=42)`. These are conservative fixed settings, not tuned parameters.

## 10. Results

| Model               | Accuracy | Macro precision | Macro recall | Macro F1 | Weighted F1 |
| ------------------- | -------: | --------------: | -----------: | -------: | ----------: |
| Logistic Regression |   0.7371 |          0.3913 |       0.3358 |   0.2907 |      0.6316 |
| Decision Tree       |   0.7350 |          0.3820 |       0.3388 |   0.3006 |      0.6380 |

These are holdout results for the full-data temporal experiment. Accuracy is not used as the sole quality criterion.

## 11. Confusion Matrix

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

## 12. Per-Class Performance

| Model               | Class   | Precision | Recall |     F1 |
| ------------------- | ------- | --------: | -----: | -----: |
| Logistic Regression | Fatal   |    0.0000 | 0.0000 | 0.0000 |
| Logistic Regression | Serious |    0.4346 | 0.0123 | 0.0239 |
| Logistic Regression | Slight  |    0.7392 | 0.9952 | 0.8483 |
| Decision Tree       | Fatal   |    0.0000 | 0.0000 | 0.0000 |
| Decision Tree       | Serious |    0.4047 | 0.0298 | 0.0555 |
| Decision Tree       | Slight  |    0.7411 | 0.9865 | 0.8464 |

The full classification reports are stored in `models/classification_baseline_metadata.json`; the compact metric table is `results/classification_baseline.csv`.

## 13. Legacy Baseline Context

The legacy reference is a 10K Random Forest with documented accuracy 0.6385 and macro F1 0.3862. It is not directly equivalent to these results because it used a different sample, pipeline, model, and split. The comparison is contextual only; no conclusion that one experiment is superior is made here.

## 14. Reproducibility

| Item          | Recorded value                                                                                       |
| ------------- | ---------------------------------------------------------------------------------------------------- |
| Python        | 3.12.10                                                                                              |
| scikit-learn  | 1.6.1                                                                                                |
| Random state  | 42 where supported                                                                                   |
| Split         | 2021–2024 development / 2025 holdout                                                                 |
| Preprocessor  | Median numeric imputation; most-frequent categorical imputation; sparse one-hot with unknown ignored |
| Feature space | 149 encoded columns                                                                                  |

The metadata artifact records feature lists, leakage exclusions, class distributions, configurations, fit times, reports, confusion matrices, and environment versions.

## 15. Computational Notes

The full CSV was loaded once per run. Logistic Regression fit took approximately 18.959 seconds and Decision Tree approximately 27.712 seconds in the local environment. Sparse one-hot encoding avoided creating a dense high-dimensional matrix. No large processed CSV was created.

## 16. Limitations

- Both clean baselines predicted zero Fatal holdout cases; the baseline is inadequate for minority-class detection.
- No class weighting or resampling was tested in this subphase.
- Prediction timing, full codebook version, geography policy, and final split requirement remain open.
- The results are not final model selection and must not be generalized beyond this temporal holdout.

## 17. Next Phase

**PHASE 5B – CLASSIFICATION MODEL COMPARISON:** compare approved classification algorithms and controlled imbalance strategies using the same leakage-safe split and evaluation protocol. Do not reinterpret this baseline as final performance.
