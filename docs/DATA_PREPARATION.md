# DATA PREPARATION

## 1. Objective

Phase 3 menetapkan kontrak preparation yang reproducible untuk full dataset sebelum feature selection dan modeling. Dokumen ini mendefinisikan perlakuan awal terhadap identifier, target, temporal fields, missing values, sentinel, anomaly, leakage, kategori, numerik, dan geografis.

Tidak ada training, balancing, feature selection final, model, sampling 10K, atau CSV processed besar pada Phase 3. Raw dataset tetap menjadi master immutable.

## 2. Input Dataset

### FACT

| Item                         |                                                     Verified value |
| ---------------------------- | -----------------------------------------------------------------: |
| Path                         | `data/raw/dft-road-casualty-statistics-collision-last-5-years.csv` |
| Rows                         |                                                            513,801 |
| Columns                      |                                                                 44 |
| Period                       |                                                          2021–2025 |
| Target                       |                                               `collision_severity` |
| Full-row duplicates          |                                                                  0 |
| `collision_index` duplicates |                                                                  0 |
| Explicit missing             |                              53 in each of four coordinate columns |

Full dataset digunakan tanpa sampling. Dataset legacy 10K (2,000 per year, `random_state=42`) tetap hanya baseline historis.

### Official codebook source

The official DfT Road Safety Open Data page identifies the **Open dataset data guide 2025** as the codebook for decoding coded variables: <https://assets.publishing.service.gov.uk/media/6a63900b2dc18ebe4c3b2bc8/dft-road-casualty-statistics-road-safety-open-dataset-data-guide-2025.xlsx>. The related official guidance page is <https://www.gov.uk/guidance/road-accident-and-safety-statistics-guidance>.

The source data is coded rather than textual. No unresolved code is relabeled by assumption in this phase. `collision_severity` labels 1 = Fatal, 2 = Serious, and 3 = Slight are retained from the verified project mapping. For all other fields, codebook confirmation is required before human-readable grouping.

## 3. Feature Roles

This is a preparation contract and initial role classification, not final feature selection. `KEEP` means eligible for the candidate preparation path; `REVIEW` means no final inclusion decision; `EXCLUDE` means blocked from predictor input for the stated reason. Raw columns remain untouched.

