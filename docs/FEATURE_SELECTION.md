# FEATURE SELECTION

## 1. Objective

Phase 4 menetapkan strategi feature selection dan algoritma untuk full dataset STATS19 (513,801 baris), tanpa final modeling. Candidate sets di dokumen ini bersifat provisional dan dapat berubah setelah validasi preparation, codebook, serta hasil modeling Phase 5.

Selection harus menjaga leakage boundary: target-derived fields, post-event consequences, identifiers, dan informasi test/future tidak boleh dipakai untuk memilih fitur. Raw dataset tetap dipertahankan.

## 2. Input Dataset

| Item            |                                                     Verified value |
| --------------- | -----------------------------------------------------------------: |
| Source          | `data/raw/dft-road-casualty-statistics-collision-last-5-years.csv` |
| Rows            |                                                            513,801 |
| Raw columns     |                                                                 44 |
| Period          |                                                          2021–2025 |
| Target          |                                               `collision_severity` |
| Legacy baseline |                         10,000 rows; 2,000/year; `random_state=42` |

The legacy baseline is not used as the primary selection dataset. For the exploratory supervised filter below, only 412,276 development rows from 2021–2024 were used; 2025 was not used for feature selection.

## 3. Feature Inventory

The following table reviews every raw feature. `Candidate` means the feature is eligible for that task's provisional set; `Review` means it requires a later decision; `Exclude` means it is blocked for the stated task or from predictor input. No raw feature is deleted.

