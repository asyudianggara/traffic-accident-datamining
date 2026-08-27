# PROJECT STATUS

Project: Tugas 2 – Penambangan Data
Case: Analisis Kecelakaan Lalu Lintas STATS19
Current Phase: PHASE 10.2 — FINAL REPORT PREPARATION
Overall Progress: PHASE 10.2 / FINAL REPORT PREPARATION
Status: IN PROGRESS

## Completed / Locked

- Audit awal Git, struktur proyek, dokumentasi, dataset, artefak, pipeline, dan aplikasi selesai pada 2026-08-27.
- Dataset raw lokal terverifikasi: `data/raw/dft-road-casualty-statistics-collision-last-5-years.csv` (513.801 baris, 44 kolom, 2021–2025, 97.669.586 byte).
- Analisis clustering legacy C3–C4 10K teridentifikasi sebagai sampling 2.000 baris per tahun (2021–2025), `random_state=42`.
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
- Phase 9.1 selesai: konflik dokumentasi legacy/final, split temporal, status evaluasi, dan handoff diperbaiki tanpa mengubah artefak.
- Phase 9.2 selesai: interpretasi hasil, batasan metodologis, klaim yang tidak didukung, dan rekomendasi validasi lanjutan didokumentasikan.
- Phase 9.3 selesai: hasil classification, clustering, validasi aplikasi, pemisahan legacy, dan batasan dikonsolidasikan untuk pelaporan final.
- Phase 9.4 selesai: paket research final, status locked, dan kesiapan traceability dikonfirmasi tanpa perubahan pada fakta penelitian atau artifact.
- Phase 10.1 selesai: blueprint laporan final dan matriks sumber/traceability disusun tanpa eksperimen baru.
- Phase 8.1 audit alignment selesai: ringkasan UI membedakan final research full dataset dari dashboard legacy 10K; prediction contract tetap lulus.
- Phase 8.2 selesai: Dashboard Dataset menampilkan ringkasan 513.801 × 44 dan split final; clustering 10K diberi label eksplisit legacy C3–C4; metrik Fatal final dan uji konsistensi UI ditambahkan.
- Phase 8.4 selesai: terminologi dokumentasi final research, classification legacy, dan clustering legacy C3–C4 dipisahkan; dependency `.venv` diverifikasi pada scikit-learn 1.9.0; validasi aplikasi tetap menggunakan kontrak 18 → 149 dan holdout 2025.
- Phase 10.2 knowledge synchronization selesai: fakta dataset, temporal split, target, fitur, preprocessing, model, metrik, clustering legacy, aplikasi, klaim, keterbatasan, dan traceability dikonsolidasikan pada `docs/PHASE10_2_RESEARCH_FACTS.md`.
- Phase 10.2.1 selesai: metadata dokumentasi diselaraskan dengan fokus persiapan laporan; tidak ada perubahan dataset, model, artifact, results ML, aplikasi, atau metodologi.

## Current

- Modeling, final artifact, dan aplikasi sudah locked; fokus aktif berpindah ke persiapan laporan akademik. Deployment-ready tetap belum diklaim.

## Current Subphase

- PHASE 10.2 — FINAL REPORT PREPARATION.

## Current Task

- Menyusun laporan akademik berdasarkan `docs/FINAL_REPORT_BLUEPRINT.md` dan `docs/PHASE10_2_RESEARCH_FACTS.md`.

## In Progress

- Penulisan laporan dimulai dari fakta yang sudah locked; tidak ada tuning, model replacement, retraining, atau eksperimen ML baru.

## Not Started

- Domain-range validation, codebook/use-case confirmation, dan deployment operasional.

## Blocked

- Deployment operasional masih menunggu validasi domain, policy geografis, versi codebook, dan acceptance criteria.

## Next Action

- Mulai penyusunan laporan akademik dari blueprint dan factsheet; jangan mengubah fakta final atau mengklaim deployment readiness.

## Do Not Do

- Jangan melakukan final model selection, tuning ekstensif, clustering, association mining, forecasting, deployment, atau mengubah artefak legacy sebelum scope phase berikutnya.

## Dataset

- Raw: `data/raw/dft-road-casualty-statistics-collision-last-5-years.csv`, lokal dan di-ignore Git.
- Full available records: 513.801 baris × 44 kolom; `collision_year` 2021: 101.087, 2022: 106.004, 2023: 104.258, 2024: 100.927, 2025: 101.525. Kolom target lama: `collision_severity`.
- Analisis clustering legacy C3–C4: artifact/dokumentasi lama menunjukkan 10.000 baris × 44 kolom, 2.000 per tahun; file dataset terpisah TIDAK DAPAT DIVERIFIKASI tersedia pada checkout ini.
- Target final classification: `collision_severity`, dengan mapping 1 = Fatal, 2 = Serious, 3 = Slight.

## Existing Models and Results

- Classification legacy baseline: Random Forest, 18 fitur input, 105 fitur encoded, train/test 8.000/2.000, `random_state=42`. Metadata melaporkan accuracy 0,6385 dan macro F1 0,3862; baseline ini historis.
- Classification final research: Random Forest balanced, 18 fitur input, 149 fitur encoded, threshold Fatal 0,50; 2025 final holdout.
- Clustering legacy baseline: K-Means `k=2`, 18 fitur input, 108 fitur encoded, 10.000 record analisis clustering legacy C3–C4; C2/C3 mengevaluasi `k=2..6`.
- Final research: `models/final_research_model.joblib`, `results/final_model_metadata.json`, dan hasil final terkait memakai kontrak 18 → 149 serta final holdout 2025.
- Legacy: `models/final_classification_metadata.json` (18 → 105), artifact clustering legacy, dan hasil C3–C4 10.000 record. Artifact/hasil legacy tidak boleh diperlakukan sebagai hasil final research.

