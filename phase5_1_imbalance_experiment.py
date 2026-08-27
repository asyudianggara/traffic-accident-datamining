"""Controlled class-weight experiment with protected 2025 holdout."""

from __future__ import annotations

import json
import platform
import time
from pathlib import Path

import pandas as pd
import sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.pipeline import Pipeline

from prepare_phase3 import CATEGORICAL_FEATURES, CLASSIFICATION_FEATURES, DATA_PATH, TARGET, build_preprocessor


RANDOM_STATE = 42
ROOT = Path(__file__).resolve().parent
RESULTS_DIR = ROOT / "results"
LABELS = [1, 2, 3]
LABEL_NAMES = {1: "Fatal", 2: "Serious", 3: "Slight"}


def load_data() -> tuple[pd.DataFrame, pd.Series, pd.DataFrame, pd.Series, pd.DataFrame, pd.Series]:
    raw = pd.read_csv(DATA_PATH, low_memory=False)
    data = raw.copy()
    data["month"] = pd.to_datetime(data["date"], format="%d/%m/%Y", errors="raise").dt.month
    data["hour"] = pd.to_datetime(data["time"], format="%H:%M", errors="raise").dt.hour
    parts = []
    for years in ([2021, 2022, 2023], [2024], [2025]):
        part = data[data["collision_year"].isin(years)].reset_index(drop=True)
        x = part[CLASSIFICATION_FEATURES].copy()
        for column in CATEGORICAL_FEATURES:
            x[column] = x[column].astype("string")
        parts.append((x, part[TARGET].copy()))
    (x_train, y_train), (x_validation, y_validation), (x_holdout, y_holdout) = parts
    if (len(x_train), len(x_validation), len(x_holdout)) != (311349, 100927, 101525):
        raise AssertionError("Unexpected Phase 5.1 temporal partition")
    return x_train, y_train, x_validation, y_validation, x_holdout, y_holdout


def make_pipeline(model) -> Pipeline:
    return Pipeline([("preprocessor", build_preprocessor()), ("model", model)])


def evaluate(estimator: Pipeline, x: pd.DataFrame, y: pd.Series) -> tuple[dict, pd.DataFrame]:
    prediction = estimator.predict(x)
    report = classification_report(y, prediction, labels=LABELS, target_names=[LABEL_NAMES[x] for x in LABELS], output_dict=True, zero_division=0)
    row = {
        "accuracy": report["accuracy"], "macro_precision": report["macro avg"]["precision"],
        "macro_recall": report["macro avg"]["recall"], "macro_f1": report["macro avg"]["f1-score"],
        "weighted_f1": report["weighted avg"]["f1-score"],
        "fatal_precision": report["Fatal"]["precision"], "fatal_recall": report["Fatal"]["recall"], "fatal_f1": report["Fatal"]["f1-score"],
        "serious_precision": report["Serious"]["precision"], "serious_recall": report["Serious"]["recall"], "serious_f1": report["Serious"]["f1-score"],
        "slight_precision": report["Slight"]["precision"], "slight_recall": report["Slight"]["recall"], "slight_f1": report["Slight"]["f1-score"],
    }
    matrix = pd.DataFrame(confusion_matrix(y, prediction, labels=LABELS), index=[LABEL_NAMES[x] for x in LABELS], columns=[LABEL_NAMES[x] for x in LABELS])
    return row, matrix