| Feature                                            | Role                  | Classification | Clustering  | Association | Leakage risk                    | Decision and reason                                               |
| -------------------------------------------------- | --------------------- | -------------- | ----------- | ----------- | ------------------------------- | ----------------------------------------------------------------- |
| `collision_index`                                  | Identifier            | Exclude        | Exclude     | Exclude     | Memorization                    | Exclude; unique traceability key                                  |
| `collision_year`                                   | Temporal              | Review         | Review      | Candidate   | Temporal proxy                  | Review for classification/clustering; retain for split/monitoring |
| `collision_ref_no`                                 | Identifier            | Exclude        | Exclude     | Exclude     | Memorization                    | Exclude; near-unique identifier                                   |
| `location_easting_osgr`                            | Geographic            | Review         | Review      | Exclude     | Area proxy                      | Review one coordinate representation only                         |
| `location_northing_osgr`                           | Geographic            | Review         | Review      | Exclude     | Area proxy                      | Review one coordinate representation only                         |
| `longitude`                                        | Geographic            | Review         | Review      | Exclude     | Area proxy                      | Review one coordinate representation only                         |
| `latitude`                                         | Geographic            | Review         | Review      | Exclude     | Area proxy                      | Review one coordinate representation only                         |
| `police_force`                                     | Administrative/code   | Review         | Review      | Exclude     | Geographic/administrative proxy | MI signal exists; review generalization and fairness              |
| `collision_severity`                               | Target                | Target only    | Exclude     | Exclude     | Direct target                   | Target only; never clustering input                               |
| `number_of_vehicles`                               | Numeric/count         | Candidate      | Candidate   | Exclude     | Timing dependent                | Domain-relevant count; verify availability                        |
| `number_of_casualties`                             | Outcome/count         | Exclude        | Exclude     | Exclude     | Post-event consequence          | Exclude from predictor input                                      |
| `date`                                             | Temporal raw          | Exclude raw    | Exclude raw | Exclude raw | Future/time encoding            | Derive `month`; do not use raw string                             |
| `day_of_week`                                      | Temporal/code         | Candidate      | Candidate   | Candidate   | Low                             | Candidate; retain code until official decoding                    |
| `time`                                             | Temporal raw          | Exclude raw    | Exclude raw | Exclude raw | Encoding/redundancy             | Derive `hour`; do not use raw string                              |
| `local_authority_district`                         | Administrative/code   | Review         | Review      | Exclude     | Area proxy                      | Review cardinality and generalization                             |
| `local_authority_ons_district`                     | Administrative/code   | Review         | Review      | Exclude     | High-cardinality proxy          | Review; avoid blind one-hot                                       |
| `local_authority_highway`                          | Administrative/code   | Review         | Review      | Exclude     | Administrative proxy            | Review redundancy and drift                                       |
| `local_authority_highway_current`                  | Administrative/code   | Review         | Review      | Exclude     | Administrative proxy            | Review overlap with highway field                                 |
| `first_road_class`                                 | Categorical/code      | Candidate      | Candidate   | Candidate   | Low                             | Domain-relevant road context; codebook required                   |
| `first_road_number`                                | Road/geographic code  | Review         | Review      | Exclude     | High-cardinality proxy          | Review; do not use as raw numeric                                 |
| `road_type`                                        | Categorical/code      | Candidate      | Candidate   | Candidate   | Low                             | Domain-relevant road context; codebook required                   |
| `speed_limit`                                      | Numeric/code          | Candidate      | Candidate   | Candidate   | Sentinel semantics              | Candidate; `-1` explicit category, not a speed                    |
| `junction_detail_historic`                         | Historical/code       | Exclude        | Exclude     | Exclude     | Historical availability         | Exclude pending domain evidence                                   |
| `junction_detail`                                  | Categorical/code      | Candidate      | Candidate   | Candidate   | Low                             | Domain-relevant junction context                                  |
| `junction_control`                                 | Categorical/code      | Candidate      | Candidate   | Candidate   | Sentinel concentration          | Candidate; preserve `-1`                                          |
| `second_road_class`                                | Categorical/code      | Candidate      | Candidate   | Candidate   | Code semantics                  | Candidate with codebook review                                    |
| `second_road_number`                               | Road/geographic code  | Review         | Review      | Exclude     | High-cardinality proxy          | Review; do not use as raw numeric                                 |
| `pedestrian_crossing_human_control_historic`       | Historical/code       | Exclude        | Exclude     | Exclude     | Historical availability         | Exclude pending domain evidence                                   |
| `pedestrian_crossing_physical_facilities_historic` | Historical/code       | Exclude        | Exclude     | Exclude     | Historical availability         | Exclude pending domain evidence                                   |
| `pedestrian_crossing`                              | Categorical/code      | Candidate      | Candidate   | Candidate   | Sentinel semantics              | Candidate with codebook review                                    |
| `light_conditions`                                 | Categorical/code      | Candidate      | Candidate   | Candidate   | Low                             | Environmental context; codebook required                          |
| `weather_conditions`                               | Categorical/code      | Candidate      | Candidate   | Candidate   | Low                             | Environmental context; codebook required                          |
| `road_surface_conditions`                          | Categorical/code      | Candidate      | Candidate   | Candidate   | Sentinel semantics              | Environmental context; preserve sentinel                          |
| `special_conditions_at_site`                       | Categorical/code      | Candidate      | Candidate   | Candidate   | Sentinel concentration          | Candidate; codebook required                                      |
| `carriageway_hazards_historic`                     | Historical/code       | Exclude        | Exclude     | Exclude     | Historical availability         | Exclude pending domain evidence                                   |
| `carriageway_hazards`                              | Categorical/code      | Candidate      | Candidate   | Candidate   | Sentinel semantics              | Candidate with codebook review                                    |
| `urban_or_rural_area`                              | Categorical/code      | Candidate      | Candidate   | Candidate   | Area proxy                      | Candidate; check code semantics                                   |
| `did_police_officer_attend_scene_of_accident`      | Event/admin code      | Exclude        | Exclude     | Exclude     | Post-event availability         | Conservative exclusion                                            |
| `trunk_road_flag`                                  | Categorical/code      | Candidate      | Candidate   | Candidate   | Code semantics                  | Candidate with codebook review                                    |
| `lsoa_of_accident_location`                        | Geographic/admin code | Review         | Review      | Exclude     | High-cardinality location proxy | Review privacy/generalization                                     |
| `enhanced_severity_collision`                      | Potential leakage     | Exclude        | Exclude     | Exclude     | Severity-derived                | Exclude                                                           |
| `collision_injury_based`                           | Potential leakage     | Exclude        | Exclude     | Exclude     | Outcome-derived                 | Exclude                                                           |
| `collision_adjusted_severity_serious`              | Potential leakage     | Exclude        | Exclude     | Exclude     | Adjusted target                 | Exclude                                                           |
| `collision_adjusted_severity_slight`               | Potential leakage     | Exclude        | Exclude     | Exclude     | Adjusted target                 | Exclude                                                           |

## 4. Leakage Screening

