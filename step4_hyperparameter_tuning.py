from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import RandomizedSearchCV, StratifiedKFold, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


RANDOM_STATE = 42
BASELINE_D_MACRO_F1 = 0.4014

ROOT = Path(__file__).resolve().parent
DATA_PATH = ROOT / "data" / "raw" / "dft-road-casualty-statistics-collision-last-5-years.csv"
MAPPING_PATH = ROOT / "data" / "processed" / "stats19_maps.json"
RESULTS_DIR = ROOT / "results"
TUNING_RESULTS_PATH = RESULTS_DIR / "hyperparameter_tuning_results.csv"
BEST_PARAMS_PATH = RESULTS_DIR / "best_hyperparameters.json"


def load_training_data() -> tuple[pd.DataFrame, pd.Series]:
    """Recreate the Step 3 Scenario D training data without using test rows."""
    df = pd.read_csv(DATA_PATH, low_memory=False)

    years = [2021, 2022, 2023, 2024, 2025]
    df_sample = (
        df[df["collision_year"].isin(years)]
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
    for column, mapping in stats19_maps.items():
        if column in df_decoded.columns:
            df_decoded[column] = df_decoded[column].astype(str).map(mapping)

    numeric_features = [
        "longitude",
        "latitude",
        "number_of_vehicles",
        "speed_limit",
        "hour",
        "month",
    ]
    categorical_features = [
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
        "did_police_officer_attend_scene_of_accident",
        "trunk_road_flag",
    ]
    feature_columns = numeric_features + categorical_features

    if len(feature_columns) != 21:
        raise RuntimeError(f"Scenario D must contain 21 features, got {len(feature_columns)}")
    if "collision_year" in feature_columns or "police_force" in feature_columns:
        raise RuntimeError("Scenario D must exclude collision_year and police_force")

    X = df_decoded[feature_columns].copy()
    y = df_decoded["collision_severity"].copy()

    if X.isna().any().any() or y.isna().any():
        raise ValueError("Scenario D contains missing values after feature preparation")

    # Recreate the exact 8,000-row training partition. The returned test
    # partition is deliberately discarded and is never passed to tuning.
    X_train, _unused_X, y_train, _unused_y = train_test_split(
        X,
        y,
        train_size=8000,
        random_state=RANDOM_STATE,
        stratify=y,
    )

    return X_train, y_train


def build_search() -> RandomizedSearchCV:
    numeric_features = [
        "longitude",
        "latitude",
        "number_of_vehicles",
        "speed_limit",
        "hour",
        "month",
    ]
    categorical_features = [
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
        "did_police_officer_attend_scene_of_accident",
        "trunk_road_flag",
    ]

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), numeric_features),
            (
                "cat",
                OneHotEncoder(handle_unknown="ignore", sparse_output=True),
                categorical_features,
            ),
        ]
    )

    pipeline = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            (
                "model",
                RandomForestClassifier(
                    class_weight="balanced",
                    random_state=RANDOM_STATE,
                    n_jobs=-1,
                ),
            ),
        ]
    )

    parameter_distributions = {
        "model__n_estimators": [200, 300, 400, 500],
        "model__max_depth": [10, 15, 20, 25, None],
        "model__min_samples_split": [2, 5, 10],
        "model__min_samples_leaf": [1, 2, 4],
        "model__max_features": ["sqrt", "log2"],
    }

    cv = StratifiedKFold(
        n_splits=5,
        shuffle=True,
        random_state=RANDOM_STATE,
    )

    # refit=False prevents construction of a final model after CV.
    return RandomizedSearchCV(
        estimator=pipeline,
        param_distributions=parameter_distributions,
        n_iter=12,
        scoring="f1_macro",
        cv=cv,
        random_state=RANDOM_STATE,
        n_jobs=-1,
        refit=False,
        return_train_score=False,
        verbose=1,
    )


