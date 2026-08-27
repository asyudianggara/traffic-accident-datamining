from __future__ import annotations

import json
from numbers import Real
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import streamlit as st


ROOT = Path(__file__).resolve().parent
MODELS_DIR = ROOT / "models"
MAP_PATH = ROOT / "data" / "processed" / "stats19_maps.json"
CLUSTERING_EVALUATION_PATH = ROOT / "results" / "clustering_k_evaluation.csv"
DATASET_RESULTS_DIR = ROOT / "results"

CLASSIFICATION_FEATURES = [
    "number_of_vehicles", "speed_limit", "first_road_class", "road_type",
    "junction_detail", "junction_control", "second_road_class",
    "pedestrian_crossing", "light_conditions", "weather_conditions",
    "road_surface_conditions", "special_conditions_at_site",
    "carriageway_hazards", "urban_or_rural_area", "trunk_road_flag",
    "day_of_week", "month", "hour",
]
CLASSIFICATION_NUMERIC_FEATURES = ["number_of_vehicles"]
CLASSIFICATION_CATEGORICAL_FEATURES = [feature for feature in CLASSIFICATION_FEATURES if feature not in CLASSIFICATION_NUMERIC_FEATURES]
CLUSTERING_NUMERIC_FEATURES = ["number_of_vehicles", "speed_limit", "hour", "month"]
CLUSTERING_CATEGORICAL_FEATURES = [
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
    "trunk_road_flag",
]
FEATURES = CLASSIFICATION_FEATURES
NUMERIC_FEATURES = CLASSIFICATION_NUMERIC_FEATURES
CATEGORICAL_FEATURES = CLASSIFICATION_CATEGORICAL_FEATURES
TARGET_LABELS = ["Fatal", "Serious", "Slight"]
CLASS_LABELS = {1: "Fatal", 2: "Serious", 3: "Slight"}
FATAL_THRESHOLD = 0.50

SCENARIO_DEFINITIONS = {
    "Input bebas": {
        "number_of_vehicles": 2,
        "speed_limit": 30,
        "hour": 12,
        "month": 7,
    },
    "Rural — speed limit tinggi": {
        "number_of_vehicles": 2,
        "speed_limit": 70,
        "hour": 14,
        "month": 6,
        "first_road_class": "A",
        "urban_or_rural_area": "Rural",
    },
    "Urban — speed limit rendah": {
        "number_of_vehicles": 2,
        "speed_limit": 30,
        "hour": 8,
        "month": 10,
        "urban_or_rural_area": "Urban",
        "road_type": "Single carriageway",
    },
    "Mixed rural": {
        "number_of_vehicles": 3,
        "speed_limit": 50,
        "hour": 18,
        "month": 3,
        "urban_or_rural_area": "Rural",
        "road_type": "Single carriageway",
    },
}

SCENARIO_WIDGET_SUFFIXES = {
    "number_of_vehicles": "vehicles",
    "speed_limit": "speed",
    "hour": "hour",
    "month": "month",
}

NAV_ITEMS = [
    "🏠 Beranda",
    "📊 Dashboard Dataset",
    "📊 Tentang Data",
    "🔮 Prediksi Severity",
    "🧩 Analisis Cluster",
    "📖 Panduan Penggunaan",
    "📚 Kamus Fitur",
    "📊 Tentang Model",
]

CLASSIFICATION_METRICS = {
    "Accuracy": "54,29%",
    "Macro Precision": "38,81%",
    "Macro Recall": "46,05%",
    "Macro F1": "37,84%",
    "Weighted F1": "58,41%",
}

CLASSIFICATION_FATAL_METRICS = {
    "Fatal Precision": "5,75%",
    "Fatal Recall": "32,97%",
    "Fatal F1": "9,80%",
}

CLUSTER_INTERPRETATIONS = {
    0: {
        "title": "Pola dominan wilayah rural",
        "summary": "Dominan pada pola kecelakaan wilayah rural dengan batas kecepatan lebih tinggi.",
        "details": [
            "Rural: 92,37%",
            "Rata-rata speed limit: 57,69",
            "Median speed limit: 60",
            "First road class A: 54,11%",
            "Single carriageway: 62,94%",
        ],
    },
    1: {
        "title": "Pola dominan wilayah urban",
        "summary": "Dominan pada pola kecelakaan wilayah urban dengan batas kecepatan lebih rendah.",
        "details": [
            "Urban: 87,47%",
            "Rata-rata speed limit: 28,51",
            "Median speed limit: 30",
            "First road class Unclassified: 41,82%",
            "Single carriageway: 75,46%",
            "Give way or uncontrolled: 48,43%",
        ],
    },
}

ACADEMIC_IDENTITY = {
    "Mata kuliah": "Rekayasa Perangkat Lunak",
    "Mahasiswa": "Asyudi Anggara",
    "NIM": "F552630019",
    "Institusi": "Universitas Tadulako (UNTAD) – Palu",
}

FEATURE_LABELS = {
    "number_of_vehicles": "Jumlah kendaraan",
    "speed_limit": "Batas kecepatan",
    "hour": "Jam kejadian",
    "month": "Bulan kejadian",
    "day_of_week": "Hari kejadian",
    "first_road_class": "Kelas jalan utama",
    "road_type": "Jenis jalan",
    "junction_detail": "Detail persimpangan",
    "junction_control": "Pengendalian persimpangan",
    "second_road_class": "Kelas jalan kedua",
    "pedestrian_crossing": "Penyeberangan pejalan kaki",
    "light_conditions": "Kondisi pencahayaan",
    "weather_conditions": "Kondisi cuaca",
    "road_surface_conditions": "Kondisi permukaan jalan",
    "special_conditions_at_site": "Kondisi khusus di lokasi",
    "carriageway_hazards": "Bahaya pada badan jalan",
    "urban_or_rural_area": "Wilayah perkotaan / pedesaan",
    "trunk_road_flag": "Penanda trunk road",
}

FEATURE_HELP = {
    "number_of_vehicles": "Jumlah kendaraan yang terlibat dalam kecelakaan.",
    "speed_limit": "Batas kecepatan yang berlaku pada lokasi kecelakaan.",
    "hour": "Jam terjadinya kecelakaan.",
    "month": "Bulan terjadinya kecelakaan.",
    "day_of_week": "Hari dalam minggu ketika kecelakaan terjadi.",
    "first_road_class": "Kelas atau klasifikasi jalan utama yang tercatat pada lokasi kecelakaan.",
    "road_type": "Jenis atau bentuk jalan tempat kecelakaan terjadi.",
    "junction_detail": "Posisi atau karakteristik kecelakaan terhadap persimpangan.",
    "junction_control": "Jenis pengendalian yang berlaku pada persimpangan, jika ada.",
    "second_road_class": "Kelas jalan kedua yang terkait dengan lokasi kecelakaan.",
    "pedestrian_crossing": "Fasilitas atau kondisi penyeberangan pejalan kaki di lokasi.",
    "light_conditions": "Kondisi pencahayaan pada saat kecelakaan.",
    "weather_conditions": "Kondisi cuaca pada saat kecelakaan.",
    "road_surface_conditions": "Kondisi permukaan jalan pada saat kecelakaan.",
    "special_conditions_at_site": "Kondisi khusus di lokasi yang tercatat dalam data.",
    "carriageway_hazards": "Bahaya atau kondisi tertentu pada badan jalan yang tercatat.",
    "urban_or_rural_area": "Menunjukkan apakah lokasi berada di wilayah perkotaan atau pedesaan.",
    "trunk_road_flag": "Penanda apakah jalan termasuk trunk road sesuai klasifikasi dataset.",
}

FEATURE_GROUPS = {
    "Informasi jalan": [
        "first_road_class", "road_type", "second_road_class", "junction_detail",
        "junction_control", "pedestrian_crossing", "carriageway_hazards", "trunk_road_flag",
    ],
    "Kondisi lingkungan": [
        "light_conditions", "weather_conditions", "road_surface_conditions",
        "special_conditions_at_site", "urban_or_rural_area",
    ],
}

