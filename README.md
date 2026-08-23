# Traffic Accident Analysis

Aplikasi analitik edukatif untuk menganalisis karakteristik kecelakaan lalu
lintas menggunakan machine learning. Project ini menggabungkan hasil penelitian
classification dan clustering dengan aplikasi Streamlit yang dapat digunakan
untuk demonstrasi akademik.

## Academic Project

- **Course**: Rekayasa Perangkat Lunak
- **Student**: Asyudi Anggara
- **NIM**: F552630019
- **Institution**: Universitas Tadulako (UNTAD) — Palu
- **Repository**: <https://github.com/asyudianggara/traffic-accident-ml>

## Overview

Project menggunakan data kecelakaan lalu lintas STATS19 untuk dua tujuan:

1. **Classification** memprediksi kelas `collision_severity`: Fatal, Serious,
   atau Slight.
2. **Clustering** menemukan kelompok karakteristik kecelakaan yang mirip tanpa
   menggunakan severity sebagai input.

Aplikasi juga menyediakan dashboard historis untuk menjelajahi hasil C3/C4 yang
sudah tersedia. Dashboard historis berbeda dari inference: dashboard membaca
output penelitian, sedangkan inference memakai model final untuk satu input baru.

## Project Objective

Tujuan project adalah memahami pipeline data mining dari preprocessing,
classification, feature ablation, hyperparameter review, K-Means clustering,
profiling cluster, hingga productization dalam aplikasi Streamlit.

Project tidak melakukan retraining atau tuning saat aplikasi dijalankan.

## Dataset

- **Source**: Department for Transport (DfT) — Road Safety Open Data / STATS19
- **Dataset**: Road Safety Data — Collisions — Last 5 Years
- **Periode**: 2021–2025
- **Sample penelitian**: 10.000 record, 2.000 record per tahun

Dataset mentah berukuran besar tidak disertakan dalam repository public.
File lokalnya di-ignore melalui `.gitignore`. Siapkan dataset pada lokasi:

```text
data/raw/dft-road-casualty-statistics-collision-last-5-years.csv
```

Mapping kecil yang diperlukan aplikasi tersedia di `data/processed/stats19_maps.json`.

## Sampling

Notebook dan script penelitian mengambil 2.000 record per tahun untuk periode
2021–2025 menggunakan `random_state=42`, sehingga total sample menjadi 10.000
record. Dashboard menampilkan output sample tersebut dan tidak mengambil sample
baru.

## Feature Selection

Pipeline final menggunakan tepat 18 input features.

### Numerik

- `number_of_vehicles`
- `speed_limit`
- `hour`
- `month`

### Kategorikal

- `day_of_week`
- `first_road_class`
- `road_type`
- `junction_detail`
- `junction_control`
- `second_road_class`
- `pedestrian_crossing`
- `light_conditions`
- `weather_conditions`
- `road_surface_conditions`
- `special_conditions_at_site`
- `carriageway_hazards`
- `urban_or_rural_area`
- `trunk_road_flag`

Classification menggunakan target `collision_severity`. Clustering tidak
menggunakan `collision_severity`, `number_of_casualties`, identifier, kode
administratif, atau fitur outcome setelah kecelakaan.

## Data Preprocessing

Preprocessing final:

- Numerik: `SimpleImputer(strategy="median")` → `StandardScaler`
- Kategorikal: `SimpleImputer(strategy="most_frequent")` →
  `OneHotEncoder(handle_unknown="ignore")`

Classification menghasilkan **105 encoded features**. Clustering menghasilkan
**108 encoded features**.

## Classification

Model final:

```text
RandomForestClassifier(
    n_estimators=300,
    max_depth=15,
    class_weight="balanced",
    random_state=42,
    n_jobs=-1,
)
```

Alur inference:

```text
18 input features → final_preprocessor.joblib → 105 encoded features
→ final_random_forest.joblib → predicted severity + probabilities
```

Hasil evaluasi final yang dicatat pada metadata artefak:

- Accuracy: **63,85%**
- Macro Precision: **38,02%**
- Macro Recall: **40,08%**
- Macro F1: **38,62%**
- Weighted F1: **64,96%**

Accuracy tidak sebaiknya dibaca sendirian karena performa antar kelas berbeda.

## Clustering

Model final:

```text
KMeans(n_clusters=2, random_state=42, n_init=10)
```

Alur inference:

```text
18 input features → final_clustering_preprocessor.joblib → 108 encoded features
→ final_kmeans.joblib → cluster + distance to centroid
```

Clustering tidak memakai target severity dan tidak menggunakan PCA untuk
membentuk cluster.

## Cluster Profiling

Hasil profiling C4 menunjukkan:

- **Cluster 0**: 2.528 record atau 25,28%; dominan rural (92,37%), mean speed
  limit 57,69, dan first road class A sebesar 54,11%.
- **Cluster 1**: 7.472 record atau 74,72%; dominan urban (87,47%), mean speed
  limit 28,51, first road class Unclassified sebesar 41,82%, single carriageway
  75,46%, dan give way or uncontrolled 48,43%.

Interpretasi tersebut bersifat deskriptif. Cluster tidak berarti Fatal,
Serious, Slight, aman, atau berbahaya.

## PCA Visualization

PCA hanya digunakan untuk membantu visualisasi hasil clustering dalam dua
dimensi:

- PC1: 14,9170%
- PC2: 9,5219%
- Total: 24,4388%

**PCA tidak digunakan untuk membentuk cluster atau melakukan prediction.**

