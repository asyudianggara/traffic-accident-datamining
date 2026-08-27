# PROJECT STATUS

Project: Tugas 2 – Penambangan Data
Case: Analisis Kecelakaan Lalu Lintas STATS19
Current Phase: PHASE 0 – AUDIT & PROJECT GOVERNANCE
Overall Progress: PHASE 0 / 10
Status: COMPLETED

## Completed

- Audit awal Git, struktur proyek, dokumentasi, dataset, artefak, pipeline, dan aplikasi selesai pada 2026-08-27.
- Dataset raw lokal terverifikasi: `data/raw/dft-road-casualty-statistics-collision-last-5-years.csv` (513.801 baris, 44 kolom, 2021–2025, 97.669.586 byte).
- Baseline lama 10K teridentifikasi sebagai sampling 2.000 baris per tahun (2021–2025), `random_state=42`.
- README, handoff, dan changelog Phase 0 dibuat/diperbarui.
- Repository GitHub baru terhubung dan checkpoint Phase 0 `3a4f9b1` berhasil dipush ke `origin/main` pada 2026-08-27.

## Current

- Menunggu instruksi eksplisit untuk PHASE 1 – DATA STRATEGY.

## Not Started

- Menetapkan strategi penggunaan seluruh baris data, validasi target/fitur, split, dan preprocessing untuk full dataset.
- Data preparation, modeling, comparison algoritma, feature selection, evaluation, dan deployment untuk Tugas 2 berbasis full dataset.

## Blocked

- Tidak ada blocker Phase 0 yang terverifikasi.

## Dataset

- Raw: `data/raw/dft-road-casualty-statistics-collision-last-5-years.csv`, lokal dan di-ignore Git.
- Full available records: 513.801 baris × 44 kolom; `collision_year` 2021: 101.087, 2022: 106.004, 2023: 104.258, 2024: 100.927, 2025: 101.525. Kolom target lama: `collision_severity`.
- Baseline 10K: artifact/dokumentasi lama menunjukkan 10.000 baris × 44 kolom, 2.000 per tahun; file dataset sample terpisah TIDAK DAPAT DIVERIFIKASI tersedia pada checkout ini.
- Target: untuk pipeline classification lama, `collision_severity`; target final Tugas 2 belum ditetapkan.

## Existing Models and Results

- Classification legacy baseline: Random Forest, 18 fitur input, 105 fitur encoded, train/test 8.000/2.000, `random_state=42`. Metadata melaporkan accuracy 0,6385 dan macro F1 0,3862.
- Clustering legacy baseline: K-Means `k=2`, 18 fitur input, 108 fitur encoded, 10.000 sampel; C2/C3 mengevaluasi `k=2..6`.
- Hasil di `results/` dan artefak di `models/` adalah hasil legacy baseline; tidak boleh diperlakukan sebagai hasil full dataset Tugas 2.

## Existing Application

- `app.py` adalah aplikasi Streamlit yang memuat artefak final legacy dan hasil historis dari `results/`; aplikasi tidak melakukan retraining saat dijalankan.
- Perintah terverifikasi: `.venv\Scripts\python.exe -m streamlit run app.py`.
- Status startup Phase 0: PASS — Streamlit diuji pada 2026-08-27 di port lokal 8502 dan mengembalikan HTTP 200; proses dihentikan setelah verifikasi.

## CRISP-DM Status

- Business Understanding: PARTIAL — case dan tujuan legacy terdokumentasi; kebutuhan spesifik Tugas 2 masih perlu dirumuskan.
- Data Understanding: PARTIAL — raw full dataset diaudit, tetapi analisis Tugas 2 belum dilakukan.
- Data Preparation: NOT STARTED — untuk full dataset Tugas 2.
- Modeling: NOT STARTED — untuk full dataset Tugas 2.
- Evaluation: NOT STARTED — untuk full dataset Tugas 2.
- Deployment: PARTIAL — aplikasi legacy tersedia, tetapi belum merepresentasikan pipeline full dataset Tugas 2.

## Tugas 2 Status

| Requirement | Status | Evidence | Gap |
|---|---|---|---|
| Analisis masalah/kebutuhan | PARTIAL | Case dan audit Phase 0 | Rumusan kebutuhan Tugas 2 belum dibuat |
| Review dataset | PARTIAL | Audit CSV raw 513.801 × 44 | EDA full dataset belum dilakukan |
| Lima peran data mining | NOT STARTED | TIDAK DAPAT DIVERIFIKASI | Belum didokumentasikan untuk Tugas 2 |
| CRISP-DM | PARTIAL | Pemetaan di dokumen ini | Tahap full dataset belum dikerjakan |
| Data preparation | NOT STARTED | Tidak ada pipeline full dataset | Menunggu Phase 1 |
| Comparison algoritma | NOT STARTED | Hasil legacy baseline ada | Perbandingan full dataset belum dilakukan |
| Feature selection | NOT STARTED | 18 fitur legacy tersedia | Seleksi untuk full dataset belum dilakukan |
| Evaluation | NOT STARTED | Metrik legacy ada | Evaluasi full dataset belum dilakukan |
| Deployment/decision making | PARTIAL | Streamlit legacy tersedia | Adaptasi ke hasil Tugas 2 belum dilakukan |

## Next Phase

PHASE 1 – DATA STRATEGY

## Important Rules

- Full dataset menjadi dataset utama Tugas 2; 10K hanya baseline/referensi.
- Project lama tidak boleh diubah.
- Jangan training, clustering, feature selection, preprocessing baru, atau membuat dataset full tanpa instruksi phase eksplisit.
- Remote GitHub terverifikasi: `https://github.com/asyudianggara/traffic-accident-datamining.git`.
- Checkpoint Phase 0 terverifikasi pada commit `3a4f9b1` dan telah dipush ke `origin/main`; jangan force push.

Last Verified: 2026-08-27
