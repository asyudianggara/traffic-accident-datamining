# Traffic Accident Analysis — Dokumentasi Master Project

> **Dokumen induk (single source of narrative)** untuk laporan tugas Rekayasa Perangkat Lunak.
> Status: hasil audit berbasis artefak repository (read-only terhadap model, notebook, dan hasil C1–C4).
> Tanggal audit final: 25 Agustus 2026.

## Fakta penting sebelum membaca

- **Tidak ada** retraining, tuning, atau eksperimen baru yang dijalankan dalam pembuatan dokumen ini.
- Semua angka final diambil dari *artifact* final dan *metadata* yang direferensikan `app.py`, atau dari *notebook*/CSV hasil C1–C4.
- Angka evaluasi classification disajikan dari dua level:
  - **Aggregate (5 metrik)**: `models/final_classification_metadata.json` — sumber kebenaran utama untuk model final (18 fitur → 105 encoded).
  - **Per-class**: `notebooks/03_classification.ipynb` (classification notebook) — laporan per kelas yang konsisten dengan aggregate metadata final (lihat *traceability*).
- `results/final_test_results.csv`, `results/final_classification_report.csv`, `results/final_confusion_matrix.*` berasal dari evaluator lama 21 fitur (`final_model_evaluation.py`) dan **tidak** dipakai sebagai sumber angka final aplikasi.

---

## 1. Identitas Project

| Item | Isi |
|---|---|
| Judul | Traffic Accident Analysis |
| Subjudul | Analisis Kecelakaan Lalu Lintas Menggunakan Machine Learning |
| Jenis tugas | Rekayasa Perangkat Lunak |
| Nama | Asyudi Anggara |
| NIM | F552630019 |
| Institusi | Universitas Tadulako (UNTAD) – Palu |
| Repository | https://github.com/asyudianggara/traffic-accident-ml |
| Branch | main |
| Bahasa/Stack | Python, Streamlit, scikit-learn, pandas, numpy, joblib, matplotlib, seaborn, altair |

---

## 2. Gambaran Umum

Project adalah aplikasi analitik edukatif yang menganalisis karakteristik kecelakaan lalu lintas jalan raya di Inggris (dataset STATS19) menggunakan dua pendekatan *machine learning*:

1. **Classification (terawasi)** — memprediksi `collision_severity` menjadi `Fatal`, `Serious`, atau `Slight`.
2. **Clustering (tidak terawasi)** — menemukan kelompok karakteristik kecelakaan yang mirip **tanpa** menggunakan severity sebagai input.

Kedua pendekatan menggunakan kontrak **18 fitur** yang sama. Hasil disajikan melalui aplikasi **Streamlit** yang beroperasi secara **inference-only** (tanpa pelatihan ulang saat runtime).

Aplikasi memiliki 8 halaman: Beranda, Dashboard Dataset, Tentang Data, Prediksi Severity, Analisis Cluster, Panduan Penggunaan, Kamus Fitur, dan Tentang Model.

---

## 3. Latar Belakang

Kecelakaan lalu lintas merupakan masalah publik. Department for Transport (DfT) Inggris menerbitkan data kecelakaan STATS19 secara terbuka. Project ini menggunakan subset data tersebut sebagai bahan studi *data mining*: memahami pola karakteristik kecelakaan dan mencoba mengelompokkan serta mengklasifikasikannya.

Tujuan akademiknya adalah mendemonstrasikan alur *Rekayasa Perangkat Lunak* modern: mulai dari pemahaman data, persiapan, *feature selection*, *preprocessing*, pembangunan model, evaluasi, hingga *productization* dalam aplikasi web.

> Catatan: *rumusan masalah* dan *penjelasan dosen/pengampu mata kuliah* belum ditemukan secara eksplisit di repository — lihat Dokumentation Gaps.

---

## 4. Tujuan

