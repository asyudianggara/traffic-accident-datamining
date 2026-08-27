# Operational Validation dan Research Readiness

## 1. Tujuan

Phase 7 memeriksa apakah final candidate Phase 6 dapat digunakan ulang secara deterministik, memiliki kontrak input/output yang jelas, dan dapat dipertanggungjawabkan sebagai artefak penelitian. Tidak ada fitting, tuning, seleksi model, atau penggunaan data 2025.

## 2. Model final

Artifact `models/final_research_model.joblib` berisi pipeline preprocessing dan `RandomForestClassifier` balanced. Model dilatih pada 412.276 baris development 2021–2024. Tahun 2025 tetap final holdout. Jumlah fitur setelah encoding adalah 149.

## 3. Input contract

Input harus berupa tabel dengan tepat 18 kolom berikut. `number_of_vehicles` diperlakukan numerik; 17 kolom lain diperlakukan kategorikal oleh pipeline, termasuk kode numerik yang dibaca sebagai kategori. Nilai resmi dan arti seluruh kode STATS19 yang belum tersedia tidak boleh diarang.

| Fitur | Tipe pipeline | Rentang/nilai yang dapat dinyatakan | Missing dan unknown | Catatan penggunaan |
|---|---|---|---|---|
| `number_of_vehicles` | Numerik | Nilai positif pada audit; batas resmi input belum terdokumentasi | Missing diimputasi median; unknown bukan kategori | Jumlah kendaraan pada collision record |
| `speed_limit` | Kategorikal | Kode speed-limit dataset; codebook resmi belum terdokumentasi | Missing diimputasi modus; unknown diabaikan encoder | Jangan mengartikan kode tanpa codebook |
| `first_road_class` | Kategorikal | Kode kelas jalan; codebook resmi belum terdokumentasi | Imputasi modus; unknown diabaikan encoder | Kondisi jalan yang tersedia pada record |
| `road_type` | Kategorikal | Kode tipe jalan; codebook resmi belum terdokumentasi | Imputasi modus; unknown diabaikan encoder | Kondisi jalan yang tersedia pada record |
| `junction_detail` | Kategorikal | Kode detail junction; codebook resmi belum terdokumentasi | Imputasi modus; unknown diabaikan encoder | Kondisi lokasi collision |
| `junction_control` | Kategorikal | Kode kontrol junction; codebook resmi belum terdokumentasi | Imputasi modus; unknown diabaikan encoder | Kondisi lokasi collision |
| `second_road_class` | Kategorikal | Kode kelas jalan kedua; codebook resmi belum terdokumentasi | Imputasi modus; unknown diabaikan encoder | Kondisi jalan yang tersedia pada record |
| `pedestrian_crossing` | Kategorikal | Kode pedestrian crossing; codebook resmi belum terdokumentasi | Imputasi modus; unknown diabaikan encoder | Kondisi fasilitas crossing |
| `light_conditions` | Kategorikal | Kode kondisi cahaya; codebook resmi belum terdokumentasi | Imputasi modus; unknown diabaikan encoder | Kondisi saat collision |
| `weather_conditions` | Kategorikal | Kode cuaca; codebook resmi belum terdokumentasi | Imputasi modus; unknown diabaikan encoder | Kondisi saat collision |
| `road_surface_conditions` | Kategorikal | Kode permukaan jalan; codebook resmi belum terdokumentasi | Imputasi modus; unknown diabaikan encoder | Kondisi saat collision |
| `special_conditions_at_site` | Kategorikal | Kode kondisi khusus; codebook resmi belum terdokumentasi | Imputasi modus; unknown diabaikan encoder | Kondisi lokasi collision |
| `carriageway_hazards` | Kategorikal | Kode hazard carriageway; codebook resmi belum terdokumentasi | Imputasi modus; unknown diabaikan encoder | Kondisi hazard yang tercatat |
| `urban_or_rural_area` | Kategorikal | Kode urban/rural; codebook resmi belum terdokumentasi | Imputasi modus; unknown diabaikan encoder | Konteks area |
| `trunk_road_flag` | Kategorikal | Kode flag trunk road; codebook resmi belum terdokumentasi | Imputasi modus; unknown diabaikan encoder | Konteks administrasi jalan |
| `day_of_week` | Kategorikal | Kode hari; arti kode resmi belum terdokumentasi | Imputasi modus; unknown diabaikan encoder | Derived dari dataset; jangan menamai kode tanpa codebook |
| `month` | Kategorikal | Nilai derived teramati 1–12 | Imputasi modus; unknown diabaikan encoder | Derived dari `date`, bukan kolom raw asli |
| `hour` | Kategorikal | Nilai derived teramati 0–23 | Imputasi modus; unknown diabaikan encoder | Derived dari `time`, bukan kolom raw asli |

Nilai sentinel coded seperti `-1` dipertahankan sebagai kategori/unknown sesuai keputusan Phase 3. Pipeline tidak memiliki domain-range validator terpisah; karena itu nilai numerik ekstrem tidak boleh dianggap tervalidasi hanya karena prediction berhasil.

Mapping lokal yang dapat diverifikasi dari `data/processed/stats19_maps.json` tersedia untuk `first_road_class`, `road_type`, `junction_detail`, `junction_control`, `light_conditions`, `weather_conditions`, `road_surface_conditions`, `urban_or_rural_area`, dan `day_of_week`, termasuk label `-1` sebagai `Data missing / out of range` pada mapping yang memilikinya. Mapping `collision_severity` juga tersedia untuk output: `1=Fatal`, `2=Serious`, `3=Slight`. Mapping lokal untuk `speed_limit`, `second_road_class`, `pedestrian_crossing`, `special_conditions_at_site`, `carriageway_hazards`, dan `trunk_road_flag` belum tersedia; nilai/kategori resminya berstatus **NOT VERIFIED**. `month` dan `hour` adalah fitur derived dengan rentang observasi 1–12 dan 0–23, bukan codebook kategori eksternal.

