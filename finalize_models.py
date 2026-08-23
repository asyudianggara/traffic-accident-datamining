from __future__ import annotations

import json
import shutil
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    precision_score,
    recall_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


RANDOM_STATE = 42
YEARS = [2021, 2022, 2023, 2024, 2025]
LABELS = ["Fatal", "Serious", "Slight"]
EXPECTED_ENCODED_CLASSIFICATION = 105
EXPECTED_ENCODED_CLUSTERING = 108
EXPECTED_CLASSIFICATION_METRICS = {
    "accuracy": 0.6385,
    "macro_precision": 0.3802,
    "macro_recall": 0.4008,
    "macro_f1": 0.3862,
    "weighted_f1": 0.6496,
}
METRIC_TOLERANCE = 0.005

ROOT = Path(__file__).resolve().parent
DATA_PATH = ROOT / "data" / "raw" / "dft-road-casualty-statistics-collision-last-5-years.csv"
MAPPING_PATH = ROOT / "data" / "processed" / "stats19_maps.json"
RESULTS_DIR = ROOT / "results"
MODELS_DIR = ROOT / "models"

NUMERIC_FEATURES = [
    "number_of_vehicles",
    "speed_limit",
    "hour",
    "month",
]
CATEGORICAL_FEATURES = [
    "day_of_week",
    "first_road_class",
    "road_type",
    "junction_detail",
    "junction_control",
    "second_road_class",
    "pedestrian_crossing",
    "light_conditions",
    "weather_conditions",
    "road_surface_conditions",
    "special_conditions_at_site",
    "carriageway_hazards",
    "urban_or_rural_area",
    "trunk_road_flag",
]
FEATURES = NUMERIC_FEATURES + CATEGORICAL_FEATURES
TARGET = "collision_severity"
FORBIDDEN_FEATURES = {
    TARGET,
    "number_of_casualties",
    "collision_index",
    "collision_ref_no",
    "identifier",
    "police_force",
    "did_police_officer_attend_scene_of_accident",
}


def assert_feature_contract() -> None:
    if len(NUMERIC_FEATURES) != 4 or len(CATEGORICAL_FEATURES) != 14:
        raise RuntimeError("The final feature contract must contain 4 numeric and 14 categorical features")
    if len(FEATURES) != 18 or len(set(FEATURES)) != 18:
        raise RuntimeError(f"Expected exactly 18 unique features, got {len(FEATURES)}")
    if set(FEATURES) & FORBIDDEN_FEATURES:
        raise RuntimeError("Target, outcome, identifier, or forbidden administrative feature detected")


def load_source_data() -> tuple[pd.DataFrame, dict]:
    df = pd.read_csv(DATA_PATH, low_memory=False)
    with MAPPING_PATH.open("r", encoding="utf-8") as mapping_file:
        mappings = json.load(mapping_file)
    return df, mappings


def make_sample(df: pd.DataFrame, mappings: dict) -> pd.DataFrame:
    sample = (
        df[df["collision_year"].isin(YEARS)]
        .groupby("collision_year", group_keys=False)
        .sample(n=2000, random_state=RANDOM_STATE)
        .reset_index(drop=True)
    )
    if len(sample) != 10000:
        raise RuntimeError(f"Expected 10,000 sampled rows, got {len(sample)}")

    sample["hour"] = pd.to_datetime(
        sample["time"], format="%H:%M", errors="coerce"
    ).dt.hour
    sample["month"] = pd.to_datetime(
        sample["date"], dayfirst=True, errors="coerce"
    ).dt.month

    decoded = sample.copy()
    for column, mapping in mappings.items():
        if column in decoded.columns:
            decoded[column] = decoded[column].astype(str).map(mapping)
    return decoded


def build_preprocessor(*, sparse_output: bool) -> ColumnTransformer:
    numeric_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )
    categorical_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            (
                "encoder",
                OneHotEncoder(
                    handle_unknown="ignore",
                    sparse_output=sparse_output,
                ),
            ),
        ]
    )
    return ColumnTransformer(
        transformers=[
            ("num", numeric_pipeline, NUMERIC_FEATURES),
            ("cat", categorical_pipeline, CATEGORICAL_FEATURES),
        ]
    )


