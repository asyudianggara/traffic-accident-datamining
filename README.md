# Tugas 2 – Penambangan Data

## Analisis Kecelakaan Lalu Lintas STATS19

Status: **PHASE 4 COMPLETED — menunggu instruksi PHASE 5**

Repository ini adalah salinan kerja baru untuk Tugas 2. Tujuannya adalah menyiapkan analisis data kecelakaan lalu lintas STATS19 dengan **seluruh baris data yang tersedia**. Artefak, hasil, dan aplikasi yang terbawa dari proyek sebelumnya hanya menjadi baseline/referensi; mereka bukan hasil final Tugas 2.

## Dataset

- Raw lokal: `data/raw/dft-road-casualty-statistics-collision-last-5-years.csv`
- Status: **VERIFIED** tersedia lokal, tetapi di-ignore Git dan tidak akan diunggah.
- Ukuran: 97.669.586 byte
- Cakupan: 513.801 baris, 44 kolom, tahun 2021–2025.
- Target legacy classification: `collision_severity`.

Baseline lama menggunakan 10.000 record: 2.000 record dari masing-masing tahun 2021–2025 melalui `groupby("collision_year").sample(n=2000, random_state=42)`. Sampling ini tidak dinyatakan stratified; split classification sesudahnya memakai `stratify=y`, `test_size=0.20`, dan `random_state=42`.

Quality audit Phase 1 memverifikasi 0 duplicate row, 53 missing pada masing-masing empat kolom koordinat, serta target valid tiga kelas: Fatal 7.553 (1,470024%), Serious 116.813 (22,735067%), dan Slight 389.435 (75,794909%). Phase 5A telah menjalankan baseline classification pada full dataset; belum ada final model selection, tuning, clustering, association mining, forecasting, atau deployment.

## Progress dan CRISP-DM

| Area                               | Status                             |
| ---------------------------------- | ---------------------------------- |
| Phase 0 – Audit & governance       | COMPLETED                          |
| Phase 1 – Data strategy            | COMPLETED                          |
| Phase 2 – Data understanding       | COMPLETED                          |
| Phase 3 – Data preparation         | COMPLETED (implemented + validated) |
| Phase 4 – Feature selection        | COMPLETED (strategy only)          |
| Phase 5A – Classification baseline | COMPLETED                          |
| Phase 5B-1 – Model comparison      | PARTIAL                            |
| Business Understanding             | PARTIAL                            |
| Data Understanding                 | COMPLETED                          |
| Data Preparation full dataset      | COMPLETED (implemented + validated) |
| Modeling full dataset              | PARTIAL (5A + 5B-1)                |
| Evaluation full dataset            | PARTIAL (comparison incomplete)    |
| Deployment untuk Tugas 2           | PARTIAL                            |

Rincian strategi tersedia di [docs/DATA_STRATEGY.md](docs/DATA_STRATEGY.md), audit deskriptif di [docs/DATA_UNDERSTANDING.md](docs/DATA_UNDERSTANDING.md), kontrak preparation di [docs/DATA_PREPARATION.md](docs/DATA_PREPARATION.md), strategi feature selection di [docs/FEATURE_SELECTION.md](docs/FEATURE_SELECTION.md), baseline di [docs/MODELING_PHASE5A.md](docs/MODELING_PHASE5A.md), dan comparison di [docs/MODELING_PHASE5B1.md](docs/MODELING_PHASE5B1.md). Status dan handoff tersedia di [docs/PROJECT_STATUS.md](docs/PROJECT_STATUS.md) dan [docs/HANDOFF.md](docs/HANDOFF.md).

## Pipeline dan Model Legacy yang Tersedia

Pipeline lama menyediakan:

- Classification: Random Forest dengan 18 fitur input, 105 fitur encoded, dan target `collision_severity`.
- Clustering: K-Means dengan 18 fitur input dan 108 fitur encoded; script C2/C3 mengevaluasi `k=2..6`, metadata final menunjukkan `k=2`.
- Aplikasi Streamlit: inference satu baris terhadap artefak legacy serta dashboard hasil historis di `results/`.

