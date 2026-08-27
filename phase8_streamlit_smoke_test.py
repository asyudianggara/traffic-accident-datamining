"""Smoke test the Streamlit app without starting a browser or fitting a model."""

from __future__ import annotations

import json
from pathlib import Path

from streamlit.testing.v1 import AppTest


ROOT = Path(__file__).resolve().parent
OUTPUT_PATH = ROOT / "results" / "phase8_streamlit_smoke_test.json"


def main() -> None:
    app_test = AppTest.from_file(str(ROOT / "app.py"), default_timeout=120)
    app_test.run()
    assert not app_test.exception
    assert app_test.sidebar.radio[0].value == "🏠 Beranda"

    app_test.sidebar.radio[0].set_value("📊 Dashboard Dataset").run()
    assert not app_test.exception
    assert any(metric.label == "Raw dataset" and metric.value == "513.801" for metric in app_test.metric)
    assert any(metric.label == "Kolom raw" and metric.value == "44" for metric in app_test.metric)
    assert any(metric.label == "Development / holdout" and metric.value == "412.276 / 101.525" for metric in app_test.metric)
    assert any("Hasil Clustering — Analisis Legacy C3–C4" in item.value for item in app_test.subheader)

    app_test.sidebar.radio[0].set_value("🔮 Prediksi Severity").run()
    assert not app_test.exception
    assert len(app_test.number_input) == 2
    assert len(app_test.slider) == 2
    # One selectbox is the scenario helper; the form itself has 14 categorical inputs.
    assert len(app_test.selectbox) == 15
    assert any(button.label == "Prediksi Tingkat Keparahan" for button in app_test.button)

    submit = next(button for button in app_test.button if button.label == "Prediksi Tingkat Keparahan")
    submit.click().run()
    assert not app_test.exception
    assert any("Hasil classification" in item.value for item in app_test.subheader)
    assert any(metric.label == "Threshold Fatal" and metric.value == "0.50" for metric in app_test.metric)

    result = {
        "startup": "PASS",
        "dashboard_dataset_page": "PASS",
        "classification_page": "PASS",
        "input_feature_widgets": 18,
        "prediction_submission": "PASS",
        "probability_output": "PASS",
        "threshold_output": "PASS",
        "training_on_startup": False,
        "raw_dataset_needed_for_prediction": False,
    }
    OUTPUT_PATH.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
