"""Build and validate the Phase 3 preparation contract.

The script reads the immutable full raw CSV, derives only ``month`` and
``hour`` in memory, fits learned preprocessing on 2021-2024 rows, and
transforms the untouched 2025 holdout. It deliberately writes only a small
validation manifest; no processed dataset or model is produced.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pandas as pd
import sklearn
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder


RANDOM_STATE = 42
ROOT = Path(__file__).resolve().parent
DATA_PATH = ROOT / "data" / "raw" / "dft-road-casualty-statistics-collision-last-5-years.csv"
MANIFEST_PATH = ROOT / "results" / "phase3_preparation_validation.json"
TARGET = "collision_severity"

CLASSIFICATION_FEATURES = [
    "number_of_vehicles", "speed_limit", "first_road_class", "road_type",
    "junction_detail", "junction_control", "second_road_class",
    "pedestrian_crossing", "light_conditions", "weather_conditions",
    "road_surface_conditions", "special_conditions_at_site",
    "carriageway_hazards", "urban_or_rural_area", "trunk_road_flag",
    "day_of_week", "month", "hour",
]
CLUSTERING_FEATURES = CLASSIFICATION_FEATURES.copy()
NUMERIC_FEATURES = ["number_of_vehicles"]
CATEGORICAL_FEATURES = [
    feature for feature in CLASSIFICATION_FEATURES if feature not in NUMERIC_FEATURES
]
EXPECTED_COLUMNS = [
    "collision_index", "collision_year", "collision_ref_no",
    "location_easting_osgr", "location_northing_osgr", "longitude", "latitude",
    "police_force", "collision_severity", "number_of_vehicles",
    "number_of_casualties", "date", "day_of_week", "time",
    "local_authority_district", "local_authority_ons_district",
    "local_authority_highway", "local_authority_highway_current",
    "first_road_class", "first_road_number", "road_type",
    "speed_limit", "junction_detail_historic", "junction_detail",
    "junction_control", "second_road_class", "second_road_number",
    "pedestrian_crossing_human_control_historic",
    "pedestrian_crossing_physical_facilities_historic", "pedestrian_crossing",
    "light_conditions", "weather_conditions", "road_surface_conditions",
    "special_conditions_at_site", "carriageway_hazards_historic",
    "carriageway_hazards", "urban_or_rural_area",
    "did_police_officer_attend_scene_of_accident", "trunk_road_flag",
    "lsoa_of_accident_location", "enhanced_severity_collision",
    "collision_injury_based", "collision_adjusted_severity_serious",
    "collision_adjusted_severity_slight",
]
EXCLUDED_FROM_PREDICTORS = [
    "collision_index", "collision_ref_no", TARGET, "number_of_casualties",
    "date", "time", "enhanced_severity_collision", "collision_injury_based",
    "collision_adjusted_severity_serious", "collision_adjusted_severity_slight",
    "did_police_officer_attend_scene_of_accident",
]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def build_preprocessor() -> ColumnTransformer:
    numeric = Pipeline([("imputer", SimpleImputer(strategy="median"))])
    categorical = Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("onehot", OneHotEncoder(handle_unknown="ignore", sparse_output=True)),
    ])
    return ColumnTransformer([
        ("numeric", numeric, NUMERIC_FEATURES),
        ("categorical", categorical, CATEGORICAL_FEATURES),
    ])


def prepare() -> dict:
    source_hash_before = sha256(DATA_PATH)
    raw = pd.read_csv(DATA_PATH, low_memory=False)
    if list(raw.columns) != EXPECTED_COLUMNS:
        raise AssertionError("Raw schema differs from the verified 44-column contract")
    if raw.shape != (513801, 44):
        raise AssertionError(f"Unexpected raw shape: {raw.shape}")
    if raw[TARGET].isna().any() or not set(raw[TARGET].unique()) <= {1, 2, 3}:
        raise AssertionError("Target is missing or contains unexpected classes")

    prepared = raw.copy()
    prepared["month"] = pd.to_datetime(
        prepared["date"], format="%d/%m/%Y", errors="raise"
    ).dt.month
    prepared["hour"] = pd.to_datetime(
        prepared["time"], format="%H:%M", errors="raise"
    ).dt.hour

    train = prepared[prepared["collision_year"] <= 2024]
    test = prepared[prepared["collision_year"] == 2025]
    if len(train) != 412276 or len(test) != 101525:
        raise AssertionError(f"Unexpected temporal split: {len(train)} / {len(test)}")

    forbidden = set(EXCLUDED_FROM_PREDICTORS)
    if forbidden.intersection(CLASSIFICATION_FEATURES):
        raise AssertionError("Leakage or identifier field entered predictor contract")
    if set(CLASSIFICATION_FEATURES) != set(CLUSTERING_FEATURES):
        raise AssertionError("Classification and clustering contracts diverged")

    x_train = train[CLASSIFICATION_FEATURES].copy()
    x_test = test[CLASSIFICATION_FEATURES].copy()
    # Coded values, including -1 sentinels, remain categorical strings.
    for column in CATEGORICAL_FEATURES:
        x_train[column] = x_train[column].astype("string")
        x_test[column] = x_test[column].astype("string")

    preprocessor = build_preprocessor()
    encoded_train = preprocessor.fit_transform(x_train)
    encoded_test = preprocessor.transform(x_test)
    encoded_train_repeat = preprocessor.transform(x_train)
    if encoded_train.shape != encoded_train_repeat.shape:
        raise AssertionError("Repeated transformation changed encoded shape")
    if encoded_train.shape[1] != encoded_test.shape[1]:
        raise AssertionError("Train/test encoded feature counts differ")
    if pd.isna(encoded_train.data).any() or pd.isna(encoded_test.data).any():
        raise AssertionError("Encoded output contains missing values")

    source_hash_after = sha256(DATA_PATH)
    if source_hash_before != source_hash_after:
        raise AssertionError("Raw dataset changed while preparation was running")

    return {
        "phase": "3",
        "source": str(DATA_PATH.relative_to(ROOT)).replace("\\", "/"),
        "source_sha256": source_hash_before,
        "raw_shape": [int(raw.shape[0]), int(raw.shape[1])],
        "target": TARGET,
        "target_classes": {str(key): int(value) for key, value in raw[TARGET].value_counts().sort_index().items()},
        "split": {"rule": "collision_year <= 2024 train; collision_year == 2025 test", "train_rows": len(train), "test_rows": len(test)},
        "classification_features": CLASSIFICATION_FEATURES,
        "clustering_features": CLUSTERING_FEATURES,
        "numeric_features": NUMERIC_FEATURES,
        "categorical_features": CATEGORICAL_FEATURES,
        "excluded_predictors": EXCLUDED_FROM_PREDICTORS,
        "sentinel_policy": "preserve coded -1 values; categorical fields are not relabeled or collapsed",
        "missing_policy": "training-fitted median for numeric and most-frequent for categorical; no rows dropped",
        "encoded_shape": {"train": list(encoded_train.shape), "test": list(encoded_test.shape)},
        "train_test_feature_count_consistent": True,
        "repeated_transform_shape_consistent": True,
        "raw_unchanged_during_run": True,
        "sklearn_version": sklearn.__version__,
        "random_state": RANDOM_STATE,
        "artifacts_written": [str(MANIFEST_PATH.relative_to(ROOT)).replace("\\", "/")],
    }


def main() -> None:
    manifest = prepare()
    MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST_PATH.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
