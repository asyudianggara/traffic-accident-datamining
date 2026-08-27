# PROJECT STATUS

Project: Tugas 2 – Penambangan Data
Case: Analisis Kecelakaan Lalu Lintas STATS19
Current Phase: PHASE 8 – APPLICATION INTEGRATION & OPERATIONAL PREDICTION
Overall Progress: PHASE 8 / 10
Status: COMPLETED

## Completed

- Audit awal Git, struktur proyek, dokumentasi, dataset, artefak, pipeline, dan aplikasi selesai pada 2026-08-27.
- Dataset raw lokal terverifikasi: `data/raw/dft-road-casualty-statistics-collision-last-5-years.csv` (513.801 baris, 44 kolom, 2021–2025, 97.669.586 byte).
- Baseline lama 10K teridentifikasi sebagai sampling 2.000 baris per tahun (2021–2025), `random_state=42`.
- README, handoff, dan changelog Phase 0 dibuat/diperbarui.
- Repository GitHub baru terhubung dan checkpoint Phase 0 `3a4f9b1` berhasil dipush ke `origin/main` pada 2026-08-27.
- Strategi full dataset, quality audit ringan, inventory 44 fitur, dan audit sampling legacy selesai; lihat `docs/DATA_STRATEGY.md`.
- Analisis deskriptif full dataset, visualisasi terarah, feature roles, data-mining relevance, dan rekomendasi preparation selesai; lihat `docs/DATA_UNDERSTANDING.md`.
- Kontrak preparation full dataset, role/status seluruh 44 fitur, leakage exclusions, sentinel/anomaly rules, temporal derivations, dan train-only pipeline strategy selesai; lihat `docs/DATA_PREPARATION.md`.
- Strategi feature selection, redundancy, candidate sets, algorithm strategy, dan desain eksperimen Phase 5 selesai; lihat `docs/FEATURE_SELECTION.md`.
- Baseline classification full dataset selesai: Logistic Regression dan Decision Tree pada development 2021–2024 dengan holdout temporal 2025; lihat `docs/MODELING_PHASE5A.md`.
- Phase 5B-1 partial: Logistic Regression dan Decision Tree selesai; Random Forest dihentikan karena bottleneck resource; HistGradientBoosting menolak sparse input; lihat `docs/MODELING_PHASE5B1.md`.
- Implementasi Phase 3 selesai melalui `prepare_phase3.py`; validation manifest kecil dibuat tanpa processed dataset/model baru.
- Implementasi Phase 4 selesai melalui `feature_selection_phase4.py`; ranking training-only, redundancy report, dan metadata reproducibility dibuat.
- Phase 5 baseline modeling selesai melalui `modeling_phase5.py`; Logistic Regression, Decision Tree, dan bounded Random Forest dievaluasi pada holdout 2025.
- Phase 5.1 selesai: empat strategi imbalance dibandingkan pada validation 2024; balanced Random Forest dipilih provisional dan dievaluasi sekali pada holdout 2025.
- Phase 5.2 selesai: threshold Fatal dipilih menggunakan validation 2024 dan dievaluasi sekali pada holdout 2025.
- Phase 6 selesai: final candidate model dipilih dan artifact/metadata dibuat tanpa memakai ulang 2025 untuk seleksi.
- Phase 7 operational validation selesai: artifact reload, input contract, prediction rule, reproducibility, dan edge cases didokumentasikan.
- Phase 8 selesai: halaman classification diintegrasikan dengan final research artifact 18→149, threshold 0,50, output probabilitas, dan smoke test Streamlit.

## Current

- Phase 8 completed; aplikasi inference classification terintegrasi, tetapi deployment-ready belum diklaim.

## Current Subphase

- PHASE 8 – APPLICATION INTEGRATION & OPERATIONAL PREDICTION (COMPLETED).

## Current Task

- Meninjau hasil integrasi aplikasi dan operational prediction sebelum deployment lanjutan.

## In Progress

- Application integration complete; tidak ada tuning, model replacement, atau retraining yang dilakukan.

## Not Started

- Domain-range validation, codebook/use-case confirmation, dan deployment operasional.

## Blocked

- Data dictionary version, prediction timing, geographic policy, and final split rule still await confirmation.

## Next Action

- Review `docs/APPLICATION_INTEGRATION.md`; konfirmasi dependency version, input policy, use case, timing prediksi, dan deployment scope.

## Do Not Do

- Jangan melakukan final model selection, tuning ekstensif, clustering, association mining, forecasting, deployment, atau mengubah artefak legacy sebelum scope phase berikutnya.

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
- Data Preparation: COMPLETED (implemented + validated) — no processed dataset or learned artifact persisted.
- Modeling: PARTIAL — Phase 5A baselines plus two completed Phase 5B-1 comparison runs; Random Forest incomplete.
- Evaluation: PARTIAL — two comparison holdout metrics recorded; complete comparison/final evaluation not started.
- Deployment: PARTIAL — aplikasi legacy tersedia, tetapi belum merepresentasikan pipeline full dataset Tugas 2.

