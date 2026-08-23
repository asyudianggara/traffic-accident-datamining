from __future__ import annotations

import json
from pathlib import Path

import joblib
import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler


RANDOM_STATE = 42
BASELINE_D_MACRO_F1_CV = 0.4014324322457347
LABELS = ["Fatal", "Serious", "Slight"]

ROOT = Path(__file__).resolve().parent
DATA_PATH = ROOT / "data" / "raw" / "dft-road-casualty-statistics-collision-last-5-years.csv"
MAPPING_PATH = ROOT / "data" / "processed" / "stats19_maps.json"
RESULTS_DIR = ROOT / "results"
MODELS_DIR = ROOT / "models"


def prepare_dataset() -> tuple[pd.DataFrame, pd.Series, pd.DataFrame, pd.Series, list[str], list[str]]:
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
        raise RuntimeError(f"Expected 21 Scenario D features, got {len(feature_columns)}")
    if "collision_year" in feature_columns or "police_force" in feature_columns:
        raise RuntimeError("Scenario D features must exclude collision_year and police_force")

    X = df_decoded[feature_columns].copy()
    y = df_decoded["collision_severity"].copy()

    if X.isna().any().any() or y.isna().any():
        raise ValueError("Missing values found in the final Scenario D dataset")

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=RANDOM_STATE,
        stratify=y,
    )

    if len(X_train) != 8000 or len(X_test) != 2000:
        raise RuntimeError(
            f"Expected 8,000 training and 2,000 test rows, got {len(X_train)} and {len(X_test)}"
        )

    return X_train, y_train, X_test, y_test, numeric_features, categorical_features


