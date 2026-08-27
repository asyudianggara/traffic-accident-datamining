# Project Fact Sheet — Legacy Baseline Snapshot

> Dokumen historis untuk baseline classification legacy dan analisis clustering legacy C3–C4 10K. Dokumen ini **bukan** sumber fakta
> final Phase 6–8. Kontrak dan metrik final dirujuk dari `docs/FINAL_MODEL.md`.
> Tanggal audit: 25 Agustus 2026.

## Identitas

- Project: Traffic Accident Analysis
- Subjudul: Analisis Kecelakaan Lalu Lintas Menggunakan Machine Learning
- Mahasiswa: Asyudi Anggara — F552630019
- Institusi: Universitas Tadulako (UNTAD) – Palu
- Mata kuliah: Rekayasa Perangkat Lunak
- Repository aktif: https://github.com/asyudianggara/traffic-accident-datamining
- Branch: main

## Dataset

- Sumber: STATS19 / DfT Road Safety Open Data (collisions, last 5 years).
- Periode: 2021–2025.
- Sampling analisis clustering legacy C3–C4: 2.000 record/tahun × 5 tahun = **10.000 record** (`random_state=42`).
- Raw CSV: 44 kolom; pembacaan penuh ≈ 513.801 baris (notebook 01). 10.000 hanya untuk analisis clustering legacy C3–C4, bukan dataset utama penelitian final.
- Mapping: `data/processed/stats19_maps.json`.
- Target classification: `collision_severity` → Fatal, Serious, Slight.
- Referensi unduhan resmi STATS19: **belum tercatat (gap)**.

## Kontrak fitur legacy classification — 18 fitur

- Numerik (4): `number_of_vehicles`, `speed_limit`, `hour`, `month`.
- Kategorikal (14): `day_of_week`, `first_road_class`, `road_type`, `junction_detail`, `junction_control`, `second_road_class`, `pedestrian_crossing`, `light_conditions`, `weather_conditions`, `road_surface_conditions`, `special_conditions_at_site`, `carriageway_hazards`, `urban_or_rural_area`, `trunk_road_flag`.
- Tidak dipakai sebagai input: `collision_severity` (target), `number_of_casualties`, `collision_index`, `collision_ref_no`, kode administratif, `police_force`, `did_police_officer_attend_scene_of_accident`, outcome severity turunan.

## Classification — Legacy Baseline 10K (historical)

- Model: `RandomForestClassifier(n_estimators=300, max_depth=15, class_weight="balanced", random_state=42, n_jobs=-1)`.
- Split legacy: **8.000 train / 2.000 test**, stratified, `random_state=42`.
- Preprocessing: numerik median → StandardScaler; kategorikal most_frequent → OneHotEncoder(`handle_unknown="ignore"`).
- Preprocessor classification **hanya fit pada X_train**.
- Dimensi: 18 → **105 encoded features** (kontrak fitur legacy classification).
- Artifact legacy: `models/final_random_forest.joblib`, `models/final_preprocessor.joblib`, `models/final_classification_metadata.json`.

### Metrik aggregate final (sumber: `final_classification_metadata.json`)

| Metrik | Nilai |
|---|---:|
| Accuracy | 63,85% |
| Macro Precision | 38,02% |
| Macro Recall | 40,08% |
| Macro F1 | 38,62% |
| Weighted F1 | 64,96% |

### Laporan per kelas (sumber: `notebooks/03_classification.ipynb`)

| Kelas | Precision | Recall | F1 | Support |
|---|---:|---:|---:|---:|
| Fatal | 0,07 | 0,14 | 0,10 | 28 |
| Serious | 0,28 | 0,32 | 0,30 | 453 |
| Slight | 0,79 | 0,74 | 0,76 | 1.519 |

Catatan: angka ini hanya baseline legacy 10K. CSV `results/final_classification_report.csv` adalah output evaluator 21 fitur (stale) dan **bukan** sumber angka final Phase 6.

## Clustering legacy C3–C4