Metrik/model/result tersebut hanya **VERIFIED sebagai baseline legacy**, bukan klaim hasil full dataset Tugas 2. Jangan membandingkan atau memakai hasilnya sebagai kesimpulan Tugas 2 tanpa eksperimen Phase berikutnya.

## Struktur Penting

```text
├── app.py                         # aplikasi Streamlit legacy
├── data/raw/                      # CSV STATS19 lokal, di-ignore Git
├── data/processed/stats19_maps.json
├── notebooks/                     # notebook lama: understanding, preparation, classification
├── models/                        # artefak legacy
├── results/                       # hasil eksperimen/profil legacy
├── clustering_c2_c3.py            # evaluasi clustering legacy
├── clustering_c4.py               # profiling/visualisasi legacy
├── finalize_models.py             # finalisasi artefak legacy
└── docs/                          # status, handoff, dan changelog proyek baru
```

## Environment dan Instalasi

Environment lokal yang dapat diverifikasi adalah `.venv`; dependensi dipin pada `requirements.txt`, termasuk Streamlit, pandas, NumPy, joblib, dan scikit-learn.

```bat
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Pembuatan environment/dependency baru tidak dilakukan dalam Phase 0.

## Menjalankan Aplikasi

Jalankan dari root proyek setelah environment tersedia:

```bat
.venv\Scripts\python.exe -m streamlit run app.py
```

Alternatif setelah aktivasi environment:

```bat
streamlit run app.py
```

Streamlit secara default membuka aplikasi pada URL lokal yang ditampilkan di terminal (umumnya `http://localhost:8501`). Status startup Phase 0: **PASS** — uji pada port lokal 8502 mengembalikan HTTP 200, lalu proses dihentikan. Aplikasi tidak diubah dan tidak melakukan training saat dijalankan.

## Notebook dan Script

- `notebooks/01_data_understanding.ipynb`, `02_data_preparation.ipynb`, dan `03_classification.ipynb` adalah bahan pipeline legacy.
- `prepare_phase3.py` adalah pipeline preparation full dataset yang hanya menghasilkan manifest validasi kecil.
- `clustering_c2_c3.py`, `clustering_c4.py`, `finalize_models.py`, dan `final_model_evaluation.py` adalah script legacy.

Jangan menjalankan notebook/script tersebut untuk Tugas 2 tanpa instruksi Phase yang eksplisit, karena dapat menghasilkan atau mengubah output baseline.

## Git dan Repository

Branch aktif: `main`. Repository GitHub Tugas 2 terverifikasi pada `https://github.com/asyudianggara/traffic-accident-datamining.git` untuk fetch dan push. Checkpoint Phase 0 `3a4f9b1` (`docs: establish project status and phase 0 audit`) berhasil dipush ke `origin/main` pada 2026-08-27. Jangan force push.

## Dokumentasi

- [Project status](docs/PROJECT_STATUS.md)
- [Handoff](docs/HANDOFF.md)
- [Changelog](docs/CHANGELOG.md)
- [Data strategy](docs/DATA_STRATEGY.md)
- [Data understanding](docs/DATA_UNDERSTANDING.md)
- [Data preparation](docs/DATA_PREPARATION.md)
- [Feature selection](docs/FEATURE_SELECTION.md)
- [Modeling Phase 5A](docs/MODELING_PHASE5A.md)
- [Modeling Phase 5B-1](docs/MODELING_PHASE5B1.md)
- Dokumen audit legacy yang dibawa dari proyek sebelumnya: `docs/PROJECT_DOCUMENTATION_MASTER.md`, `docs/PROJECT_FACT_SHEET.md`, dan `docs/DOCUMENTATION_GAPS.md`.

## Next Phase

**PHASE 5 – MODELING:** compare approved algorithms using the documented provisional feature set and protected temporal holdout.
