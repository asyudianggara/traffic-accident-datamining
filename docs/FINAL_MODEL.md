# Final Model Selection dan Evaluation

## Status keputusan

Phase 6 memilih **FINAL CANDIDATE MODEL**, bukan model production-ready. Use case, waktu prediksi, codebook resmi, kebijakan geografis, dan aturan split final masih perlu dikonfirmasi.

## Sumber data dan target

Sumber adalah `data/raw/dft-road-casualty-statistics-collision-last-5-years.csv` (513.801 baris, 44 kolom, 2021–2025). Target adalah `collision_severity` dengan kelas Fatal, Serious, dan Slight.

Model dilatih pada development 2021–2024 (412.276 baris). Tahun 2025 (101.525 baris) adalah final temporal holdout. Holdout tidak digunakan untuk fit atau seleksi baru pada Phase 6; metriknya diambil dari evaluasi Phase 5.2 yang telah dibekukan.

## Kontrak fitur dan leakage

Delapan belas fitur: `number_of_vehicles`, `speed_limit`, `first_road_class`, `road_type`, `junction_detail`, `junction_control`, `second_road_class`, `pedestrian_crossing`, `light_conditions`, `weather_conditions`, `road_surface_conditions`, `special_conditions_at_site`, `carriageway_hazards`, `urban_or_rural_area`, `trunk_road_flag`, `day_of_week`, `month`, dan `hour`.

`collision_index` serta identifier administratif dikeluarkan. Target, casualty/severity outcome, adjusted severity, number of casualties, police attendance, dan informasi post-event dikeluarkan karena berpotensi membocorkan outcome. Fitur geografis tidak dimasukkan ke candidate 18 karena kebijakan geografis dan missingness belum difinalkan. Exclusion didasarkan pada peran data dan waktu ketersediaan, bukan sekadar predictive power.

## Kandidat dan keputusan

Kandidat: Logistic baseline, Decision Tree baseline, Random Forest baseline, Random Forest balanced, serta Random Forest balanced dengan threshold Fatal 0,50. Kriteria: Macro F1, Macro Recall, Fatal F1/Recall/Precision, Weighted F1, interpretability, compute, reproducibility, dan tujuan riset.

| Checkpoint | Konfigurasi | Macro F1 | Macro Recall | Fatal F1 | Fatal Recall | Fatal Precision | Weighted F1 |
|---|---|---:|---:|---:|---:|---:|---:|
| Phase 5 baseline | RF balanced + argmax | 0,338636 | 0,488989 | 0,068577 | 0,607020 | 0,036341 | 0,544655 |
| Phase 5.1 | RF balanced + argmax | 0,340556 | 0,489751 | 0,069784 | 0,607020 | 0,037020 | 0,550559 |
| Phase 5.2 / final candidate | RF balanced + Fatal threshold 0,50 | **0,378410** | 0,460542 | **0,097955** | 0,329663 | **0,057524** | **0,584129** |

Final candidate: `RandomForestClassifier(n_estimators=100, max_depth=12, min_samples_leaf=20, max_features="sqrt", class_weight="balanced", random_state=42)` dengan preprocessing Phase 3. Jika `P(Fatal) >= 0,50`, prediksi Fatal; selain itu pilih probabilitas terbesar antara Serious dan Slight. Threshold dipilih memakai validation 2024 karena menghasilkan Macro F1 dan Fatal F1 tertinggi pada kandidat terbatas.

## Evaluasi final holdout 2025

Metrik berikut berasal dari `results/phase5_2_final_holdout.csv` dan tidak dihitung ulang pada Phase 6:

- Accuracy: 0,542930
- Macro Precision: 0,388070
- Macro Recall: 0,460542
- Macro F1: 0,378410
- Weighted F1: 0,584129
- Fatal Precision: 0,057524
- Fatal Recall: 0,329663
- Fatal F1: 0,097955

Trade-off utama: threshold menaikkan Fatal precision dan Fatal F1 dibanding argmax, tetapi menurunkan Fatal recall dari 0,607020 menjadi 0,329663. Precision Fatal tetap rendah; model tidak boleh dipakai sebagai sistem keputusan keselamatan tanpa validasi operasional tambahan.

## Preparation dan reproducibility

Pipeline memakai median imputation untuk `number_of_vehicles`, most-frequent imputation untuk 17 fitur kategorikal, dan sparse `OneHotEncoder(handle_unknown="ignore")`. Parameter dipelajari dari development data saja. Kategori baru ditangani oleh encoder; sentinel coded values dipertahankan sesuai aturan Phase 3, bukan diganti diam-diam. IQR flags tidak dihapus sebagai outlier.

Jalankan `python finalize_research_model.py` untuk mereproduksi artifact. Pipeline plus threshold berada di `models/final_research_model.joblib`; metadata dan perbandingan di `results/final_model_metadata.json` dan `results/final_model_comparison.csv`. `random_state=42` digunakan. Validasi Phase 6 lulus: script dapat dikompilasi, 149 encoded features konsisten, raw CSV tidak berubah, holdout tidak masuk fit/seleksi baru, dan pembanding konsisten dengan hasil Phase 5.2.

## Classification dan clustering

Classification memakai target dan pipeline di atas. Clustering memerlukan pipeline terpisah tanpa target dan tanpa class weighting/threshold; artefak clustering legacy tidak diubah dan clustering baru bukan bagian Phase 6.

## Keterbatasan dan keputusan belum selesai

Kelas tetap tidak seimbang, temporal shift mungkin ada, dan fitur kategorikal menghasilkan representasi sparse. Metrik adalah predictive association, bukan kausalitas. Sebelum production atau integrasi aplikasi perlu konfirmasi use case/timing, versi codebook, kebijakan geografis, split yang disetujui, serta kriteria operasional Fatal recall/precision.