- Algoritma: K-Means.
- Data: seluruh **10.000 record analisis clustering legacy C3–C4** (tanpa split train/test).
- Preprocessing: sama dengan classification, **fit pada seluruh 10.000 record analisis clustering legacy C3–C4**.
- Dimensi: 18 → **108 encoded features**.
- Final: `KMeans(n_clusters=2, random_state=42, n_init=10)`.
- Artifact: `models/final_kmeans.joblib`, `models/final_clustering_preprocessor.joblib`, `models/final_clustering_metadata.json`.
- Cluster 0 = **2.528** (25,28%); Cluster 1 = **7.472** (74,72%).
- Pemilihan k=2: Silhouette tertinggi (0,143490), Davies-Bouldin terendah (2,387075), Calinski-Harabasz tertinggi (1287,425737).
- **Cluster bukan severity.**

### Evaluasi k (sumber: `results/clustering_k_evaluation.csv`)

| k | Inertia | Silhouette | Davies-Bouldin | Calinski-Harabasz |
|---:|---:|---:|---:|---:|
| 2 | 95756,560557 | 0,143490 | 2,387075 | 1287,425737 |
| 3 | 89650,949954 | 0,089714 | 2,763991 | 1027,902184 |
| 4 | 85735,264751 | 0,083531 | 2,821309 | 868,672373 |
| 5 | 82928,578533 | 0,085248 | 2,624441 | 758,056056 |
| 6 | 80289,582594 | 0,080003 | 2,506223 | 692,012594 |

### Profil cluster (sumber: `results/clustering_numeric_profile.csv`, `clustering_categorical_profile.csv`)

- Cluster 0: speed_limit mean 57,6938 / median 60; Rural 92,37%; first_road_class A 54,11%; junction_detail Not at or within 20m 77,29%; pedestrian_crossing 0 = 96,52%.
- Cluster 1: speed_limit mean 28,5091 / median 30; Urban 87,47%; first_road_class Unclassified 41,82%; road_type Single carriageway 75,46%; junction_control Give way or uncontrolled 48,43%.

## PCA (hanya visualisasi, setelah K-Means)

- PC1: 14,9170%; PC2: 9,5219%; Total: **24,4388%** (sumber: `results/clustering_pca_variance.csv`).
- PCA tidak dipakai untuk menentukan k, membentuk cluster, atau prediksi classification.

## Artifact final

- Classification legacy: `final_random_forest.joblib`, `final_preprocessor.joblib`, `final_classification_metadata.json`.
- Classification final research: `final_research_model.joblib` dengan kontrak fitur final research **18 fitur → 149 encoded**; lihat `docs/FINAL_MODEL.md`.
- Clustering: `final_kmeans.joblib`, `final_clustering_preprocessor.joblib`, `final_clustering_metadata.json`.
- Legacy 21 fitur (di-ignore, tidak dipakai app): `final_random_forest_legacy_21_features.joblib`, `final_preprocessor_legacy_21_features.joblib`.

## Streamlit

- `app.py`, mode inference-only (tanpa retraining/tuning/PCA inference).
- 8 halaman: Beranda, Dashboard Dataset, Tentang Data, Prediksi Severity, Analisis Cluster, Panduan Penggunaan, Kamus Fitur, Tentang Model.

## Testing

- `py_compile` PASS; Streamlit startup HTTP 200 PASS; AppTest 8 halaman PASS.
- Classification legacy 18→105, final research 18→149, dan clustering legacy C3–C4 18→108 PASS.
- Artifact load (149/108) PASS; metadata check PASS; aplikasi tidak menukar artifact legacy dengan final research PASS.
- Runtime `.venv` dan dependency terpin pada scikit-learn 1.9.0, sesuai versi artifact.

## Status kualitas

- Artifact load/shape: PASS.
- Angka classification legacy: bersumber dari metadata + notebook 03 (konsisten).
- Angka classification final Phase 6: bersumber dari `docs/FINAL_MODEL.md` dan metadata final research.
- CSV evaluation classification lama (21 fitur): stale — jangan kutip sebagai final.
- Diagram RPL formal & test case matrix: belum ada (gap).
