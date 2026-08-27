# Integrasi Aplikasi dan Operational Prediction

## Model yang digunakan

Halaman classification pada `app.py` memuat `models/final_research_model.joblib`. Artifact berisi pipeline preprocessing dan Random Forest final candidate Phase 6. Aplikasi tidak melakukan fit, retraining, tuning, atau feature selection saat startup maupun inference.

Ringkasan UI membedakan dataset final research (513.801 baris, 2021–2025,
development 2021–2024, holdout 2025) dari dashboard clustering legacy 10.000
record. Dashboard legacy tidak menjadi sumber metrik classification final.

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
- Compile `app.py` dan kedua test script: PASS.
- Tahun 2025 tidak dipakai untuk fitting atau pemilihan model baru.

## Batasan

Dashboard dan clustering tetap menggunakan artefak legacy masing-masing. Aplikasi belum memiliki domain-range validator khusus, codebook lengkap belum terverifikasi, dan model tidak production-ready. Raw CSV tidak diperlukan untuk inference classification; aplikasi hanya memuat artifact dan metadata/mapping yang diperlukan.