The following are excluded before any supervised selection: `collision_severity` from predictor matrices, `enhanced_severity_collision`, `collision_injury_based`, `collision_adjusted_severity_serious`, `collision_adjusted_severity_slight`, `number_of_casualties`, and `did_police_officer_attend_scene_of_accident`. `collision_index` and `collision_ref_no` are also excluded as identifiers.

Evidence is field role and availability risk documented in Phase 3, not a claim based on target correlation. `number_of_vehicles`, administrative fields, and geographic fields remain review items because their availability and generalization depend on the final use case.

The 2025 temporal holdout is not used for supervised feature selection. Any later model-based importance must be calculated on training/development data and treated as exploratory evidence, never as final test performance.

## 5. Classification Feature Selection

### Domain filter

The provisional classification core contains context available in a collision-level record and not directly derived from severity: `number_of_vehicles`, `speed_limit`, `first_road_class`, `road_type`, `junction_detail`, `junction_control`, `second_road_class`, `pedestrian_crossing`, `light_conditions`, `weather_conditions`, `road_surface_conditions`, `special_conditions_at_site`, `carriageway_hazards`, `urban_or_rural_area`, `trunk_road_flag`, `day_of_week`, `month`, and `hour`.

`police_force`, `collision_year`, administrative fields, and geography are not in this core because of proxy, drift, privacy, or timing risks. They remain review candidates for a controlled ablation in a later phase.

### Exploratory mutual information

Mutual information was calculated on the 2021–2024 development rows only, with coded variables treated as discrete categories. It is a filter signal, not model accuracy or causal evidence:

| Rank | Feature                      |       MI |
| ---: | ---------------------------- | -------: |
|    1 | `police_force`               | 0.013387 |
|    2 | `number_of_vehicles`         | 0.008132 |
|    3 | `speed_limit`                | 0.007641 |
|    4 | `junction_control`           | 0.005801 |
|    5 | `urban_or_rural_area`        | 0.005355 |
|    6 | `road_type`                  | 0.004598 |
|    7 | `pedestrian_crossing`        | 0.004517 |
|    8 | `trunk_road_flag`            | 0.003744 |
|    9 | `special_conditions_at_site` | 0.003381 |
|   10 | `second_road_class`          | 0.003328 |
|   11 | `junction_detail`            | 0.003052 |
|   12 | `light_conditions`           | 0.002891 |
|   13 | `carriageway_hazards`        | 0.002437 |
|   14 | `hour`                       | 0.002346 |
|   15 | `road_surface_conditions`    | 0.001907 |
|   16 | `weather_conditions`         | 0.001876 |
|   17 | `first_road_class`           | 0.001258 |
|   18 | `day_of_week`                | 0.000709 |
|   19 | `month`                      | 0.000284 |
|   20 | `collision_year`             | 0.000198 |

Interpretation: `police_force` has the strongest exploratory signal but is not automatically selected because administrative/geographic proxy risk can outweigh a filter score. The core retains domain-relevant fields with lower MI for later controlled comparison. MI was not used to select a final feature set.

## 6. Clustering Feature Selection

Clustering must exclude `collision_severity`, all target-derived fields, post-event outcomes, and identifiers. The provisional clustering core is the same 18 context variables as the classification core, excluding target and leakage fields by construction: `number_of_vehicles`, `speed_limit`, `first_road_class`, `road_type`, `junction_detail`, `junction_control`, `second_road_class`, `pedestrian_crossing`, `light_conditions`, `weather_conditions`, `road_surface_conditions`, `special_conditions_at_site`, `carriageway_hazards`, `urban_or_rural_area`, `trunk_road_flag`, `day_of_week`, `month`, and `hour`.

`collision_year`, police-force/admin fields, and geographic coordinates are review-only clustering extensions because they can dominate distance through drift, area, or high cardinality. Identifiers and severity are excluded. Numeric counts require scale review; coded categories require categorical encoding; one-hot output should remain sparse where possible. No K-Means or alternative clustering was run in Phase 4.

## 7. Association Feature Selection

Association analysis is best suited to interpretable categorical transactions, not raw identifiers or high-cardinality geography. The provisional basket contains:

`day_of_week`, `first_road_class`, `road_type`, `speed_limit`, `junction_detail`, `junction_control`, `second_road_class`, `pedestrian_crossing`, `light_conditions`, `weather_conditions`, `road_surface_conditions`, `special_conditions_at_site`, `carriageway_hazards`, `urban_or_rural_area`, and `trunk_road_flag`.

