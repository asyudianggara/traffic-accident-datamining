# PROJECT STATUS

Project: Tugas 2 – Penambangan Data
Case: Analisis Kecelakaan Lalu Lintas STATS19
Current Phase: PHASE 2 – DATA UNDERSTANDING
Overall Progress: PHASE 2 / 10
Status: COMPLETED

## Completed

- Audit awal Git, struktur proyek, dokumentasi, dataset, artefak, pipeline, dan aplikasi selesai pada 2026-08-27.
- Dataset raw lokal terverifikasi: `data/raw/dft-road-casualty-statistics-collision-last-5-years.csv` (513.801 baris, 44 kolom, 2021–2025, 97.669.586 byte).
- Baseline lama 10K teridentifikasi sebagai sampling 2.000 baris per tahun (2021–2025), `random_state=42`.
- README, handoff, dan changelog Phase 0 dibuat/diperbarui.
- Repository GitHub baru terhubung dan checkpoint Phase 0 `3a4f9b1` berhasil dipush ke `origin/main` pada 2026-08-27.
- Strategi full dataset, quality audit ringan, inventory 44 fitur, dan audit sampling legacy selesai; lihat `docs/DATA_STRATEGY.md`.
- Analisis deskriptif full dataset, visualisasi terarah, feature roles, data-mining relevance, dan rekomendasi preparation selesai; lihat `docs/DATA_UNDERSTANDING.md`.

## Current

- Phase 2 completed; menunggu instruksi eksplisit untuk PHASE 3 – DATA PREPARATION.

## Current Task

- Menunggu instruksi eksplisit untuk memulai PHASE 3 – DATA PREPARATION.

## In Progress

- Tidak ada pekerjaan implementasi; dokumentasi dan visualisasi Phase 2 selesai pada 2026-08-27.

## Not Started

- Finalisasi feature contract, codebook, leakage exclusions, dan pipeline preparation.
- Data preparation, modeling, comparison algoritma, feature selection, evaluation, dan deployment untuk Tugas 2 berbasis full dataset.

## Blocked

- Data dictionary resmi lengkap, timing prediksi, dan aturan split masih menunggu konfirmasi.

## Next Action

- Menunggu instruksi eksplisit untuk memulai PHASE 3 – DATA PREPARATION.

## Do Not Do

- Jangan melakukan feature selection final, modeling, balancing, tuning, PCA, association mining, deployment, atau mengubah artefak legacy sebelum scope phase berikutnya.

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

- Business Understanding: PARTIAL — case tersedia; use case/waktu prediksi masih open question.
- Data Understanding: COMPLETED — schema, kualitas dasar, target, periode, dan baseline/full comparison terverifikasi.
- Data Preparation: PARTIAL — strategi dirancang, belum diimplementasikan.
- Modeling: NOT STARTED — untuk full dataset Tugas 2.
- Evaluation: NOT STARTED — untuk full dataset Tugas 2.
- Deployment: PARTIAL — aplikasi legacy tersedia, tetapi belum merepresentasikan pipeline full dataset Tugas 2.

## Tugas 2 Status

| Requirement                | Status      | Evidence                                                               | Gap                                        |
| -------------------------- | ----------- | ---------------------------------------------------------------------- | ------------------------------------------ |
| Analisis masalah/kebutuhan | PARTIAL     | Case dan audit Phase 0                                                 | Rumusan kebutuhan Tugas 2 belum dibuat     |
| Review dataset             | COMPLETED   | `docs/DATA_STRATEGY.md`: schema, quality, target, 44-feature inventory | EDA/domain audit lanjutan Phase 2          |
| Lima peran data mining     | NOT STARTED | TIDAK DAPAT DIVERIFIKASI                                               | Belum didokumentasikan untuk Tugas 2       |
| CRISP-DM                   | PARTIAL     | Pemetaan di dokumen ini                                                | Tahap full dataset belum dikerjakan        |
| Data preparation           | PARTIAL     | Strategi preprocessing dan leakage prevention didokumentasikan         | Implementasi menunggu instruksi            |
| Comparison algoritma       | NOT STARTED | Hasil legacy baseline ada                                              | Perbandingan full dataset belum dilakukan  |
| Feature selection          | NOT STARTED | 18 fitur legacy tersedia                                               | Seleksi untuk full dataset belum dilakukan |
| Evaluation                 | NOT STARTED | Metrik legacy ada                                                      | Evaluasi full dataset belum dilakukan      |
| Deployment/decision making | PARTIAL     | Streamlit legacy tersedia                                              | Adaptasi ke hasil Tugas 2 belum dilakukan  |

## Next Phase

PHASE 3 – DATA PREPARATION

## Important Rules

- Full dataset menjadi dataset utama Tugas 2; 10K hanya baseline/referensi.
- Project lama tidak boleh diubah.
- Jangan training, clustering, feature selection, preprocessing baru, atau membuat dataset full tanpa instruksi phase eksplisit.
- Jangan menganggap visualisasi dan pola Phase 2 sebagai hubungan kausal atau hasil model.
- Remote GitHub terverifikasi: `https://github.com/asyudianggara/traffic-accident-datamining.git`.
- Checkpoint Phase 0 terverifikasi pada commit `3a4f9b1` dan telah dipush ke `origin/main`; jangan force push.

## Verified Facts

- CSV aktual: 513.801 × 44, 2021-01-01 s.d. 2025-12-31; 0 duplicate row; `collision_severity` valid dengan tiga kelas.
- Missing eksplisit hanya pada empat kolom koordinat (53 masing-masing); kode sentinel `-1` perlu penanganan kategorikal.
- Proporsi Serious per tahun meningkat secara deskriptif dari 21,06% (2021) menjadi 24,81% (2025); Fatal tetap sekitar 1,4–1,5%.
- Volume tertinggi tercatat pada jam 16–17 dan hari kode 6; arti kode hari memerlukan data dictionary resmi.

## Decisions

- Full dataset adalah kandidat master Tugas 2; 10K hanya baseline legacy.
- Tidak ada model, artifact, processed dataset besar, atau perubahan aplikasi pada Phase 1.
- Split temporal direkomendasikan secara kondisional; keputusan final menunggu use case.
- Phase 2 tidak melakukan balancing, preprocessing permanen, sampling 10K, atau pemodelan.

## Open Questions

- Definisi use case/timing prediksi, split yang diharapkan dosen, penggunaan fitur geografis/admin, dan lokasi data dictionary lengkap.
- Codebook resmi STATS19 dan fitur data-mining yang wajib untuk penilaian masih perlu dikonfirmasi.

Last Verified: 2026-08-27
