# Integrasi Aplikasi dan Operational Prediction

## Model yang digunakan

Halaman classification pada `app.py` memuat `models/final_research_model.joblib`. Artifact berisi pipeline preprocessing dan Random Forest final candidate Phase 6. Aplikasi tidak melakukan fit, retraining, tuning, atau feature selection saat startup maupun inference.

Ringkasan UI dan Dashboard Dataset membedakan dataset raw penelitian (513.801
baris × 44 kolom, 2021–2025) dari analisis clustering legacy C3–C4 yang
menggunakan 10.000 record. Dashboard legacy tidak menjadi sumber metrik
classification final.

## Kontrak tampilan dataset

Dashboard menampilkan hierarki data penelitian berikut:

- Raw dataset: 513.801 record, 44 kolom, periode 2021–2025.
- Development: 412.276 record pada 2021–2024.
- Training: 311.349 record pada 2021–2023.
- Validation: 100.927 record pada 2024.
- Final holdout: 101.525 record pada 2025.

Training digunakan untuk pembelajaran; validation untuk pemilihan strategi,
model, dan threshold; setelah keputusan final model di-refit pada development.
Tahun 2025 dipertahankan sebagai final holdout dan tidak digunakan untuk
fitting, tuning, feature selection, threshold search, atau model selection.

Untuk mengurangi loading yang tidak diperlukan, halaman Beranda, Dashboard
Dataset, Tentang Data, dan Panduan Penggunaan tidak memuat joblib model.
Artifact dimuat melalui cache hanya ketika halaman Prediksi Severity, Analisis
Cluster, Kamus Fitur, atau Tentang Model membutuhkannya. Aplikasi tetap tidak
membaca raw CSV untuk inference dan tidak melakukan training saat startup.

Section `Hasil Clustering — Analisis Legacy C3–C4` memisahkan hasil C3–C4
secara visual dan naratif. Angka 10.000 hanya merujuk pada 2.000 record per
tahun untuk clustering legacy, bukan jumlah dataset penelitian atau data
classification.

- Input: 18 fitur
- Encoded output: 149 fitur
- Class order internal: `[1, 2, 3]`
- Mapping: `1=Fatal`, `2=Serious`, `3=Slight`
- Fatal threshold: `0.50`
- Rule: jika `P(Fatal) >= 0.50`, hasil Fatal; selain itu pilih probabilitas terbesar antara Serious dan Slight.

## Input dan prediction flow

Form meminta tepat 18 fitur final: `number_of_vehicles`, `speed_limit`, `first_road_class`, `road_type`, `junction_detail`, `junction_control`, `second_road_class`, `pedestrian_crossing`, `light_conditions`, `weather_conditions`, `road_surface_conditions`, `special_conditions_at_site`, `carriageway_hazards`, `urban_or_rural_area`, `trunk_road_flag`, `day_of_week`, `month`, dan `hour`.

Form tidak meminta target, casualty fields, outcome-derived fields, atau identifier. Nilai kategorikal dikonversi ke string sebelum masuk pipeline final. Unknown category mengikuti `handle_unknown="ignore"`; missing yang kompatibel mengikuti imputasi artifact. Input numeric tidak valid atau input tidak lengkap ditolak oleh pipeline.

Alur: `INPUT FORM → VALIDASI BENTUK/TIPE → PREPROCESSING → 149 ENCODED FEATURES → RANDOM FOREST → PROBABILITAS MODEL → THRESHOLD FATAL 0,50 → HASIL KELAS`.

UI menampilkan class, probabilitas prediksi model untuk Fatal/Serious/Slight, threshold Fatal, dan penjelasan bahwa probabilitas bukan kepastian. Interpretasi model adalah post-event severity classification, bukan pre-event accident risk prediction.

## Dependency dan validasi

`requirements.txt` menetapkan `scikit-learn==1.9.0`, sesuai versi saat artifact dibuat. Jalankan aplikasi dari root:

```bat
.venv\Scripts\python.exe -m streamlit run app.py
```

Runtime 1.8.0 sebelumnya masih dapat melakukan inference tetapi menampilkan `InconsistentVersionWarning`; compatibility lintas versi belum diverifikasi. Environment deployment harus memakai versi 1.9.0.

- `phase8_application_consistency.py`: PASS; prediction aplikasi dan pipeline langsung sama pada sample development deterministik, termasuk probabilitas dalam toleransi `1e-12`.
- `phase8_streamlit_smoke_test.py`: PASS; startup, halaman classification, 18 input widget, submit prediction, probability output, dan threshold output berhasil.
- `phase8_2_ui_consistency.py`: PASS; kontrak angka/label dataset, konteks 10.000, dan render seluruh 8 halaman diperiksa.
- Compile `app.py` dan ketiga test script: PASS.
- Tahun 2025 tidak dipakai untuk fitting atau pemilihan model baru.

## Batasan

Dashboard dan clustering tetap menggunakan artefak legacy masing-masing. Aplikasi belum memiliki domain-range validator khusus, codebook lengkap belum terverifikasi, dan model tidak production-ready. Raw CSV tidak diperlukan untuk inference classification; aplikasi hanya memuat artifact dan metadata/mapping yang diperlukan.