def prepare_classification_data(
    decoded: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    X = decoded[FEATURES].copy()
    y = decoded[TARGET].copy()
    if y.isna().any():
        raise RuntimeError("Missing collision_severity values in classification data")
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=RANDOM_STATE,
        stratify=y,
    )
    if (len(X_train), len(X_test)) != (8000, 2000):
        raise RuntimeError(f"Expected train/test sizes 8000/2000, got {len(X_train)}/{len(X_test)}")
    return X_train, X_test, y_train, y_test


def train_and_validate_classification(
    decoded: pd.DataFrame,
) -> dict:
    X_train, X_test, y_train, y_test = prepare_classification_data(decoded)
    preprocessor = build_preprocessor(sparse_output=True)
    X_train_encoded = preprocessor.fit_transform(X_train)
    X_test_encoded = preprocessor.transform(X_test)
    feature_names = preprocessor.get_feature_names_out()
    if len(feature_names) != EXPECTED_ENCODED_CLASSIFICATION:
        raise RuntimeError(
            f"Expected 105 classification encoded features, got {len(feature_names)}"
        )

    model = RandomForestClassifier(
        n_estimators=300,
        max_depth=15,
        class_weight="balanced",
        random_state=RANDOM_STATE,
        n_jobs=-1,
    )
    model.fit(X_train_encoded, y_train)
    y_pred = model.predict(X_test_encoded)
    metrics = {
        "accuracy": float(accuracy_score(y_test, y_pred)),
        "macro_precision": float(
            precision_score(y_test, y_pred, labels=LABELS, average="macro", zero_division=0)
        ),
        "macro_recall": float(
            recall_score(y_test, y_pred, labels=LABELS, average="macro", zero_division=0)
        ),
        "macro_f1": float(
            f1_score(y_test, y_pred, labels=LABELS, average="macro", zero_division=0)
        ),
        "weighted_f1": float(
            f1_score(y_test, y_pred, labels=LABELS, average="weighted", zero_division=0)
        ),
    }
    differences = {
        name: abs(metrics[name] - expected)
        for name, expected in EXPECTED_CLASSIFICATION_METRICS.items()
    }
    if any(value > METRIC_TOLERANCE for value in differences.values()):
        raise RuntimeError(
            "Classification metrics differ materially from the audited notebook: "
            + json.dumps({"actual": metrics, "expected": EXPECTED_CLASSIFICATION_METRICS, "difference": differences})
        )

    candidate_model = MODELS_DIR / "final_random_forest.candidate.joblib"
    candidate_preprocessor = MODELS_DIR / "final_preprocessor.candidate.joblib"
    joblib.dump(model, candidate_model)
    joblib.dump(preprocessor, candidate_preprocessor)

    loaded_model = joblib.load(candidate_model)
    loaded_preprocessor = joblib.load(candidate_preprocessor)
    loaded_train = loaded_preprocessor.transform(X_train)
    loaded_test = loaded_preprocessor.transform(X_test)
    if len(loaded_preprocessor.get_feature_names_out()) != EXPECTED_ENCODED_CLASSIFICATION:
        raise RuntimeError("Loaded classification preprocessor does not expose 105 features")
    if getattr(loaded_model, "n_features_in_", None) != EXPECTED_ENCODED_CLASSIFICATION:
        raise RuntimeError("Loaded classification model does not expect 105 features")
    smoke_predictions = loaded_model.predict(loaded_test[:5])
    if len(smoke_predictions) != 5 or loaded_train.shape[1] != EXPECTED_ENCODED_CLASSIFICATION:
        raise RuntimeError("Classification artifact smoke test failed")

    metadata = {
        "model": "RandomForestClassifier",
        "target": TARGET,
        "feature_count_original": 18,
        "feature_count_encoded": EXPECTED_ENCODED_CLASSIFICATION,
        "numeric_features": NUMERIC_FEATURES,
        "categorical_features": CATEGORICAL_FEATURES,
        "train_size": int(len(X_train)),
        "test_size": int(len(X_test)),
        "random_state": RANDOM_STATE,
        "n_estimators": 300,
        "max_depth": 15,
        "class_weight": "balanced",
        "metrics": metrics,
    }
    print("Classification validation: PASS")
    print(json.dumps({"metrics": metrics, "encoded_features": len(feature_names)}, indent=2))
    return {
        "model": model,
        "preprocessor": preprocessor,
        "metadata": metadata,
        "candidate_model": candidate_model,
        "candidate_preprocessor": candidate_preprocessor,
    }


