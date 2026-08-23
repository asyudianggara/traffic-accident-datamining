from __future__ import annotations

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.metrics import (
    calinski_harabasz_score,
    davies_bouldin_score,
    silhouette_score,
)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


RANDOM_STATE = 42
YEARS = [2021, 2022, 2023, 2024, 2025]
K_VALUES = [2, 3, 4, 5, 6]

ROOT = Path(__file__).resolve().parent
DATA_PATH = ROOT / "data" / "raw" / "dft-road-casualty-statistics-collision-last-5-years.csv"
MAPPING_PATH = ROOT / "data" / "processed" / "stats19_maps.json"
RESULTS_DIR = ROOT / "results"

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
FORBIDDEN_FEATURES = {
    "collision_severity",
    "number_of_casualties",
    "did_police_officer_attend_scene_of_accident",
    "collision_index",
    "collision_ref_no",
    "police_force",
    "local_authority_district",
    "local_authority_ons_district",
    "local_authority_highway",
    "local_authority_highway_current",
    "lsoa_of_accident_location",
}


def load_clustering_data() -> pd.DataFrame:
    df = pd.read_csv(DATA_PATH, low_memory=False)

    df_sample = (
        df[df["collision_year"].isin(YEARS)]
        .groupby("collision_year", group_keys=False)
        .sample(n=2000, random_state=RANDOM_STATE)
        .reset_index(drop=True)
    )

    df_sample["hour"] = pd.to_datetime(
        df_sample["time"], format="%H:%M", errors="coerce"
    ).dt.hour
    df_sample["month"] = pd.to_datetime(
        df_sample["date"], dayfirst=True, errors="coerce"
    ).dt.month

    with MAPPING_PATH.open("r", encoding="utf-8") as mapping_file:
        stats19_maps = json.load(mapping_file)

    # Decode only selected clustering features. The target and outcome columns
    # are not selected, transformed, or used anywhere in this script.
    df_decoded = df_sample.copy()
    for column in FEATURES:
        if column in stats19_maps:
            df_decoded[column] = df_decoded[column].astype(str).map(stats19_maps[column])

    if len(FEATURES) != 18:
        raise RuntimeError(f"Expected 18 clustering features, got {len(FEATURES)}")
    if set(FEATURES) & FORBIDDEN_FEATURES:
        raise RuntimeError("Forbidden target, outcome, identifier, or administrative feature detected")

    return df_decoded[FEATURES].copy()


def build_preprocessor() -> ColumnTransformer:
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
                    sparse_output=False,
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


def main() -> None:
    X_cluster = load_clustering_data()

    preprocessor = build_preprocessor()
    X_encoded = preprocessor.fit_transform(X_cluster)

    rows = []
    for k in K_VALUES:
        kmeans = KMeans(
            n_clusters=k,
            random_state=RANDOM_STATE,
            n_init=10,
        )
        labels = kmeans.fit_predict(X_encoded)

        rows.append(
            {
                "k": k,
                "inertia": float(kmeans.inertia_),
                "silhouette": float(silhouette_score(X_encoded, labels)),
                "davies_bouldin": float(davies_bouldin_score(X_encoded, labels)),
                "calinski_harabasz": float(calinski_harabasz_score(X_encoded, labels)),
            }
        )

    evaluation_df = pd.DataFrame(rows)
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    evaluation_df.to_csv(RESULTS_DIR / "clustering_k_evaluation.csv", index=False)

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(evaluation_df["k"], evaluation_df["inertia"], marker="o")
    ax.set_title("K-Means Elbow Evaluation")
    ax.set_xlabel("Number of clusters (k)")
    ax.set_ylabel("Inertia")
    ax.set_xticks(K_VALUES)
    ax.grid(alpha=0.25)
    fig.tight_layout()
    fig.savefig(RESULTS_DIR / "clustering_elbow.png", dpi=160)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(evaluation_df["k"], evaluation_df["silhouette"], marker="o")
    ax.set_title("K-Means Silhouette Evaluation")
    ax.set_xlabel("Number of clusters (k)")
    ax.set_ylabel("Silhouette Score")
    ax.set_xticks(K_VALUES)
    ax.grid(alpha=0.25)
    fig.tight_layout()
    fig.savefig(RESULTS_DIR / "clustering_silhouette.png", dpi=160)
    plt.close(fig)

    print(f"Clustering rows: {len(X_cluster)}")
    print(f"Original clustering features: {len(FEATURES)}")
    print(f"Encoded feature count: {X_encoded.shape[1]}")
    print("\nEvaluation k=2..6:")
    print(evaluation_df.to_string(index=False))
    print("\nBest silhouette k:", int(evaluation_df.loc[evaluation_df["silhouette"].idxmax(), "k"]))
    print("Best Davies-Bouldin k:", int(evaluation_df.loc[evaluation_df["davies_bouldin"].idxmin(), "k"]))
    print("Best Calinski-Harabasz k:", int(evaluation_df.loc[evaluation_df["calinski_harabasz"].idxmax(), "k"]))
    print("\nSaved:")
    print(RESULTS_DIR / "clustering_k_evaluation.csv")
    print(RESULTS_DIR / "clustering_elbow.png")
    print(RESULTS_DIR / "clustering_silhouette.png")


if __name__ == "__main__":
    main()