Each transaction would contain field-value items such as `road_type=<code>` and `weather_conditions=<code>`. Sentinel values remain explicit items until their official semantics are confirmed. `month` and `hour` may be added as discretized categorical items after the temporal question is fixed. Administrative/geographic high-cardinality fields, identifiers, target, and leakage fields are excluded from the initial basket. No Apriori or FP-Growth run was performed.

## 8. Temporal Features

The provisional temporal set is `collision_year`, derived `month`, `day_of_week`, and derived `hour`. Raw `date` and `time` are excluded from feature matrices after derivation. `collision_year` is primarily reserved for temporal split and drift monitoring rather than the classification core.

For optional forecasting, use aggregated collision counts by an explicitly chosen time grain and reserve 2025 as a future holdout. A row-level severity target is classification, not forecasting. Forecasting remains open until horizon, aggregation, and business question are specified.

## 9. Redundancy Analysis

| FACT                                                                                  | INTERPRETATION                                                                     | ACTION                                                                |
| ------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------- | --------------------------------------------------------------------- |
| `date` contains calendar information and `month` is derived from it                   | Raw date and month duplicate information at different representations              | Use derived `month`; exclude raw date from matrices                   |
| `time` contains clock information and `hour` is derived from it                       | Raw time and hour duplicate information at different granularity                   | Use derived `hour`; exclude raw time from matrices                    |
| `collision_index` is unique and `collision_ref_no` has 2,964 duplicates               | Both are identifiers, not collision context                                        | Exclude from all candidate predictors                                 |
| Easting/northing and longitude/latitude describe alternative location representations | Including all four may duplicate geographic signal and increase missing/proxy risk | Review one representation at most; do not decide final geography here |
| `local_authority_highway` and `_current` have related names and cardinality           | They may overlap or represent different specification versions                     | Compare definitions before selecting either                           |
| Historical junction/crossing/hazard fields overlap current fields by subject          | Historical values may duplicate or conflict with current specification             | Exclude provisionally; require domain confirmation                    |
| `speed_limit` has seven coded values including `-1`                                   | Numeric storage does not make it unrestricted continuous data                      | Treat as coded/ordinal candidate and preserve sentinel                |

No automatic removal was based on correlation. A later redundancy check must use training data and documented semantic/codebook evidence.

## 10. Feature Selection Methods

| Method                | Strength                                                         | Weakness/risk                                                                | Appropriate use                                |
| --------------------- | ---------------------------------------------------------------- | ---------------------------------------------------------------------------- | ---------------------------------------------- |
| Domain-based          | Respects availability, semantics, privacy, and leakage           | Depends on codebook and use-case knowledge                                   | First screening and exclusion rules            |
| Filter/statistical    | Fast and model-independent                                       | Univariate signal can miss interactions and be unstable in sparse groups     | Development-only screening                     |
| Mutual information    | Captures nonlinear dependence without fitting a predictive model | Sensitive to encoding, sample structure, and does not establish causality    | Exploratory ranking, never sole selector       |
| Tree-based importance | Can reveal interactions and nonlinear usefulness                 | Model-dependent, biased by cardinality, and risks leakage/test contamination | Later exploratory importance on training folds |
| Redundancy analysis   | Limits duplicate representations and improves interpretability   | Correlation may miss semantic overlap and categorical redundancy             | Pair/representation review before modeling     |

The recommended sequence is domain/leakage screening, redundancy review, development-only filter evidence, then controlled training-fold model importance. Final selection must be evaluated in Phase 5 without using the final holdout for selection.

## 11. Provisional Feature Sets

| Set                       | Count | Provisional members                                                                                                                                                                                                                                                                                                                                         |
| ------------------------- | ----: | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `CLASSIFICATION_FEATURES` |    18 | `number_of_vehicles`, `speed_limit`, `first_road_class`, `road_type`, `junction_detail`, `junction_control`, `second_road_class`, `pedestrian_crossing`, `light_conditions`, `weather_conditions`, `road_surface_conditions`, `special_conditions_at_site`, `carriageway_hazards`, `urban_or_rural_area`, `trunk_road_flag`, `day_of_week`, `month`, `hour` |
| `CLUSTERING_FEATURES`     |    18 | Same context core as classification; target, leakage, and identifiers excluded                                                                                                                                                                                                                                                                              |
| `ASSOCIATION_FEATURES`    |    15 | `day_of_week`, `first_road_class`, `road_type`, `speed_limit`, `junction_detail`, `junction_control`, `second_road_class`, `pedestrian_crossing`, `light_conditions`, `weather_conditions`, `road_surface_conditions`, `special_conditions_at_site`, `carriageway_hazards`, `urban_or_rural_area`, `trunk_road_flag`                                        |
| `TEMPORAL_FEATURES`       |     4 | `collision_year`, `month`, `day_of_week`, `hour`                                                                                                                                                                                                                                                                                                            |