GLOSSARY = {
    "Classification": "Metode untuk memprediksi kelas atau kategori yang telah ditentukan.",
    "Clustering": "Metode untuk menemukan kelompok data berdasarkan kemiripan karakteristik.",
    "Random Forest": "Algoritma classification yang menggabungkan banyak decision tree.",
    "K-Means": "Algoritma clustering yang membagi data menjadi sejumlah kelompok.",
    "Feature": "Variabel atau karakteristik yang digunakan model.",
    "Target": "Nilai yang ingin diprediksi dalam classification.",
    "Preprocessing": "Proses menyiapkan data sebelum diberikan ke model.",
    "Imputation": "Proses mengisi nilai data yang kosong.",
    "One-Hot Encoding": "Teknik mengubah kategori menjadi representasi numerik untuk model.",
    "StandardScaler": "Proses menstandarkan fitur numerik agar berada pada skala sebanding.",
    "Inference": "Proses menggunakan model yang sudah dilatih untuk menghasilkan prediksi baru.",
    "Probability": "Nilai keluaran model untuk setiap kelas; bukan jaminan kebenaran.",
    "Centroid": "Titik pusat suatu cluster pada K-Means.",
    "PCA": "Teknik reduksi dimensi yang pada project ini hanya digunakan untuk visualisasi clustering, bukan prediction.",
}


def require_files() -> None:
    required = [
        MODELS_DIR / "final_research_model.joblib",
        ROOT / "results" / "final_model_metadata.json",
        MODELS_DIR / "final_kmeans.joblib",
        MODELS_DIR / "final_clustering_preprocessor.joblib",
        MODELS_DIR / "final_clustering_metadata.json",
        MAP_PATH,
    ]
    missing = [str(path.relative_to(ROOT)) for path in required if not path.exists()]
    if missing:
        raise FileNotFoundError("Artefak final yang dibutuhkan tidak ditemukan: " + ", ".join(missing))


@st.cache_resource(show_spinner=False)
def load_artifacts() -> dict:
    require_files()
    with (ROOT / "results" / "final_model_metadata.json").open("r", encoding="utf-8") as file:
        classification_metadata = json.load(file)
    with (MODELS_DIR / "final_clustering_metadata.json").open("r", encoding="utf-8") as file:
        clustering_metadata = json.load(file)
    with MAP_PATH.open("r", encoding="utf-8") as file:
        mappings = json.load(file)

    final_artifact = joblib.load(MODELS_DIR / "final_research_model.joblib")
    classification_model = final_artifact["pipeline"]
    classification_preprocessor = classification_model.named_steps["preprocessor"]
    clustering_model = joblib.load(MODELS_DIR / "final_kmeans.joblib")
    clustering_preprocessor = joblib.load(MODELS_DIR / "final_clustering_preprocessor.joblib")

    if classification_metadata.get("encoded_feature_count") != 149:
        raise RuntimeError("Artefak classification bukan konfigurasi final 18 fitur")
    if clustering_metadata.get("feature_count_original") != 18:
        raise RuntimeError("Artefak clustering bukan konfigurasi final 18 fitur")
    if clustering_metadata.get("feature_count_encoded") != 108:
        raise RuntimeError("Artefak clustering bukan konfigurasi final 108 fitur")
    if len(classification_preprocessor.get_feature_names_out()) != 149:
        raise RuntimeError("Preprocessor classification tidak menghasilkan 149 fitur")
    if len(clustering_preprocessor.get_feature_names_out()) != 108:
        raise RuntimeError("Preprocessor clustering tidak menghasilkan 108 fitur")
    if list(classification_model.named_steps["model"].classes_) != [1, 2, 3]:
        raise RuntimeError("Urutan kelas classification tidak sesuai kontrak [1, 2, 3]")
    if getattr(clustering_model, "n_features_in_", None) != 108:
        raise RuntimeError("Model clustering tidak mengharapkan 108 fitur")

    classification_encoder = classification_preprocessor.named_transformers_["categorical"].named_steps["onehot"]
    clustering_encoder = clustering_preprocessor.named_transformers_["cat"].named_steps["encoder"]
    classification_category_options = {
        feature: list(values)
        for feature, values in zip(CLASSIFICATION_CATEGORICAL_FEATURES, classification_encoder.categories_)
    }
    clustering_category_options = {
        feature: list(values)
        for feature, values in zip(CLUSTERING_CATEGORICAL_FEATURES, clustering_encoder.categories_)
    }

    if CLUSTERING_EVALUATION_PATH.exists():
        clustering_evaluation = pd.read_csv(CLUSTERING_EVALUATION_PATH)
    else:
        clustering_evaluation = pd.DataFrame({
            "k": [2, 3, 4, 5, 6],
            "inertia": [95756.560557, 89650.949954, 85735.264751, 82928.578533, 80289.582594],
            "silhouette": [0.143490, 0.089714, 0.083531, 0.085248, 0.080003],
            "davies_bouldin": [2.387075, 2.763991, 2.821309, 2.624441, 2.506223],
            "calinski_harabasz": [1287.425737, 1027.902184, 868.672373, 758.056056, 692.012594],
        })

    return {
        "classification_model": classification_model,
        "classification_preprocessor": classification_preprocessor,
        "classification_metadata": classification_metadata,
        "classification_threshold": float(final_artifact["threshold"]),
        "clustering_model": clustering_model,
        "clustering_preprocessor": clustering_preprocessor,
        "clustering_metadata": clustering_metadata,
        "mappings": mappings,
        "classification_category_options": classification_category_options,
        "clustering_category_options": clustering_category_options,
        "clustering_evaluation": clustering_evaluation,
    }


@st.cache_data(show_spinner=False)
def load_dataset_results() -> dict:
    files = {
        "cluster_size": "clustering_cluster_size.csv",
        "numeric_profile": "clustering_numeric_profile.csv",
        "categorical_profile": "clustering_categorical_profile.csv",
        "feature_comparison": "clustering_feature_comparison.csv",
        "k_evaluation": "clustering_k_evaluation.csv",
        "pca_variance": "clustering_pca_variance.csv",
    }
    data = {}
    missing = []
    for key, filename in files.items():
        path = DATASET_RESULTS_DIR / filename
        if path.exists():
            data[key] = pd.read_csv(path)
        else:
            missing.append(filename)
    data["missing"] = missing
    data["pca_image"] = DATASET_RESULTS_DIR / "clustering_pca.png"
    data["elbow_image"] = DATASET_RESULTS_DIR / "clustering_elbow.png"
    data["silhouette_image"] = DATASET_RESULTS_DIR / "clustering_silhouette.png"
    return data


def inject_styles() -> None:
    st.markdown(
        """
        <style>
        :root { --ink: #17324d; --muted: #5b7180; --teal: #1f7a78; --pale: #eef7f6; --line: #dbe6ea; }
        .block-container { max-width: 1180px; padding-top: 2.2rem; padding-bottom: 3.5rem; }
        .hero { padding: 2rem 2.2rem; border: 1px solid #cfe3e4; border-radius: 22px; background: linear-gradient(120deg, #15344e 0%, #1e6f73 100%); color: white; margin-bottom: 1.5rem; box-shadow: 0 12px 30px rgba(23,50,77,.12); }
        .hero h1 { margin: 0 0 .45rem 0; font-size: clamp(2rem, 4vw, 3.2rem); letter-spacing: -.03em; }
        .hero p { max-width: 720px; margin: 0; color: #e0f3f0; font-size: 1.1rem; line-height: 1.6; }
        .eyebrow { color: #8dd9d2; font-size: .78rem; font-weight: 700; letter-spacing: .11em; text-transform: uppercase; margin-bottom: .5rem; }
        .result-card { padding: 1.35rem 1.5rem; border: 1px solid #b9e2dc; border-radius: 17px; background: var(--pale); margin-top: 1rem; }
        .result-card h2 { color: var(--ink); margin: 0 0 .35rem 0; }
        .result-card p { color: #385b65; margin-bottom: 0; }
        .severity-card { padding: 1.7rem; border-radius: 18px; background: linear-gradient(135deg, #15344e, #1f7a78); color: white; text-align: center; }
        .severity-card .label { font-size: .85rem; opacity: .8; text-transform: uppercase; letter-spacing: .12em; }
        .severity-card .value { font-size: 2.3rem; font-weight: 750; margin-top: .4rem; }
        .section-banner { padding: 1.25rem 1.4rem; border-radius: 18px; margin: .4rem 0 1.35rem; }
        .section-banner .section-kicker { font-size: .76rem; font-weight: 750; letter-spacing: .12em; text-transform: uppercase; margin-bottom: .35rem; }
        .section-banner h2 { margin: 0 0 .35rem; color: var(--ink); }
        .section-banner p { margin: 0; color: #385b65; line-height: 1.55; }
        .section-banner.classification { background: #edf5fc; border: 1px solid #c5dcef; }
        .section-banner.classification .section-kicker { color: #23649b; }
        .section-banner.clustering { background: #fff5e9; border: 1px solid #f0d4a9; }
        .section-banner.clustering .section-kicker { color: #a15b13; }
        .section-banner.data { background: #f5f6f7; border: 1px solid #d9e0e5; }
        .section-banner.data .section-kicker { color: #52616b; }
        .footer { margin-top: 3rem; padding-top: 1.2rem; border-top: 1px solid var(--line); color: var(--muted); font-size: .82rem; text-align: center; }
        </style>
        """,
        unsafe_allow_html=True,
    )