| Feature                                            | Role                           | Initial decision                                   | Status  | Reason                                             |
| -------------------------------------------------- | ------------------------------ | -------------------------------------------------- | ------- | -------------------------------------------------- |
| `collision_index`                                  | Identifier                     | Preserve for traceability; exclude from predictors | EXCLUDE | Unique record identifier                           |
| `collision_year`                                   | Temporal                       | Preserve for split/monitoring; review as predictor | REVIEW  | Year may encode temporal drift                     |
| `collision_ref_no`                                 | Identifier                     | Preserve for traceability; exclude from predictors | EXCLUDE | Not unique; identifier-like                        |
| `location_easting_osgr`                            | Geographic                     | Review one geographic representation               | REVIEW  | 53 missing; potentially redundant/proxy            |
| `location_northing_osgr`                           | Geographic                     | Review one geographic representation               | REVIEW  | 53 missing; potentially redundant/proxy            |
| `longitude`                                        | Geographic                     | Review one geographic representation               | REVIEW  | 53 missing; potentially redundant/proxy            |
| `latitude`                                         | Geographic                     | Review one geographic representation               | REVIEW  | 53 missing; potentially redundant/proxy            |
| `police_force`                                     | Administrative/code            | Review after use-case decision                     | REVIEW  | Administrative/geographic proxy risk               |
| `collision_severity`                               | Target                         | Keep as target, never as input                     | KEEP    | Three verified classes                             |
| `number_of_vehicles`                               | Numeric/count                  | Keep candidate; validate availability              | REVIEW  | Count may be available at-scene; timing unresolved |
| `number_of_casualties`                             | Outcome/count                  | Exclude pending explicit post-event use case       | EXCLUDE | Consequence of collision; leakage risk             |
| `date`                                             | Temporal                       | Derive approved calendar fields; exclude raw date  | REVIEW  | Raw timestamp should not enter directly            |
| `day_of_week`                                      | Temporal/code                  | Keep candidate as coded category                   | REVIEW  | Code meaning requires official guide               |
| `time`                                             | Temporal                       | Derive `hour`; exclude raw time                    | REVIEW  | Raw time should not enter directly                 |
| `local_authority_district`                         | Administrative/code            | Review; retain code until codebook confirmed       | REVIEW  | Administrative proxy/sentinel risk                 |
| `local_authority_ons_district`                     | Administrative/code            | Review cardinality/generalization                  | REVIEW  | High-cardinality geographic proxy                  |
| `local_authority_highway`                          | Administrative/code            | Review cardinality/generalization                  | REVIEW  | Administrative/geographic proxy                    |
| `local_authority_highway_current`                  | Administrative/code            | Review redundancy with highway field               | REVIEW  | Possible versioned duplicate                       |
| `first_road_class`                                 | Categorical/code               | Keep candidate as coded category                   | KEEP    | Low cardinality; codebook required                 |
| `first_road_number`                                | Road/geographic code           | Review or exclude after domain decision            | REVIEW  | High cardinality/location proxy                    |
| `road_type`                                        | Categorical/code               | Keep candidate as coded category                   | KEEP    | Low cardinality; codebook required                 |
| `speed_limit`                                      | Numeric/code                   | Keep candidate; treat `-1` explicitly              | KEEP    | Seven observed codes; `-1` sentinel                |
| `junction_detail_historic`                         | Historical/code                | Exclude pending domain confirmation                | EXCLUDE | Historical duplicate/availability risk             |
| `junction_detail`                                  | Categorical/code               | Keep candidate as coded category                   | KEEP    | Sentinel and codebook handling required            |
| `junction_control`                                 | Categorical/code               | Keep candidate as coded category                   | KEEP    | Large `-1` sentinel group                          |
| `second_road_class`                                | Categorical/code               | Review codebook and sparsity                       | REVIEW  | Road-context code not fully mapped locally         |
| `second_road_number`                               | Road/geographic code           | Review or exclude after domain decision            | REVIEW  | High cardinality/location proxy                    |
| `pedestrian_crossing_human_control_historic`       | Historical/code                | Exclude pending domain confirmation                | EXCLUDE | Historical field                                   |
| `pedestrian_crossing_physical_facilities_historic` | Historical/code                | Exclude pending domain confirmation                | EXCLUDE | Historical field                                   |
| `pedestrian_crossing`                              | Categorical/code               | Keep candidate as coded category                   | REVIEW  | Sentinel and codebook handling required            |
| `light_conditions`                                 | Categorical/code               | Keep candidate as coded category                   | KEEP    | Low cardinality; codebook required                 |
| `weather_conditions`                               | Categorical/code               | Keep candidate as coded category                   | KEEP    | Low cardinality; codebook required                 |
| `road_surface_conditions`                          | Categorical/code               | Keep candidate as coded category                   | KEEP    | Sentinel and codebook handling required            |
| `special_conditions_at_site`                       | Categorical/code               | Keep candidate as coded category                   | REVIEW  | Codebook required; many `-1` values                |
| `carriageway_hazards_historic`                     | Historical/code                | Exclude pending domain confirmation                | EXCLUDE | Historical field                                   |
| `carriageway_hazards`                              | Categorical/code               | Keep candidate as coded category                   | REVIEW  | Codebook required; sentinel present                |
| `urban_or_rural_area`                              | Categorical/code               | Keep candidate as coded category                   | KEEP    | Low cardinality; rare/sentinel values              |
| `did_police_officer_attend_scene_of_accident`      | Event/administrative code      | Exclude pending timing confirmation                | EXCLUDE | May be recorded after event                        |
| `trunk_road_flag`                                  | Categorical/code               | Keep candidate as coded category                   | REVIEW  | Codebook required; sentinel present                |
| `lsoa_of_accident_location`                        | Geographic/administrative code | Review privacy and cardinality                     | REVIEW  | High-cardinality location proxy                    |
| `enhanced_severity_collision`                      | Potential leakage              | Exclude                                            | EXCLUDE | Severity-derived                                   |
| `collision_injury_based`                           | Potential leakage              | Exclude                                            | EXCLUDE | Injury/outcome-derived                             |
| `collision_adjusted_severity_serious`              | Potential leakage              | Exclude                                            | EXCLUDE | Adjusted severity-derived                          |
| `collision_adjusted_severity_slight`               | Potential leakage              | Exclude                                            | EXCLUDE | Adjusted severity-derived                          |

