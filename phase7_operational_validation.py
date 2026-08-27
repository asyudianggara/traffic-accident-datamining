"""Operational validation for the Phase 6 final candidate artifact.

This script only loads the persisted artifact and exercises inference. It does
not fit, tune, select, or evaluate a model, and it excludes 2025 from samples.
"""

from __future__ import annotations

import json
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import sklearn

from prepare_phase3 import CLASSIFICATION_FEATURES, DATA_PATH


ROOT = Path(__file__).resolve().parent
ARTIFACT_PATH = ROOT / "models" / "final_research_model.joblib"
OUTPUT_PATH = ROOT / "results" / "phase7_operational_validation.json"


def apply_final_rule(proba: np.ndarray, classes: list[str], threshold: float) -> list[str]:
    fatal_index = classes.index("Fatal")
    serious_index = classes.index("Serious")
    slight_index = classes.index("Slight")
    predictions = []
    for row in proba:
        if row[fatal_index] >= threshold:
            predictions.append("Fatal")
        else:
            predictions.append(classes[serious_index if row[serious_index] >= row[slight_index] else slight_index])
    return predictions


def main() -> None:
    artifact = joblib.load(ARTIFACT_PATH)
    final_metadata = json.loads((ROOT / "results" / "final_model_metadata.json").read_text(encoding="utf-8"))
    pipeline = artifact["pipeline"]
    features = artifact["feature_list"]
    threshold = float(artifact["threshold"])
    model = pipeline.named_steps["model"]
    raw_classes = [int(value) for value in model.classes_]
    label_map = {int(key): value for key, value in artifact["label_map"].items()}
    classes = [label_map[int(value)] for value in raw_classes]
    encoded_names = pipeline.named_steps["preprocessor"].get_feature_names_out()

    assert features == CLASSIFICATION_FEATURES
    assert len(encoded_names) == 149
    assert raw_classes == [1, 2, 3]
    assert classes == ["Fatal", "Serious", "Slight"]
    assert threshold == 0.50
    assert hasattr(pipeline, "predict") and hasattr(pipeline, "predict_proba")

    raw = pd.read_csv(DATA_PATH, low_memory=False)
    development = raw.loc[raw["collision_year"] <= 2024].copy()
    assert len(development) == 412276
    development["month"] = pd.to_datetime(development["date"], format="%d/%m/%Y", errors="raise").dt.month
    development["hour"] = pd.to_datetime(development["time"], format="%H:%M", errors="raise").dt.hour
    sample = development.sort_values("collision_index").head(3).copy()
    inputs = sample[features].copy()
    inputs["month"] = pd.to_numeric(inputs["month"], errors="raise").astype("string")
    inputs["hour"] = pd.to_numeric(inputs["hour"], errors="raise").astype("string")
    for column in features:
        if column != "number_of_vehicles":
            inputs[column] = inputs[column].astype("string")

    transformed = pipeline.named_steps["preprocessor"].transform(inputs)
    assert transformed.shape == (3, 149)
    probabilities_one = pipeline.predict_proba(inputs)
    probabilities_two = pipeline.predict_proba(inputs.copy())
    predictions_one = apply_final_rule(probabilities_one, classes, threshold)
    predictions_two = apply_final_rule(probabilities_two, classes, threshold)
    assert np.allclose(probabilities_one, probabilities_two, rtol=1e-12, atol=1e-12)
    assert predictions_one == predictions_two
    assert apply_final_rule(np.array([[0.50, 0.20, 0.30]]), classes, threshold) == ["Fatal"]
    assert len(predictions_one) == len(inputs)
    assert all(abs(float(row.sum()) - 1.0) < 1e-9 for row in probabilities_one)

    missing_input = inputs.iloc[[0]].copy()
    missing_input["number_of_vehicles"] = np.nan
    missing_input["weather_conditions"] = np.nan
    missing_prediction = pipeline.predict_proba(missing_input)

    unknown_input = inputs.iloc[[0]].copy()
    unknown_input["weather_conditions"] = "__SYNTHETIC_UNKNOWN_CATEGORY__"
    unknown_prediction = pipeline.predict_proba(unknown_input)

    invalid_type_error = None
    invalid_type_input = inputs.iloc[[0]].copy()
    invalid_type_input["number_of_vehicles"] = "not-a-number"
    try:
        pipeline.predict(invalid_type_input)
    except Exception as exc:  # expected: numeric transformer rejects non-numeric input
        invalid_type_error = type(exc).__name__

    incomplete_error = None
    incomplete_input = inputs.drop(columns=["hour"])
    try:
        pipeline.predict(incomplete_input)
    except Exception as exc:  # expected: missing feature is rejected by transformer
        incomplete_error = type(exc).__name__

    result = {
        "phase": "7",
        "artifact_loaded": True,
        "artifact": str(ARTIFACT_PATH.relative_to(ROOT)),
        "artifact_training_sklearn_version": final_metadata["sklearn_version"],
        "runtime_sklearn_version": sklearn.__version__,
        "runtime_version_compatibility": "NOT VERIFIED" if final_metadata["sklearn_version"] != sklearn.__version__ else "MATCH",
        "feature_contract_count": len(features),
        "encoded_feature_count": len(encoded_names),
        "class_order": {"estimator_codes": raw_classes, "labels": classes},
        "threshold": threshold,
        "development_sample_rows": len(inputs),
        "development_sample_source": "raw dataset rows with collision_year <= 2024; deterministic first 3 by collision_index",
        "prediction": {"passed": True, "classes": predictions_one, "threshold_boundary_test": "PASS"},
        "probability": {"passed": True, "rows_sum_to_one": True, "repeated_identical": True},
        "edge_cases": {
            "missing_values": {"status": "PASS", "behavior": "pipeline imputation produced probabilities", "probability_rows": len(missing_prediction)},
            "unknown_category": {"status": "PASS", "behavior": "handle_unknown=ignore produced probabilities", "probability_rows": len(unknown_prediction)},
            "out_of_pattern_numeric": {"status": "NOT VERIFIED", "reason": "pipeline has no standalone domain-range validator"},
            "invalid_numeric_type": {"status": "PASS", "behavior": "prediction rejected invalid numeric type", "error": invalid_type_error},
            "incomplete_input": {"status": "PASS", "behavior": "prediction rejected missing feature", "error": incomplete_error},
        },
        "holdout_2025_used": False,
        "fit_or_selection_performed": False,
        "raw_dataset_modified": False,
    }
    assert invalid_type_error is not None
    assert incomplete_error is not None
    OUTPUT_PATH.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