def option_label(value: object, feature: str, mappings: dict) -> str:
    if isinstance(value, Real) and not isinstance(value, bool):
        numeric_value = float(value)
        code = str(int(numeric_value)) if numeric_value.is_integer() else str(numeric_value)
        mapped = mappings.get(feature, {}).get(code)
        if mapped:
            return f"{mapped} (kode {code})"
        return f"Kode {code} (kode STATS19)"
    return str(value)


def scenario_option(artifacts: dict, feature: str, preferred: str) -> object | None:
    options = artifacts["classification_category_options"].get(feature, [])
    needle = preferred.lower()
    for option in options:
        if needle in option_label(option, feature, artifacts["mappings"]).lower():
            return option
    return None


def apply_classification_scenario(artifacts: dict) -> None:
    scenario_name = st.session_state.get("classification_scenario", "Input bebas")
    defaults = SCENARIO_DEFINITIONS[scenario_name]
    for feature, value in defaults.items():
        if feature in SCENARIO_WIDGET_SUFFIXES:
            widget_key = f"classification_{SCENARIO_WIDGET_SUFFIXES[feature]}"
            st.session_state[widget_key] = value
        else:
            selected = scenario_option(artifacts, feature, str(value))
            if selected is not None:
                st.session_state[f"classification_{feature}"] = selected


def render_select(values: dict, artifacts: dict, feature: str, category_options_key: str, prefix: str) -> None:
    values[feature] = st.selectbox(
        FEATURE_LABELS[feature],
        options=artifacts[category_options_key][feature],
        format_func=lambda value, current=feature: option_label(value, current, artifacts["mappings"]),
        help=FEATURE_HELP[feature],
        key=f"{prefix}_{feature}",
    )


def input_form(artifacts: dict, prefix: str, category_options_key: str, submit_label: str) -> tuple[dict, bool]:
    values: dict = {}
    with st.form(f"{prefix}_form", border=True):
        with st.container(border=True):
            st.subheader("🚗 Informasi kendaraan")
            vehicle_left, vehicle_right = st.columns(2)
            with vehicle_left:
                vehicle_kwargs = {}
                if f"{prefix}_vehicles" not in st.session_state:
                    vehicle_kwargs["value"] = 2
                values["number_of_vehicles"] = st.number_input(
                    "Jumlah kendaraan", min_value=1, max_value=20, step=1,
                    help=FEATURE_HELP["number_of_vehicles"], key=f"{prefix}_vehicles", **vehicle_kwargs
                )
            with vehicle_right:
                speed_kwargs = {}
                if f"{prefix}_speed" not in st.session_state:
                    speed_kwargs["value"] = 30
                values["speed_limit"] = st.number_input(
                    "Batas kecepatan", min_value=10, max_value=100, step=10,
                    help=FEATURE_HELP["speed_limit"], key=f"{prefix}_speed", **speed_kwargs
                )

        with st.container(border=True):
            st.subheader("🛣️ Informasi jalan")
            road_features = FEATURE_GROUPS["Informasi jalan"]
            for start in range(0, len(road_features), 2):
                road_left, road_right = st.columns(2)
                with road_left:
                    render_select(values, artifacts, road_features[start], category_options_key, prefix)
                with road_right:
                    render_select(values, artifacts, road_features[start + 1], category_options_key, prefix)

        with st.container(border=True):
            st.subheader("🌦️ Kondisi lingkungan")
            environment_features = FEATURE_GROUPS["Kondisi lingkungan"]
            for start in range(0, len(environment_features), 2):
                env_left, env_right = st.columns(2)
                with env_left:
                    render_select(values, artifacts, environment_features[start], category_options_key, prefix)
                if start + 1 < len(environment_features):
                    with env_right:
                        render_select(values, artifacts, environment_features[start + 1], category_options_key, prefix)

        with st.container(border=True):
            st.subheader("📅 Waktu kejadian")
            time_left, time_middle, time_right = st.columns(3)
            with time_left:
                render_select(values, artifacts, "day_of_week", category_options_key, prefix)
            with time_middle:
                hour_kwargs = {}
                if f"{prefix}_hour" not in st.session_state:
                    hour_kwargs["value"] = 12
                values["hour"] = st.slider(
                    "Jam kejadian", min_value=0, max_value=23,
                    help=FEATURE_HELP["hour"], key=f"{prefix}_hour", **hour_kwargs
                )
            with time_right:
                month_kwargs = {}
                if f"{prefix}_month" not in st.session_state:
                    month_kwargs["value"] = 7
                values["month"] = st.slider(
                    "Bulan kejadian", min_value=1, max_value=12,
                    help=FEATURE_HELP["month"], key=f"{prefix}_month", **month_kwargs
                )

        submitted = st.form_submit_button(submit_label, type="primary", width="stretch")
    return values, submitted


def values_to_frame(values: dict) -> pd.DataFrame:
    return pd.DataFrame([{feature: values[feature] for feature in FEATURES}], columns=FEATURES)


def classification_frame(values: dict) -> pd.DataFrame:
    frame = values_to_frame(values)
    for feature in CLASSIFICATION_CATEGORICAL_FEATURES:
        frame[feature] = frame[feature].astype("string")
    return frame[CLASSIFICATION_FEATURES]


def final_classification_prediction(model, frame: pd.DataFrame, threshold: float) -> tuple[str, np.ndarray]:
    probabilities = model.predict_proba(frame)[0]
    class_indices = {int(code): index for index, code in enumerate(model.named_steps["model"].classes_)}
    if probabilities[class_indices[1]] >= threshold:
        prediction_code = 1
    else:
        prediction_code = max((2, 3), key=lambda code: probabilities[class_indices[code]])
    return CLASS_LABELS[prediction_code], probabilities


def navigate_to(page: str) -> None:
    st.session_state["page_nav"] = page


def render_identity() -> None:
    with st.container(border=True):
        st.caption("Identitas akademik")
        st.write(
            f"**{ACADEMIC_IDENTITY['Mata kuliah']}** · {ACADEMIC_IDENTITY['Mahasiswa']} · "
            f"{ACADEMIC_IDENTITY['NIM']} · {ACADEMIC_IDENTITY['Institusi']}"
        )


def render_section_banner(kind: str, kicker: str, title: str, description: str) -> None:
    st.markdown(
        f"<div class='section-banner {kind}'><div class='section-kicker'>{kicker}</div>"
        f"<h2>{title}</h2><p>{description}</p></div>",
        unsafe_allow_html=True,
    )


def render_pipeline(steps: list[str]) -> None:
    with st.container(border=True):
        st.caption("Alur analisis")
        st.markdown(" → ".join(f"**{step}**" for step in steps))


def render_research_data_split() -> None:
    st.subheader("Pembagian Data Penelitian")
    split_columns = st.columns(4)
    split_values = [
        ("Training", "311.349", "2021–2023"),
        ("Validation", "100.927", "2024"),
        ("Development", "412.276", "2021–2024"),
        ("Final holdout", "101.525", "2025"),
    ]
    for column, (label, value, period) in zip(split_columns, split_values):
        with column.container(border=True):
            st.metric(label, value)
            st.caption(period)
    st.caption(
        "Training digunakan untuk pembelajaran model. Validation digunakan untuk pemilihan strategi, model, dan threshold. "
        "Setelah keputusan final, model di-refit pada development 2021–2024. Tahun 2025 disimpan sebagai final holdout "
        "dan tidak digunakan untuk fitting, tuning, feature selection, threshold search, atau model selection."
    )