## 4. Identifier Handling

`collision_index` and `collision_ref_no` are retained in raw records and may be carried in a traceability table or split manifest. Neither is an input predictor. `collision_index` can identify a row across preparation outputs; it must not be used as a numeric or categorical model feature. `collision_ref_no` is not a primary key because 2,964 duplicate values were observed.

## 5. Target Preparation

Keep `collision_severity` unchanged as an integer target with three classes:

| Code | Label   | Preparation rule |
| ---: | ------- | ---------------- |
|    1 | Fatal   | Keep             |
|    2 | Serious | Keep             |
|    3 | Slight  | Keep             |

The target has no missing values or unexpected codes. Do not oversample, undersample, apply SMOTE, or otherwise balance in Phase 3. Any class weighting or resampling belongs to a later modeling/evaluation experiment and must occur inside training folds only.

## 6. Missing Value Strategy

### FACT

| Feature                  | Missing | Percent | Type       |
| ------------------------ | ------: | ------: | ---------- |
| `location_easting_osgr`  |      53 | 0.0103% | Geographic |
| `location_northing_osgr` |      53 | 0.0103% | Geographic |
| `longitude`              |      53 | 0.0103% | Geographic |
| `latitude`               |      53 | 0.0103% | Geographic |

No row is deleted solely because coordinates are missing. If a geographic representation is approved, its imputation is fitted on training rows only and the missingness pattern is preserved in the validation/test transformation. If geography is excluded, all four coordinate fields are excluded consistently.

### ACTION

For future numeric pipelines, use a training-fitted median imputer only after the geographic decision. For categorical pipelines, use an explicit missing category where missingness exists; do not infer missingness from arbitrary numeric codes.

## 7. Sentinel Value Strategy

Sentinels are not automatically replaced. Their semantic class must come from the official data guide. Until then, coded fields are treated as categorical values and `-1` is preserved as an explicit `missing/out-of-range` code where the local mapping already verifies that meaning.

Observed sentinel counts from the full dataset include:

| Feature                      | Sentinel/value |   Count | Preparation action             |
| ---------------------------- | -------------: | ------: | ------------------------------ |
| `speed_limit`                |           `-1` |       3 | Preserve; never treat as speed |
| `junction_detail`            |           `-1` |  19,982 | Preserve as explicit category  |
| `junction_control`           |           `-1` | 217,897 | Preserve as explicit category  |
| `pedestrian_crossing`        |           `-1` |  11,238 | Preserve pending codebook      |
| `light_conditions`           |           `-1` |      34 | Preserve pending codebook      |
| `weather_conditions`         |           `-1` |      12 | Preserve pending codebook      |
| `road_surface_conditions`    |           `-1` |   3,527 | Preserve as explicit category  |
| `special_conditions_at_site` |           `-1` | 151,370 | Preserve pending codebook      |
| `carriageway_hazards`        |           `-1` |   9,891 | Preserve pending codebook      |
| `urban_or_rural_area`        |           `-1` |       8 | Preserve pending codebook      |
| `trunk_road_flag`            |           `-1` |  36,318 | Preserve pending codebook      |

Zero is not globally treated as missing: its meaning is field-specific and must be decoded from the official guide. No `-2` values were observed in the audited coded fields. No automatic category merging is permitted in this phase.

## 8. Invalid Value Handling

The following full-dataset checks were performed without deleting records:

