"""Compare application inference with the persisted Phase 6 contract."""

from __future__ import annotations

import json
from pathlib import Path

import joblib
import numpy as np
import pandas as pd

import app
from prepare_phase3 import DATA_PATH


ROOT = Path(__file__).resolve().parent
OUTPUT_PATH = ROOT / "results" / "phase8_application_consistency.json"


def main() -> None:
    artifacts = app.load_artifacts()
    final_artifact = joblib.load(ROOT / "models" / "final_research_model.joblib")
    raw = pd.read_csv(DATA_PATH, low_memory=False)
    development = raw.loc[raw["collision_year"] <= 2024].copy()
    development["month"] = pd.to_datetime(development["date"], format="%d/%m/%Y", errors="raise").dt.month
    development["hour"] = pd.to_datetime(development["time"], format="%H:%M", errors="raise").dt.hour
    row = development.sort_values("collision_index").iloc[0]
    values = {feature: row[feature] for feature in app.CLASSIFICATION_FEATURES}
    frame = app.classification_frame(values)

    app_prediction, app_probability = app.final_classification_prediction(
        artifacts["classification_model"], frame, artifacts["classification_threshold"]
    )
    direct_probability = final_artifact["pipeline"].predict_proba(frame)[0]
    direct_prediction, _ = app.final_classification_prediction(
        final_artifact["pipeline"], frame, final_artifact["threshold"]
    )
    assert app_prediction == direct_prediction
    assert np.allclose(app_probability, direct_probability, rtol=1e-12, atol=1e-12)

    result = {
        "app_artifacts_loaded": True,
        "sample_source": "development row with collision_year <= 2024; first collision_index",
        "feature_count": len(frame.columns),
        "encoded_feature_count": len(artifacts["classification_preprocessor"].get_feature_names_out()),
        "application_prediction": app_prediction,
        "direct_prediction": direct_prediction,
        "prediction_match": True,
        "probability_match_within_tolerance": True,
        "threshold": artifacts["classification_threshold"],
        "raw_dataset_modified": False,
        "holdout_2025_used": False,
    }
    OUTPUT_PATH.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