def validate_c4_assignments(labels: np.ndarray) -> None:
    assignment_path = RESULTS_DIR / "clustering_final_assignments.csv"
    if not assignment_path.exists():
        raise RuntimeError(f"Missing audited C4 assignment file: {assignment_path}")
    existing = pd.read_csv(assignment_path, usecols=["cluster"])
    existing_labels = existing["cluster"].to_numpy(dtype=int)
    if len(existing_labels) != 10000:
        raise RuntimeError(f"Expected 10,000 audited C4 assignments, got {len(existing_labels)}")
    if not np.array_equal(labels.astype(int), existing_labels):
        raise RuntimeError("New K-Means assignments do not exactly match the audited C4 assignments")
    counts = pd.Series(labels).value_counts().sort_index().to_dict()
    if counts != {0: 2528, 1: 7472}:
        raise RuntimeError(f"Unexpected C4 cluster counts: {counts}")


def train_and_validate_clustering(decoded: pd.DataFrame) -> dict:
    X_cluster = decoded[FEATURES].copy()
    preprocessor = build_preprocessor(sparse_output=False)
    X_encoded = preprocessor.fit_transform(X_cluster)
    feature_names = preprocessor.get_feature_names_out()
    if len(feature_names) != EXPECTED_ENCODED_CLUSTERING:
        raise RuntimeError(
            f"Expected 108 clustering encoded features, got {len(feature_names)}"
        )

    model = KMeans(n_clusters=2, random_state=RANDOM_STATE, n_init=10)
    labels = model.fit_predict(X_encoded)
    validate_c4_assignments(labels)

    candidate_model = MODELS_DIR / "final_kmeans.candidate.joblib"
    candidate_preprocessor = MODELS_DIR / "final_clustering_preprocessor.candidate.joblib"
    joblib.dump(model, candidate_model)
    joblib.dump(preprocessor, candidate_preprocessor)

    loaded_model = joblib.load(candidate_model)
    loaded_preprocessor = joblib.load(candidate_preprocessor)
    loaded_encoded = loaded_preprocessor.transform(X_cluster)
    loaded_labels = loaded_model.predict(loaded_encoded)
    if loaded_encoded.shape[0] != 10000 or loaded_encoded.shape[1] != EXPECTED_ENCODED_CLUSTERING:
        raise RuntimeError("Loaded clustering artifact has an unexpected transformed shape")
    if sorted(np.unique(loaded_labels).tolist()) != [0, 1]:
        raise RuntimeError("Loaded clustering artifact did not produce labels 0 and 1")
    validate_c4_assignments(loaded_labels)

    metadata = {
        "algorithm": "KMeans",
        "n_clusters": 2,
        "random_state": RANDOM_STATE,
        "n_init": 10,
        "feature_count_original": 18,
        "feature_count_encoded": EXPECTED_ENCODED_CLUSTERING,
        "numeric_features": NUMERIC_FEATURES,
        "categorical_features": CATEGORICAL_FEATURES,
        "sample_size": 10000,
        "cluster_0_count": 2528,
        "cluster_1_count": 7472,
    }
    print("Clustering validation: PASS")
    print(json.dumps({"encoded_features": len(feature_names), "cluster_counts": {"0": 2528, "1": 7472}}, indent=2))
    return {
        "model": model,
        "preprocessor": preprocessor,
        "metadata": metadata,
        "candidate_model": candidate_model,
        "candidate_preprocessor": candidate_preprocessor,
    }