def main() -> None:
    (
        X_train,
        y_train,
        X_test,
        y_test,
        numeric_features,
        categorical_features,
    ) = prepare_dataset()

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

    # Fit preprocessing only on the 8,000-row training set.
    X_train_encoded = preprocessor.fit_transform(X_train)

    final_model = RandomForestClassifier(
        n_estimators=300,
        max_depth=15,
        class_weight="balanced",
        random_state=RANDOM_STATE,
        n_jobs=-1,
    )

    # Fit the selected final configuration once on all 8,000 training rows.
    final_model.fit(X_train_encoded, y_train)

    # Transform test data only after the final model has been fit.
    X_test_encoded = preprocessor.transform(X_test)

    # The test set is evaluated once, using one prediction pass.
    y_pred = final_model.predict(X_test_encoded)

    overall_results = pd.DataFrame(
        [
            {"metric": "Accuracy", "value": accuracy_score(y_test, y_pred)},
            {
                "metric": "Macro Precision",
                "value": precision_score(y_test, y_pred, labels=LABELS, average="macro", zero_division=0),
            },
            {
                "metric": "Macro Recall",
                "value": recall_score(y_test, y_pred, labels=LABELS, average="macro", zero_division=0),
            },
            {
                "metric": "Macro F1",
                "value": f1_score(y_test, y_pred, labels=LABELS, average="macro", zero_division=0),
            },
            {
                "metric": "Weighted F1",
                "value": f1_score(y_test, y_pred, labels=LABELS, average="weighted", zero_division=0),
            },
        ]
    )

    report = classification_report(
        y_test,
        y_pred,
        labels=LABELS,
        target_names=LABELS,
        output_dict=True,
        zero_division=0,
    )
    report_df = pd.DataFrame(report).T.reset_index().rename(columns={"index": "label"})

    cm = confusion_matrix(y_test, y_pred, labels=LABELS)
    cm_df = pd.DataFrame(cm, index=LABELS, columns=LABELS)
    cm_df.index.name = "true_label"
    cm_df.columns.name = "predicted_label"

    feature_names = preprocessor.get_feature_names_out()
    feature_importance_df = pd.DataFrame(
        {
            "encoded_feature": feature_names,
            "importance": final_model.feature_importances_,
        }
    ).sort_values("importance", ascending=False)

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    MODELS_DIR.mkdir(parents=True, exist_ok=True)

    overall_results.to_csv(RESULTS_DIR / "final_test_results.csv", index=False)
    cm_df.to_csv(RESULTS_DIR / "final_confusion_matrix.csv")
    report_df.to_csv(RESULTS_DIR / "final_classification_report.csv", index=False)
    joblib.dump(final_model, MODELS_DIR / "final_random_forest.joblib")
    joblib.dump(preprocessor, MODELS_DIR / "final_preprocessor.joblib")

    fig, ax = plt.subplots(figsize=(7, 6))
    image = ax.imshow(cm, interpolation="nearest", cmap="Blues")
    ax.figure.colorbar(image, ax=ax)
    ax.set(
        xticks=range(len(LABELS)),
        yticks=range(len(LABELS)),
        xticklabels=LABELS,
        yticklabels=LABELS,
        ylabel="True label",
        xlabel="Predicted label",
        title="Final Random Forest - Test Confusion Matrix",
    )
    threshold = cm.max() / 2.0
    for row in range(cm.shape[0]):
        for column in range(cm.shape[1]):
            ax.text(
                column,
                row,
                format(cm[row, column], "d"),
                ha="center",
                va="center",
                color="white" if cm[row, column] > threshold else "black",
            )
    fig.tight_layout()
    fig.savefig(RESULTS_DIR / "final_confusion_matrix.png", dpi=160)
    plt.close(fig)

    top_features = feature_importance_df.head(20).sort_values("importance", ascending=True)
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.barh(top_features["encoded_feature"], top_features["importance"])
    ax.set_xlabel("Random Forest importance")
    ax.set_ylabel("Preprocessed / encoded feature")
    ax.set_title("Final Random Forest Feature Importance (Top 20 Encoded Features)")
    fig.tight_layout()
    fig.savefig(RESULTS_DIR / "final_feature_importance.png", dpi=160)
    plt.close(fig)

    macro_f1_test = float(overall_results.loc[overall_results["metric"] == "Macro F1", "value"].iloc[0])
    weighted_f1_test = float(overall_results.loc[overall_results["metric"] == "Weighted F1", "value"].iloc[0])
    accuracy_test = float(overall_results.loc[overall_results["metric"] == "Accuracy", "value"].iloc[0])
    class_metrics = report_df.set_index("label")

    print(f"Training rows: {len(X_train)}")
    print(f"Test rows: {len(X_test)}")
    print(f"Encoded feature count: {len(feature_names)}")
    print(f"Accuracy Test: {accuracy_test:.12f}")
    print(f"Macro F1 Test: {macro_f1_test:.12f}")
    print(f"Weighted F1 Test: {weighted_f1_test:.12f}")
    print(f"Recall Fatal: {class_metrics.loc['Fatal', 'recall']:.12f}")
    print(f"F1 Fatal: {class_metrics.loc['Fatal', 'f1-score']:.12f}")
    print(f"Recall Serious: {class_metrics.loc['Serious', 'recall']:.12f}")
    print(f"F1 Serious: {class_metrics.loc['Serious', 'f1-score']:.12f}")
    print(f"Recall Slight: {class_metrics.loc['Slight', 'recall']:.12f}")
    print(f"F1 Slight: {class_metrics.loc['Slight', 'f1-score']:.12f}")
    print("Confusion Matrix [Fatal, Serious, Slight]:")
    print(cm_df.to_string())
    print(f"Baseline D Macro F1 CV: {BASELINE_D_MACRO_F1_CV:.12f}")
    print(
        "Macro F1 Test minus Baseline D Macro F1 CV (percentage points): "
        f"{(macro_f1_test - BASELINE_D_MACRO_F1_CV) * 100:.6f}"
    )
    print("Top encoded features:")
    print(feature_importance_df.head(20).to_string(index=False))


if __name__ == "__main__":
    main()
