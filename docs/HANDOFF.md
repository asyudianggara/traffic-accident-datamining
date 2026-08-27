# HANDOFF

## Current Phase

PHASE 10.2 — FINAL REPORT PREPARATION

Blueprint laporan Phase 10.1 tetap tersedia dan tidak diubah.

Modeling, final artifact, dan application consistency sudah locked. Fokus
berikutnya adalah penulisan laporan akademik menggunakan factsheet yang telah
disinkronkan.

## Last Completed

- Audit strategi full dataset: schema/quality 513.801 × 44, target, inventory 44 fitur, leakage risks, baseline comparison, dan sampling legacy.
- `docs/DATA_STRATEGY.md` dibuat tanpa membuat data/model/artifact baru.
- `docs/DATA_UNDERSTANDING.md` dibuat dengan audit deskriptif full dataset dan lima visualisasi terarah; tidak ada model baru.
- `docs/DATA_PREPARATION.md` dibuat dengan kontrak preparation seluruh 44 fitur, leakage/sentinel/anomaly rules, dan train-only pipeline design; tidak ada data turunan atau model baru.
- `docs/FEATURE_SELECTION.md` dibuat dengan review seluruh 44 fitur, provisional sets, exploratory MI pada development data, redundancy review, algorithm strategy, dan Phase 5 experiment design; tidak ada final model.
- `docs/MODELING_PHASE5A.md` dibuat dan dua baseline full-dataset pipeline selesai: Logistic Regression dan Decision Tree dengan 2025 temporal holdout.
- `docs/MODELING_PHASE5B1.md` dibuat; Logistic Regression dan Decision Tree comparison selesai, RF dihentikan karena resource bottleneck, dan HGB ditolak sparse input.
- `prepare_phase3.py` dibuat; full raw dataset diprepare in-memory dengan train-only preprocessing dan validasi kecil.
- `feature_selection_phase4.py` dibuat; evidence MI/tree importance, redundancy, dan stability training-only dihasilkan.
- `modeling_phase5.py` dibuat; tiga baseline classification dievaluasi pada temporal holdout 2025.
- `phase5_1_imbalance_experiment.py` dibuat; empat strategi diuji pada validation 2024 dan balanced Random Forest dievaluasi sekali pada 2025.
- `phase5_2_threshold_analysis.py` dibuat; threshold Fatal 0.50 dipilih pada validation 2024 dan diuji sekali pada 2025.
- `finalize_research_model.py` dibuat; final candidate Random Forest balanced + threshold Fatal 0,50 difit pada development 2021–2024.
- `docs/FINAL_MODEL.md`, `results/final_model_metadata.json`, `results/final_model_comparison.csv`, dan `models/final_research_model.joblib` dibuat.

## Current State

