# HANDOFF

## Current Phase

PHASE 1 – DATA STRATEGY (COMPLETED)

## Last Completed

- Audit strategi full dataset: schema/quality 513.801 × 44, target, inventory 44 fitur, leakage risks, baseline comparison, dan sampling legacy.
- `docs/DATA_STRATEGY.md` dibuat tanpa membuat data/model/artifact baru.

## Current State

- Raw STATS19 tersedia lokal di `data/raw/dft-road-casualty-statistics-collision-last-5-years.csv`: 513.801 baris, 44 kolom, periode 2021–2025. File di-ignore Git.
- Baseline legacy adalah 10.000 baris (2.000/tahun, `random_state=42`). Tidak ada file sample terpisah yang dapat diverifikasi.
- Pipeline legacy memakai `collision_severity`, Random Forest 18→105 fitur, serta K-Means 18→108 fitur. Hasilnya bukan hasil full dataset Tugas 2.
- Aplikasi `app.py` Streamlit memuat artefak legacy; tidak diubah. Uji startup Phase 0 pada port lokal 8502 mengembalikan HTTP 200, lalu proses dihentikan.
- Branch aktif: `main`. Remote `origin` terverifikasi menuju `https://github.com/asyudianggara/traffic-accident-datamining.git` untuk fetch dan push. Checkpoint Phase 0 `3a4f9b1` berhasil dipush ke `origin/main`.
- Full dataset adalah kandidat master; 10K hanya legacy baseline. Target `collision_severity`: Fatal 7.553 (1,470024%), Serious 116.813 (22,735067%), Slight 389.435 (75,794909%).

## Files Changed

- `README.md`
- `docs/PROJECT_STATUS.md`
- `docs/HANDOFF.md`
- `docs/CHANGELOG.md`
- `docs/DATA_STRATEGY.md`

## Files Not Changed

- Dataset raw/processed, notebook, script pipeline, model/artifact, hasil legacy, dependensi, `.gitignore`, dan `app.py`.

## Verified Results

- Raw full data: 513.801 × 44, tahun 2021–2025.
- Sampling legacy: `groupby("collision_year").sample(n=2000, random_state=42)` untuk 2021–2025.
- Classification legacy split: `test_size=0.20`, `random_state=42`, `stratify=y`.
- Clustering legacy: `KMeans`, evaluasi `k=2..6`, final metadata `k=2`.
- Full CSV: 0 duplicate row; 53 missing pada masing-masing empat kolom koordinat; seluruh date/time valid; tidak ada kode tak terpetakan pada kolom yang memiliki mapping lokal.

## Unverified Items

- Keberadaan file dataset sample 10K terpisah dan waktu persis sampling pertama kali dilakukan.
- Definisi use case/timing prediksi, split yang diminta dosen, penggunaan fitur geografis/admin, dan data dictionary STATS19 lengkap.

## Known Issues

- README dan identitas remote sebelumnya mengacu pada proyek lama/course lama; README utama sudah diselaraskan sebagai Phase 0, tetapi aplikasi dan `README_APP.md` masih legacy dan sengaja tidak diubah.
- Leakage risk: outcome/adjusted severity fields, number of casualties, dan police-attendance harus dikeluarkan/ditinjau sebelum model.

## Do Not

- Jangan mengubah project lama.
- Jangan membuat dataset turunan/full baru, training, clustering, feature selection, tuning, atau mengubah artefak legacy.
- Jangan force-push atau mengganti remote tanpa instruksi eksplisit.

## Next Required Action

Setelah instruksi eksplisit Phase 2: lengkapi data dictionary, domain audit, dan EDA terarah; finalisasi spesifikasi feature/quality tanpa training atau modeling.

## STOP CONDITION

Jangan masuk Phase 1 sebelum mendapat instruksi eksplisit.
