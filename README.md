# Tugas 2 – Penambangan Data

## Analisis Kecelakaan Lalu Lintas STATS19

Status: **PHASE 8.4 — final system consistency and documentation correction completed; Phase 10.1 blueprint retained**

Repository ini adalah salinan kerja baru untuk Tugas 2. Tujuannya adalah menyiapkan analisis data kecelakaan lalu lintas STATS19 dengan **seluruh baris data yang tersedia**. Final research artifact dan hasil final dirujuk secara eksplisit; artifact classification lama dan artifact clustering legacy tetap dipertahankan sebagai baseline/referensi historis.

## Dataset

- Raw lokal: `data/raw/dft-road-casualty-statistics-collision-last-5-years.csv`
- Status: **VERIFIED** tersedia lokal, tetapi di-ignore Git dan tidak akan diunggah.
- Ukuran: 97.669.586 byte
- Cakupan: 513.801 baris, 44 kolom, tahun 2021–2025.
- Target classification final research: `collision_severity`.

Analisis clustering legacy C3–C4 menggunakan 10.000 record: 2.000 record dari masing-masing tahun 2021–2025 melalui `groupby("collision_year").sample(n=2000, random_state=42)`. Data ini bukan dataset utama penelitian final. Split classification legacy sesudahnya memakai `stratify=y`, `test_size=0.20`, dan `random_state=42`.

Pada aplikasi, 10.000 record hanya ditampilkan sebagai **clustering legacy C3–C4**. Ringkasan utama Dashboard Dataset menggunakan raw dataset 513.801 × 44 dan memisahkan development 412.276, training 311.349, validation 100.927, serta final holdout 2025 sebanyak 101.525 record.

Quality audit Phase 1 memverifikasi 0 duplicate row, 53 missing pada masing-masing empat kolom koordinat, serta target valid tiga kelas: Fatal 7.553 (1,470024%), Serious 116.813 (22,735067%), dan Slight 389.435 (75,794909%). Phase 6 memilih final candidate classification: Random Forest balanced dengan threshold Fatal 0,50. Phase 7 memvalidasi artifact dan contract; Phase 8 mengintegrasikannya ke halaman classification Streamlit; Phase 8.2 menyelaraskan UI dataset raw/split final dengan clustering legacy C3–C4 10K. Model belum deployment-ready.

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
| Phase 8.2 – UI consistency         | COMPLETED                          |
| Business Understanding             | PARTIAL                            |
| Data Understanding                 | COMPLETED                          |
| Data Preparation full dataset      | COMPLETED (implemented + validated) |
| Modeling full dataset              | COMPLETED WITH LIMITATIONS         |
| Evaluation full dataset            | COMPLETED WITH LIMITATIONS         |
| Deployment untuk Tugas 2           | PARTIAL                            |

Rincian strategi tersedia di [docs/DATA_STRATEGY.md](docs/DATA_STRATEGY.md), audit deskriptif di [docs/DATA_UNDERSTANDING.md](docs/DATA_UNDERSTANDING.md), kontrak preparation di [docs/DATA_PREPARATION.md](docs/DATA_PREPARATION.md), strategi feature selection di [docs/FEATURE_SELECTION.md](docs/FEATURE_SELECTION.md), baseline di [docs/MODELING_PHASE5A.md](docs/MODELING_PHASE5A.md), dan comparison di [docs/MODELING_PHASE5B1.md](docs/MODELING_PHASE5B1.md). Status dan handoff tersedia di [docs/PROJECT_STATUS.md](docs/PROJECT_STATUS.md) dan [docs/HANDOFF.md](docs/HANDOFF.md).
Rincian final model tersedia di [docs/FINAL_MODEL.md](docs/FINAL_MODEL.md). Status dan handoff tersedia di [docs/PROJECT_STATUS.md](docs/PROJECT_STATUS.md) dan [docs/HANDOFF.md](docs/HANDOFF.md).
Interpretasi hasil dan keterbatasan tersedia di [docs/RESEARCH_INTERPRETATION.md](docs/RESEARCH_INTERPRETATION.md).
Konsolidasi hasil final tersedia di [docs/FINAL_RESULTS_CONSOLIDATION.md](docs/FINAL_RESULTS_CONSOLIDATION.md).
Blueprint laporan final tersedia di [docs/FINAL_REPORT_BLUEPRINT.md](docs/FINAL_REPORT_BLUEPRINT.md).

## Pipeline dan Artifact yang Tersedia

Final research menyediakan:

- Classification final research: `models/final_research_model.joblib`, 18 fitur → 149 encoded features, Random Forest balanced, threshold Fatal 0,50, dan final holdout 2025.

Pipeline legacy menyediakan:

- Classification legacy: Random Forest dengan 18 fitur input, 105 fitur encoded, dan target `collision_severity`.
- Clustering legacy C3–C4: K-Means dengan 18 fitur input dan 108 fitur encoded; script C2/C3 mengevaluasi `k=2..6`, metadata final menunjukkan `k=2` pada 10.000 record legacy.
- Aplikasi Streamlit: inference satu baris terhadap artifact final research untuk classification, artifact clustering legacy, serta dashboard hasil historis di `results/`.

Metrik/model/result legacy hanya **VERIFIED sebagai baseline historis**, bukan klaim hasil full dataset Tugas 2. Hasil final research dirujuk dari `results/final_model_metadata.json` dan `docs/FINAL_MODEL.md`.

## Struktur Penting

```text
├── app.py                         # aplikasi Streamlit inference-only
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
- [Modeling Phase 5 baselines](docs/MODELING_PHASE5.md)
- [Final model selection](docs/FINAL_MODEL.md)
- [Operational validation](docs/OPERATIONAL_VALIDATION.md)
- [Application integration](docs/APPLICATION_INTEGRATION.md)
- [Phase 8.2 UI consistency test](phase8_2_ui_consistency.py)
- Dokumen audit legacy yang dibawa dari proyek sebelumnya: `docs/PROJECT_DOCUMENTATION_MASTER.md`, `docs/PROJECT_FACT_SHEET.md`, dan `docs/DOCUMENTATION_GAPS.md`.

## Next Phase

**PHASE 10.1 — FINAL REPORT BLUEPRINT:** selesai; deployment operasional tetap belum diklaim siap.