def main() -> None:
    X_train, y_train = load_training_data()
    search = build_search()

    print(f"Training rows used for tuning: {len(X_train)}")
    print("Test rows are not used.")
    print("Starting RandomizedSearchCV: n_iter=12, cv=5, scoring=f1_macro")
    search.fit(X_train, y_train)

    cv_results = pd.DataFrame(search.cv_results_)
    results = pd.DataFrame(
        {
            "rank": cv_results["rank_test_score"].astype(int),
            "n_estimators": cv_results["param_model__n_estimators"].astype(int),
            "max_depth": cv_results["param_model__max_depth"].where(
                cv_results["param_model__max_depth"].notna(), None
            ),
            "min_samples_split": cv_results["param_model__min_samples_split"].astype(int),
            "min_samples_leaf": cv_results["param_model__min_samples_leaf"].astype(int),
            "max_features": cv_results["param_model__max_features"].astype(str),
            "mean_macro_f1": cv_results["mean_test_score"].astype(float),
            "std_macro_f1": cv_results["std_test_score"].astype(float),
            "split0_macro_f1": cv_results["split0_test_score"].astype(float),
            "split1_macro_f1": cv_results["split1_test_score"].astype(float),
            "split2_macro_f1": cv_results["split2_test_score"].astype(float),
            "split3_macro_f1": cv_results["split3_test_score"].astype(float),
            "split4_macro_f1": cv_results["split4_test_score"].astype(float),
        }
    ).sort_values(["rank", "mean_macro_f1"], ascending=[True, False])
    results = results.reset_index(drop=True)

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    results.to_csv(TUNING_RESULTS_PATH, index=False)

    best_row = results.iloc[0]
    best_params = {
        "n_estimators": int(best_row["n_estimators"]),
        "max_depth": None if pd.isna(best_row["max_depth"]) else int(best_row["max_depth"]),
        "min_samples_split": int(best_row["min_samples_split"]),
        "min_samples_leaf": int(best_row["min_samples_leaf"]),
        "max_features": str(best_row["max_features"]),
        "class_weight": "balanced",
        "random_state": RANDOM_STATE,
    }
    best_macro_f1 = float(best_row["mean_macro_f1"])
    improvement_percentage_points = (best_macro_f1 - BASELINE_D_MACRO_F1) * 100
    best_payload = {
        "scenario": "D (without collision_year and police_force)",
        "num_features": 21,
        "training_rows": int(len(X_train)),
        "cv": "StratifiedKFold(n_splits=5, shuffle=True, random_state=42)",
        "scoring": "f1_macro",
        "n_iter": 12,
        "random_state": RANDOM_STATE,
        "refit": False,
        "best_params": best_params,
        "best_macro_f1_mean": best_macro_f1,
        "best_macro_f1_std": float(best_row["std_macro_f1"]),
        "baseline_D_macro_f1_mean": BASELINE_D_MACRO_F1,
        "improvement_percentage_points": improvement_percentage_points,
    }
    with BEST_PARAMS_PATH.open("w", encoding="utf-8") as best_file:
        json.dump(best_payload, best_file, indent=2)

    print("\n12 combinations tested:")
    print(
        results[
            [
                "n_estimators",
                "max_depth",
                "min_samples_split",
                "min_samples_leaf",
                "max_features",
                "mean_macro_f1",
                "std_macro_f1",
            ]
        ].to_string(index=False)
    )
    print("\nBest parameters:")
    print(json.dumps(best_params, indent=2))
    print(f"Best Macro F1: {best_macro_f1:.12f}")
    print(f"Baseline D Macro F1: {BASELINE_D_MACRO_F1:.4f}")
    print(f"Improvement / decline (percentage points): {improvement_percentage_points:.6f}")
    print(f"Saved tuning results: {TUNING_RESULTS_PATH}")
    print(f"Saved best parameters: {BEST_PARAMS_PATH}")


if __name__ == "__main__":
    main()