def render_fatal_metrics() -> None:
    st.caption("Metrik kelas Fatal pada final holdout 2025")
    metric_columns = st.columns(3)
    for column, (label, value) in zip(metric_columns, CLASSIFICATION_FATAL_METRICS.items()):
        with column.container(border=True):
            st.metric(label, value)


def render_model_cards() -> None:
    st.subheader("🤖 Model machine learning")
    model_columns = st.columns(3)
    cards = [
        (
            "🌳 Random Forest",
            "Classification · supervised learning",
            "Output: Fatal / Serious / Slight",
            "Menggabungkan banyak decision tree untuk menghasilkan prediksi severity.",
        ),
        (
            "📍 K-Means",
            "Clustering · unsupervised learning",
            "Output: Cluster 0 / Cluster 1",
            "Membagi data berdasarkan kedekatan karakteristik terhadap centroid.",
        ),
        (
            "◌ PCA",
            "Visualisasi hasil clustering",
            "Bukan model prediction",
            "Dipakai setelah K-Means hanya untuk membantu melihat pola dalam dua dimensi.",
        ),
    ]
    for column, (title, subtitle, output, detail) in zip(model_columns, cards):
        with column.container(border=True, height="stretch"):
            st.subheader(title)
            st.caption(subtitle)
            st.write(output)
            st.write(detail)


def render_evaluation_explanations() -> None:
    with st.expander("Bagaimana membaca evaluasi?", icon=":material/help:"):
        st.markdown(
            "**Accuracy** — persentase prediksi yang benar dari seluruh data.\n\n"
            "**Precision** — dari prediksi suatu kelas, seberapa banyak yang benar.\n\n"
            "**Recall** — dari data yang sebenarnya termasuk suatu kelas, seberapa banyak yang ditemukan model.\n\n"
            "**F1** — gabungan precision dan recall.\n\n"
            "**Silhouette** — seberapa baik data berada dalam cluster; nilai lebih tinggi umumnya lebih baik.\n\n"
            "**Davies-Bouldin** — kemiripan antar-cluster; nilai lebih rendah umumnya lebih baik.\n\n"
            "**Calinski-Harabasz** — kualitas pemisahan cluster; nilai lebih tinggi umumnya lebih baik.\n\n"
            "**Inertia** — jumlah kuadrat jarak data ke centroid. Nilainya biasanya turun saat k bertambah, "
            "sehingga tidak digunakan sendirian untuk memilih k."
        )


def render_home() -> None:
    st.markdown(
        "<div class='hero'><div class='eyebrow'>Data mining · STATS19</div><h1>Traffic Accident Analysis</h1><p>Analisis Kecelakaan Lalu Lintas Menggunakan Machine Learning</p></div>",
        unsafe_allow_html=True,
    )
    st.write("Aplikasi ini membantu memahami data kecelakaan lalu lintas melalui dua pendekatan machine learning: classification dan clustering.")
    render_section_banner(
        "data",
        "Data vs inference",
        "Pahami dulu sumber dan tujuan analisis",
        "Dashboard membaca hasil penelitian historis. Halaman prediksi dan cluster menerima data baru "
        "lalu menjalankan inference menggunakan model yang sudah dilatih.",
    )

    cards = st.columns(2)
    with cards[0].container(border=True, height="stretch"):
        st.subheader("📊 Data penelitian")
        st.write("Dataset final research STATS19 berisi 513.801 record periode 2021–2025.")
        st.caption("Development 412.276 · final holdout 2025: 101.525 · 18 fitur input")
        st.button("Dashboard Dataset", key="home_dataset", on_click=navigate_to, args=("📊 Dashboard Dataset",), width="stretch")
    with cards[1].container(border=True, height="stretch"):
        st.subheader("🔮 Data baru / inference")
        st.write("Masukkan karakteristik kecelakaan baru untuk memperoleh prediksi severity atau kelompok karakteristik.")
        st.button("Prediksi Severity", key="home_classification", on_click=navigate_to, args=("🔮 Prediksi Severity",), width="stretch")
        st.button("Analisis Cluster", key="home_clustering", on_click=navigate_to, args=("🧩 Analisis Cluster",), width="stretch")

    st.subheader("Bagaimana cara kerjanya?")
    flow = st.columns(4)
    for column, title, detail in zip(
        flow,
        ["Input data", "Preprocessing", "Model machine learning", "Hasil analisis"],
        ["18 karakteristik", "Imputation, scaling, encoding", "Random Forest atau K-Means", "Severity atau cluster"],
    ):
        with column.container(border=True):
            st.markdown(f"**{title}**")
            st.caption(detail)
    st.caption("Data penelitian → preprocessing → model → hasil analisis")
    st.caption("Data baru → preprocessing yang sama → model final → prediksi / cluster")

    render_model_cards()

    st.subheader("Mulai dalam 3 langkah")
    steps = st.columns(3)
    for column, number, text in zip(steps, ["1", "2", "3"], ["Pilih metode analisis", "Isi karakteristik kecelakaan", "Klik tombol analisis dan baca hasilnya"]):
        with column.container(border=True):
            st.metric("Langkah", number)
            st.write(text)

    st.subheader("Untuk siapa aplikasi ini?")
    st.write("Mahasiswa · Dosen · Peneliti · Pengguna yang ingin memahami hasil analisis data kecelakaan")
    render_identity()
    st.info("Prediksi classification hanya berdasarkan karakteristik input yang dimasukkan, bukan prediksi risiko kecelakaan secara umum.", icon=":material/info:")


def profile_value(profile: pd.DataFrame, cluster: int, feature: str, column: str) -> object:
    rows = profile[(profile["cluster"] == cluster) & (profile["feature"] == feature)]
    if rows.empty:
        return "-"
    return rows.iloc[0][column]