1. Membangun pipeline *classification* untuk memprediksi tingkat keparahan kecelakaan.
2. Membangun pipeline *clustering* untuk menemukan pola kelompok karakteristik kecelakaan.
3. Mencegah *data leakage* (target dan identifier tidak dipakai sebagai input clustering).
4. Menyajikan hasil melalui aplikasi Streamlit yang mudah dipahami pengguna awam.
5. Mendokumentasikan seluruh *pipeline* dan hasil secara terverifikasi untuk laporan RPL.

---

## 5. Dataset

| Item | Fakta |
|---|---|
| Sumber | Department for Transport (DfT) — Road Safety Open Data / STATS19 |
| Nama file lokal | `dft-road-casualty-statistics-collision-last-5-years.csv` |
| Periode | 2021–2025 |
| Sampling | 2.000 record per tahun, `random_state=42` |
| Total sample penelitian | **10.000 record** |
| Kolom raw | 44 kolom (lihat *data dictionary* di notebook 01) |
| Raw CSV | Di-ignore Git (`data/raw/`); tidak di-upload ke repository publik |
| Mapping | `data/processed/stats19_maps.json` (kode STATS19 → label) |

**Penting:** angka 10.000 adalah **sample penelitian**, bukan keseluruhan populasi STATS19. Pembacaan penuh dataset (notebook 01) mencatat ratusan ribu baris (≈ 513.801 baris). Sample 10.000 dibentuk melalui `groupby(collision_year).sample(n=2000)` agar tiap tahun seimbang.

Referensi unduhan resmi STATS19 **belum** tercatat di repository (gap — lihat DOCUMENTATION_GAPS.md).

---

## 6. Feature Selection

### 6.1 Kontrak fitur final — tepat 18 fitur

| Fitur | Tipe | Arti (bahasa awam) | Classification | Clustering |
|---|---|---|---|---|
| `number_of_vehicles` | Numerik | Jumlah kendaraan terlibat | Ya | Ya |
| `speed_limit` | Numerik | Batas kecepatan jalan (mph) | Ya | Ya |
| `hour` | Numerik | Jam kejadian (0–23, dari `time`) | Ya | Ya |
| `month` | Numerik | Bulan kejadian (1–12, dari `date`) | Ya | Ya |
| `day_of_week` | Kategorikal | Hari dalam seminggu | Ya | Ya |
| `first_road_class` | Kategorikal | Kelas jalan utama (A, B, Motorway, dll) | Ya | Ya |
| `road_type` | Kategorikal | Tipe jalan (Single carriageway, dll) | Ya | Ya |
| `junction_detail` | Kategorikal | Detail persimpangan | Ya | Ya |
| `junction_control` | Kategorikal | Kendali persimpangan | Ya | Ya |
| `second_road_class` | Kategorikal | Kelas jalan kedua | Ya | Ya |
| `pedestrian_crossing` | Kategorikal | Fasilitas penyeberangan pejalan kaki | Ya | Ya |
| `light_conditions` | Kategorikal | Kondisi cahaya | Ya | Ya |
| `weather_conditions` | Kategorikal | Kondisi cuaca | Ya | Ya |
| `road_surface_conditions` | Kategorikal | Kondisi permukaan jalan | Ya | Ya |
| `special_conditions_at_site` | Kategorikal | Kondisi khusus di lokasi | Ya | Ya |
| `carriageway_hazards` | Kategorikal | Bahaya di badan jalan | Ya | Ya |
| `urban_or_rural_area` | Kategorikal | Area urban/rural | Ya | Ya |
| `trunk_road_flag` | Kategorikal | Flag jalan nasional (trunk road) | Ya | Ya |

**Total: 4 numerik + 14 kategorikal = 18 fitur.**

### 6.2 Fitur yang TIDAK digunakan sebagai input

