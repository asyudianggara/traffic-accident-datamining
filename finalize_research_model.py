"""Create the Phase 6 final-candidate artifact without evaluating 2025 again."""

from __future__ import annotations

import json
import platform
import time
from pathlib import Path

import joblib
import pandas as pd
import sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline

from prepare_phase3 import CATEGORICAL_FEATURES, CLASSIFICATION_FEATURES, DATA_PATH, TARGET, build_preprocessor


RANDOM_STATE = 42
FATAL_THRESHOLD = 0.50
ROOT = Path(__file__).resolve().parent
MODELS_DIR = ROOT / "models"
RESULTS_DIR = ROOT / "results"
MODEL_PATH = MODELS_DIR / "final_research_model.joblib"
METADATA_PATH = RESULTS_DIR / "final_model_metadata.json"
COMPARISON_PATH = RESULTS_DIR / "final_model_comparison.csv"


def load_development() -> tuple[pd.DataFrame, pd.Series]:
    raw = pd.read_csv(DATA_PATH, low_memory=False)
    development = raw[raw["collision_year"] <= 2024].copy().reset_index(drop=True)
    if len(development) != 412276:
        raise AssertionError("Final candidate must be fit on exactly 412,276 development rows")
    development["month"] = pd.to_datetime(development["date"], format="%d/%m/%Y", errors="raise").dt.month
    development["hour"] = pd.to_datetime(development["time"], format="%H:%M", errors="raise").dt.hour
    x = development[CLASSIFICATION_FEATURES].copy()
    for column in CATEGORICAL_FEATURES:
        x[column] = x[column].astype("string")
    if TARGET in x or set(x.columns) != set(CLASSIFICATION_FEATURES):
        raise AssertionError("Feature contract or target leakage guard failed")
    return x, development[TARGET].copy()


def candidate_pipeline() -> Pipeline:
    return Pipeline([
        ("preprocessor", build_preprocessor()),
        ("model", RandomForestClassifier(
            n_estimators=100, max_depth=12, min_samples_leaf=20, max_features="sqrt",
            class_weight="balanced", n_jobs=-1, random_state=RANDOM_STATE,
        )),
    ])


def phase5_random_forest_metrics() -> dict:
    comparison = pd.read_csv(RESULTS_DIR / "phase5_model_comparison.csv")
    metrics = comparison.loc[comparison["model"] == "random_forest"].iloc[0].to_dict()
    report = pd.read_csv(RESULTS_DIR / "phase5_classification_report.csv")
    for label, field in [("Serious", "serious_f1"), ("Slight", "slight_f1")]:
        metrics[field] = float(report[(report["model"] == "random_forest") & (report["label"] == label)]["f1-score"].iloc[0])
    return metrics


def main() -> None:
    x_development, y_development = load_development()
    pipeline = candidate_pipeline()
    started = time.perf_counter()
    pipeline.fit(x_development, y_development)
    train_seconds = time.perf_counter() - started
    encoded_features = int(pipeline.named_steps["preprocessor"].transform(x_development).shape[1])
    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    artifact = {
        "pipeline": pipeline,
        "threshold": FATAL_THRESHOLD,
        "prediction_rule": "Jika P(Fatal) >= threshold, prediksi Fatal; selain itu pilih probabilitas terbesar antara Serious dan Slight.",
        "feature_list": CLASSIFICATION_FEATURES,
        "target": TARGET,
        "label_map": {1: "Fatal", 2: "Serious", 3: "Slight"},
    }
    joblib.dump(artifact, MODEL_PATH)

    phase5 = phase5_random_forest_metrics()
    phase51 = pd.read_csv(RESULTS_DIR / "phase5_1_final_holdout_metrics.csv").iloc[0].to_dict()
    phase52 = pd.read_csv(RESULTS_DIR / "phase5_2_final_holdout.csv")
    threshold_metrics = phase52.loc[phase52["rule"] == "fatal_threshold"].iloc[0].to_dict()
    fields = ["accuracy", "macro_precision", "macro_recall", "macro_f1", "weighted_f1", "fatal_precision", "fatal_recall", "fatal_f1", "serious_f1", "slight_f1"]
    consolidated = pd.DataFrame([
        {"checkpoint": "Phase 5 baseline", "configuration": "Random Forest balanced + default argmax", **{field: float(phase5[field]) for field in fields}},
        {"checkpoint": "Phase 5.1", "configuration": "Random Forest balanced + default argmax", **{field: float(phase51[field]) for field in fields}},
        {"checkpoint": "Phase 5.2 / final candidate", "configuration": "Random Forest balanced + Fatal threshold 0.50", **{field: float(threshold_metrics[field]) for field in fields}},
    ])
    consolidated.to_csv(COMPARISON_PATH, index=False)
    metadata = {
        "phase": "6", "status": "final_candidate_model", "dataset": str(DATA_PATH.relative_to(ROOT)).replace("\\", "/"),
        "training_period": "2021-2024", "training_rows": len(x_development), "holdout_period": "2025", "holdout_rows": 101525,
        "target": TARGET, "features": CLASSIFICATION_FEATURES, "preprocessing": "Median imputation untuk number_of_vehicles; most-frequent imputation dan OneHotEncoder sparse dengan handle_unknown=ignore untuk 17 fitur kategorikal.",
        "model": "RandomForestClassifier(n_estimators=100, max_depth=12, min_samples_leaf=20, max_features=sqrt, class_weight=balanced, n_jobs=-1, random_state=42)",
        "threshold": FATAL_THRESHOLD, "decision_rule": artifact["prediction_rule"], "random_state": RANDOM_STATE,
        "encoded_feature_count": encoded_features, "artifact": str(MODEL_PATH.relative_to(ROOT)).replace("\\", "/"),
        "final_holdout_metrics_source": "results/phase5_2_final_holdout.csv (hasil sebelumnya; 2025 tidak dievaluasi ulang pada Phase 6)",
        "selection_rationale": "Threshold 0.50 dipilih pada validation 2024 karena Macro F1 dan Fatal F1 tertinggi dalam kandidat terbatas; 2025 hanya digunakan sebagai evaluasi final yang telah dibekukan.",
        "train_seconds": train_seconds, "python_version": platform.python_version(), "sklearn_version": sklearn.__version__,
        "holdout_used_for_fit": False, "holdout_used_for_new_selection": False,
    }
    METADATA_PATH.write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"artifact": str(MODEL_PATH), "training_rows": len(x_development), "encoded_features": encoded_features, "train_seconds": train_seconds}, indent=2))


if __name__ == "__main__":
    main()