def render_about_data(artifacts: dict) -> None:
    st.title("Tentang data")
    render_section_banner(
        "data",
        "Sumber dan cakupan penelitian",
        "Data apa yang digunakan project ini?",
        "Project ini menggunakan seluruh dataset final research STATS19 periode 2021–2025. "
        "Dashboard clustering yang tersedia tetap merupakan hasil historis legacy C3–C4 dari 10.000 record.",
    )

    metric_columns = st.columns(4)
    for column, label, value in zip(
        metric_columns,
        ["Raw dataset", "Development / holdout", "Fitur input", "Pendekatan ML"],
        ["513.801", "412.276 / 101.525", "18", "2"],
    ):
        with column.container(border=True):
            st.metric(label, value)

    with st.container(border=True):
        st.subheader("Sumber data")
        st.write("Sumber data: **STATS19** — dataset data kecelakaan lalu lintas jalan.")
        st.write("Dataset raw penelitian: **513.801 record × 44 kolom**. Clustering legacy C3–C4 menggunakan **10.000 record**, yaitu 2.000 record per tahun.")
        st.caption("Classification final memakai development 2021–2024 dan final holdout 2025. Dashboard clustering tetap menampilkan hasil legacy 10K.")
        st.caption("URL resmi STATS19 belum disimpan sebagai referensi project. Tambahkan URL resmi jika diperlukan untuk laporan akademik.")

    render_research_data_split()

    st.subheader("18 fitur yang digunakan")
    numeric, categorical = st.columns(2)
    with numeric.container(border=True):
        st.markdown(f"**Fitur numerik ({len(NUMERIC_FEATURES)})**")
        st.markdown("\n".join(f"- {feature}" for feature in NUMERIC_FEATURES))
    with categorical.container(border=True):
        st.markdown(f"**Fitur kategorikal ({len(CATEGORICAL_FEATURES)})**")
        st.markdown("\n".join(f"- {feature}" for feature in CATEGORICAL_FEATURES))
    st.caption(f"{len(NUMERIC_FEATURES)} fitur numerik + {len(CATEGORICAL_FEATURES)} fitur kategorikal = 18 fitur input sesuai pipeline final.")

    st.subheader("Pemisahan classification dan clustering")
    classification, clustering = st.columns(2)
    with classification.container(border=True):
        st.subheader("🔵 Classification")
        st.write("Target: collision_severity dengan kelas Fatal, Serious, dan Slight.")
        st.markdown("- Training/eksperimen: **311.349 record (2021–2023)**\n- Validation: **100.927 record (2024)**\n- Refit development: **412.276 record (2021–2024)**\n- Final holdout: **101.525 record (2025)**\n- Tujuan: memprediksi kelas pada data baru")
    with clustering.container(border=True):
        st.subheader("🟠 Clustering")
        st.write("Clustering legacy C3–C4 menggunakan **10.000 record** untuk menemukan kelompok karakteristik.")
        st.markdown("- Tidak memakai collision_severity\n- Tidak memakai number_of_casualties\n- Tidak memakai identifier atau kode administratif")

    st.subheader("Data yang sengaja tidak digunakan")
    st.info(
        "Clustering berfokus pada pola karakteristik kecelakaan. Karena itu target severity, jumlah korban, "
        "identifier, kode administratif, dan variabel outcome tidak digunakan sebagai input clustering.",
        icon=":material/block:",
    )

    st.subheader("Preprocessing")
    render_pipeline(["Data mentah", "Imputation", "Scaling / encoding", "Model"])
    prep_left, prep_right = st.columns(2)
    with prep_left.container(border=True):
        st.subheader("Classification")
        st.markdown("- Numerik: Median Imputation\n- Kategorikal: Most Frequent Imputation → One-Hot Encoding")
        st.caption("18 fitur → 149 encoded features. Final preprocessor dipelajari dari development 2021–2024.")
    with prep_right.container(border=True):
        st.subheader("Clustering")
        st.markdown("- Numerik: imputation bila diperlukan → StandardScaler\n- Kategorikal: Most Frequent Imputation → One-Hot Encoding")
        st.caption("18 fitur → 108 encoded features. Preprocessor dipelajari dari clustering legacy C3–C4 menggunakan 10.000 record.")
    st.write("Imputation menangani nilai kosong. One-Hot Encoding mengubah kategori menjadi representasi numerik.")

    st.subheader("Mengapa data ini digunakan?")
    st.write("Fitur yang dipilih menggambarkan kendaraan, jalan, persimpangan, kondisi lingkungan, dan waktu kejadian. "
             "Karakteristik tersebut relevan untuk memahami pola kecelakaan tanpa memasukkan target classification ke clustering.")
    render_identity()


def render_dataset_dashboard(artifacts: dict) -> None:
    st.title("Dashboard dataset")
    render_section_banner(
        "data",
        "Hasil analisis data penelitian",
        "Dashboard dataset penelitian",
        "Ringkasan berikut menggunakan dataset final research. Bagian clustering di bawah dipisahkan sebagai analisis legacy C3–C4 dengan 10.000 record. "
        "Dashboard ini tidak melakukan training ulang dan bukan halaman inference.",
    )
    results = load_dataset_results()
    if results["missing"]:
        st.warning("Sebagian output dataset belum tersedia: " + ", ".join(results["missing"]))
        return

    cluster_size = results["cluster_size"]
    numeric_profile = results["numeric_profile"]
    categorical_profile = results["categorical_profile"]
    evaluation = results["k_evaluation"]
    pca_variance = results["pca_variance"]

    st.subheader("Ringkasan dataset")
    with st.container(horizontal=True):
        st.metric("Raw dataset", "513.801", border=True)
        st.metric("Kolom raw", "44", border=True)
        st.metric("Periode", "2021–2025", border=True)
        st.metric("Fitur final", "18", border=True)
        st.metric("Development / holdout", "412.276 / 101.525", border=True)

    st.info(
        "Split classification final: train 2021–2023 = 311.349, validation 2024 = 100.927, "
        "refit development 2021–2024 = 412.276, dan final holdout 2025 = 101.525. "
        "Hasil clustering pada bagian berikut berasal dari pipeline legacy C3–C4 dengan 10.000 record dan bukan seluruh raw dataset.",
        icon=":material/info:",
    )

    render_research_data_split()

    st.subheader("🟠 Hasil Clustering — Analisis Legacy C3–C4")
    st.write("Bagian ini merangkum ukuran, profil, evaluasi k, dan visualisasi cluster. Semua hasil berasal dari output C3–C4 yang sudah tersedia.")
    st.subheader("Distribusi cluster")
    distribution_left, distribution_right = st.columns(2)
    with distribution_left.container(border=True):
        st.bar_chart(cluster_size.set_index("cluster")["count"], x_label="Cluster", y_label="Jumlah record")
    with distribution_right.container(border=True):
        distribution_table = cluster_size.copy()
        distribution_table["cluster"] = distribution_table["cluster"].map(lambda value: f"Cluster {value}")
        distribution_table["percentage"] = distribution_table["percentage"].map(lambda value: f"{value:.2f}%")
        st.dataframe(distribution_table, hide_index=True, width="stretch")

    st.subheader("Profil cluster")
    profile_columns = st.columns(2)
    for column, cluster in zip(profile_columns, [0, 1]):
        cluster_rows = cluster_size[cluster_size["cluster"] == cluster]
        count = int(cluster_rows.iloc[0]["count"])
        percentage = float(cluster_rows.iloc[0]["percentage"])
        with column.container(border=True):
            st.subheader(f"Cluster {cluster}")
            st.metric("Record", f"{count:,}".replace(",", "."), f"{percentage:.2f}%")
            if cluster == 0:
                st.write("Cluster 0 menunjukkan pola karakteristik yang dominan pada wilayah rural dan batas kecepatan yang relatif lebih tinggi.")
                rural = profile_value(categorical_profile, cluster, "urban_or_rural_area", "dominant_percentage")
                road_class = profile_value(categorical_profile, cluster, "first_road_class", "dominant_percentage")
                speed_mean = profile_value(numeric_profile, cluster, "speed_limit", "mean")
                speed_median = profile_value(numeric_profile, cluster, "speed_limit", "median")
                st.markdown(f"- Rural: **{float(rural):.2f}%**\n- Mean speed limit: **{float(speed_mean):.2f}**\n- Median speed limit: **{float(speed_median):.0f}**\n- First road class A: **{float(road_class):.2f}%**")
            else:
                st.write("Cluster 1 menunjukkan pola karakteristik yang dominan pada wilayah urban dan batas kecepatan yang relatif lebih rendah.")
                urban = profile_value(categorical_profile, cluster, "urban_or_rural_area", "dominant_percentage")
                road_class = profile_value(categorical_profile, cluster, "first_road_class", "dominant_percentage")
                road_type = profile_value(categorical_profile, cluster, "road_type", "dominant_percentage")
                junction = profile_value(categorical_profile, cluster, "junction_control", "dominant_percentage")
                speed_mean = profile_value(numeric_profile, cluster, "speed_limit", "mean")
                speed_median = profile_value(numeric_profile, cluster, "speed_limit", "median")
                st.markdown(f"- Urban: **{float(urban):.2f}%**\n- Mean speed limit: **{float(speed_mean):.2f}**\n- Median speed limit: **{float(speed_median):.0f}**\n- Unclassified first road class: **{float(road_class):.2f}%**\n- Single carriageway: **{float(road_type):.2f}%**\n- Give way or uncontrolled: **{float(junction):.2f}%**")
    st.caption("Interpretasi cluster bersifat deskriptif berdasarkan profiling C4. Cluster bukan severity, tingkat keamanan, atau tingkat bahaya.")

    st.subheader("Evaluasi K-Means")
    display_evaluation = evaluation.copy()
    for column_name in ["inertia", "silhouette", "davies_bouldin", "calinski_harabasz"]:
        display_evaluation[column_name] = display_evaluation[column_name].map(lambda value: f"{value:.6f}")
    st.dataframe(display_evaluation, hide_index=True, width="stretch")
    chart_data = evaluation.set_index("k")
    first_charts = st.columns(2)
    with first_charts[0].container(border=True):
        st.markdown("**Elbow / inertia**")
        st.line_chart(chart_data["inertia"], x_label="k", y_label="Inertia")
    with first_charts[1].container(border=True):
        st.markdown("**Silhouette**")
        st.line_chart(chart_data["silhouette"], x_label="k", y_label="Silhouette")
    second_charts = st.columns(2)
    with second_charts[0].container(border=True):
        st.markdown("**Davies-Bouldin**")
        st.line_chart(chart_data["davies_bouldin"], x_label="k", y_label="Davies-Bouldin")
    with second_charts[1].container(border=True):
        st.markdown("**Calinski-Harabasz**")
        st.line_chart(chart_data["calinski_harabasz"], x_label="k", y_label="Calinski-Harabasz")
    st.success("k=2 dipilih karena memiliki Silhouette tertinggi, Davies-Bouldin terendah, dan Calinski-Harabasz tertinggi.", icon=":material/check_circle:")

    st.subheader("Visualisasi PCA")
    pca_left, pca_right = st.columns([1, 1.4])
    with pca_left.container(border=True):
        variance_table = pca_variance.copy()
        variance_table["explained_variance_ratio"] = variance_table["explained_variance_ratio"].map(lambda value: f"{value:.4%}")
        st.dataframe(variance_table, hide_index=True, width="stretch")
        st.caption("PCA digunakan hanya untuk membantu visualisasi hasil clustering dalam dua dimensi. PCA tidak digunakan untuk membentuk cluster.")
    with pca_right.container(border=True):
        if results["pca_image"].exists():
            st.image(str(results["pca_image"]), caption="PCA visualization dari hasil C4")

    with st.expander("Detail profil fitur C4", icon=":material/table_chart:"):
        st.dataframe(results["feature_comparison"], hide_index=True, width="stretch")

    st.subheader("🔵 Hasil classification — evaluasi model")
    st.caption("Metrik berikut adalah evaluasi final candidate Random Forest pada final holdout 2025 (101.525 record).")
    metric_columns = st.columns(5)
    for column, (label, value) in zip(metric_columns, CLASSIFICATION_METRICS.items()):
        with column.container(border=True):
            st.metric(label, value)
    render_fatal_metrics()
    st.caption("Accuracy tidak sebaiknya dibaca sendirian karena performa model antar kelas berbeda. Classification dan clustering memiliki tujuan berbeda.")
    st.info("Report dan confusion matrix CSV yang tersimpan tidak ditampilkan karena nilainya tidak cocok dengan metadata artefak classification final 18 fitur. Dashboard hanya menampilkan metrik final yang tercatat pada metadata artefak.", icon=":material/info:")
    render_evaluation_explanations()