| Fitur/grup | Alasan (berdasarkan implementasi) |
|---|---|
| `collision_severity` | Target classification; tidak boleh menjadi input clustering (leakage). |
| `number_of_casualties` | Konsekuensi/outcome setelah kecelakaan; berpotensi leakage. |
| `collision_index`, `collision_ref_no` | Identifier unik; tidak informatif dan overfitting. |
| Kode administratif (`police_force`, `local_authority_*`, `lsoa_of_accident_location`) | Kode administratif/lokasi; tidak dipakai. |
| `did_police_officer_attend_scene_of_accident` | Respons pasca-kejadian, bukan kondisi awal. |
| `enhanced_severity_collision`, `collision_injury_based`, `collision_adjusted_severity_*` | Variabel severity turunan; target leakage. |

> Alasan pemilihan 18 fitur secara eksplisit (decision record) **belum** tersedia sebagai dokumen formal — lihat DOCUMENTATION_GAPS.md. Implementasi membuktikan daftar dan *exclusion check* (`FORBIDDEN_FEATURES` di `finalize_models.py`/`clustering_c2_c3.py`).

---

## 7. Preprocessing

Pipeline final menggunakan dua *preprocessor* terpisah (classification & clustering) dengan struktur transformasi yang sama:

| Jenis | Langkah | Penjelasan awam |
|---|---|---|
| Numerik | `SimpleImputer(strategy="median")` → `StandardScaler` | Isi nilai kosong dengan **median** (nilai tengah), lalu seragamkan skala. |
| Kategorikal | `SimpleImputer(strategy="most_frequent")` → `OneHotEncoder(handle_unknown="ignore")` | Isi nilai kosong dengan **nilai paling sering muncul**, lalu ubah kategori menjadi kolom biner (One-Hot). `handle_unknown="ignore"` membuat kategori tak dikenal menjadi nol. |

**Istilah sederhana:**
- *Imputation* = mengisi data yang hilang.
- *Median* = nilai tengah (lebih tahan terhadap nilai ekstrem dibanding rata-rata).
- *Most frequent* = modus (nilai yang paling sering muncul).
- *Scaling* = menyamakan skala agar fitur numerik tidak mendominasi karena satuan berbeda.
- *One-Hot Encoding* = mengubah teks/kategori menjadi angka 0/1 agar bisa diproses model.
- `handle_unknown="ignore"` = jika ada kategori baru saat inference, tidak error, cukup diberi nilai 0.

---

## 8. Classification

- **Target:** `collision_severity` → `Fatal`, `Serious`, `Slight`.
- **Tipe:** *Supervised learning* (data berlabel).
- **Model:** `RandomForestClassifier`.
- **Data:** 10.000 sample dibagi **8.000 train / 2.000 test** (`test_size=0.20`, `stratify=y`, `random_state=42`).
- **Encoded:** 18 → **105** fitur (preprocessor *fit* hanya pada `X_train`).
- **Alur:** `18 fitur → final_preprocessor.joblib → 105 encoded → final_random_forest.joblib → kelas + probabilitas`.

Classification preprocessor **hanya di-fit pada X_train**, lalu X_test hanya di-*transform*. Ini mencegah leakage dari data test.

---

## 9. Random Forest

Random Forest adalah kumpulan banyak *Decision Tree* (pohon keputusan). Setiap pohon belajar dari subset data, lalu prediksi akhir ditentukan melalui voting (untuk klasifikasi) atau rata-rata.

- *Decision Tree*: membagi data berdasarkan aturan sederhana (mis. "speed_limit > 30?").
- *Random Forest*: menggabungkan ratusan pohon sehingga lebih stabil dan akurat daripada satu pohon.
- *Probability*: model memberikan probabilitas untuk tiap kelas (bukan kepastian).
- *Inference*: model final sudah dilatih; aplikasi hanya menjalankan prediksi.

**Konfigurasi aktual (terverifikasi dari `final_classification_metadata.json` + `finalize_models.py`):**

```text
RandomForestClassifier(
    n_estimators=300,
    max_depth=15,
    class_weight="balanced",
    random_state=42,
    n_jobs=-1,
)
```

> Alasan pemilihan hyperparameter tidak didokumentasikan secara eksplisit; `class_weight="balanced"` digunakan untuk menangani ketidakseimbangan kelas (Fatal sangat sedikit).

---

## 10. Evaluasi Classification