| Check                  | FACT                                                          | INTERPRETATION                                                                      | ACTION                                         |
| ---------------------- | ------------------------------------------------------------- | ----------------------------------------------------------------------------------- | ---------------------------------------------- |
| `collision_year`       | 0 values outside 2021–2025                                    | Year range is internally consistent                                                 | Retain; assert range in pipeline               |
| `number_of_vehicles`   | 0 non-positive values; maximum 26                             | Positive counts are valid structurally; high values need domain review              | Retain; do not remove outliers                 |
| `number_of_casualties` | 0 non-positive values; maximum 142                            | Positive counts are structurally valid but outcome timing remains a leakage concern | Exclude as predictor pending use-case decision |
| `speed_limit`          | 0 values outside `-1, 20, 30, 40, 50, 60, 70`                 | Observed codes are structurally consistent; `-1` is not a physical limit            | Preserve codes; decode officially              |
| Latitude/longitude     | 0 non-missing values outside latitude 49–61 or longitude -8–2 | Coordinates are within the observed Great Britain screening bounds                  | Retain missingness; do not spatially model     |
| Date/time              | 0 parse failures                                              | Temporal strings are structurally valid                                             | Derive fields inside pipeline                  |
| Coded fields           | 0 values below `-1`                                           | No unexpected lower sentinel was detected                                           | Assert lower bound; codebook still required    |

The checks are validation guards, not proof that every value is semantically correct. IQR outliers from Phase 2 are retained because an unusual value is not automatically erroneous.

## 9. Leakage Prevention

The following fields are blocked from predictor input:

| Feature/group                                                               | Risk                              | Evidence                                    | Decision                                   |
| --------------------------------------------------------------------------- | --------------------------------- | ------------------------------------------- | ------------------------------------------ |
| `collision_severity`                                                        | Target leakage                    | Label being predicted                       | Target only                                |
| `enhanced_severity_collision`                                               | Direct/near-direct target leakage | Severity-derived field name and role        | Exclude                                    |
| `collision_injury_based`                                                    | Outcome leakage                   | Injury-derived field                        | Exclude                                    |
| `collision_adjusted_severity_serious`, `collision_adjusted_severity_slight` | Adjusted target leakage           | Severity adjustment fields                  | Exclude                                    |
| `number_of_casualties`                                                      | Post-event consequence            | Casualty count can be known after collision | Exclude pending explicit post-event design |
| `did_police_officer_attend_scene_of_accident`                               | Availability leakage              | Attendance may be recorded after response   | Exclude pending timing confirmation        |
| Identifiers                                                                 | Memorization/proxy risk           | Unique or near-unique record codes          | Exclude                                    |

`number_of_vehicles`, location, and administrative fields remain timing/generalization review items. No leakage claim is made solely from association; the decision follows availability and field semantics.

## 10. Temporal Feature Preparation

Derived fields are created in the preparation pipeline, after the source split rule is applied and without modifying the raw CSV:

| Derived field | Source | Rule                                          | Status             |
| ------------- | ------ | --------------------------------------------- | ------------------ |
| `month`       | `date` | Parse `%d/%m/%Y`, extract calendar month 1–12 | Approved candidate |
| `hour`        | `time` | Parse `%H:%M`, extract hour 0–23              | Approved candidate |

`collision_year` is retained for temporal splitting and monitoring. Raw `date` and `time` are not passed directly as unparsed predictors. No future or post-event temporal feature is created. Day-code decoding must use the official guide; no weekday label is guessed.

## 11. Categorical Preparation

Treat coded categorical fields as categorical, even when stored as integers. Preserve code values and sentinel categories until codebook verification. Candidate low-cardinality fields include road/environment/junction codes and `day_of_week`; high-cardinality administrative/geographic fields require explicit review.

For the eventual pipeline:

- fit an explicit-missing or most-frequent imputer on training data only;
- fit the encoder on training data only and define an unknown-category policy for validation/test;
- use sparse one-hot output where appropriate;
- do not merge rare categories before measuring their support and verifying their meanings;
- document any later rare-category grouping as a modeling/preparation decision with a threshold and rationale.

## 12. Numerical Preparation

Candidate measurement/count fields are `number_of_vehicles`, `number_of_casualties`, and geographic coordinates; `speed_limit` is a coded/ordinal candidate rather than an unrestricted continuous measurement. Preserve extreme values pending domain review.

For a later estimator that needs scaling, fit the scaler on training data only and apply it unchanged to validation/test. Tree-based estimators may not require scaling; distance-based clustering would require a separate, explicitly documented scaling path. No scaler is fitted in Phase 3.