Counts are intentionally different because each task has different leakage, representation, and interpretability requirements. These are not final feature selections.

## 12. Algorithm Strategy

### Classification

Candidate algorithms are Logistic Regression (interpretable linear baseline), Decision Tree (transparent nonlinear baseline), Random Forest (robust nonlinear ensemble and legacy comparator), Gradient Boosting, and HistGradientBoosting where encoded input and missing-value handling are compatible. No algorithm is declared best before Phase 5 evaluation.

### Clustering

K-Means is a candidate for the encoded/scaled context core and can be compared with a justified alternative such as agglomerative clustering if resources and representation permit. Candidate `k` values should be selected for evaluation, not assumed from the legacy `k=2`. No clustering is run here.

### Association

Apriori and FP-Growth are candidates for the categorical basket. FP-Growth may be preferable for larger transaction sets, but support, confidence, lift, and interpretability thresholds must be set before comparison. No rules are mined here.

### Forecasting

No forecasting algorithm is selected yet. It becomes appropriate only if the project defines an aggregate collision-count target, time grain, horizon, and future holdout.

## 13. Modeling Experiment Design

### Classification

- Use the full dataset and provisional temporal holdout: 2021–2024 development, 2025 final test, if the use case confirms future generalization.
- Fit preprocessing and any selection only on training/development data; do not use the final test set for selection.
- Compare the candidate algorithms against a documented majority-class and legacy-reference context without conflating legacy 10K results with full-dataset results.
- Keep the three-class target and do not silently balance. If class weighting or resampling is studied later, apply it only within training folds.
- Fix and record seeds, schema, codebook version, feature set, split IDs/rule, and dependency versions.

### Clustering

- Exclude target, leakage, and identifiers.
- Evaluate a predeclared range of candidate `k` values after encoding/scaling decisions.
- Record silhouette, inertia, cluster sizes, and descriptive profiles; do not use cluster quality as classification performance.

### Association

- Build transactions from the provisional categorical basket with explicit field prefixes.
- Record support, confidence, lift, rule count, and semantic interpretability.
- Preserve sentinel items until codebook resolution and document any later minimum-support threshold.

## 14. Evaluation Metrics

Classification must report accuracy, precision, recall, F1, macro F1, weighted F1, confusion matrix, and per-class precision/recall/F1. Fatal-class recall and F1 are mandatory because Fatal is 1.47% of the full target.

Clustering must report silhouette, inertia where applicable, cluster sizes, stability/seed sensitivity where feasible, and interpretable profiles. Association must report support, confidence, lift, coverage/rule count, and semantic review. Forecasting, if approved later, must use time-ordered validation and horizon-appropriate error metrics.

## 15. Risks

- MI and future model importance can select proxies rather than robust causal or operational features.
- `police_force`, administrative, and geographic fields may improve a filter score while reducing generalization or raising privacy concerns.
- Sparse categories and sentinel-heavy fields can make importance unstable.
- Temporal drift may make a random split optimistic.
- Encoded categorical dimensionality may affect clustering distance and model memory.
- Unresolved official codebook meanings limit semantic interpretation.

## 16. Open Questions

1. Should the official DfT 2025 data guide be frozen as the project codebook version?
2. Is the use case pre-event, at-scene, or post-event prediction?
3. Are geographic and administrative fields allowed by the assignment and acceptable for generalization/privacy?
4. Should `police_force` be evaluated in a controlled ablation despite its proxy risk?
5. Is the 2025 temporal holdout required, or does the rubric require stratified random splitting?
6. Which association-mining role and support threshold are required by the assignment?

## 17. Next Phase

**PHASE 5 – MODELING:** implement the approved preparation contract, compare candidate algorithms, and evaluate provisional feature sets without using the final holdout for feature selection. Do not perform Phase 5 modeling in this checkpoint.