### 10.1 Metrik aggregate (sumber: `models/final_classification_metadata.json`)

| Metrik | Nilai | Arti sederhana |
|---|---:|---|
| Accuracy | **63,85%** | Persentase prediksi benar dari seluruh data test. |
| Macro Precision | **38,02%** | Rata-rata precision antar kelas (setiap kelas dianggap sama penting). |
| Macro Recall | **40,08%** | Rata-rata recall antar kelas. |
| Macro F1 | **38,62%** | Rata-rata F1 antar kelas. |
| Weighted F1 | **64,96%** | F1 rata-rata berbobot terhadap jumlah data tiap kelas. |

> Jangan menyimpulkan model "sangat akurat" hanya dari accuracy 63,85%. Karena kelas tidak seimbang (Fatal sangat sedikit), **Macro F1 (38,62%) jauh lebih rendah dari Weighted F1 (64,96%)** — ini menunjukkan performa pada kelas minoritas (Fatal) lemah.

### 10.2 Laporan per kelas (sumber: `notebooks/03_classification.ipynb`)

| Kelas | Precision | Recall | F1 | Support |
|---|---:|---:|---:|---:|
| Fatal | 0,07 | 0,14 | 0,10 | 28 |
| Serious | 0,28 | 0,32 | 0,30 | 453 |
| Slight | 0,79 | 0,74 | 0,76 | 1.519 |
| **Total** | — | — | — | 2.000 |

Angka per kelas di atas konsisten dengan aggregate metadata final (macro dari baris di atas ≈ 0,38 / 0,40 / 0,3867, sesuai metadata 0,3802 / 0,4008 / 0,3862). Precision Fatal 0,0708 tercatat eksplisit di notebook 03.

**Cara membaca:**
- *Precision* tinggi berarti jika model bilang "Fatal", kemungkinan benar besar. Di sini Fatal precision hanya 0,07 → banyak prediksi Fatal yang salah.
- *Recall* tinggi berarti model berhasil menemukan sebagian besar kasus Fatal yang sesungguhnya. Di sini Fatal recall 0,14 → model hanya menangkap 14% kasus Fatal.
- Kelas `Slight` dominan dan memiliki performa terbaik; kelas `Fatal` sangat sulit diprediksi karena jumlahnya sedikit (28 dari 2.000).

---

## 11. Clustering

- **Algoritma:** K-Means (unsupervised learning).
- **Input:** 18 fitur (sama dengan classification).
- **Encoded:** 18 → **108** fitur (preprocessor *fit* pada **seluruh** 10.000 sample).
- **Data:** seluruh 10.000 record (tanpa split train/test).
- **Final:** `K=2`.
- **Alur:** `18 fitur → final_clustering_preprocessor.joblib → 108 encoded → final_kmeans.joblib → cluster + distance to centroid`.

Clustering **tidak** menggunakan `collision_severity` sebagai input dan **tidak** menggunakan PCA untuk membentuk cluster.

---

## 12. K-Means

K-Means membagi data menjadi *k* kelompok (cluster) berdasarkan kedekatan karakteristik terhadap **centroid** (pusat cluster).

- *Cluster*: kelompok data dengan karakteristik serupa.
- *Centroid*: titik pusat tiap cluster dalam ruang fitur.
- *Distance to centroid*: jarak data ke pusat cluster; semakin kecil, semakin mirip dengan cluster tersebut.

**Konfigurasi aktual (terverifikasi dari `final_clustering_metadata.json` + `clustering_c4.py`):**

```text
KMeans(n_clusters=2, random_state=42, n_init=10)
```

> **Cluster bukan severity.** Cluster 0 dan Cluster 1 hanya label nomor K-Means. Jangan menulis "Cluster 0 = Fatal" atau "Cluster 1 = Slight".

---

## 13. Evaluasi k

C3 (`clustering_c2_c3.py`) mengevaluasi `k = 2..6` menggunakan empat metrik:

| k | Inertia | Silhouette | Davies-Bouldin | Calinski-Harabasz |
|---:|---:|---:|---:|---:|
| 2 | 95756,560557 | **0,143490** | **2,387075** | **1287,425737** |
| 3 | 89650,949954 | 0,089714 | 2,763991 | 1027,902184 |
| 4 | 85735,264751 | 0,083531 | 2,821309 | 868,672373 |
| 5 | 82928,578533 | 0,085248 | 2,624441 | 758,056056 |
| 6 | 80289,582594 | 0,080003 | 2,506223 | 692,012594 |

**Kesimpulan: k = 2.**
Alasan:
- **Silhouette tertinggi** (0,143490) — pemisahan cluster terbaik.
- **Davies-Bouldin terendah** (2,387075) — kemiripan antar-cluster terendah.
- **Calinski-Harabasz tertinggi** (1287,425737) — kualitas pemisahan tertinggi.

Inertia turun seiring bertambahnya k (wajar), sehingga tidak dipakai sendirian untuk memilih k.

---

## 14. Profil Cluster

| Ukuran | Cluster 0 | Cluster 1 |
|---|---:|---:|
| Jumlah record | 2.528 | 7.472 |
| Persentase | 25,28% | 74,72% |

**Fitur numerik (mean / median):**

| Fitur | Cluster 0 | Cluster 1 |
|---|---:|---:|
| `number_of_vehicles` | 1,9276 / 2 | 1,7855 / 2 |
| `speed_limit` | 57,6938 / 60 | 28,5091 / 30 |
| `hour` | 13,0455 / 14 | 13,9421 / 15 |
| `month` | 6,7698 / 7 | 6,6096 / 7 |

**Kategori dominan (deskriptif):**

- **Cluster 0**: Rural 92,37%, `first_road_class` = A 54,11%, `junction_detail` = Not at or within 20 metres of junction 77,29%, `pedestrian_crossing` kategori 0 = 96,52%. → pola **wilayah rural, batas kecepatan lebih tinggi**.
- **Cluster 1**: Urban 87,47%, `first_road_class` = Unclassified 41,82%, `road_type` = Single carriageway 75,46%, `junction_control` = Give way or uncontrolled 48,43%. → pola **wilayah urban, batas kecepatan lebih rendah**.

Interpretasi bersifat **deskriptif** dari profil fitur, bukan label yang dipelajari. Cluster ID 0/1 tidak memiliki makna ordinal atau severity.

---

## 15. PCA

PCA (Principal Component Analysis) diterapkan **SETELAH** final K-Means **hanya untuk visualisasi** dua dimensi (`clustering_c4.py`).

| Komponen | Explained variance |
|---|---:|
| PC1 | 14,9170% |
| PC2 | 9,5219% |
| **Total** | **24,4388%** |

PCA **tidak** digunakan untuk: menentukan k, membentuk cluster, atau prediksi classification. PCA hanya membantu melihat sebaran cluster dalam plot 2D.

---

## 16. Implementasi Streamlit

- **Framework:** Streamlit (`app.py`).
- **Mode:** inference-only (tanpa retraining, tuning, atau PCA inference).
- **Pemuatan:** `app.py` memuat artifact final dan metadata; tidak memanggil `final_model_evaluation.py`.

### Halaman aktual (8)

| # | Halaman | Tujuan | Isi utama | Input | Output | Manfaat |
|---|---|---|---|---|---|---|
| 1 | Beranda | Pengantar & quick start | Penjelasan tujuan, alur, identitas akademik | — | Navigasi | Memahami ruang lingkup |
| 2 | Dashboard Dataset | Hasil historis C3/C4 | Distribusi, profil, evaluasi k, PCA | — | Grafik & tabel | Eksplorasi hasil penelitian |
| 3 | Tentang Data | Sumber & pemisahan analisis | STATS19, periode, sampling, target, 18 fitur | — | Penjelasan | Pahami data vs inference |
| 4 | Prediksi Severity | Inference classification | Form 18 fitur, probabilitas | 18 fitur | Kelas + probabilitas | Prediksi severity data baru |
| 5 | Analisis Cluster | Inference clustering | Form 18 fitur, jarak centroid | 18 fitur | Cluster + interpretasi | Kelompok karakteristik data baru |
| 6 | Panduan Penggunaan | Cara pakai & glosarium | Langkah & istilah ML | — | Panduan | Pengguna awam |
| 7 | Kamus Fitur | Arti 18 fitur | Tabel fitur + pencarian | — | Kamus | Referensi fitur |
| 8 | Tentang Model | Penjelasan akademik | Konfigurasi, evaluasi, leakage, keterbatasan | — | Dokumentasi | Penjelasan ke dosen |

