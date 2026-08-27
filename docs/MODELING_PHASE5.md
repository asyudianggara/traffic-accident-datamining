# MODELING PHASE 5

## 1. Objective

Phase 5 menetapkan baseline classification pada full STATS19 dataset dengan kontrak fitur Phase 4. Tujuannya adalah membandingkan beberapa algoritma secara class-aware; ini bukan final model selection atau production deployment.

## 2. Dataset and Split

- Source: `data/raw/dft-road-casualty-statistics-collision-last-5-years.csv`
- Raw data: 513,801 rows × 44 columns, 2021–2025
- Target: `collision_severity` (1 Fatal, 2 Serious, 3 Slight)
- Development/train: 412,276 rows, 2021–2024
- Temporal holdout/test: 101,525 rows, 2025
- No 2025 row was used to fit preprocessing or models.

## 3. Feature and Preprocessing Contract

The unchanged 18-feature provisional core is: `number_of_vehicles`, `speed_limit`, `first_road_class`, `road_type`, `junction_detail`, `junction_control`, `second_road_class`, `pedestrian_crossing`, `light_conditions`, `weather_conditions`, `road_surface_conditions`, `special_conditions_at_site`, `carriageway_hazards`, `urban_or_rural_area`, `trunk_road_flag`, `day_of_week`, `month`, and `hour`.

`number_of_vehicles` uses training-fitted median imputation. The other 17 coded fields use training-fitted most-frequent imputation and sparse `OneHotEncoder(handle_unknown="ignore")`. Sentinel `-1` values remain explicit categorical values. The target, identifiers, casualties, raw date/time, outcome-derived fields, and police attendance are excluded from predictors.

## 4. Baseline Models

| Model | Configuration |
|---|---|
| Logistic Regression | `solver=lbfgs`, `max_iter=1000`, `class_weight=balanced`, `random_state=42` |
| Decision Tree | `max_depth=12`, `min_samples_leaf=20`, `class_weight=balanced`, `random_state=42` |
| Random Forest | `n_estimators=100`, `max_depth=12`, `min_samples_leaf=20`, `max_features=sqrt`, `class_weight=balanced`, `n_jobs=-1`, `random_state=42` |

HistGradientBoosting was not run because the established preprocessing produces sparse input and dense conversion was not justified for this baseline checkpoint.

## 5. Holdout Results

| Model | Accuracy | Macro Precision | Macro Recall | Macro F1 | Weighted F1 | Fatal Precision | Fatal Recall | Fatal F1 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Random Forest | 0.4750 | 0.3796 | 0.4890 | **0.3386** | 0.5447 | 0.0363 | 0.6070 | 0.0686 |
| Decision Tree | 0.4394 | 0.3670 | 0.4628 | 0.3195 | 0.5099 | 0.0336 | 0.5643 | 0.0635 |
| Logistic Regression | 0.3754 | 0.3774 | 0.4770 | 0.2959 | 0.4382 | 0.0340 | **0.6125** | 0.0645 |

Complete per-class reports are in `results/phase5_classification_report.csv`; confusion matrices are in `results/phase5_confusion_matrix_<model>.csv`.

## 6. Comparison and Provisional Best Baseline

Random Forest is the provisional best baseline because it has the highest Macro F1 (0.3386), Macro Recall (0.4890), and Weighted F1 among these runs. Logistic Regression has slightly higher Fatal Recall (0.6125 versus 0.6070), so Random Forest is not superior on every minority-class measure. All models have very low Fatal precision and Fatal F1; accuracy is therefore not an adequate selection criterion.

This ranking is provisional. No extensive tuning, resampling, SMOTE, final model selection, or deployment decision was performed.

## 7. Runtime and Reproducibility

| Model | Training seconds | Prediction seconds | Encoded features |
|---|---:|---:|---:|
| Logistic Regression | 78.17 | 2.02 | 149 |
| Decision Tree | 90.35 | 1.33 | 149 |
| Random Forest | 122.67 | 2.07 | 149 |

The reproducible entry point is `modeling_phase5.py`. Compact machine-readable artifacts are `results/phase5_model_comparison.csv`, `results/phase5_classification_report.csv`, three confusion matrices, and `results/phase5_metadata.json`.

## 8. Validation and Limitations

- All models used exactly the same temporal holdout and 149-feature encoded space.
- Target and identifier leakage guards passed.
- Preprocessing was fitted on development rows only.
- Raw dataset, Phase 3/4 artifacts, legacy models/results, and `app.py` were not modified.
- Natural class imbalance was addressed with class weights only; no synthetic or test-set resampling was used.
- The 2025 holdout is a single future-year evaluation and must remain protected from later selection.
- The use case, official codebook freeze, geographic policy, and final split policy remain open.

## 9. Next Phase

Controlled imbalance and final evaluation can be scoped after review. Any later experiment must preserve the 2025 holdout and report Macro F1, Macro Recall, Fatal Recall, and Fatal F1 alongside accuracy.