- Raw STATS19 tersedia lokal di `data/raw/dft-road-casualty-statistics-collision-last-5-years.csv`: 513.801 baris, 44 kolom, periode 2021–2025. File di-ignore Git.
- Analisis clustering legacy C3–C4 memakai 10.000 baris (2.000/tahun, `random_state=42`). Tidak ada file dataset terpisah yang dapat diverifikasi.
- Pipeline legacy memakai `collision_severity`, Random Forest 18→105 fitur, serta K-Means 18→108 fitur. Hasilnya historis dan bukan hasil final research.
- Aplikasi `app.py` Streamlit memuat `models/final_research_model.joblib` untuk classification dan artefak clustering legacy; inference-only.
- Branch aktif: `main`. Remote `origin` terverifikasi menuju `https://github.com/asyudianggara/traffic-accident-datamining.git` untuk fetch dan push. Checkpoint Phase 0 `3a4f9b1` berhasil dipush ke `origin/main`.
- Full dataset adalah kandidat master; 10K hanya analisis clustering legacy C3–C4. Target `collision_severity`: Fatal 7.553 (1,470024%), Serious 116.813 (22,735067%), Slight 389.435 (75,794909%).
- Phase 2 memverifikasi pola temporal, statistik numerik, distribusi kategori, target-versus-fitur, missingness, feature roles, dan relevansi lima peran data mining.
- Phase 3 memverifikasi range/logical checks, mempertahankan target tiga kelas tanpa balancing, dan mendokumentasikan derived `month`/`hour` serta provisional temporal holdout.
- Phase 4 menetapkan provisional classification/clustering sets (18 masing-masing), association basket (15), temporal set (4), dan leakage-safe selection rules.
- Phase 5A menggunakan 412.276 development rows dan 101.525 holdout rows; preprocessing fitted pada development saja; kedua model mencatat Fatal recall 0.
- Phase 5B-1 memakai split/features/preprocessing yang sama; hanya dua model completed dengan metrik valid, keduanya Fatal recall 0.
- Phase 6 memilih final candidate; metrik 2025 diambil dari hasil Phase 5.2 yang telah dibekukan dan tidak dievaluasi ulang untuk seleksi.
- Phase 7 memvalidasi reload/prediction artifact, 18-feature contract, 149 encoded features, threshold, reproducibility, dan edge cases tanpa fitting atau pemilihan model baru.
- Phase 8 mengintegrasikan `models/final_research_model.joblib` ke halaman classification tanpa retraining; prediction consistency dan Streamlit smoke test lulus.
- Phase 9.2 mendokumentasikan interpretasi final holdout, trade-off Fatal, batasan metodologis, klaim yang tidak didukung, dan status research readiness.
- Phase 9.3 mengonsolidasikan hasil final classification, clustering, validasi aplikasi, pemisahan legacy, dan batasan untuk pelaporan.
- Phase 9.4 mengunci paket research final dan traceability tanpa mengubah fakta penelitian atau artifact.
- Phase 10.1 menyusun blueprint laporan final, matriks sumber, dan checklist traceability.
- Phase 8.1 melakukan audit alignment aplikasi: teks UI final research, split temporal, dan dashboard legacy diperjelas; `py_compile`, consistency test, dan smoke test lulus.
- Phase 8.2 menyelaraskan Dashboard Dataset agar ukuran raw/final split tidak tertukar dengan clustering legacy C3–C4 10K, menampilkan metrik Fatal final, dan menambahkan uji konsistensi UI untuk 8 halaman.
- Phase 8.4 memperbaiki terminologi dokumentasi final research versus legacy, menegaskan kontrak final 18→149 dan holdout 2025, serta memverifikasi `.venv` pada scikit-learn 1.9.0.
- Phase 10.2 melakukan knowledge synchronization dan membuat `docs/PHASE10_2_RESEARCH_FACTS.md` sebagai sumber fakta internal sebelum penulisan laporan.
- Phase 10.2.1 menyelaraskan metadata `PROJECT_STATUS.md` dan `HANDOFF.md` dengan status final modeling dan fokus report preparation; tidak ada artifact atau hasil ML yang diubah.

## Files Changed

- `README.md`
- `docs/PROJECT_STATUS.md`
- `docs/HANDOFF.md`
- `docs/CHANGELOG.md`
- `docs/DATA_STRATEGY.md`
- `docs/DATA_UNDERSTANDING.md` dan `docs/figures/data-understanding/*.png`
- `docs/DATA_PREPARATION.md`
- `prepare_phase3.py` dan `results/phase3_preparation_validation.json`
- `feature_selection_phase4.py`, `results/feature_selection_summary.csv`, `results/feature_selection_redundancy.csv`, dan `results/feature_selection_metadata.json`
- `modeling_phase5.py`, `docs/MODELING_PHASE5.md`, `results/phase5_model_comparison.csv`, `results/phase5_classification_report.csv`, `results/phase5_confusion_matrix_*.csv`, dan `results/phase5_metadata.json`
- `phase5_1_imbalance_experiment.py`, `results/phase5_1_*.csv`, dan `results/phase5_1_imbalance_metadata.json`
- `phase5_2_threshold_analysis.py`, `results/phase5_2_*.csv`, `results/phase5_2_*.png`, dan `results/phase5_2_metadata.json`
- `docs/FEATURE_SELECTION.md`
- `docs/MODELING_PHASE5B1.md`, `models/classification_phase5b_logistic_regression.joblib`, `models/classification_phase5b_decision_tree.joblib`, `models/classification_phase5b_metadata.json`, dan `results/classification_phase5b_comparison.csv`
- `finalize_research_model.py`, `docs/FINAL_MODEL.md`, `models/final_research_model.joblib`, `results/final_model_metadata.json`, dan `results/final_model_comparison.csv`
- `phase7_operational_validation.py`, `docs/OPERATIONAL_VALIDATION.md`, dan `results/phase7_operational_validation.json`
- `app.py`, `docs/APPLICATION_INTEGRATION.md`, `phase8_application_consistency.py`, `phase8_streamlit_smoke_test.py`, `phase8_2_ui_consistency.py`, dan hasil JSON Phase 8.
- `docs/MODELING_PHASE5A.md`, `models/classification_baseline_logistic_regression.joblib`, `models/classification_baseline_decision_tree.joblib`, `models/classification_baseline_metadata.json`, dan `results/classification_baseline.csv`