def render_classification(artifacts: dict) -> None:
    st.title("Prediksi tingkat keparahan kecelakaan")
    render_section_banner(
        "classification",
        "🔵 Classification — prediksi tingkat keparahan",
        "Gunakan model berlabel untuk memprediksi collision_severity",
        "Classification memprediksi suatu kelas berdasarkan pola yang dipelajari dari data berlabel. "
        "Pada project ini kelasnya adalah Fatal, Serious, dan Slight.",
    )
    st.write("Halaman ini digunakan untuk memprediksi data baru. Hasilnya bukan hasil pengelompokan cluster.")
    render_pipeline(["Data kecelakaan", "18 fitur", "Preprocessing", "Random Forest", "Prediksi severity"])
    with st.expander("🌳 Apa itu Random Forest?", icon=":material/forest:"):
        st.write("Random Forest menggabungkan banyak decision tree. Setiap tree memberikan keputusan, kemudian hasil dari banyak tree digabungkan menjadi prediksi akhir.")
        st.markdown("- Model: **Random Forest**\n- Trees: **100**\n- max_depth: **12**\n- min_samples_leaf: **20**\n- class_weight: **balanced**\n- random_state: **42**\n- Fitur awal: **18**\n- Setelah preprocessing dan One-Hot Encoding: **149**")
        st.caption("Artifact `models/final_research_model.joblib` adalah final research model yang sudah dilatih. Evaluasinya menggunakan final holdout 2025 sebanyak 101.525 record; saat data baru dimasukkan, aplikasi hanya menjalankan inference dan tidak melakukan training ulang.")

    st.selectbox(
        "Gunakan contoh skenario",
        options=list(SCENARIO_DEFINITIONS),
        key="classification_scenario",
        help="Memilih skenario hanya mengisi contoh nilai awal. Semua input tetap dapat diedit sebelum prediksi.",
        on_change=apply_classification_scenario,
        args=(artifacts,),
    )

    values, submitted = input_form(artifacts, "classification", "classification_category_options", "Prediksi Tingkat Keparahan")
    if not submitted:
        st.caption("Tip: arahkan kursor ke ikon bantuan (?) pada setiap input untuk membaca arti fitur.")
        return

    model = artifacts["classification_model"]
    threshold = artifacts["classification_threshold"]
    frame = classification_frame(values)
    prediction, probabilities = final_classification_prediction(model, frame, threshold)

    st.subheader("🔵 Hasil classification")
    st.markdown(f"<div class='severity-card'><div class='label'>Prediksi tingkat keparahan</div><div class='value'>{prediction}</div></div>", unsafe_allow_html=True)
    st.write("Input baru telah diproses dengan preprocessor final, lalu diprediksi oleh Random Forest.")
    if probabilities is not None:
        st.subheader("Probability")
        probability_columns = st.columns(len(model.classes_))
        for column, label_code, probability in zip(probability_columns, model.named_steps["model"].classes_, probabilities):
            label = CLASS_LABELS[int(label_code)]
            with column:
                st.metric(label, f"{probability:.2%}")
                st.progress(float(probability), text=f"{label}: {probability:.2%}")
        probability_table = pd.DataFrame(
            {"Kelas": [CLASS_LABELS[int(label)] for label in model.named_steps["model"].classes_], "Probability": probabilities}
        ).set_index("Kelas")
        st.bar_chart(probability_table, y="Probability", x_label="Kelas", y_label="Probability", height=250)
        st.caption("Probabilitas prediksi model menunjukkan skor relatif untuk tiap kelas, bukan kepastian atau jaminan hasil pasti.")
        st.metric("Threshold Fatal", f"{threshold:.2f}")
        st.info("Jika probabilitas Fatal mencapai threshold, hasil diputuskan sebagai Fatal. Jika tidak, kelas Serious/Slight dengan probabilitas terbesar dipilih.", icon=":material/info:")

    with st.expander("Bagaimana hasil ini diperoleh?", icon=":material/account_tree:"):
        st.write("18 fitur input → preprocessing → 149 fitur hasil encoding → Random Forest → threshold Fatal 0,50 → prediksi collision_severity")
    st.warning("Hasil ini merupakan prediksi model machine learning berdasarkan karakteristik input dan bukan diagnosis atau penilaian resmi tingkat keparahan kecelakaan.", icon=":material/warning:")