def backup_old_artifact(final_path: Path, legacy_path: Path, expected_features: int) -> str:
    if not final_path.exists():
        return "missing"
    old = joblib.load(final_path)
    old_features = getattr(old, "n_features_in_", None)
    if old_features == expected_features:
        return "already-compatible"
    if legacy_path.exists():
        raise RuntimeError(
            f"Refusing to overwrite existing legacy backup: {legacy_path}"
        )
    shutil.move(str(final_path), str(legacy_path))
    return "backed-up"


def commit_artifacts(classification: dict, clustering: dict) -> dict:
    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    model_backup = backup_old_artifact(
        MODELS_DIR / "final_random_forest.joblib",
        MODELS_DIR / "final_random_forest_legacy_21_features.joblib",
        EXPECTED_ENCODED_CLASSIFICATION,
    )
    preprocessor_backup = backup_old_artifact(
        MODELS_DIR / "final_preprocessor.joblib",
        MODELS_DIR / "final_preprocessor_legacy_21_features.joblib",
        EXPECTED_ENCODED_CLASSIFICATION,
    )

    os_replace_pairs = [
        (classification["candidate_model"], MODELS_DIR / "final_random_forest.joblib"),
        (classification["candidate_preprocessor"], MODELS_DIR / "final_preprocessor.joblib"),
        (clustering["candidate_model"], MODELS_DIR / "final_kmeans.joblib"),
        (clustering["candidate_preprocessor"], MODELS_DIR / "final_clustering_preprocessor.joblib"),
    ]
    for source, destination in os_replace_pairs:
        source.replace(destination)

    classification_metadata_path = MODELS_DIR / "final_classification_metadata.json"
    clustering_metadata_path = MODELS_DIR / "final_clustering_metadata.json"
    classification_metadata_path.write_text(
        json.dumps(classification["metadata"], indent=2) + "\n",
        encoding="utf-8",
    )
    clustering_metadata_path.write_text(
        json.dumps(clustering["metadata"], indent=2) + "\n",
        encoding="utf-8",
    )
    return {
        "classification_model_backup": model_backup,
        "classification_preprocessor_backup": preprocessor_backup,
    }


def main() -> None:
    assert_feature_contract()
    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    df, mappings = load_source_data()
    decoded = make_sample(df, mappings)

    classification = train_and_validate_classification(decoded)
    clustering = train_and_validate_clustering(decoded)
    backups = commit_artifacts(classification, clustering)

    print("\nFINAL MODEL ARTIFACT: PASS")
    print("Classification:")
    print(f"  original features = 18")
    print(f"  encoded features = {classification['metadata']['feature_count_encoded']}")
    print(f"  train size = {classification['metadata']['train_size']}")
    print(f"  test size = {classification['metadata']['test_size']}")
    for key, value in classification["metadata"]["metrics"].items():
        print(f"  {key} = {value:.12f}")
    print("  model file = models/final_random_forest.joblib")
    print("  preprocessor file = models/final_preprocessor.joblib")
    print("Clustering:")
    print("  original features = 18")
    print("  encoded features = 108")
    print("  k = 2")
    print("  random_state = 42")
    print("  n_init = 10")
    print("  cluster 0 = 2528")
    print("  cluster 1 = 7472")
    print("  model file = models/final_kmeans.joblib")
    print("  preprocessor file = models/final_clustering_preprocessor.joblib")
    print("Artifact checks:")
    print("  classification save/load = PASS")
    print("  classification 105 encoded features = PASS")
    print("  clustering save/load = PASS")
    print("  clustering 108 encoded features = PASS")
    print("  clustering 10,000 assignments = PASS")
    print("Legacy backup status:")
    print(f"  random forest = {backups['classification_model_backup']}")
    print(f"  preprocessor = {backups['classification_preprocessor_backup']}")


if __name__ == "__main__":
    main()
