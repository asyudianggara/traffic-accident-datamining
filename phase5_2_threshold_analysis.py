"""Analyze a Fatal probability threshold with a protected 2025 holdout."""

from __future__ import annotations

import json
import platform
import time
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.pipeline import Pipeline

from prepare_phase3 import CATEGORICAL_FEATURES, CLASSIFICATION_FEATURES, DATA_PATH, TARGET, build_preprocessor


RANDOM_STATE = 42
ROOT = Path(__file__).resolve().parent
RESULTS_DIR = ROOT / "results"
LABELS = [1, 2, 3]
LABEL_NAMES = {1: "Fatal", 2: "Serious", 3: "Slight"}
THRESHOLDS = [0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 0.50]


def split_data() -> tuple[pd.DataFrame, pd.Series, pd.DataFrame, pd.Series, pd.DataFrame, pd.Series]:
    raw = pd.read_csv(DATA_PATH, low_memory=False)
    data = raw.copy()
    data["month"] = pd.to_datetime(data["date"], format="%d/%m/%Y", errors="raise").dt.month
    data["hour"] = pd.to_datetime(data["time"], format="%H:%M", errors="raise").dt.hour
    result = []
    for years in ([2021, 2022, 2023], [2024], [2025]):
        part = data[data["collision_year"].isin(years)].reset_index(drop=True)
        x = part[CLASSIFICATION_FEATURES].copy()
        for column in CATEGORICAL_FEATURES:
            x[column] = x[column].astype("string")
        result.append((x, part[TARGET].copy()))
    (x_train, y_train), (x_validation, y_validation), (x_holdout, y_holdout) = result
    if (len(x_train), len(x_validation), len(x_holdout)) != (311349, 100927, 101525):
        raise AssertionError("Unexpected temporal partition")
    return x_train, y_train, x_validation, y_validation, x_holdout, y_holdout


def make_model() -> Pipeline:
    model = RandomForestClassifier(
        n_estimators=100, max_depth=12, min_samples_leaf=20, max_features="sqrt",
        class_weight="balanced", n_jobs=-1, random_state=RANDOM_STATE,
    )
    return Pipeline([("preprocessor", build_preprocessor()), ("model", model)])


def threshold_predictions(probabilities, threshold: float):
    fatal = probabilities[:, 0]
    predictions = probabilities[:, 1:].argmax(axis=1) + 2
    predictions[fatal >= threshold] = 1
    return predictions


def metrics_for(y_true: pd.Series, prediction) -> tuple[dict, pd.DataFrame]:
    report = classification_report(y_true, prediction, labels=LABELS, target_names=[LABEL_NAMES[x] for x in LABELS], output_dict=True, zero_division=0)
    row = {
        "accuracy": report["accuracy"], "macro_precision": report["macro avg"]["precision"], "macro_recall": report["macro avg"]["recall"], "macro_f1": report["macro avg"]["f1-score"], "weighted_f1": report["weighted avg"]["f1-score"],
        "fatal_precision": report["Fatal"]["precision"], "fatal_recall": report["Fatal"]["recall"], "fatal_f1": report["Fatal"]["f1-score"],
        "serious_precision": report["Serious"]["precision"], "serious_recall": report["Serious"]["recall"], "serious_f1": report["Serious"]["f1-score"],
        "slight_precision": report["Slight"]["precision"], "slight_recall": report["Slight"]["recall"], "slight_f1": report["Slight"]["f1-score"],
    }
    matrix = pd.DataFrame(confusion_matrix(y_true, prediction, labels=LABELS), index=[LABEL_NAMES[x] for x in LABELS], columns=[LABEL_NAMES[x] for x in LABELS])
    return row, matrix