## Model Evaluation

C3 mengevaluasi `k=2,3,4,5,6` dengan inertia, Silhouette,
Davies-Bouldin, dan Calinski-Harabasz. `k=2` dipilih karena memiliki Silhouette
tertinggi, Davies-Bouldin terendah, dan Calinski-Harabasz tertinggi.

Output C3/C4 tersedia di `results/`, termasuk:

- `clustering_k_evaluation.csv`
- `clustering_cluster_size.csv`
- `clustering_numeric_profile.csv`
- `clustering_categorical_profile.csv`
- `clustering_feature_comparison.csv`
- `clustering_final_assignments.csv`
- `clustering_pca_variance.csv`
- `clustering_elbow.png`
- `clustering_silhouette.png`
- `clustering_pca.png`

## Web Application

Jalankan aplikasi dari root project:

```bat
.venv\Scripts\activate
streamlit run app.py
```

Atau:

```bat
.venv\Scripts\python.exe -m streamlit run app.py
```

## Application Features

Sidebar aplikasi menyediakan:

- Beranda
- Dashboard Dataset
- Prediksi Severity
- Analisis Cluster
- Panduan Penggunaan
- Kamus Fitur
- Tentang Model

Dashboard Dataset membaca output historis C3/C4. Prediksi Severity dan Analisis
Cluster melakukan inference satu baris menggunakan artefak final. Kamus Fitur
memiliki pencarian dan mapping kategori yang tersedia.

## System Architecture

```text
STATS19 raw dataset
        ↓
Sampling + feature engineering pada notebook/script penelitian
        ↓
Preprocessing final
        ├── Random Forest classification artifact
        └── K-Means clustering artifact
        ↓
Streamlit
        ├── Dashboard Dataset: hasil CSV/PNG C3-C4
        └── Inference: input 18 fitur → model final
```

## Installation

```bat
git clone https://github.com/asyudianggara/traffic-accident-ml.git
cd traffic-accident-ml
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Dataset mentah perlu disiapkan secara lokal karena tidak di-upload ke GitHub.
Model final dan mapping yang diperlukan aplikasi disimpan terpisah dari dataset
mentah.

## Running Locally

```bat
.venv\Scripts\python.exe -m streamlit run app.py
```

Notebook penelitian berada di `notebooks/`. Script C2/C3, C4, dan finalisasi
artefak berada di root project. Aplikasi tidak perlu menjalankan script tersebut
untuk inference.

## Usage Guide

1. Gunakan **Dashboard Dataset** untuk membaca hasil penelitian historis.
2. Gunakan **Prediksi Severity** untuk memasukkan karakteristik satu kecelakaan
   dan membaca kelas serta probabilitas model.
3. Gunakan **Analisis Cluster** untuk mengetahui kelompok karakteristik dan
   jarak ke centroid.
4. Gunakan **Panduan Penggunaan**, **Kamus Fitur**, dan **Tentang Model** untuk
   memahami istilah, evaluasi, dan keterbatasan.

## Project Structure

```text
traffic-accident-ml/
├── app.py
├── README.md
├── README_APP.md
├── requirements.txt
├── data/
│   ├── raw/                  # dataset lokal, tidak di-commit
│   └── processed/            # mapping STATS19 yang diperlukan
├── models/                   # artefak final yang digunakan aplikasi
├── notebooks/                # notebook penelitian C1-C3/classification
├── results/                  # hasil eksperimen dan profiling C3-C4
├── src/
└── .gitignore
```

## Model Artifacts

Classification:

- `models/final_random_forest.joblib`
- `models/final_preprocessor.joblib`
- `models/final_classification_metadata.json`

Clustering:

- `models/final_kmeans.joblib`
- `models/final_clustering_preprocessor.joblib`
- `models/final_clustering_metadata.json`

Artifact legacy 21 fitur tersedia lokal sebagai backup penelitian, tetapi tidak
digunakan aplikasi dan tetap di-ignore oleh Git.

## Testing

Validasi yang telah dilakukan:

- Python compile `app.py`
- Streamlit startup dengan HTTP 200
- Streamlit AppTest untuk Beranda, Dashboard Dataset, Prediksi Severity,
  Analisis Cluster, Panduan, Kamus Fitur, dan Tentang Model
- Classification: 18 input → 105 encoded features → prediction
- Clustering: 18 input → 108 encoded features → cluster
- Pengecekan bahwa aplikasi tidak merujuk artifact legacy atau
  `final_model_evaluation.py`

Tidak ada retraining atau hyperparameter tuning saat testing aplikasi.

## Limitations

- Model dibuat dari sample 10.000 record periode 2021–2025.
- Kualitas hasil bergantung pada kesesuaian karakteristik input.
- Performa classification antar kelas tidak sama; Macro F1 lebih rendah daripada
  Weighted F1.
- Clustering menemukan pola berdasarkan fitur yang digunakan, bukan tingkat
  keparahan kecelakaan.
- PCA hanya digunakan untuk visualisasi dua dimensi.
- Dashboard bersifat deskriptif dan tidak memperbarui hasil penelitian secara
  otomatis.

## Disclaimer

Hasil merupakan prediksi model berdasarkan karakteristik input dan bukan
penilaian resmi tingkat keparahan kecelakaan. Cluster bukan label severity,
tingkat keamanan, atau tingkat bahaya.

## Author

Asyudi Anggara — F552630019
Universitas Tadulako (UNTAD) — Palu
Mata Kuliah: Rekayasa Perangkat Lunak