def render_clustering(artifacts: dict) -> None:
    st.title("Identifikasi pola kecelakaan")
    render_section_banner(
        "clustering",
        "🟠 Clustering — identifikasi pola kecelakaan",
        "Gunakan unsupervised learning untuk menemukan kelompok karakteristik",
        "Clustering mengelompokkan data berdasarkan kemiripan karakteristik tanpa menggunakan label severity sebagai dasar pembentukan kelompok.",
    )
    render_pipeline(["Data kecelakaan", "18 fitur", "Preprocessing", "K-Means", "Cluster 0 / Cluster 1"])
    st.warning("CLUSTER BUKAN TINGKAT KEPARAHAN. Cluster hanya menunjukkan kelompok karakteristik yang mirip, bukan Fatal, Serious, atau Slight.", icon=":material/warning:")
    with st.expander("📍 Apa itu K-Means?", icon=":material/hub:"):
        st.write("K-Means membagi data menjadi sejumlah kelompok berdasarkan kedekatan karakteristik terhadap pusat kelompok yang disebut centroid.")
        st.markdown("- k = **2** berarti model membentuk dua kelompok\n- Setiap input ditempatkan pada cluster yang paling dekat\n- Distance to centroid mengukur kedekatan input dengan pusat cluster\n- Jarak yang lebih kecil berarti karakteristik input lebih dekat dengan centroid")
        st.caption("Konfigurasi aktual: K-Means, k=2, n_init=10, random_state=42, 10.000 record legacy C3–C4, 18 fitur awal, 108 fitur encoded.")

    values, submitted = input_form(artifacts, "clustering", "clustering_category_options", "Temukan Cluster")
    if not submitted:
        st.caption("Tip: cluster menunjukkan kemiripan karakteristik, bukan tingkat keparahan.")
        return

    frame = values_to_frame(values)
    preprocessor = artifacts["clustering_preprocessor"]
    model = artifacts["clustering_model"]
    encoded = preprocessor.transform(frame)
    cluster = int(model.predict(encoded)[0])
    distances = model.transform(encoded)[0]
    distance = float(distances[cluster])
    interpretation = CLUSTER_INTERPRETATIONS[cluster]

    st.subheader("🟠 Hasil clustering")
    st.markdown(f"<div class='result-card'><h2>Cluster terdekat: Cluster {cluster}</h2><p>{interpretation['summary']}</p></div>", unsafe_allow_html=True)
    st.write(f"Input Anda memiliki karakteristik yang lebih dekat dengan Cluster {cluster}.")
    metric_left, metric_right = st.columns(2)
    with metric_left:
        st.metric("Nomor cluster", f"Cluster {cluster}")
    with metric_right:
        st.metric("Jarak ke centroid", f"{distance:.4f}", help="Jarak ke centroid menunjukkan seberapa dekat karakteristik input terhadap pusat cluster. Nilai yang lebih kecil berarti input lebih dekat dengan pusat cluster tersebut.")

    st.subheader(f"Karakteristik dominan Cluster {cluster}")
    for detail in interpretation["details"]:
        st.write(f"• {detail}")
    st.info("Interpretasi cluster bersifat deskriptif. Cluster tidak menunjukkan bahwa suatu kondisi lebih berbahaya atau memiliki severity tertentu.", icon=":material/info:")


def render_guide() -> None:
    st.title("Panduan penggunaan")
    st.write("Gunakan panduan ini untuk memahami alur aplikasi dan membaca hasilnya tanpa perlu pengetahuan teknis mendalam.")
    with st.container(border=True):
        st.subheader("Memulai aplikasi")
        st.markdown("1. Buka halaman Beranda.\n2. Pilih Prediksi Severity atau Analisis Cluster.\n3. Isi 18 karakteristik.\n4. Pastikan semua input sudah benar.\n5. Klik tombol analisis.\n6. Baca hasil dan penjelasannya.")
    with st.expander("Cara menggunakan Tentang Data", icon=":material/database:"):
        st.markdown("1. Buka halaman **Tentang Data**.\n2. Baca sumber STATS19, periode, sampling, target, dan 18 fitur.\n3. Gunakan bagian pemisahan analisis untuk membedakan classification dan clustering.")
    with st.expander("Cara menggunakan Dashboard Dataset", icon=":material/dashboard:"):
        st.markdown("1. Buka halaman **Dashboard Dataset**.\n2. Baca ringkasan dataset penelitian dan pembagian data.\n3. Perhatikan bahwa analisis cluster adalah legacy C3–C4 dengan 10.000 record.\n4. Bandingkan profil Cluster 0 dan Cluster 1.\n5. Gunakan tabel dan grafik evaluasi K-Means untuk memahami alasan pemilihan k=2.\n6. Baca visualisasi PCA sebagai bantuan visual saja; PCA tidak digunakan untuk membentuk cluster.")
    with st.expander("Cara menggunakan Prediksi Severity", icon=":material/analytics:"):
        st.markdown("1. Buka halaman **Prediksi Severity**.\n2. Isi informasi kendaraan, jalan, kondisi lingkungan, dan waktu kejadian.\n3. Baca hasil kelas Fatal, Serious, atau Slight.\n4. Gunakan probabilitas sebagai keluaran model, bukan kepastian.\n5. Perhatikan disclaimer sebelum menarik kesimpulan.")
    with st.expander("Cara menggunakan Clustering", icon=":material/hub:"):
        st.markdown("1. Buka halaman **Analisis Cluster**.\n2. Isi karakteristik kecelakaan yang ingin dianalisis.\n3. Klik **Temukan Cluster**.\n4. Baca cluster dan jarak ke centroid.\n5. Gunakan profil C4 untuk memahami pola, bukan untuk menyimpulkan severity atau keamanan.")
    with st.container(border=True):
        st.subheader("Bagaimana membaca hasil")
        st.markdown("- **Prediction**: kelas yang dipilih Random Forest.\n- **Probability**: keluaran model untuk masing-masing kelas; bukan jaminan kebenaran.\n- **Cluster**: kelompok karakteristik yang paling dekat dengan input.\n- **Jarak centroid**: kedekatan input dengan pusat cluster; bukan probabilitas.")
    with st.container(border=True):
        st.subheader("Hal yang perlu diperhatikan")
        st.markdown("- Model bukan pengganti penilaian resmi.\n- Hasil bergantung pada karakteristik input.\n- Model final dipelajari dari data penelitian; clustering yang ditampilkan pada dashboard berasal dari legacy C3–C4.\n- Classification dan clustering memiliki tujuan berbeda.\n- Clustering tidak menggunakan collision_severity sebagai input.")
    st.subheader("Glosarium machine learning")
    for term, definition in GLOSSARY.items():
        with st.expander(term):
            st.write(definition)


def render_feature_dictionary(artifacts: dict) -> None:
    st.title("Kamus fitur")
    st.write("Cari nama fitur, istilah jalan, cuaca, junction, atau arti fitur untuk memahami input yang digunakan model.")
    query = st.text_input("Cari fitur", placeholder="Contoh: weather, junction, road, speed", key="feature_search")
    rows = []
    for feature in FEATURES:
        options = artifacts["classification_category_options"].get(feature, [])
        examples = ", ".join(option_label(value, feature, artifacts["mappings"]) for value in options[:3])
        rows.append({
            "Nama fitur": feature,
            "Nama tampilan": FEATURE_LABELS[feature],
            "Arti": FEATURE_HELP[feature],
            "Contoh nilai": examples or "-",
            "Kategori": "Numerik" if feature in NUMERIC_FEATURES else "Kategorikal",
        })
    dictionary = pd.DataFrame(rows)
    if query.strip():
        search = query.strip().lower()
        mask = dictionary.astype(str).apply(lambda column: column.str.lower().str.contains(search, na=False)).any(axis=1)
        dictionary = dictionary[mask]

    numeric, categorical = st.tabs(["Fitur numerik", "Fitur kategorikal"])
    with numeric:
        st.dataframe(
            dictionary[dictionary["Kategori"] == "Numerik"],
            hide_index=True,
            width="stretch",
            height=360,
            column_config={
                "Nama fitur": st.column_config.TextColumn(width="medium"),
                "Nama tampilan": st.column_config.TextColumn(width="medium"),
                "Arti": st.column_config.TextColumn(width="large"),
                "Contoh nilai": st.column_config.TextColumn(width="medium"),
                "Kategori": st.column_config.TextColumn(width="small"),
            },
        )
    with categorical:
        st.dataframe(
            dictionary[dictionary["Kategori"] == "Kategorikal"],
            hide_index=True,
            width="stretch",
            height=520,
            column_config={
                "Nama fitur": st.column_config.TextColumn(width="medium"),
                "Nama tampilan": st.column_config.TextColumn(width="medium"),
                "Arti": st.column_config.TextColumn(width="large"),
                "Contoh nilai": st.column_config.TextColumn(width="medium"),
                "Kategori": st.column_config.TextColumn(width="small"),
            },
        )