## Files Not Changed in Documentation Audit

- Dataset raw/processed, notebook, script pipeline, model/artifact, hasil legacy, dependensi, `.gitignore`, dan source aplikasi/model.

## Verified Results

- Raw full data: 513.801 × 44, tahun 2021–2025.
- Sampling analisis clustering legacy C3–C4: `groupby("collision_year").sample(n=2000, random_state=42)` untuk 2021–2025.
- Classification legacy split: `test_size=0.20`, `random_state=42`, `stratify=y`.
- Clustering legacy: `KMeans`, evaluasi `k=2..6`, final metadata `k=2`.
- Full CSV: 0 duplicate row; 53 missing pada masing-masing empat kolom koordinat; seluruh date/time valid; tidak ada kode tak terpetakan pada kolom yang memiliki mapping lokal.
- Target Serious meningkat secara deskriptif dari 21,06% pada 2021 menjadi 24,81% pada 2025; volume data tertinggi berada pada jam 16–17.
- Official DfT data-guide source identified; unresolved coded values remain unchanged until the guide version is frozen.
- Exploratory MI used only 2021–2024 development rows; 2025 was not used for feature selection.
- Logistic Regression holdout macro F1 0.2907; Decision Tree holdout macro F1 0.3006; Fatal recall 0 untuk keduanya.
- Logistic Regression holdout macro F1 0.2907; Decision Tree holdout macro F1 0.3006; Fatal recall 0 untuk keduanya.
- Phase 8.2 UI contract: raw 513.801, development 412.276, train 311.349, validation 100.927, holdout 101.525, classification 18→149, clustering legacy C3–C4 10.000; validasi terbaru PASS.
- Phase 8.4 documentation contract: final research 18→149 dan holdout 2025 dipisahkan dari classification legacy 18→105 serta clustering legacy C3–C4 10K; `.venv` diverifikasi pada scikit-learn 1.9.0.

## Unverified Items

- Keberadaan file dataset analisis clustering legacy C3–C4 10K terpisah dan waktu persis sampling pertama kali dilakukan.
- Definisi use case/timing prediksi, split yang diminta dosen, penggunaan fitur geografis/admin, dan data dictionary STATS19 lengkap.
- Arti seluruh kode unresolved dan daftar fitur data-mining yang wajib dinilai masih belum terverifikasi.
- Prediction timing, geographic/privacy policy, official codebook version, and operational acceptance criteria remain unconfirmed.

## Known Issues

- README dan identitas remote sebelumnya mengacu pada proyek lama/course lama; README utama sudah diselaraskan sebagai Phase 0, tetapi aplikasi dan `README_APP.md` masih legacy dan sengaja tidak diubah.
- Leakage risk: outcome/adjusted severity fields, number of casualties, dan police-attendance harus dikeluarkan/ditinjau sebelum model.
- Pola target-versus-fitur bersifat deskriptif; kategori langka memerlukan kehati-hatian dan tidak boleh dibaca sebagai hubungan kausal.
- Range checks found no structural invalids in the audited full dataset; IQR flags are retained, not deleted.
- Final candidate research-ready with conditions but not deployment-ready; runtime `.venv` dan artifact sama-sama menggunakan scikit-learn 1.9.0. Alignment environment PASS, tetapi compatibility lintas versi bukan klaim penelitian; domain-range validation tetap perlu dikonfirmasi.
- Phase 5B-1 RF tidak menghasilkan result setelah ~27 menit/~1.08 GB RAM; HGB tidak dijalankan karena established sparse preprocessing incompatible.
- Baselines preserve natural imbalance; no SMOTE, over/undersampling, or class weighting was applied.

## Do Not

- Jangan mengubah project lama.
- Jangan melakukan deployment operasional, association mining, atau forecasting sebelum scope berikutnya dikonfirmasi. Integrasi app dan clustering legacy sudah ada dan tidak boleh diubah tanpa scope eksplisit.
- Jangan force-push atau mengganti remote tanpa instruksi eksplisit.

## Next Required Action

Gunakan `docs/FINAL_REPORT_BLUEPRINT.md` dan `docs/PHASE10_2_RESEARCH_FACTS.md`
untuk menyusun laporan akademik. Jangan melakukan retraining/modeling ulang,
dan jangan klaim deployment readiness sebelum dependency version, input policy,
domain validation, dan open methodological decisions selesai.

## STOP CONDITION

Jangan lanjut deployment sebelum final candidate dan open methodological decisions direview.