## 13. Geographic Features

Status: **REVIEW**, not final KEEP or EXCLUDE.

The four coordinate fields share the same 53 missing records. Do not use all four automatically because OSGR and latitude/longitude are alternative representations. Before modeling, confirm assignment/privacy policy, choose at most one representation, assess generalization across years/areas, and fit any imputation using training data only. `lsoa_of_accident_location` is a high-cardinality geographic/administrative code and remains review-only. No spatial model or geographic clustering is performed in Phase 3.

## 14. Train/Test Strategy

The use case and assessment rule are still open, so this is a provisional recommendation:

| Strategy                                                 | Strength                                                          | Risk                                                         | Status                         |
| -------------------------------------------------------- | ----------------------------------------------------------------- | ------------------------------------------------------------ | ------------------------------ |
| Stratified random split                                  | Comparable to legacy and preserves rare class proportions         | Can mix temporal regimes and overstate future generalization | Benchmark option               |
| Temporal holdout: 2021–2024 development, 2025 final test | Tests future-year generalization and avoids future-to-past mixing | Requires a use case where future-year prediction is intended | Recommended provisional option |

Use the temporal holdout if the task is prediction using information available at the time of collision and future generalization matters. Otherwise, obtain the academic requirement before finalizing the split. In either case, split before fitting any imputer, encoder, scaler, or other learned transform. Never create the final dataset by sampling 10K.

## 15. Preprocessing Pipeline

The eventual implementation should follow this order:

1. Read the raw full dataset and assert schema, row count, target values, and raw checksum.
2. Parse/validate `date` and `time`; derive `month` and `hour` without changing raw columns.
3. Preserve `collision_index` for traceability and remove identifiers/leakage fields from predictor input.
4. Apply the approved temporal or random split using full-dataset rows.
5. Fit numeric imputation and optional scaling on training rows only.
6. Fit categorical missing handling and encoder on training rows only with explicit unknown handling.
7. Transform validation/test with the fitted training objects.
8. Record schema, feature roles, excluded fields, split rule, counts, codebook version, and dependency versions in a manifest.

No learned preprocessing object or processed CSV is created by this documentation-only Phase 3 checkpoint.

## 16. Data Preparation Decisions

1. Use all 513,801 raw records; retain the legacy 10K only for historical comparison.
2. Preserve all raw columns and do not delete rows for coordinate missingness or IQR flags.
3. Keep the target as three unbalanced classes; postpone balancing to modeling/evaluation.
4. Exclude identifiers and outcome/severity-derived fields from predictor input.
5. Preserve unresolved codes rather than inventing labels or merging categories.
6. Derive only `month` and `hour`, inside a reproducible pipeline.
7. Keep geographic fields and administrative fields in REVIEW pending use-case, privacy, and codebook decisions.
8. Use temporal holdout as the provisional recommendation; obtain academic confirmation before locking it.
9. Require all learned transforms to be fitted on training data only.

## 17. Risks

- Prediction timing is unresolved, so availability-based leakage exclusions may change.
- The local mapping does not provide a complete official codebook for all fields.
- Sentinel values can be confused with valid zeros or ordinary numeric values.
- Class imbalance may require later training-only weighting or resampling.
- Rare and high-cardinality geographic/administrative categories may overfit.
- The 2025 data may differ in collection or reporting from earlier years; temporal drift must be evaluated later.

## 18. Open Questions

1. Which official data guide version should be frozen for the project manifest?
2. Is the assignment use case pre-event, at-scene, or post-event prediction?
3. Are `number_of_casualties` and police attendance allowed under that timing? The conservative default is exclusion.
4. Are geographic and administrative features permitted and acceptable for privacy/generalization?
5. Should 2025 be the final test year, or does the academic rubric require a stratified random split?
6. Which data-mining roles are mandatory, and does the association task require a dedicated transaction representation?

## 19. Next Phase

**PHASE 5 – MODELING:** use this preparation contract and `docs/FEATURE_SELECTION.md` to evaluate approved algorithms and provisional feature sets. Do not use the final holdout for feature selection.
