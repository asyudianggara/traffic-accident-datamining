from __future__ import annotations

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.compose import ColumnTransformer
from sklearn.decomposition import PCA
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


RANDOM_STATE = 42
FINAL_K = 2
YEARS = [2021, 2022, 2023, 2024, 2025]

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
    "collision_index",
    "collision_ref_no",
    "police_force",
    "local_authority_district",
    "local_authority_ons_district",
    "local_authority_highway",
    "local_authority_highway_current",
    "lsoa_of_accident_location",
    "did_police_officer_attend_scene_of_accident",
}


def load_clustering_features() -> pd.DataFrame:
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

    df_decoded = df_sample.copy()
    for column in FEATURES:
        if column in stats19_maps:
            df_decoded[column] = df_decoded[column].astype(str).map(stats19_maps[column])

    if len(FEATURES) != 18:
        raise RuntimeError(f"Expected 18 clustering features, got {len(FEATURES)}")
    if set(FEATURES) & FORBIDDEN_FEATURES:
        raise RuntimeError("Forbidden target, outcome, identifier, or administrative feature detected")

    feature_frame = df_decoded[FEATURES].copy()
    if len(feature_frame) != 10000:
        raise RuntimeError(f"Expected 10,000 clustering rows, got {len(feature_frame)}")

    return feature_frame


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
                OneHotEncoder(handle_unknown="ignore", sparse_output=False),
            ),
        ]
    )

    return ColumnTransformer(
        transformers=[
            ("num", numeric_pipeline, NUMERIC_FEATURES),
            ("cat", categorical_pipeline, CATEGORICAL_FEATURES),
        ]
    )


def make_cluster_size_table(assignments: pd.DataFrame) -> pd.DataFrame:
    sizes = assignments["cluster"].value_counts().sort_index().rename("count")
    result = sizes.to_frame().reset_index().rename(columns={"index": "cluster"})
    result["percentage"] = result["count"] / len(assignments) * 100
    return result


