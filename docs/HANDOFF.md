# HANDOFF

## Current Phase

PHASE 0 – AUDIT & PROJECT GOVERNANCE (COMPLETED)

## Last Completed

- Audit read-only terhadap Git, struktur, data, pipeline, artefak, hasil, dan entry point Streamlit.
- Dokumentasi governance Phase 0 dibuat pada 2026-08-27.

## Current State

- Raw STATS19 tersedia lokal di `data/raw/dft-road-casualty-statistics-collision-last-5-years.csv`: 513.801 baris, 44 kolom, periode 2021–2025. File di-ignore Git.
- Baseline legacy adalah 10.000 baris (2.000/tahun, `random_state=42`). Tidak ada file sample terpisah yang dapat diverifikasi.
- Pipeline legacy memakai `collision_severity`, Random Forest 18→105 fitur, serta K-Means 18→108 fitur. Hasilnya bukan hasil full dataset Tugas 2.
- Aplikasi `app.py` Streamlit memuat artefak legacy; tidak diubah. Uji startup Phase 0 pada port lokal 8502 mengembalikan HTTP 200, lalu proses dihentikan.
- Branch aktif: `main`. Remote `origin` terverifikasi menuju `https://github.com/asyudianggara/traffic-accident-datamining.git` untuk fetch dan push. Checkpoint Phase 0 `3a4f9b1` berhasil dipush ke `origin/main`.

## Files Changed

- `README.md`
- `docs/PROJECT_STATUS.md`
- `docs/HANDOFF.md`
- `docs/CHANGELOG.md`

## Files Not Changed

- Dataset raw/processed, notebook, script pipeline, model/artifact, hasil legacy, dependensi, `.gitignore`, dan `app.py`.

## Verified Results

- Raw full data: 513.801 × 44, tahun 2021–2025.
- Sampling legacy: `groupby("collision_year").sample(n=2000, random_state=42)` untuk 2021–2025.
- Classification legacy split: `test_size=0.20`, `random_state=42`, `stratify=y`.
- Clustering legacy: `KMeans`, evaluasi `k=2..6`, final metadata `k=2`.

## Unverified Items

- Keberadaan file dataset sample 10K terpisah.
- Waktu persis sampling pertama kali dilakukan.
- Tidak ada item startup aplikasi yang belum diverifikasi pada Phase 0; interaksi semua halaman tidak diuji.

## Known Issues

- README dan identitas remote sebelumnya mengacu pada proyek lama/course lama; README utama sudah diselaraskan sebagai Phase 0, tetapi aplikasi dan `README_APP.md` masih legacy dan sengaja tidak diubah.

## Do Not

- Jangan mengubah project lama.
- Jangan membuat dataset turunan/full baru, training, clustering, feature selection, tuning, atau mengubah artefak legacy.
- Jangan force-push atau mengganti remote tanpa instruksi eksplisit.

## Next Required Action

Setelah instruksi eksplisit Phase 1: tetapkan strategi penggunaan seluruh baris dataset, validasi record/target/fitur, split, serta strategi preprocessing. Jangan mulai eksekusi modeling pada tahap tersebut tanpa scope berikutnya.

## STOP CONDITION

Jangan masuk Phase 1 sebelum mendapat instruksi eksplisit.
