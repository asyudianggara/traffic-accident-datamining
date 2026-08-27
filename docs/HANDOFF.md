# HANDOFF

## Current Phase

PHASE 2 – DATA UNDERSTANDING (COMPLETED)

## Last Completed

- Audit strategi full dataset: schema/quality 513.801 × 44, target, inventory 44 fitur, leakage risks, baseline comparison, dan sampling legacy.
- `docs/DATA_STRATEGY.md` dibuat tanpa membuat data/model/artifact baru.
- `docs/DATA_UNDERSTANDING.md` dibuat dengan audit deskriptif full dataset dan lima visualisasi terarah; tidak ada model baru.

## Current State

- Raw STATS19 tersedia lokal di `data/raw/dft-road-casualty-statistics-collision-last-5-years.csv`: 513.801 baris, 44 kolom, periode 2021–2025. File di-ignore Git.
- Baseline legacy adalah 10.000 baris (2.000/tahun, `random_state=42`). Tidak ada file sample terpisah yang dapat diverifikasi.
- Pipeline legacy memakai `collision_severity`, Random Forest 18→105 fitur, serta K-Means 18→108 fitur. Hasilnya bukan hasil full dataset Tugas 2.
- Aplikasi `app.py` Streamlit memuat artefak legacy; tidak diubah. Uji startup Phase 0 pada port lokal 8502 mengembalikan HTTP 200, lalu proses dihentikan.
- Branch aktif: `main`. Remote `origin` terverifikasi menuju `https://github.com/asyudianggara/traffic-accident-datamining.git` untuk fetch dan push. Checkpoint Phase 0 `3a4f9b1` berhasil dipush ke `origin/main`.
- Full dataset adalah kandidat master; 10K hanya legacy baseline. Target `collision_severity`: Fatal 7.553 (1,470024%), Serious 116.813 (22,735067%), Slight 389.435 (75,794909%).
- Phase 2 memverifikasi pola temporal, statistik numerik, distribusi kategori, target-versus-fitur, missingness, feature roles, dan relevansi lima peran data mining.

## Files Changed

- `README.md`
- `docs/PROJECT_STATUS.md`
- `docs/HANDOFF.md`
- `docs/CHANGELOG.md`
- `docs/DATA_STRATEGY.md`
- `docs/DATA_UNDERSTANDING.md` dan `docs/figures/data-understanding/*.png`

## Files Not Changed

- Dataset raw/processed, notebook, script pipeline, model/artifact, hasil legacy, dependensi, `.gitignore`, dan `app.py`.

## Verified Results

- Raw full data: 513.801 × 44, tahun 2021–2025.
- Sampling legacy: `groupby("collision_year").sample(n=2000, random_state=42)` untuk 2021–2025.
- Classification legacy split: `test_size=0.20`, `random_state=42`, `stratify=y`.
- Clustering legacy: `KMeans`, evaluasi `k=2..6`, final metadata `k=2`.
- Full CSV: 0 duplicate row; 53 missing pada masing-masing empat kolom koordinat; seluruh date/time valid; tidak ada kode tak terpetakan pada kolom yang memiliki mapping lokal.
- Target Serious meningkat secara deskriptif dari 21,06% pada 2021 menjadi 24,81% pada 2025; volume data tertinggi berada pada jam 16–17.

## Unverified Items

- Keberadaan file dataset sample 10K terpisah dan waktu persis sampling pertama kali dilakukan.
- Definisi use case/timing prediksi, split yang diminta dosen, penggunaan fitur geografis/admin, dan data dictionary STATS19 lengkap.
- Arti seluruh kode unresolved dan daftar fitur data-mining yang wajib dinilai masih belum terverifikasi.

## Known Issues

- README dan identitas remote sebelumnya mengacu pada proyek lama/course lama; README utama sudah diselaraskan sebagai Phase 0, tetapi aplikasi dan `README_APP.md` masih legacy dan sengaja tidak diubah.
- Leakage risk: outcome/adjusted severity fields, number of casualties, dan police-attendance harus dikeluarkan/ditinjau sebelum model.
- Pola target-versus-fitur bersifat deskriptif; kategori langka memerlukan kehati-hatian dan tidak boleh dibaca sebagai hubungan kausal.

## Do Not

- Jangan mengubah project lama.
- Jangan membuat dataset turunan/full baru, training, clustering, feature selection final, tuning, PCA, association mining, atau mengubah artefak legacy.
- Jangan force-push atau mengganti remote tanpa instruksi eksplisit.

## Next Required Action

Setelah instruksi eksplisit Phase 3: tetapkan feature contract, code decoding, leakage exclusions, temporal derivations, missing-value handling, dan reproducible preparation pipeline.

## STOP CONDITION

Jangan masuk Phase 3 sebelum mendapat instruksi eksplisit.