## Existing Application

- `app.py` adalah aplikasi Streamlit inference-only yang memuat `models/final_research_model.joblib` untuk classification dan artefak clustering legacy; aplikasi tidak melakukan retraining saat dijalankan.
- Perintah terverifikasi: `.venv\Scripts\python.exe -m streamlit run app.py`.
- Status startup Phase 0: PASS — Streamlit diuji pada 2026-08-27 di port lokal 8502 dan mengembalikan HTTP 200; proses dihentikan setelah verifikasi.
- Phase 8.2 UI consistency test: `phase8_2_ui_consistency.py` memeriksa angka dataset, label clustering legacy C3–C4, larangan label dataset utama untuk 10K, dan render seluruh 8 halaman.

## CRISP-DM Status

- Business Understanding: PARTIAL — case tersedia; use case/waktu prediksi masih open question.
- Data Understanding: COMPLETED — schema, kualitas dasar, target, periode, dan baseline/full comparison terverifikasi.
- Data Preparation: COMPLETED (implemented + validated) — no processed dataset or learned artifact persisted.
- Modeling: COMPLETED — Phase 5, 5.1, 5.2, dan Phase 6 final candidate telah diselesaikan.
- Evaluation: COMPLETED WITH LIMITATIONS — final holdout 2025 telah dievaluasi; keterbatasan dan metrik minoritas didokumentasikan.
- Deployment: PARTIAL — integrasi aplikasi selesai, tetapi deployment operasional belum diklaim siap.

## Tugas 2 Status

| Requirement                | Status      | Evidence                                                                     | Gap                                       |
| -------------------------- | ----------- | ---------------------------------------------------------------------------- | ----------------------------------------- |
| Analisis masalah/kebutuhan | PARTIAL     | Case dan audit Phase 0                                                       | Rumusan kebutuhan Tugas 2 belum dibuat    |
| Review dataset             | COMPLETED   | `docs/DATA_STRATEGY.md`: schema, quality, target, 44-feature inventory       | EDA/domain audit lanjutan Phase 2         |
| Lima peran data mining     | NOT STARTED | TIDAK DAPAT DIVERIFIKASI                                                     | Belum didokumentasikan untuk Tugas 2      |
| CRISP-DM                   | COMPLETED WITH LIMITATIONS | Pemetaan tahap data hingga evaluasi terdokumentasi | Deployment operasional dan use case formal masih terbuka |
| Data preparation           | COMPLETED   | `docs/DATA_PREPARATION.md`: feature roles, rules, leakage, train-only design | Implementation remains for later scope    |
| Comparison algoritma       | COMPLETED   | `docs/MODELING_PHASE5.md`, `docs/MODELING_PHASE5B1.md`, dan Phase 5.2        | HGB sparse incompatibility tetap dicatat  |
| Feature selection          | COMPLETED   | `docs/FEATURE_SELECTION.md`: provisional sets and selection strategy         | Final selection after Phase 5 evidence    |
| Evaluation                 | COMPLETED   | `docs/FINAL_MODEL.md`: final holdout metrics dan keterbatasan               | Validasi operasional lanjutan             |
| Deployment/decision making | PARTIAL     | `docs/APPLICATION_INTEGRATION.md` dan `docs/OPERATIONAL_VALIDATION.md`       | Deployment operasional belum diklaim       |

## Next Phase

PHASE 10.2 — ACADEMIC REPORT WRITING

## Important Rules

- Full dataset menjadi dataset utama Tugas 2; 10K hanya digunakan untuk baseline classification historis dan analisis clustering legacy C3–C4.
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

- Full dataset adalah kandidat master Tugas 2; analisis clustering legacy C3–C4 menggunakan 10K dan tidak menggantikan dataset utama.
- Tidak ada model, artifact, processed dataset besar, atau perubahan aplikasi pada Phase 1.
- Split temporal final: train 2021–2023, validation 2024, refit development 2021–2024, dan holdout 2025.
- Phase 2 tidak melakukan balancing, preprocessing permanen, sampling baru untuk analisis clustering legacy C3–C4 10K, atau pemodelan.
- Phase 3 preserves raw data, defines train-only fitting for learned transforms, and creates only a small validation manifest; no processed CSV or model artifact is created.
- Phase 4 does not train final models, tune hyperparameters, run PCA, mine association rules, or change legacy artifacts.
- Phase 5A applied no balancing and created only two baseline pipelines, metadata, and one concise metrics CSV.
- Phase 5B-1 did not apply SMOTE or resampling; only the requested RF class-weight configuration was attempted and did not complete.

## Open Questions

- Definisi use case/timing prediksi, split yang diharapkan dosen, penggunaan fitur geografis/admin, dan lokasi data dictionary lengkap.
- Codebook resmi STATS19 dan fitur data-mining yang wajib untuk penilaian masih perlu dikonfirmasi.
- Final prediction timing, official data-guide version to freeze, geography/privacy policy, and final split rule remain open.
- Provisional sets: classification 18, clustering 18, association 15, temporal 4; final inclusion remains subject to Phase 5 evidence.
- Phase 5B-1 mencatat RF resource bottleneck dan HGB sparse incompatibility; keputusan final tetap didokumentasikan pada Phase 6.
- Baseline holdout macro F1: Logistic Regression 0.2907; Decision Tree 0.3006; these are not final model-selection results.

Last Verified: 2026-08-27