## Tugas 2 Status

| Requirement                | Status      | Evidence                                                                     | Gap                                       |
| -------------------------- | ----------- | ---------------------------------------------------------------------------- | ----------------------------------------- |
| Analisis masalah/kebutuhan | PARTIAL     | Case dan audit Phase 0                                                       | Rumusan kebutuhan Tugas 2 belum dibuat    |
| Review dataset             | COMPLETED   | `docs/DATA_STRATEGY.md`: schema, quality, target, 44-feature inventory       | EDA/domain audit lanjutan Phase 2         |
| Lima peran data mining     | NOT STARTED | TIDAK DAPAT DIVERIFIKASI                                                     | Belum didokumentasikan untuk Tugas 2      |
| CRISP-DM                   | PARTIAL     | Pemetaan di dokumen ini                                                      | Tahap full dataset belum dikerjakan       |
| Data preparation           | COMPLETED   | `docs/DATA_PREPARATION.md`: feature roles, rules, leakage, train-only design | Implementation remains for later scope    |
| Comparison algoritma       | PARTIAL     | `docs/MODELING_PHASE5B1.md`: two completed comparison models                 | RF incomplete; HGB incompatible           |
| Feature selection          | COMPLETED   | `docs/FEATURE_SELECTION.md`: provisional sets and selection strategy         | Final selection after Phase 5 evidence    |
| Evaluation                 | PARTIAL     | `docs/MODELING_PHASE5A.md`: temporal holdout metrics                         | Final evaluation belum dilakukan          |
| Deployment/decision making | PARTIAL     | Streamlit legacy tersedia                                                    | Adaptasi ke hasil Tugas 2 belum dilakukan |

## Next Phase

PHASE 9 – DEPLOYMENT / OPERATIONAL HANDOFF (SCOPE TO BE CONFIRMED)

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
- Official DfT open-data page identifies the 2025 data guide as the codebook source; unresolved codes remain coded and are not relabeled by assumption.
- Full-dataset range checks found 0 invalid years, non-positive vehicle/casualty counts, unsupported speed-limit codes, out-of-screening-range coordinates, date/time parse failures, or values below `-1` in audited coded fields.
- Exploratory MI on development rows ranked `police_force`, `number_of_vehicles`, `speed_limit`, and `junction_control` highest; this is not model performance.
- Phase 5A used 412,276 development rows and 101,525 untouched 2025 holdout rows; both baseline models had Fatal recall 0.0000.
- Phase 5B-1 repeated the same split/features/preprocessing; completed-model Macro F1: Logistic 0.2907, Tree 0.3006; Fatal recall 0 for both.
- Random Forest (`300` trees, balanced weights) was stopped after approximately 27 minutes and approximately 1.08 GB RAM without result; HGB rejected sparse input.

## Decisions

- Full dataset adalah kandidat master Tugas 2; 10K hanya baseline legacy.
- Tidak ada model, artifact, processed dataset besar, atau perubahan aplikasi pada Phase 1.
- Split temporal direkomendasikan secara kondisional; keputusan final menunggu use case.
- Phase 2 tidak melakukan balancing, preprocessing permanen, sampling 10K, atau pemodelan.
- Phase 3 preserves raw data, defines train-only fitting for learned transforms, and creates only a small validation manifest; no processed CSV or model artifact is created.
- Phase 4 does not train final models, tune hyperparameters, run PCA, mine association rules, or change legacy artifacts.
- Phase 5A applied no balancing and created only two baseline pipelines, metadata, and one concise metrics CSV.
- Phase 5B-1 did not apply SMOTE or resampling; only the requested RF class-weight configuration was attempted and did not complete.

## Open Questions

- Definisi use case/timing prediksi, split yang diharapkan dosen, penggunaan fitur geografis/admin, dan lokasi data dictionary lengkap.
- Codebook resmi STATS19 dan fitur data-mining yang wajib untuk penilaian masih perlu dikonfirmasi.
- Final prediction timing, official data-guide version to freeze, geography/privacy policy, and final split rule remain open.
- Provisional sets: classification 18, clustering 18, association 15, temporal 4; final inclusion remains subject to Phase 5 evidence.
- Phase 5B-1 is PARTIAL; no numeric rank is assigned to incomplete Random Forest or unrun HistGradientBoosting.
- Baseline holdout macro F1: Logistic Regression 0.2907; Decision Tree 0.3006; these are not final model-selection results.

Last Verified: 2026-08-27