def main() -> None:
    x_train, y_train, x_validation, y_validation, x_holdout, y_holdout = split_data()
    validation_model = make_model()
    started = time.perf_counter()
    validation_model.fit(x_train, y_train)
    validation_train_seconds = time.perf_counter() - started
    validation_probabilities = validation_model.predict_proba(x_validation)
    probability_frame = pd.DataFrame(validation_probabilities, columns=[LABEL_NAMES[x] for x in LABELS])
    probability_summary = pd.DataFrame({"class": [LABEL_NAMES[x] for x in LABELS], "mean": probability_frame.mean(axis=0).to_numpy(), "median": probability_frame.median(axis=0).to_numpy(), "p95": probability_frame.quantile(0.95).to_numpy()})
    rows, matrices = [], {}
    default_metrics, default_matrix = metrics_for(y_validation, validation_model.predict(x_validation))
    default_metrics.update({"rule": "default_argmax", "threshold": None})
    rows.append(default_metrics)
    matrices["default"] = default_matrix
    for threshold in THRESHOLDS:
        metrics, matrix = metrics_for(y_validation, threshold_predictions(validation_probabilities, threshold))
        metrics.update({"rule": "fatal_threshold", "threshold": threshold})
        rows.append(metrics)
        matrices[f"threshold_{threshold:.2f}"] = matrix
    validation = pd.DataFrame(rows)
    candidates = validation[validation["rule"] == "fatal_threshold"].copy()
    selected_row = candidates.sort_values(["macro_f1", "macro_recall", "fatal_f1", "fatal_precision", "threshold"], ascending=[False, False, False, False, True]).iloc[0]
    selected_threshold = float(selected_row["threshold"])

    final_model = make_model()
    x_development = pd.concat([x_train, x_validation], ignore_index=True)
    y_development = pd.concat([y_train, y_validation], ignore_index=True)
    started = time.perf_counter()
    final_model.fit(x_development, y_development)
    final_train_seconds = time.perf_counter() - started
    final_probabilities = final_model.predict_proba(x_holdout)
    final_default, default_holdout_matrix = metrics_for(y_holdout, final_model.predict(x_holdout))
    final_threshold, threshold_holdout_matrix = metrics_for(y_holdout, threshold_predictions(final_probabilities, selected_threshold))
    final_rows = []
    for rule, metrics in [("default_argmax", final_default), ("fatal_threshold", final_threshold)]:
        final_rows.append({"rule": rule, "threshold": None if rule == "default_argmax" else selected_threshold, **metrics})
    baseline = pd.read_csv(RESULTS_DIR / "phase5_model_comparison.csv")
    phase51 = pd.read_csv(RESULTS_DIR / "phase5_1_final_holdout_metrics.csv").iloc[0]
    comparison_rows = [
        {"checkpoint": "phase5_baseline_random_forest", "rule": "default_argmax", **{key: float(baseline[baseline["model"] == "random_forest"].iloc[0][key]) for key in ["accuracy", "macro_f1", "macro_recall", "fatal_precision", "fatal_recall", "fatal_f1"]}},
        {"checkpoint": "phase5_1_balanced_random_forest", "rule": "default_argmax", **{key: float(phase51[key]) for key in ["accuracy", "macro_f1", "macro_recall", "fatal_precision", "fatal_recall", "fatal_f1"]}},
        {"checkpoint": "phase5_2_threshold_adjusted", "rule": "fatal_threshold", **{key: final_threshold[key] for key in ["accuracy", "macro_f1", "macro_recall", "fatal_precision", "fatal_recall", "fatal_f1"]}},
    ]
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    validation.to_csv(RESULTS_DIR / "phase5_2_threshold_validation.csv", index=False)
    probability_summary.to_csv(RESULTS_DIR / "phase5_2_probability_summary.csv", index=False)
    pd.DataFrame(final_rows).to_csv(RESULTS_DIR / "phase5_2_final_holdout.csv", index=False)
    pd.DataFrame(comparison_rows).to_csv(RESULTS_DIR / "phase5_2_threshold_comparison.csv", index=False)
    default_holdout_matrix.to_csv(RESULTS_DIR / "phase5_2_confusion_matrix_default.csv")
    threshold_holdout_matrix.to_csv(RESULTS_DIR / "phase5_2_confusion_matrix_threshold.csv")
    chart_data = validation[validation["rule"] == "fatal_threshold"]
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.plot(chart_data["threshold"], chart_data["fatal_precision"], marker="o", label="Fatal precision")
    ax.plot(chart_data["threshold"], chart_data["fatal_recall"], marker="o", label="Fatal recall")
    ax.plot(chart_data["threshold"], chart_data["fatal_f1"], marker="o", label="Fatal F1")
    ax.set(xlabel="Fatal probability threshold", ylabel="Score", title="Phase 5.2 Fatal Threshold Sensitivity (2024 validation)")
    ax.grid(alpha=0.25); ax.legend(); fig.tight_layout(); fig.savefig(RESULTS_DIR / "phase5_2_threshold_sensitivity.png", dpi=160); plt.close(fig)
    metadata = {
        "phase": "5.2", "source": str(DATA_PATH.relative_to(ROOT)).replace("\\", "/"), "target": TARGET, "feature_list": CLASSIFICATION_FEATURES,
        "train_period": "2021-2023", "validation_period": "2024", "holdout_period": "2025", "train_rows": len(x_train), "validation_rows": len(x_validation), "holdout_rows": len(x_holdout),
        "rule": "if P(Fatal) >= threshold predict Fatal; otherwise predict argmax(P(Serious), P(Slight))", "candidate_thresholds": THRESHOLDS,
        "selected_provisional_threshold": selected_threshold, "selection_source": "2024 validation only", "holdout_used_for_selection": False,
        "validation_train_seconds": validation_train_seconds, "final_train_seconds": final_train_seconds, "encoded_feature_count_validation": int(validation_model.named_steps["preprocessor"].transform(x_train).shape[1]), "encoded_feature_count_final": int(final_model.named_steps["preprocessor"].transform(x_development).shape[1]),
        "random_state": RANDOM_STATE, "python_version": platform.python_version(), "sklearn_version": sklearn.__version__, "baseline_artifacts_overwritten": False,
    }
    (RESULTS_DIR / "phase5_2_metadata.json").write_text(json.dumps(metadata, indent=2, default=str) + "\n", encoding="utf-8")
    print(validation[["rule", "threshold", "macro_f1", "macro_recall", "fatal_precision", "fatal_recall", "fatal_f1"]].to_string(index=False))
    print("selected_provisional_threshold:", selected_threshold)
    print(pd.DataFrame(final_rows)[["rule", "threshold", "macro_f1", "macro_recall", "fatal_precision", "fatal_recall", "fatal_f1"]].to_string(index=False))


if __name__ == "__main__":
    main()
