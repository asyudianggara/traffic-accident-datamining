"""Establish Phase 5 classification baselines on the full STATS19 data."""

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
from sklearn.tree import DecisionTreeClassifier

from prepare_phase3 import (
    CATEGORICAL_FEATURES,
    CLASSIFICATION_FEATURES,
    DATA_PATH,
    TARGET,
    build_preprocessor,
)


RANDOM_STATE = 42
ROOT = Path(__file__).resolve().parent
RESULTS_DIR = ROOT / "results"
LABELS = [1, 2, 3]
LABEL_NAMES = {1: "Fatal", 2: "Serious", 3: "Slight"}


def load_split() -> tuple[pd.DataFrame, pd.Series, pd.DataFrame, pd.Series]:
    raw = pd.read_csv(DATA_PATH, low_memory=False)
    data = raw.copy()
    data["month"] = pd.to_datetime(data["date"], format="%d/%m/%Y", errors="raise").dt.month
    data["hour"] = pd.to_datetime(data["time"], format="%H:%M", errors="raise").dt.hour
    train = data[data["collision_year"] <= 2024].reset_index(drop=True)
    test = data[data["collision_year"] == 2025].reset_index(drop=True)
    x_train = train[CLASSIFICATION_FEATURES].copy()
    x_test = test[CLASSIFICATION_FEATURES].copy()
    for column in CATEGORICAL_FEATURES:
        x_train[column] = x_train[column].astype("string")
        x_test[column] = x_test[column].astype("string")
    return x_train, train[TARGET], x_test, test[TARGET]


def pipeline(model) -> Pipeline:
    return Pipeline([("preprocessor", build_preprocessor()), ("model", model)])


def main() -> None:
    x_train, y_train, x_test, y_test = load_split()
    if len(x_train) != 412276 or len(x_test) != 101525:
        raise AssertionError("Phase 5 temporal split does not match the established contract")
    if set(x_train.columns) != set(CLASSIFICATION_FEATURES) or TARGET in x_train.columns:
        raise AssertionError("Feature contract or target leakage guard failed")

    models = {
        "logistic_regression": LogisticRegression(
            solver="lbfgs", max_iter=1000, class_weight="balanced", random_state=RANDOM_STATE
        ),
        "decision_tree": DecisionTreeClassifier(
            max_depth=12, min_samples_leaf=20, class_weight="balanced", random_state=RANDOM_STATE
        ),
        "random_forest": RandomForestClassifier(
            n_estimators=100, max_depth=12, min_samples_leaf=20,
            max_features="sqrt", class_weight="balanced", n_jobs=-1, random_state=RANDOM_STATE
        ),
    }
    comparison_rows = []
    report_rows = []
    matrices = {}
    run_metadata = {}
    for name, model in models.items():
        estimator = pipeline(model)
        started = time.perf_counter()
        estimator.fit(x_train, y_train)
        train_seconds = time.perf_counter() - started
        started = time.perf_counter()
        prediction = estimator.predict(x_test)
        prediction_seconds = time.perf_counter() - started
        report = classification_report(
            y_test, prediction, labels=LABELS, target_names=[LABEL_NAMES[x] for x in LABELS],
            output_dict=True, zero_division=0
        )
        matrix = confusion_matrix(y_test, prediction, labels=LABELS)
        matrices[name] = pd.DataFrame(matrix, index=[LABEL_NAMES[x] for x in LABELS], columns=[LABEL_NAMES[x] for x in LABELS])
        comparison_rows.append({
            "model": name, "accuracy": report["accuracy"],
            "macro_precision": report["macro avg"]["precision"], "macro_recall": report["macro avg"]["recall"],
            "macro_f1": report["macro avg"]["f1-score"], "weighted_f1": report["weighted avg"]["f1-score"],
            "fatal_precision": report["Fatal"]["precision"], "fatal_recall": report["Fatal"]["recall"],
            "fatal_f1": report["Fatal"]["f1-score"], "train_seconds": train_seconds,
            "prediction_seconds": prediction_seconds, "encoded_feature_count": estimator.named_steps["preprocessor"].transform(x_train).shape[1],
        })
        for label in ["Fatal", "Serious", "Slight"]:
            report_rows.append({"model": name, "label": label, **report[label]})
        report_rows.extend({"model": name, "label": label, **report[label]} for label in ["macro avg", "weighted avg"])
        run_metadata[name] = {"configuration": model.get_params(), "train_seconds": train_seconds, "prediction_seconds": prediction_seconds}

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(comparison_rows).sort_values(["macro_f1", "macro_recall", "fatal_recall"], ascending=False).to_csv(RESULTS_DIR / "phase5_model_comparison.csv", index=False)
    pd.DataFrame(report_rows).to_csv(RESULTS_DIR / "phase5_classification_report.csv", index=False)
    for name, matrix in matrices.items():
        matrix.to_csv(RESULTS_DIR / f"phase5_confusion_matrix_{name}.csv")
    compatibility = "not_run: HistGradientBoosting requires dense input; sparse-to-dense conversion was not attempted"
    metadata = {
        "phase": "5", "source": str(DATA_PATH.relative_to(ROOT)).replace("\\", "/"),
        "target": TARGET, "feature_list": CLASSIFICATION_FEATURES,
        "development_period": "2021-2024", "holdout_period": "2025",
        "train_rows": len(x_train), "test_rows": len(x_test), "random_state": RANDOM_STATE,
        "preprocessing": "Phase 3 ColumnTransformer: median numeric imputation; most-frequent categorical imputation; OneHotEncoder(handle_unknown=ignore, sparse_output=True)",
        "class_weight": "balanced", "hist_gradient_boosting": compatibility,
        "python_version": platform.python_version(), "sklearn_version": sklearn.__version__,
        "models": run_metadata, "test_year_used_for_fit": False,
    }
    (RESULTS_DIR / "phase5_metadata.json").write_text(json.dumps(metadata, indent=2, default=str) + "\n", encoding="utf-8")
    print(pd.DataFrame(comparison_rows).to_string(index=False))
    print(compatibility)


if __name__ == "__main__":
    main()