def make_numeric_profile(assignments: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for cluster_id, group in assignments.groupby("cluster", sort=True):
        for feature in NUMERIC_FEATURES:
            values = group[feature]
            rows.append(
                {
                    "cluster": int(cluster_id),
                    "feature": feature,
                    "count": int(values.count()),
                    "mean": float(values.mean()),
                    "median": float(values.median()),
                    "min": float(values.min()),
                    "max": float(values.max()),
                }
            )
    return pd.DataFrame(rows)


def make_categorical_profile(assignments: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for cluster_id, group in assignments.groupby("cluster", sort=True):
        cluster_size = len(group)
        for feature in CATEGORICAL_FEATURES:
            values = group[feature].astype(object)
            values = values.where(values.notna(), "Missing")
            counts = values.value_counts(dropna=False)
            dominant_category = counts.index[0]
            dominant_count = int(counts.iloc[0])
            rows.append(
                {
                    "cluster": int(cluster_id),
                    "feature": feature,
                    "dominant_category": str(dominant_category),
                    "dominant_count": dominant_count,
                    "dominant_percentage": dominant_count / cluster_size * 100,
                }
            )
    return pd.DataFrame(rows)


def make_feature_comparison(
    assignments: pd.DataFrame,
    numeric_profile: pd.DataFrame,
    categorical_profile: pd.DataFrame,
) -> pd.DataFrame:
    rows = []

    for feature in NUMERIC_FEATURES:
        profile = numeric_profile[numeric_profile["feature"] == feature].set_index("cluster")
        cluster_0_mean = float(profile.loc[0, "mean"])
        cluster_1_mean = float(profile.loc[1, "mean"])
        mean_difference = cluster_1_mean - cluster_0_mean
        rows.append(
            {
                "Feature": feature,
                "Type": "numeric",
                "Cluster 0": f"mean={cluster_0_mean:.4f}; median={profile.loc[0, 'median']:.4f}",
                "Cluster 1": f"mean={cluster_1_mean:.4f}; median={profile.loc[1, 'median']:.4f}",
                "Perbedaan/Keterangan": f"mean Cluster 1 - Cluster 0 = {mean_difference:.4f}",
            }
        )

    for feature in CATEGORICAL_FEATURES:
        profile = categorical_profile[categorical_profile["feature"] == feature].set_index("cluster")
        category_0 = profile.loc[0, "dominant_category"]
        category_1 = profile.loc[1, "dominant_category"]
        percentage_0 = float(profile.loc[0, "dominant_percentage"])
        percentage_1 = float(profile.loc[1, "dominant_percentage"])
        if category_0 == category_1:
            note = f"kategori dominan sama; selisih proporsi = {percentage_1 - percentage_0:.4f} percentage points"
        else:
            note = "kategori dominan berbeda"
        rows.append(
            {
                "Feature": feature,
                "Type": "categorical",
                "Cluster 0": f"{category_0} ({percentage_0:.4f}%)",
                "Cluster 1": f"{category_1} ({percentage_1:.4f}%)",
                "Perbedaan/Keterangan": note,
            }
        )

    return pd.DataFrame(rows)


def main() -> None:
    X_cluster = load_clustering_features()
    preprocessor = build_preprocessor()

    # Unsupervised preprocessing is fit on the complete clustering sample.
    X_encoded = preprocessor.fit_transform(X_cluster)

    # C4 final K-Means only. C3 k-search is intentionally not repeated.
    kmeans_final = KMeans(
        n_clusters=FINAL_K,
        random_state=RANDOM_STATE,
        n_init=10,
    )
    cluster_labels = kmeans_final.fit_predict(X_encoded)

    if sorted(set(cluster_labels)) != [0, 1]:
        raise RuntimeError(f"Expected cluster labels [0, 1], got {sorted(set(cluster_labels))}")
    if len(cluster_labels) != 10000:
        raise RuntimeError("Expected 10,000 cluster assignments")

    assignments = X_cluster.copy()
    assignments["cluster"] = cluster_labels

    cluster_size = make_cluster_size_table(assignments)
    numeric_profile = make_numeric_profile(assignments)
    categorical_profile = make_categorical_profile(assignments)
    feature_comparison = make_feature_comparison(
        assignments,
        numeric_profile,
        categorical_profile,
    )

    # PCA is applied only after final K-Means, solely for visualization.
    pca = PCA(n_components=2, random_state=RANDOM_STATE)
    X_pca = pca.fit_transform(X_encoded)
    pca_df = pd.DataFrame(
        {
            "PC1": X_pca[:, 0],
            "PC2": X_pca[:, 1],
            "cluster": cluster_labels,
        }
    )
    explained_variance = pd.DataFrame(
        {
            "component": ["PC1", "PC2"],
            "explained_variance_ratio": pca.explained_variance_ratio_,
        }
    )
    explained_variance.loc[len(explained_variance)] = [
        "Total",
        float(pca.explained_variance_ratio_.sum()),
    ]

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    assignments.to_csv(RESULTS_DIR / "clustering_final_assignments.csv", index=False)
    cluster_size.to_csv(RESULTS_DIR / "clustering_cluster_size.csv", index=False)
    numeric_profile.to_csv(RESULTS_DIR / "clustering_numeric_profile.csv", index=False)
    categorical_profile.to_csv(RESULTS_DIR / "clustering_categorical_profile.csv", index=False)
    feature_comparison.to_csv(RESULTS_DIR / "clustering_feature_comparison.csv", index=False)
    explained_variance.to_csv(RESULTS_DIR / "clustering_pca_variance.csv", index=False)

    fig, ax = plt.subplots(figsize=(9, 6))
    for cluster_id, color in [(0, "tab:blue"), (1, "tab:orange")]:
        subset = pca_df[pca_df["cluster"] == cluster_id]
        ax.scatter(
            subset["PC1"],
            subset["PC2"],
            s=20,
            alpha=0.55,
            color=color,
            label=f"Cluster {cluster_id}",
        )
    ax.set_title("PCA Visualization of Final K-Means Clusters")
    ax.set_xlabel("PC1")
    ax.set_ylabel("PC2")
    ax.legend()
    ax.grid(alpha=0.2)
    fig.tight_layout()
    fig.savefig(RESULTS_DIR / "clustering_pca.png", dpi=160)
    plt.close(fig)

    print("Final K-Means selesai.")
    print(f"Jumlah record: {len(assignments)}")
    print(f"Jumlah fitur awal: {len(FEATURES)}")
    print(f"Jumlah fitur setelah encoding: {X_encoded.shape[1]}")
    print(f"Final k: {FINAL_K}")
    print(f"Random state: {RANDOM_STATE}")
    print("n_init: 10")
    print("\nUkuran cluster:")
    print(cluster_size.to_string(index=False))
    print("\nProfil numerik:")
    print(numeric_profile.to_string(index=False))
    print("\nProfil kategorikal dominan:")
    print(categorical_profile.to_string(index=False))
    print("\nPerbandingan fitur:")
    print(feature_comparison.to_string(index=False))
    print("\nExplained variance:")
    print(explained_variance.to_string(index=False))
    print("\nOutput C4 berhasil dibuat di:", RESULTS_DIR.resolve())


if __name__ == "__main__":
    main()