## 4. Prediction contract

Alur inference:

`RAW INPUT → VALIDATION SHAPE/TYPE → PREPROCESSING → ENCODING → RANDOM FOREST → CLASS PROBABILITY → FATAL THRESHOLD 0.50 → FINAL CLASS`

Aturan final tidak berubah:

```text
Jika P(Fatal) >= 0.50:
    prediksi = Fatal
Jika tidak:
    prediksi = kelas dengan probabilitas terbesar antara Serious dan Slight
```

Output adalah class `Fatal`, `Serious`, atau `Slight`, serta probability vector dalam urutan estimator `[1, 2, 3]` yang dipetakan melalui artifact menjadi `[Fatal, Serious, Slight]`. Probability adalah skor model terkalibrasi secara internal, bukan probabilitas kausal atau jaminan kejadian individual; threshold tidak mengubah kualitas kalibrasi.

## 5. Threshold policy

Threshold Fatal 0,50 ditetapkan pada validation 2024 dan dibekukan. Threshold meningkatkan Fatal precision/F1 pada holdout 2025 dibanding argmax, tetapi menurunkan Fatal recall. Phase 7 tidak mencari threshold baru.

## 6. Reproducibility

Validator `phase7_operational_validation.py` memuat artifact dari disk, mengambil tiga baris deterministik dari development (`collision_year <= 2024`), menjalankan `predict_proba` dua kali, menerapkan rule threshold, dan menulis `results/phase7_operational_validation.json`. Tidak ada `fit`, `fit_transform`, atau pemilihan ulang model.

Runtime inference berhasil pada environment saat ini. Namun artifact dibuat dengan scikit-learn 1.9.0 sedangkan runtime yang menjalankan validator adalah 1.8.0 dan menghasilkan `InconsistentVersionWarning`. Cross-version compatibility **NOT VERIFIED** dan perlu environment yang dipin sama sebelum deployment.

## 7. Edge-case testing

- Missing numerik/kategorikal memakai `numpy.nan`: **PASS**, imputasi menghasilkan probabilitas.
- Unknown category: **PASS**, `handle_unknown="ignore"` menghasilkan probabilitas.
- Invalid numeric type: **PASS**, pipeline menolak dengan `ValueError`.
- Input tidak lengkap: **PASS**, pipeline menolak dengan `ValueError`.
- Numeric di luar pola umum: **NOT VERIFIED**, karena belum ada domain-range validator terpisah.
- Prediction berulang: **PASS**, class identik dan probability konsisten dalam toleransi numerik `1e-12`.

## 8. Prediction timing dan use case

Interpretasi yang didukung evidence saat ini adalah **post-event severity classification**: model memprediksi `collision_severity` dari kondisi collision yang sudah tersedia pada record. Ini bukan **pre-event accident risk prediction**, karena fitur dan target berasal dari record kecelakaan yang telah terjadi. Tidak ada klaim bahwa model memprediksi apakah kecelakaan akan terjadi sebelum event.

## 9. Acceptance criteria

| Kriteria | Status | Evidence |
|---|---|---|
| Artifact dapat di-load | PASS | Validator berhasil load joblib |
| 18 input feature tersedia | PASS | Contract dan assertion validator |
| Encoded feature count = 149 | PASS | Pipeline `get_feature_names_out()` |
| Preprocessing konsisten | PASS | Pipeline persisted dipakai langsung |
| Prediction dapat dijalankan | PASS | Tiga input development |
| `predict_proba` konsisten | PASS | Repeat inference dan `allclose` |
| Threshold Fatal = 0,50 | PASS | Assertion artifact |
| Repeated prediction identik | PASS | Class output identik |
| Invalid input handling jelas | PASS | `ValueError` untuk type/incomplete |
| 2025 tidak digunakan fit/selection | PASS | Validator hanya development; metadata Phase 6 |
| Raw dataset tidak berubah | PASS | Tidak ada operasi write ke raw; perlu diverifikasi lagi pada Git review |
| Domain-range validation | NOT VERIFIED | Belum tersedia pada pipeline |
| Cross-version sklearn compatibility | NOT VERIFIED | Artifact 1.9.0, runtime 1.8.0 |

Tidak ada acceptance criterion yang dinyatakan FAIL. Dua hal berstatus NOT VERIFIED membatasi klaim deployment readiness.

## 10. Limitations

Model memiliki Fatal precision rendah, sensitif terhadap threshold dan temporal shift, serta tidak memiliki validasi domain-range pada input. Kode kategori belum seluruhnya memiliki codebook resmi yang dibekukan. Probability bukan confidence klinis/kausal. Input baru harus menggunakan representasi `numpy.nan` atau nilai missing yang kompatibel, bukan `pd.NA` untuk kolom numerik pada runtime yang diuji.

## 11. Research readiness

**READY WITH CONDITIONS.** Artifact, preprocessing, class order, input/output contract, threshold, reproducibility test, dan batas prediction timing telah terdokumentasi. Model layak digunakan sebagai final candidate penelitian, dengan catatan versi dependency, codebook, use case, dan domain validation perlu difinalkan.

## 12. Deployment readiness

**NOT READY.** Tidak ada perubahan `app.py` pada Phase 7. Deployment memerlukan environment dependency yang sama, input validation/range policy, codebook resmi, acceptance criteria operasional, dan keputusan use case/prediction timing.
