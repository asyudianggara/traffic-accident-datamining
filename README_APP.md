# Traffic Accident Analysis — Streamlit App

Aplikasi analitik edukatif berbasis Streamlit untuk memahami analisis kecelakaan
lalu lintas melalui dashboard historis dan dua pendekatan machine learning:

- **Dashboard Dataset**: eksplorasi output penelitian C3/C4 yang sudah tersedia.
- **Tentang Data**: sumber STATS19, sampling, target, 18 fitur, dan pemisahan analisis.
- **Prediksi Severity**: Random Forest memprediksi kelas `Fatal`, `Serious`, atau `Slight`.
- **Analisis Cluster**: K-Means mengelompokkan karakteristik kecelakaan yang mirip.

Aplikasi ini hanya melakukan inference terhadap model final. Tidak ada training,
tuning, PCA untuk prediction, atau pemanggilan `final_model_evaluation.py`.

Project akademik: Rekayasa Perangkat Lunak · Asyudi Anggara · F552630019 ·
Universitas Tadulako (UNTAD) — Palu.

## Fitur aplikasi

Navigasi utama tersedia di sidebar:

- **Beranda**: penjelasan tujuan, alur, dan quick start.
- **Dashboard Dataset**: distribusi, profiling, evaluasi K-Means, dan PCA visualization.
- **Tentang Data**: sumber data, periode, sampling, target, fitur, dan preprocessing.
- **Prediksi Severity**: form 18 fitur dengan bantuan istilah dan probabilitas model.
- **Analisis Cluster**: form 18 fitur, nomor cluster, jarak centroid, dan interpretasi C4.
- **Panduan Penggunaan**: langkah penggunaan dan glosarium machine learning.
- **Kamus Fitur**: pencarian nama, arti, contoh nilai, dan kategori 18 fitur.
- **Tentang Model**: konfigurasi, evaluasi, pemilihan k, dan keterbatasan.

## Requirements

Gunakan `requirements.txt` project yang sudah mencakup Streamlit, Pandas, NumPy,
Joblib, dan Scikit-learn.

## Instalasi dan menjalankan

Dari root project:

```bat
.venv\Scripts\activate
streamlit run app.py
```

Atau langsung menggunakan interpreter virtual environment:

```bat
.venv\Scripts\python.exe -m streamlit run app.py
```

## Input dan preprocessing

Aplikasi menggunakan tepat 18 fitur final:

- Numerik: `number_of_vehicles`, `speed_limit`, `hour`, `month`.
- Kategorikal: `day_of_week`, `first_road_class`, `road_type`,
  `junction_detail`, `junction_control`, `second_road_class`,
  `pedestrian_crossing`, `light_conditions`, `weather_conditions`,
  `road_surface_conditions`, `special_conditions_at_site`,
  `carriageway_hazards`, `urban_or_rural_area`, `trunk_road_flag`.

Preprocessing numerik menggunakan median imputation lalu `StandardScaler`.
Preprocessing kategorikal menggunakan most-frequent imputation lalu
`OneHotEncoder(handle_unknown="ignore")`.

Input classification menghasilkan 105 fitur encoded. Input clustering menghasilkan
108 fitur encoded. Mapping kategori dibaca dari
`data/processed/stats19_maps.json`; kategori yang tidak memiliki mapping resmi
ditampilkan sebagai kode STATS19.

## Struktur model final

Classification:

- `models/final_random_forest.joblib`
- `models/final_preprocessor.joblib`
- `models/final_classification_metadata.json`
- Random Forest: 300 trees, `max_depth=15`, `class_weight=balanced`, `random_state=42`

Clustering:

- `models/final_kmeans.joblib`
- `models/final_clustering_preprocessor.joblib`
- `models/final_clustering_metadata.json`
- K-Means: `k=2`, `n_init=10`, `random_state=42`

Artifact legacy 21 fitur tidak digunakan oleh aplikasi.

## Cara membaca hasil

Prediction adalah kelas yang dipilih Random Forest berdasarkan kombinasi input.
Probabilitas adalah keluaran model untuk masing-masing kelas, bukan kepastian
atau keputusan resmi.

Cluster menunjukkan kelompok karakteristik yang paling dekat dengan input.
Jarak ke centroid menunjukkan kedekatan terhadap pusat cluster; nilainya bukan
probabilitas. Profil Cluster 0 dan Cluster 1 hanya mengikuti profiling C4 dan
tidak berarti fatal, serious, slight, aman, atau berbahaya.

## Dashboard Dataset

Dashboard membaca hasil historis dari `results/`, termasuk distribusi cluster,
profil numerik/kategorikal, evaluasi k=2–6, grafik metrik K-Means, dan visualisasi
PCA. Dashboard bukan inference dan tidak menjalankan training. PCA hanya dipakai
untuk visualisasi dan tidak digunakan untuk membentuk cluster.

## Evaluasi yang ditampilkan

Classification:

- Accuracy: 63,85%
- Macro Precision: 38,02%
- Macro Recall: 40,08%
- Macro F1: 38,62%
- Weighted F1: 64,96%

Accuracy tidak dibaca sendirian karena performa antar kelas berbeda.

Pada evaluasi C3, `k=2` dipilih karena memiliki Silhouette tertinggi,
Davies-Bouldin terendah, dan Calinski-Harabasz tertinggi.

## Keterbatasan dan disclaimer

- Model dibuat berdasarkan sample 10.000 record periode 2021–2025.
- Hasil bergantung pada kualitas dan karakteristik input.
- Performa classification antar kelas tidak sama.
- Clustering menemukan pola berdasarkan fitur yang digunakan, bukan tingkat keparahan.
- PCA pada project hanya untuk visualisasi clustering, bukan prediction.

Hasil merupakan prediksi model berdasarkan karakteristik input dan bukan
penilaian resmi tingkat keparahan kecelakaan.

## Validasi

Regression test Streamlit memeriksa startup, pemuatan artifact final, delapan
halaman navigasi, classification inference, clustering inference, serta
jumlah fitur encoded 105 dan 108.
