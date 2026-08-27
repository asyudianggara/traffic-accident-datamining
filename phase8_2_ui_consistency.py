"""Validasi kontrak tampilan final research dan clustering legacy C3-C4."""

from __future__ import annotations

import json
import re
from pathlib import Path

from streamlit.testing.v1 import AppTest

import app


ROOT = Path(__file__).resolve().parent
APP_SOURCE = ROOT / "app.py"
OUTPUT_PATH = ROOT / "results" / "phase8_2_ui_consistency.json"

REQUIRED_UI_TEXT = [
    "Dataset raw penelitian: **513.801 record × 44 kolom**",
    "Pembagian Data Penelitian",
    "Training",
    "311.349",
    "Validation",
    "100.927",
    "Development",
    "412.276",
    "Final holdout",
    "101.525",
    "18 fitur → 149 encoded features",
    "18 fitur → 108 encoded features",
    "Hasil Clustering — Analisis Legacy C3–C4",
    "10.000 record legacy C3–C4",
    "Fatal Precision",
    "5,75%",
    "Fatal Recall",
    "32,97%",
    "Fatal F1",
    "9,80%",
    "Fatal threshold = 0,50",
]

EXPECTED_PAGES = [
    "🏠 Beranda",
    "📊 Dashboard Dataset",
    "📊 Tentang Data",
    "🔮 Prediksi Severity",
    "🧩 Analisis Cluster",
    "📖 Panduan Penggunaan",
    "📚 Kamus Fitur",
    "📊 Tentang Model",
]


def assert_static_contract() -> dict[str, str]:
    source = APP_SOURCE.read_text(encoding="utf-8")
    for expected in REQUIRED_UI_TEXT:
        assert expected in source, f"Teks kontrak UI tidak ditemukan: {expected}"

    assert app.NAV_ITEMS == EXPECTED_PAGES
    assert 'st.metric("Sample", "10.000"' not in source
    assert not re.search(r"(?i)sample.{0,40}10[.,]?000", source)

    legacy_lines = [line for line in source.splitlines() if "10.000" in line]
    assert legacy_lines, "Angka legacy 10.000 tidak ditemukan pada konteks clustering"
    for line in legacy_lines:
        normalized = line.lower()
        assert "legacy" in normalized or "c3–c4" in normalized, (
            "Angka 10.000 harus diberi konteks clustering legacy C3–C4: " + line.strip()
        )

    return {
        "dataset_raw": "PASS",
        "data_split": "PASS",
        "classification_18_to_149": "PASS",
        "clustering_legacy_10k_labeled": "PASS",
        "no_ambiguous_10k_dataset_label": "PASS",
    }


def assert_all_pages_render() -> dict[str, str]:
    app_test = AppTest.from_file(str(APP_SOURCE), default_timeout=120)
    app_test.run()
    assert not app_test.exception
    assert app_test.sidebar.radio[0].value == EXPECTED_PAGES[0]

    statuses: dict[str, str] = {}
    for page in EXPECTED_PAGES:
        app_test.sidebar.radio[0].set_value(page).run()
        assert not app_test.exception, f"Halaman gagal dirender: {page}"
        if page == "📊 Dashboard Dataset":
            dashboard_metrics = {
                "Raw dataset": "513.801",
                "Kolom raw": "44",
                "Development / holdout": "412.276 / 101.525",
                "Fatal Precision": "5,75%",
                "Fatal Recall": "32,97%",
                "Fatal F1": "9,80%",
            }
            for label, value in dashboard_metrics.items():
                assert any(metric.label == label and metric.value == value for metric in app_test.metric), (
                    f"Metrik Dashboard tidak sesuai: {label}={value}"
                )
        statuses[page] = "PASS"

    return statuses


def main() -> None:
    static_checks = assert_static_contract()
    page_checks = assert_all_pages_render()
    result = {
        "status": "PASS",
        "static_checks": static_checks,
        "pages": page_checks,
        "dataset_raw_records": 513801,
        "development_records": 412276,
        "training_records": 311349,
        "validation_records": 100927,
        "holdout_2025_records": 101525,
        "final_input_features": 18,
        "final_encoded_features": 149,
        "legacy_clustering_records": 10000,
        "legacy_clustering_label": "Clustering legacy C3–C4",
    }
    OUTPUT_PATH.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=True))


if __name__ == "__main__":
    main()
