# Konsolidasi Hasil Final Riset

## Status dan ruang lingkup

Dokumen ini mengonsolidasikan hasil Phase 3 sampai Phase 9.2 untuk pelaporan
riset. Angka diambil dari metadata dan hasil yang sudah tersedia; tidak ada
eksperimen atau evaluasi ulang yang dijalankan pada Phase 9.3.

Model final berstatus **final candidate penelitian**, bukan model production-ready.

## Dataset dan desain evaluasi

- Sumber: `data/raw/dft-road-casualty-statistics-collision-last-5-years.csv`.
- Ukuran: 513.801 baris dan 44 kolom, periode 2021–2025.
- Target: `collision_severity` dengan mapping 1 = Fatal, 2 = Serious, 3 = Slight.
- Fitur classification: 18 fitur, menghasilkan 149 encoded features.
- Training/eksperimen: 2021–2023, 311.349 baris.
- Validation strategi dan threshold: 2024, 100.927 baris.
- Refit development final: 2021–2024, 412.276 baris.
- Final holdout: 2025, 101.525 baris.

Holdout 2025 tidak digunakan untuk fitting, feature selection, threshold tuning,
hyperparameter tuning, atau model selection.

## Hasil classification final

Konfigurasi final adalah Random Forest balanced dengan `n_estimators=100`,
`max_depth=12`, `min_samples_leaf=20`, `max_features="sqrt"`, dan
`random_state=42`. Threshold Fatal adalah 0,50: jika `P(Fatal) >= 0,50`,
hasilnya Fatal; jika tidak, dipilih probabilitas terbesar antara Serious dan
Slight.

Metrik final holdout 2025:

| Metrik | Nilai |
|---|---:|
| Accuracy | 0,542930 |
| Macro Precision | 0,388070 |
| Macro Recall | 0,460542 |
| Macro F1 | 0,378410 |
| Weighted F1 | 0,584129 |
| Fatal Precision | 0,057524 |
| Fatal Recall | 0,329663 |
| Fatal F1 | 0,097955 |

Interpretasi utama: performa antar kelas tidak merata. Weighted F1 lebih tinggi
karena dipengaruhi kelas dominan, sementara metrik Fatal tetap rendah. Threshold
0,50 meningkatkan Fatal precision dan Fatal F1 dibanding argmax pada eksperimen
yang sudah ditetapkan, tetapi menurunkan Fatal recall. Threshold ini merupakan
keputusan trade-off untuk kandidat terbatas, bukan aturan optimal universal.

## Hasil clustering

Clustering menggunakan pipeline terpisah, tanpa target dan tanpa class weighting
atau threshold. Kontraknya adalah 18 fitur dan 108 encoded features dengan
K-Means `k=2`.

Profil cluster menunjukkan perbedaan deskriptif terutama pada konteks
urban/rural dan speed limit. Cluster 0 dan Cluster 1 bukan label severity,
tidak memiliki makna ordinal, dan bukan ukuran tingkat bahaya.

## Validasi aplikasi dan artifact

Artifact classification final yang digunakan aplikasi adalah
`models/final_research_model.joblib`. Evidence Phase 7–8 menunjukkan:

| Pemeriksaan | Status |
|---|---|
| Artifact dapat di-load | PASS |
| Input 18 fitur | PASS |
| Output 149 encoded features | PASS |
| Class order 1/2/3 → Fatal/Serious/Slight | PASS |
| Threshold Fatal 0,50 | PASS |
| Prediction dan probabilitas konsisten | PASS |
| Unknown category handling | PASS |
| Incomplete/invalid input rejection | PASS |
| Holdout 2025 tidak digunakan | PASS |
| Domain-range validation penuh | NOT VERIFIED |
| Cross-version scikit-learn compatibility | NOT VERIFIED |

Aplikasi berjalan inference-only dan tidak melakukan training atau tuning.

## Pemisahan legacy dan final

Artifact serta hasil 10K/18→105 dan clustering 18→108 dipertahankan sebagai
baseline historis. Hasil tersebut tidak boleh dikutip sebagai metrik final
research. Sumber final classification adalah `results/final_model_metadata.json`,
`results/phase5_2_final_holdout.csv`, dan `docs/FINAL_MODEL.md`.

## Batasan dan klaim yang diperbolehkan

Hasil berlaku pada dataset STATS19 Inggris dan periode yang diuji. Model
merupakan post-event severity classification, bukan prediksi apakah kecelakaan
akan terjadi. Hasil tidak membuktikan kausalitas, tidak menjamin performa pada
tahun/wilayah lain, dan tidak boleh digunakan sebagai keputusan keselamatan
otomatis.

Keterbatasan penting lainnya adalah minoritas Fatal, kemungkinan temporal shift,
codebook kategori yang belum seluruhnya dibekukan, belum adanya domain-range
validator penuh, serta kompatibilitas dependency lintas versi yang belum
terverifikasi penuh. Detail interpretasi tersedia di
`docs/RESEARCH_INTERPRETATION.md`.

## Kesimpulan akhir

Project menghasilkan pipeline classification final candidate yang reproducible,
pipeline clustering deskriptif, dan integrasi aplikasi inference-only. Bukti
yang tersedia cukup untuk pelaporan hasil eksperimen dengan batasan yang jelas.
Project belum mendukung klaim production readiness atau penggunaan sebagai
sistem keputusan keselamatan.