---

## 17. Testing

Pengujian yang tercatat (smoke/functional, bukan eksperimen statistik baru):

| Pemeriksaan | Status |
|---|---|
| `py_compile` app.py & script | PASS |
| Streamlit startup (HTTP 200) | PASS |
| Streamlit AppTest seluruh 8 halaman | PASS |
| Classification inference (18 → 105 → prediksi) | PASS |
| Clustering inference (18 → 108 → cluster) | PASS |
| Artifact classification load (shape 105) | PASS |
| Artifact clustering load (shape 108) | PASS |
| `n_features_in_` model = 105 / 108 | PASS |
| Metadata check (18 fitur, k=2, cluster 2528/7472) | PASS |
| Legacy artifact tidak direferensikan app | PASS |
| `git diff --check` (whitespace) | PASS (tanpa error) |

---

## 18. Data Leakage

Audit mendukung bahwa pipeline bebas leakage pada desain utama:

- `collision_severity` **tidak** digunakan sebagai input clustering (target classification).
- `collision_severity` adalah **target** classification, tidak ikut di-fit sebagai fitur.
- `number_of_casualties` **tidak** digunakan pada clustering.
- Identifier (`collision_index`, `collision_ref_no`) **tidak** digunakan.
- Kode administratif (`police_force`, `local_authority_*`, `lsoa_*`) **tidak** digunakan.
- Classification preprocessor **hanya fit pada X_train**; X_test hanya transform.
- PCA dilakukan **setelah** K-Means (bukan input K-Means).
- PCA **tidak** dipakai untuk prediksi classification.
- Cluster **tidak** digunakan sebagai input classification.
- Pemilihan k **tidak** menggunakan target.

---

## 19. Artifact

### Artifact final (dipakai aplikasi)

| Fungsi | File |
|---|---|
| Classification model | `models/final_random_forest.joblib` |
| Classification preprocessor | `models/final_preprocessor.joblib` |
| Classification metadata | `models/final_classification_metadata.json` |
| Clustering model | `models/final_kmeans.joblib` |
| Clustering preprocessor | `models/final_clustering_preprocessor.joblib` |
| Clustering metadata | `models/final_clustering_metadata.json` |

### Legacy (backup lokal, di-ignore Git, TIDAK dipakai aplikasi)

- `models/final_random_forest_legacy_21_features.joblib`
- `models/final_preprocessor_legacy_21_features.joblib`

Legacy artifact adalah hasil pipeline 21 fitur lama dan **tidak** menggantikan artifact final. Aplikasi `app.py` tidak mereferensikan artifact legacy.

---

## 20. Aspek Rekayasa Perangkat Lunak

| Aspek RPL | Status di project |
|---|---|
| Requirement | Ada (implisit: classification + clustering + aplikasi). Use-case formal belum ada. |
| Functional requirement | Ada (prediksi severity, analisis cluster, dashboard). |
| Non-functional requirement | Ada sebagian (inference-only, performa, kemudahan penggunaan). |
| UI/UX | Ada (Streamlit, 8 halaman, banner, kamus fitur). |
| Architecture | Ada (raw → sampling → preprocessing → model → Streamlit). |
| Model artifact | Ada (joblib + metadata, serialisasi jelas). |
| Testing | Ada (AppTest, py_compile, smoke). Test case matrix formal belum ada. |
| Documentation | Ada (README, README_APP, docs/). |
| Local deployment | Ada (venv + `streamlit run app.py`). |
| Git/GitHub | Ada (repo GitHub, branch main, version control). |
| Diagram RPL | **Belum ada** (use-case, activity, sequence, component, deployment). |

