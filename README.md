# Tugas 2 – Penambangan Data

## Analisis Kecelakaan Lalu Lintas STATS19

Status: **PHASE 0 COMPLETED — menunggu instruksi PHASE 1**

Repository ini adalah salinan kerja baru untuk Tugas 2. Tujuannya adalah menyiapkan analisis data kecelakaan lalu lintas STATS19 dengan **seluruh baris data yang tersedia**. Artefak, hasil, dan aplikasi yang terbawa dari proyek sebelumnya hanya menjadi baseline/referensi; mereka bukan hasil final Tugas 2.

## Dataset

- Raw lokal: `data/raw/dft-road-casualty-statistics-collision-last-5-years.csv`
- Status: **VERIFIED** tersedia lokal, tetapi di-ignore Git dan tidak akan diunggah.
- Ukuran: 97.669.586 byte
- Cakupan: 513.801 baris, 44 kolom, tahun 2021–2025.
- Target legacy classification: `collision_severity`.

Baseline lama menggunakan 10.000 record: 2.000 record dari masing-masing tahun 2021–2025 melalui `groupby("collision_year").sample(n=2000, random_state=42)`. Sampling ini tidak dinyatakan stratified; split classification sesudahnya memakai `stratify=y`, `test_size=0.20`, dan `random_state=42`.

**Penting:** full dataset belum dipreproses, belum dibuatkan dataset turunan, dan belum digunakan untuk modeling pada Phase 0.

## Progress dan CRISP-DM

| Area | Status |
|---|---|
| Phase 0 – Audit & governance | COMPLETED |
| Business Understanding | PARTIAL |
| Data Understanding | PARTIAL |
| Data Preparation full dataset | NOT STARTED |
| Modeling full dataset | NOT STARTED |
| Evaluation full dataset | NOT STARTED |
| Deployment untuk Tugas 2 | PARTIAL |

Rincian status, gap tugas, dan evidence tersedia di [docs/PROJECT_STATUS.md](docs/PROJECT_STATUS.md). Handoff antarsesi/agent tersedia di [docs/HANDOFF.md](docs/HANDOFF.md).

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
- `clustering_c2_c3.py`, `clustering_c4.py`, `finalize_models.py`, dan `final_model_evaluation.py` adalah script legacy.

Jangan menjalankan notebook/script tersebut untuk Tugas 2 tanpa instruksi Phase yang eksplisit, karena dapat menghasilkan atau mengubah output baseline.

## Git dan Repository

Branch aktif: `main`. Repository GitHub Tugas 2 terverifikasi pada `https://github.com/asyudianggara/traffic-accident-datamining.git` untuk fetch dan push. Checkpoint Phase 0 `3a4f9b1` (`docs: establish project status and phase 0 audit`) berhasil dipush ke `origin/main` pada 2026-08-27. Jangan force push.

## Dokumentasi

- [Project status](docs/PROJECT_STATUS.md)
- [Handoff](docs/HANDOFF.md)
- [Changelog](docs/CHANGELOG.md)
- Dokumen audit legacy yang dibawa dari proyek sebelumnya: `docs/PROJECT_DOCUMENTATION_MASTER.md`, `docs/PROJECT_FACT_SHEET.md`, dan `docs/DOCUMENTATION_GAPS.md`.

## Next Phase

**PHASE 1 – DATA STRATEGY:** menentukan strategi penggunaan seluruh baris dataset, memvalidasi jumlah record, target dan fitur, split, serta strategi preprocessing. Tahap tersebut tidak dimulai sebelum instruksi eksplisit.