def main() -> None:
    x_train, y_train, x_validation, y_validation, x_holdout, y_holdout = load_data()
    strategies = {
        "logistic_none": LogisticRegression(solver="lbfgs", max_iter=1000, class_weight=None, random_state=RANDOM_STATE),
        "logistic_balanced": LogisticRegression(solver="lbfgs", max_iter=1000, class_weight="balanced", random_state=RANDOM_STATE),
        "random_forest_none": RandomForestClassifier(n_estimators=100, max_depth=12, min_samples_leaf=20, max_features="sqrt", class_weight=None, n_jobs=-1, random_state=RANDOM_STATE),
        "random_forest_balanced": RandomForestClassifier(n_estimators=100, max_depth=12, min_samples_leaf=20, max_features="sqrt", class_weight="balanced", n_jobs=-1, random_state=RANDOM_STATE),
    }
    validation_rows, validation_reports, validation_matrices, configurations = [], [], {}, {}
    for name, model in strategies.items():
        estimator = make_pipeline(model)
        started = time.perf_counter()
        estimator.fit(x_train, y_train)
        train_seconds = time.perf_counter() - started
        started = time.perf_counter()
        metrics, matrix = evaluate(estimator, x_validation, y_validation)
        metrics.update({"strategy": name, "train_seconds": train_seconds, "prediction_seconds": time.perf_counter() - started, "encoded_feature_count": estimator.named_steps["preprocessor"].transform(x_train).shape[1]})
        validation_rows.append(metrics)
        report = classification_report(y_validation, estimator.predict(x_validation), labels=LABELS, target_names=[LABEL_NAMES[x] for x in LABELS], output_dict=True, zero_division=0)
        validation_reports.extend({"strategy": name, "label": label, **report[label]} for label in ["Fatal", "Serious", "Slight", "macro avg", "weighted avg"])
        validation_matrices[name] = matrix
        configurations[name] = model.get_params()

    validation = pd.DataFrame(validation_rows).sort_values(["macro_f1", "macro_recall", "fatal_f1", "fatal_precision"], ascending=False).reset_index(drop=True)
    selected = str(validation.iloc[0]["strategy"])
    selected_model = strategies[selected]
    final_estimator = make_pipeline(selected_model)
    final_started = time.perf_counter()
    final_estimator.fit(pd.concat([x_train, x_validation], ignore_index=True), pd.concat([y_train, y_validation], ignore_index=True))
    final_train_seconds = time.perf_counter() - final_started
    final_started = time.perf_counter()
    final_metrics, final_matrix = evaluate(final_estimator, x_holdout, y_holdout)
    final_prediction_seconds = time.perf_counter() - final_started
    final_metrics.update({"strategy": selected, "train_seconds": final_train_seconds, "prediction_seconds": final_prediction_seconds, "encoded_feature_count": final_estimator.named_steps["preprocessor"].transform(pd.concat([x_train, x_validation], ignore_index=True)).shape[1]})
    baseline = pd.read_csv(RESULTS_DIR / "phase5_model_comparison.csv")
    baseline_row = baseline[baseline["model"] == "random_forest"].iloc[0]
    comparison = pd.DataFrame([
        {"source": "phase5_baseline_random_forest", "strategy": "random_forest_balanced", **{key: float(baseline_row[key]) for key in ["accuracy", "macro_precision", "macro_recall", "macro_f1", "weighted_f1", "fatal_precision", "fatal_recall", "fatal_f1"]}},
        {"source": "phase5_1_final_selected", "strategy": selected, **{key: final_metrics[key] for key in ["accuracy", "macro_precision", "macro_recall", "macro_f1", "weighted_f1", "fatal_precision", "fatal_recall", "fatal_f1"]}},
    ])
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    validation.to_csv(RESULTS_DIR / "phase5_1_imbalance_comparison.csv", index=False)
    pd.DataFrame(validation_reports).to_csv(RESULTS_DIR / "phase5_1_imbalance_validation_report.csv", index=False)
    for name, matrix in validation_matrices.items():
        matrix.to_csv(RESULTS_DIR / f"phase5_1_imbalance_confusion_matrix_{name}.csv")
    pd.DataFrame([final_metrics]).to_csv(RESULTS_DIR / "phase5_1_final_holdout_metrics.csv", index=False)
    final_matrix.to_csv(RESULTS_DIR / "phase5_1_final_confusion_matrix.csv")
    comparison.to_csv(RESULTS_DIR / "phase5_1_baseline_comparison.csv", index=False)
    metadata = {
        "phase": "5.1", "source": str(DATA_PATH.relative_to(ROOT)).replace("\\", "/"), "target": TARGET,
        "feature_list": CLASSIFICATION_FEATURES, "train_period": "2021-2023", "validation_period": "2024", "holdout_period": "2025",
        "train_rows": len(x_train), "validation_rows": len(x_validation), "holdout_rows": len(x_holdout), "test_year_used_for_selection": False,
        "strategies": configurations, "selected_strategy": selected, "selection_order": ["macro_f1", "macro_recall", "fatal_f1", "fatal_precision"],
        "final_fit_rows": len(x_train) + len(x_validation), "random_state": RANDOM_STATE, "python_version": platform.python_version(), "sklearn_version": sklearn.__version__,
        "no_smote_or_synthetic_data": True, "baseline_artifacts_overwritten": False,
    }
    (RESULTS_DIR / "phase5_1_imbalance_metadata.json").write_text(json.dumps(metadata, indent=2, default=str) + "\n", encoding="utf-8")
    print(validation.to_string(index=False))
    print("selected_strategy:", selected)
    print(pd.DataFrame([final_metrics]).to_string(index=False))


if __name__ == "__main__":
    main()