---

## 21. Keterbatasan

- Sample hanya 10.000 record (bukan seluruh populasi STATS19 ≈ 513.801 baris).
- Dataset berasal dari STATS19 Inggris; generalisasi ke wilayah lain belum teruji.
- Performa antar kelas classification tidak seimbang (Macro F1 38,62% « Weighted F1 64,96%).
- Kelas `Fatal` sangat sulit diprediksi (hanya 28/2.000 pada test).
- Clustering bersifat **deskriptif**, bukan prediksi severity.
- Cluster **bukan** tingkat keparahan/keamanan/bahaya.
- Aplikasi adalah alat bantu edukatif, **bukan** sistem penilaian resmi.
- Kualitas inference bergantung pada kesesuaian & kelengkapan input.
- Aplikasi beroperasi inference-only (tanpa retraining saat runtime).

---

## 22. Kesimpulan

Project berhasil membangun dua pipeline ML (classification & clustering) di atas kontrak 18 fitur yang konsisten, dengan artifact final terpisah dan aplikasi Streamlit inference-only. Integritas utama terjaga: target tidak bocor ke clustering, preprocessing terpisah, dan PCA hanya untuk visualisasi. Risiko dokumentasi terbesar adalah output evaluasi classification lama (21 fitur) yang namanya tampak final; dokumen ini menjadikan metadata final + notebook 03 sebagai sumber angka classification yang sah.

---

## 23. Documentation Gaps

Lihat `docs/DOCUMENTATION_GAPS.md` untuk daftar lengkap. Ringkasan:

1. CSV evaluasi classification lama (`final_test_results.csv`, `final_classification_report.csv`, `final_confusion_matrix.*`) berasal dari evaluator 21 fitur — **bukan** sumber angka final.
2. Alasan pemilihan 18 fitur (decision record) belum formal.
3. Referensi unduhan resmi STATS19 + lisensi belum tercatat.
4. Diagram RPL formal (use-case, activity, sequence, component, deployment) belum ada.
5. Test case matrix permanen belum ada.
6. Data dictionary 44 kolom formal belum ada.
7. Manifest provenance (checksum artifact, commit Git pembuat output) belum ada.
8. Per-class classification report untuk 18 fitur tersedia di notebook 03 (konsisten dengan metadata), namun belum diekspor ke CSV final.

---

## 24. Rekomendasi Isi Laporan (Word/PDF)

1. Halaman judul + identitas (Asyudi Anggara / F552630019 / UNTAD / RPL).
2. Abstrak & kata kunci.
3. Pendahuluan: latar belakang, tujuan, batasan.
4. Landasan teori: classification vs clustering, Random Forest, K-Means, PCA, preprocessing.
5. Analisis kebutuhan & rancangan (tambahkan diagram RPL bila memungkinkan).
6. Dataset & data understanding (STATS19, 10.000 sample, 18 fitur).
7. Data preparation & audit leakage.
8. Metodologi classification (Random Forest, 8.000/2.000, 105 encoded).
9. Metodologi clustering C2–C4 (108 encoded, k=2, profil, PCA).
10. Implementasi Streamlit (8 halaman, inference-only).
11. Hasil & pembahasan (metrik aggregate + per-class + cluster profile).
12. Pengujian & traceability.
13. Keterbatasan & pekerjaan lanjutan.
14. Kesimpulan.
15. Daftar pustaka (tambahkan sumber STATS19 resmi).
16. Lampiran: tabel k, profil cluster, PCA, screenshot UI, kamus fitur.

---

## Lampiran A — Inventory File