def render_about(artifacts: dict) -> None:
    st.title("Tentang model")
    st.write("Ringkasan akademik project, model final, preprocessing, evaluasi, dan batasan analisis.")
    render_identity()

    st.subheader("1. Ringkasan project")
    st.write("Traffic Accident Analysis adalah project analisis kecelakaan lalu lintas menggunakan machine learning. "
             "Classification memprediksi collision_severity, sedangkan clustering menemukan kelompok karakteristik kecelakaan.")
    render_pipeline(["DATA STATS19", "DATA UNDERSTANDING", "FEATURE SELECTION", "PREPROCESSING", "CLASSIFICATION / CLUSTERING"])
    st.caption("PCA hanya digunakan setelah final K-Means untuk membantu visualisasi cluster.")

    st.subheader("2. Sumber data dan sampling")
    with st.container(border=True):
        st.write("Sumber: **STATS19** · Dataset: data kecelakaan lalu lintas jalan · Periode: **2021–2025**")
        st.write("Dataset final research: **513.801 record** pada periode 2021–2025.")
        st.caption("Clustering legacy C3–C4 menggunakan 10.000 record. URL resmi STATS19 belum tersedia di project dan tidak digantikan dengan URL buatan.")

    st.subheader("3. Dataset dan 18 fitur")
    data_metrics = st.columns(4)
    for column, label, value in zip(
        data_metrics,
        ["Raw dataset", "Development / holdout", "Fitur awal", "Metode ML"],
        ["513.801", "412.276 / 101.525", "18", "2"],
    ):
        with column.container(border=True):
            st.metric(label, value)
    feature_left, feature_right = st.columns(2)
    with feature_left.container(border=True):
        st.markdown("**Numerik (1)**")
        st.markdown("\n".join(f"- {feature}" for feature in NUMERIC_FEATURES))
    with feature_right.container(border=True):
        st.markdown("**Kategorikal (17)**")
        st.markdown("\n".join(f"- {feature}" for feature in CATEGORICAL_FEATURES))
    st.caption("Target classification: collision_severity. Target tidak digunakan sebagai input clustering.")

    st.subheader("4. Preprocessing dan data leakage check")
    render_pipeline(["Data mentah", "Imputation", "Scaling / encoding", "Model"])
    prep_columns = st.columns(2)
    with prep_columns[0].container(border=True):
        st.subheader("Classification")
        st.write("Numerik: Median Imputation")
        st.write("Kategorikal: Most Frequent Imputation → One-Hot Encoding")
        st.caption("18 → 149 encoded features. Preprocessor fit pada development 2021–2024; holdout 2025 hanya ditransform.")
    with prep_columns[1].container(border=True):
        st.subheader("Clustering")
        st.write("Numerik: imputation bila diperlukan → StandardScaler")
        st.write("Kategorikal: Most Frequent Imputation → One-Hot Encoding")
        st.caption("18 → 108 encoded features. Preprocessor fit pada clustering legacy C3–C4 menggunakan 10.000 record.")
    st.success("Data leakage check: test set tidak dipakai untuk fitting preprocessor classification.", icon=":material/check_circle:")

    st.subheader("5. Classification — Random Forest")
    with st.container(border=True):
        st.write("Random Forest adalah supervised learning yang menggabungkan banyak decision tree. "
                 "Setiap tree memberi keputusan dan hasilnya digabungkan menjadi prediksi akhir.")
        st.markdown("- Model: **Random Forest**\n- 100 trees\n- max_depth = 12\n- min_samples_leaf = 20\n- class_weight = balanced\n- random_state = 42\n- Output: Fatal / Serious / Slight\n- Fatal threshold = 0,50")
        st.caption("Model final sudah dilatih sebelumnya. Aplikasi hanya menjalankan inference, tanpa retraining atau tuning.")
    st.subheader("Evaluasi classification")
    st.caption("Metrik berikut berasal dari evaluasi final research model pada final holdout 2025 (101.525 record).")
    metric_columns = st.columns(5)
    for column, (label, value) in zip(metric_columns, CLASSIFICATION_METRICS.items()):
        with column.container(border=True):
            st.metric(label, value)
    render_fatal_metrics()
    render_evaluation_explanations()

    st.subheader("6. Clustering — K-Means")
    with st.container(border=True):
        st.write("K-Means adalah unsupervised learning yang membagi data menjadi kelompok berdasarkan kedekatan karakteristik terhadap centroid.")
        st.markdown("- k = 2\n- n_init = 10\n- random_state = 42\n- Record clustering legacy C3–C4: 10.000\n- Output: Cluster 0 / Cluster 1")
        st.warning("Cluster bukan severity. Cluster tidak memakai collision_severity, number_of_casualties, identifier, atau kode administratif.", icon=":material/warning:")

    st.subheader("7. Evaluasi jumlah cluster")
    display_evaluation = artifacts["clustering_evaluation"].copy()
    for column in ["inertia", "silhouette", "davies_bouldin", "calinski_harabasz"]:
        if column in display_evaluation:
            display_evaluation[column] = display_evaluation[column].map(lambda value: f"{value:.6f}")
    st.dataframe(display_evaluation, hide_index=True, width="stretch")
    st.success("k=2 dipertahankan berdasarkan evaluasi C3 yang sudah tersedia; angka tidak dihitung ulang oleh aplikasi.", icon=":material/check_circle:")

    st.subheader("8. Profil cluster")
    profile_columns = st.columns(2)
    for column, cluster in zip(profile_columns, [0, 1]):
        with column.container(border=True):
            st.subheader(f"Cluster {cluster}")
            for detail in CLUSTER_INTERPRETATIONS[cluster]["details"]:
                st.write(f"• {detail}")
    st.caption("Profil bersifat deskriptif dan tidak boleh dibaca sebagai tingkat bahaya atau severity.")

    st.subheader("9. PCA untuk visualisasi")
    pca_results = load_dataset_results()
    if not pca_results["missing"]:
        variance_table = pca_results["pca_variance"].copy()
        variance_table["explained_variance_ratio"] = variance_table["explained_variance_ratio"].map(lambda value: f"{value:.4%}")
        st.dataframe(variance_table, hide_index=True, width="stretch")
        st.caption("PC1 = 14,9170% · PC2 = 9,5219% · Total = 24,4388%. PCA hanya visualisasi setelah final K-Means, bukan input K-Means dan bukan model prediction.")
    else:
        st.info("Output PCA belum tersedia.", icon=":material/info:")

    st.subheader("10. Inference dan batasan")
    st.markdown("- Data penelitian digunakan untuk membangun dan mengevaluasi model.\n- Data baru digunakan saat aplikasi menjalankan inference.\n- Probability adalah keyakinan relatif model, bukan jaminan kebenaran.\n- Distance to centroid adalah kedekatan input ke pusat cluster, bukan probabilitas.\n- Model bukan pengganti penilaian resmi atau diagnosis kecelakaan.\n- Hasil bergantung pada kualitas dan karakteristik data input.")
    st.caption("Konfigurasi model, feature selection, preprocessing, hasil C1–C4, dan artifact final tidak diubah oleh aplikasi.")

    st.subheader("11. Model yang digunakan")
    render_model_cards()

def render_footer() -> None:
    st.markdown("<div class='footer'>Traffic Accident Analysis<br>Machine Learning Classification &amp; Clustering<br>Rekayasa Perangkat Lunak · Asyudi Anggara · F552630019</div>", unsafe_allow_html=True)


def main() -> None:
    st.set_page_config(
        page_title="Traffic Accident Analysis",
        page_icon=":material/traffic:",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    inject_styles()
    st.sidebar.title("Traffic Accident Analysis")
    st.sidebar.caption("Classification & Clustering")
    st.sidebar.caption("Model Data Mining")
    st.sidebar.markdown("---")
    st.session_state.setdefault("page_nav", NAV_ITEMS[0])
    page = st.sidebar.radio("Navigasi", NAV_ITEMS, key="page_nav")
    st.sidebar.markdown("---")
    st.sidebar.caption("Inference-only app · tidak ada retraining")

    artifact_pages = {
        "🔮 Prediksi Severity",
        "🧩 Analisis Cluster",
        "📚 Kamus Fitur",
        "📊 Tentang Model",
    }
    artifacts = {}
    if page in artifact_pages:
        try:
            artifacts = load_artifacts()
        except Exception as error:
            st.error("Artefak final tidak dapat dimuat.", icon=":material/error:")
            st.exception(error)
            st.stop()

    if page == "🏠 Beranda":
        render_home()
    elif page == "📊 Dashboard Dataset":
        render_dataset_dashboard(artifacts)
    elif page == "📊 Tentang Data":
        render_about_data(artifacts)
    elif page == "🔮 Prediksi Severity":
        render_classification(artifacts)
    elif page == "🧩 Analisis Cluster":
        render_clustering(artifacts)
    elif page == "📖 Panduan Penggunaan":
        render_guide()
    elif page == "📚 Kamus Fitur":
        render_feature_dictionary(artifacts)
    else:
        render_about(artifacts)
    render_footer()


if __name__ == "__main__":
    main()