| File | Fungsi | Relevansi | Status |
|---|---|---|---|
| `app.py` | Aplikasi Streamlit inference | Tinggi | Aktif |
| `README.md` | README utama repo | Tinggi | Aktif |
| `README_APP.md` | Dokumentasi aplikasi | Sedang | Aktif |
| `requirements.txt` | Dependency Python | Tinggi | Aktif |
| `.gitignore` | Ignore raw data/legacy/venv | Tinggi | Aktif |
| `notebooks/01_data_understanding.ipynb` | C1 Data Understanding | Tinggi | Aktif |
| `notebooks/02_data_preparation.ipynb` | Persiapan data/feature engineering | Tinggi | Aktif |
| `notebooks/03_classification.ipynb` | Classification + per-class report | Tinggi | Aktif |
| `clustering_c2_c3.py` | C2 preprocessing + C3 evaluasi k | Tinggi | Aktif |
| `clustering_c4.py` | C4 K-Means final + profil + PCA | Tinggi | Aktif |
| `finalize_models.py` | Finalisasi & validasi artifact | Tinggi | Aktif |
| `final_model_evaluation.py` | Evaluator lama 21 fitur (stale) | Rendah | Jangan pakai sbg sumber final |
| `step4_hyperparameter_tuning.py` | Tuning historis 21 fitur | Rendah | Historis |
| `models/final_*.joblib` / `*.json` | Artifact final | Tinggi | Aktif (allowlist) |
| `models/*legacy_21_features.joblib` | Backup lama | Rendah | Di-ignore |
| `results/clustering_*.csv` / `*.png` | Output C3/C4 | Tinggi | Aktif |
| `results/final_*.csv` / `*.png` | Evaluasi classification lama | Rendah | Stale (21 fitur) |
| `data/processed/stats19_maps.json` | Mapping kode STATS19 | Tinggi | Aktif |
| `docs/PROJECT_DOCUMENTATION_MASTER.md` | Dokumentasi induk | Tinggi | Dokumen ini |
| `docs/PROJECT_FACT_SHEET.md` | Fakta & angka final | Tinggi | Aktif |
| `docs/DOCUMENTATION_GAPS.md` | Gap dokumentasi | Tinggi | Aktif |

## Lampiran B — Traceability Matrix

| Klaim | Bukti | File | Status |
|---|---|---|---|
| Sample 10.000 (2.000/tahun) | Sampling `random_state=42` | `finalize_models.py`, `clustering_c2_c3.py` | Terverifikasi |
| 18 fitur final | `FEATURES` / `FORBIDDEN_FEATURES` | `finalize_models.py`, `clustering_*.py` | Terverifikasi |
| Classification 105 encoded | `feature_count_encoded` | `final_classification_metadata.json` | Terverifikasi |
| Clustering 108 encoded | `feature_count_encoded` | `final_clustering_metadata.json` | Terverifikasi |
| RF config (300/15/balanced/42) | metadata + kode | `final_classification_metadata.json` | Terverifikasi |
| Accuracy 63,85% | `metrics.accuracy` | `final_classification_metadata.json` | Terverifikasi |
| Macro F1 38,62% | `metrics.macro_f1` | `final_classification_metadata.json` | Terverifikasi |
| Per-class (Fatal 0,07/0,14/0,10, dst) | classification report | `notebooks/03_classification.ipynb` (baris 1071–1073) | Terverifikasi, konsisten dgn metadata |
| K-Means k=2 | `n_clusters` | `final_clustering_metadata.json` | Terverifikasi |
| k=2 terbaik (silhouette/db/ch) | evaluasi | `results/clustering_k_evaluation.csv` | Terverifikasi |
| Cluster 0 = 2.528 | `cluster_0_count` | `final_clustering_metadata.json` | Terverifikasi |
| Cluster 1 = 7.472 | `cluster_1_count` | `final_clustering_metadata.json` | Terverifikasi |
| PCA hanya visualisasi | `PCA` setelah K-Means | `clustering_c4.py` | Terverifikasi |
| PCA total 24,4388% | `explained_variance_ratio` | `results/clustering_pca_variance.csv` | Terverifikasi |
| Legacy CSV tidak final | source 21 fitur | `final_model_evaluation.py` | Gap (stale) |
