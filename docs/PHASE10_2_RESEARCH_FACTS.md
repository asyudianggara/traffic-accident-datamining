# Phase 10.2 — Research Facts Synchronization

Dokumen ini menjadi factsheet internal sebelum penulisan laporan penelitian.
Isinya hanya merangkum fakta, hasil, batasan, dan sumber yang sudah tersedia di
repository. Dokumen ini tidak membuat eksperimen baru dan tidak menggantikan
artifact atau metadata final.

## A. Identitas Penelitian

| Item | Nilai | Sumber File | Status |
|---|---|---|---|
| Project | Traffic Accident Analysis / Tugas 2 Penambangan Data | `README.md`, `docs/PROJECT_STATUS.md` | VERIFIED |
| Dataset | STATS19 road collision dataset | `docs/DATA_STRATEGY.md`, `docs/DATA_PREPARATION.md` | VERIFIED |
| Branch | `main` | Git checkpoint | VERIFIED |
| Remote | `origin/main` | Git checkpoint | VERIFIED |
| Pendekatan | Classification severity dan clustering deskriptif | `docs/FINAL_REPORT_BLUEPRINT.md`, `docs/RESEARCH_INTERPRETATION.md` | VERIFIED |

## B. Dataset

| FACT | VALUE | SOURCE FILE | STATUS |
|---|---|---|---|
| Raw dataset | 513.801 baris × 44 kolom | `docs/DATA_STRATEGY.md`, `docs/DATA_UNDERSTANDING.md` | VERIFIED |
| Periode | 2021–2025 | `docs/DATA_STRATEGY.md`, `docs/DATA_UNDERSTANDING.md` | VERIFIED |
| Tahun 2021 | 101.087 record | `docs/PROJECT_STATUS.md` | VERIFIED |
| Tahun 2022 | 106.004 record | `docs/PROJECT_STATUS.md` | VERIFIED |
| Tahun 2023 | 104.258 record | `docs/PROJECT_STATUS.md` | VERIFIED |
| Tahun 2024 | 100.927 record | `docs/PROJECT_STATUS.md` | VERIFIED |
| Tahun 2025 | 101.525 record | `docs/PROJECT_STATUS.md` | VERIFIED |
| Dataset utama | Seluruh raw dataset yang tersedia | `docs/DATA_STRATEGY.md`, `docs/DATA_PREPARATION.md` | VERIFIED |
| Dataset legacy 10K | Bukan dataset utama; digunakan untuk baseline historis dan analisis clustering legacy C3–C4 | `README.md`, `docs/PROJECT_FACT_SHEET.md` | VERIFIED |

## C. Temporal Split

| FACT | VALUE | SOURCE FILE | STATUS |
|---|---|---|---|
| Training/model development | 2021–2023, 311.349 record | `docs/FINAL_MODEL.md`, `docs/FINAL_RESULTS_CONSOLIDATION.md` | VERIFIED |
| Validation | 2024, 100.927 record | `docs/FINAL_MODEL.md`, `docs/MODELING_PHASE5.md` | VERIFIED |
| Development/refit | 2021–2024, 412.276 record | `docs/FINAL_MODEL.md`, `docs/DATA_PREPARATION.md` | VERIFIED |
| Final holdout | 2025, 101.525 record | `docs/FINAL_MODEL.md`, `docs/FINAL_RESULTS_CONSOLIDATION.md` | VERIFIED |
| Proteksi holdout | 2025 tidak digunakan untuk training, feature selection, tuning, threshold selection, atau model selection | `docs/FINAL_MODEL.md`, `docs/OPERATIONAL_VALIDATION.md` | VERIFIED |

Strategi temporal tidak boleh diganti menjadi random split. Tahun 2025 hanya
digunakan sebagai final unseen holdout untuk evaluasi generalisasi temporal.

## D. Target

| FACT | VALUE | SOURCE FILE | STATUS |
|---|---|---|---|
| Target | `collision_severity` | `docs/FINAL_MODEL.md` | VERIFIED |
| Kode 1 | Fatal | `docs/FINAL_MODEL.md`, `docs/PROJECT_STATUS.md` | VERIFIED |
| Kode 2 | Serious | `docs/FINAL_MODEL.md`, `docs/PROJECT_STATUS.md` | VERIFIED |
| Kode 3 | Slight | `docs/FINAL_MODEL.md`, `docs/PROJECT_STATUS.md` | VERIFIED |
| Distribusi Fatal | 7.553 record | `docs/PROJECT_STATUS.md` | VERIFIED |
| Distribusi Serious | 116.813 record | `docs/PROJECT_STATUS.md` | VERIFIED |
| Distribusi Slight | 389.435 record | `docs/PROJECT_STATUS.md` | VERIFIED |
| Imbalance | Fatal adalah kelas minoritas | `docs/DATA_UNDERSTANDING.md`, `docs/RESEARCH_INTERPRETATION.md` | VERIFIED |

## E. Delapan Belas Fitur Final

### Numerik

1. `number_of_vehicles`

### Kategorikal atau fitur turunan waktu

1. `speed_limit`
2. `first_road_class`
3. `road_type`
4. `junction_detail`
5. `junction_control`
6. `second_road_class`
7. `pedestrian_crossing`
8. `light_conditions`
9. `weather_conditions`
10. `road_surface_conditions`
11. `special_conditions_at_site`
12. `carriageway_hazards`
13. `urban_or_rural_area`
14. `trunk_road_flag`
15. `day_of_week`
16. `month`
17. `hour`

| FACT | VALUE | SOURCE FILE | STATUS |
|---|---|---|---|
| Fitur original | 18 | `docs/FINAL_MODEL.md`, `results/final_model_metadata.json` | VERIFIED |
| Fitur encoded | 149 | `docs/FINAL_MODEL.md`, `results/final_model_metadata.json` | VERIFIED |
| Tidak digunakan | Target, identifier, casualty/outcome-derived fields, dan leakage fields | `docs/FINAL_MODEL.md`, `docs/DATA_PREPARATION.md` | VERIFIED |

## F. Preprocessing

| FACT | VALUE | SOURCE FILE | STATUS |
|---|---|---|---|
| Fitting preprocessing | Train-only/development-only | `docs/DATA_PREPARATION.md`, `docs/FINAL_MODEL.md` | VERIFIED |
| Numerik | Imputation dan scaling sesuai pipeline final | `docs/DATA_PREPARATION.md`, `docs/FINAL_MODEL.md` | VERIFIED |
| Kategorikal | Imputation dan sparse One-Hot Encoding | `docs/DATA_PREPARATION.md`, `docs/FINAL_MODEL.md` | VERIFIED |
| Kategori baru | `handle_unknown="ignore"` | `docs/DATA_PREPARATION.md`, `docs/OPERATIONAL_VALIDATION.md` | VERIFIED |
| Sentinel `-1` | Dipertahankan sesuai strategi preprocessing; tidak diganti dengan asumsi | `docs/DATA_PREPARATION.md` | VERIFIED |

## G. Feature Selection

Feature selection tidak menggunakan tahun 2025. Evidence yang sudah tersedia:

- Mutual Information pada development 2021–2024.
- Decision Tree feature importance.
- Redundancy analysis.
- Stability analysis.
- Leakage screening terhadap target, identifier, dan outcome-derived fields.

Recommended provisional feature set yang digunakan untuk final research terdiri
atas 18 fitur pada Bagian E. Predictive association tidak boleh ditulis sebagai
hubungan sebab-akibat.

Sumber: `docs/FEATURE_SELECTION.md`, `docs/DATA_PREPARATION.md`.

## H. Baseline Models

Model baseline yang terdokumentasi:

- Logistic Regression.
- Decision Tree.
- Random Forest.

Random Forest menjadi provisional best baseline berdasarkan kombinasi Macro F1,
Macro Recall, Weighted F1, dan pertimbangan kelas Fatal. Hasil baseline lama 10K
atau evaluator lama 21 fitur hanya menjadi konteks historis dan bukan sumber
metrik final research.

Sumber: `docs/MODELING_PHASE5.md`, `docs/MODELING_PHASE5A.md`,
`docs/MODELING_PHASE5B1.md`.

## I. Imbalance Experiment

Phase 5.1 membandingkan strategi tanpa weighting dan balanced weighting pada
validation 2024. SMOTE, synthetic data, over-sampling, dan under-sampling tidak
digunakan.

Random Forest dengan `class_weight="balanced"` dipilih secara provisional untuk
dilanjutkan ke evaluasi threshold dan final candidate.

Sumber: `docs/MODELING_PHASE5.md`, `docs/FINAL_MODEL.md`.

## J. Threshold Experiment

Threshold Fatal ditetapkan sebesar 0,50 melalui analisis pada validation 2024.

Aturan prediksi:

```text
Jika P(Fatal) >= 0,50:
    prediksi Fatal
Jika tidak:
    pilih probabilitas terbesar antara Serious dan Slight
```

Threshold tersebut merupakan keputusan trade-off pada kandidat terbatas. Hasil
yang terdokumentasi menunjukkan Fatal precision dan Fatal F1 meningkat,
sedangkan Fatal recall menurun. Threshold 0,50 bukan akurasi Fatal dan bukan
aturan optimal universal.

Sumber: `docs/FINAL_MODEL.md`, `docs/MODELING_PHASE5.md`,
`docs/RESEARCH_INTERPRETATION.md`.

## K. Final Model

| FACT | VALUE | SOURCE FILE | STATUS |
|---|---|---|---|
| Artifact | `models/final_research_model.joblib` | `docs/FINAL_MODEL.md`, `docs/APPLICATION_INTEGRATION.md` | VERIFIED |
| Model | Random Forest | `docs/FINAL_MODEL.md` | VERIFIED |
| `class_weight` | `balanced` | `docs/FINAL_MODEL.md` | VERIFIED |
| `n_estimators` | 100 | `docs/FINAL_MODEL.md` | VERIFIED |
| `max_depth` | 12 | `docs/FINAL_MODEL.md` | VERIFIED |
| `min_samples_leaf` | 20 | `docs/FINAL_MODEL.md` | VERIFIED |
| `max_features` | `sqrt` | `docs/FINAL_MODEL.md` | VERIFIED |
| `random_state` | 42 | `docs/FINAL_MODEL.md` | VERIFIED |
| Input contract | 18 fitur | `results/final_model_metadata.json` | VERIFIED |
| Encoded contract | 149 fitur | `results/final_model_metadata.json` | VERIFIED |
| Threshold | Fatal 0,50 | `results/final_model_metadata.json`, `docs/FINAL_MODEL.md` | VERIFIED |

## L. Final 2025 Evaluation

| Metrik | Nilai | Sumber |
|---|---:|---|
| Accuracy | 0,542930 | `results/final_model_metadata.json`, `results/phase5_2_final_holdout.csv` |
| Macro Precision | 0,388070 | Sumber yang sama |
| Macro Recall | 0,460542 | Sumber yang sama |
| Macro F1 | 0,378410 | Sumber yang sama |
| Weighted F1 | 0,584129 | Sumber yang sama |
| Fatal Precision | 0,057524 | Sumber yang sama |
| Fatal Recall | 0,329663 | Sumber yang sama |
| Fatal F1 | 0,097955 | Sumber yang sama |

Interpretasi wajib: model menghasilkan accuracy keseluruhan 54,29% pada holdout
2025, sedangkan performa kelas Fatal memiliki precision 5,75%, recall 32,97%,
dan F1-score 9,80%. Jangan menulis bahwa model memiliki akurasi 54% untuk
memprediksi kecelakaan Fatal.

## M. Clustering Legacy

| FACT | VALUE | SOURCE FILE | STATUS |
|---|---|---|---|
| Konteks | Analisis clustering legacy C3–C4 | `README.md`, `docs/PROJECT_FACT_SHEET.md` | VERIFIED |
| Record | 10.000 | `models/final_clustering_metadata.json`, `docs/FINAL_RESULTS_CONSOLIDATION.md` | VERIFIED |
| Fitur original | 18 | `models/final_clustering_metadata.json` | VERIFIED |
| Fitur encoded | 108 | `models/final_clustering_metadata.json` | VERIFIED |
| Algoritma | K-Means | `models/final_clustering_metadata.json` | VERIFIED |
| Jumlah cluster | `k=2` | `models/final_clustering_metadata.json` | VERIFIED |
| PCA | Hanya untuk visualisasi | `docs/FINAL_RESULTS_CONSOLIDATION.md`, `docs/PROJECT_FACT_SHEET.md` | VERIFIED |
| Status | Eksploratif/deskriptif, bukan severity prediction | `docs/RESEARCH_INTERPRETATION.md` | VERIFIED |

10.000 record tidak boleh disebut sebagai dataset utama penelitian final dan
clustering tidak boleh diberi label Fatal, Serious, atau Slight.

## N. Application

| FACT | VALUE | SOURCE FILE | STATUS |
|---|---|---|---|
| Framework | Streamlit | `docs/APPLICATION_INTEGRATION.md` | VERIFIED |
| Mode | Inference-only | `docs/APPLICATION_INTEGRATION.md`, `docs/OPERATIONAL_VALIDATION.md` | VERIFIED |
| Classification artifact | `models/final_research_model.joblib` | `docs/APPLICATION_INTEGRATION.md` | VERIFIED |
| Input | 18 fitur | `docs/APPLICATION_INTEGRATION.md` | VERIFIED |
| Encoded output | 149 fitur | `docs/APPLICATION_INTEGRATION.md` | VERIFIED |
| Output | Kelas dan probabilitas Fatal/Serious/Slight | `docs/APPLICATION_INTEGRATION.md` | VERIFIED |
| Startup training | Tidak dilakukan | `docs/APPLICATION_INTEGRATION.md` | VERIFIED |
| Raw CSV saat inference | Tidak dibaca | `docs/APPLICATION_INTEGRATION.md` | VERIFIED |
| Clustering pada aplikasi | Tetap legacy C3–C4 | `README.md`, `docs/APPLICATION_INTEGRATION.md` | VERIFIED |
| Dependency | `scikit-learn==1.9.0` | `requirements.txt`, `.venv` checkpoint | VERIFIED |

## O. Limitations

Keterbatasan yang boleh ditulis:

- Dataset hanya mencakup STATS19 Inggris periode 2021–2025.
- Holdout 2025 hanya mewakili satu periode temporal.
- Kelas Fatal merupakan kelas minoritas dengan performa rendah.
- Generalisasi ke wilayah atau tahun lain belum terbukti.
- Codebook resmi dan sebagian definisi kode kategori perlu dibekukan secara eksplisit.
- Domain-range validation penuh belum tersedia.
- Use case dan waktu prediksi formal masih perlu dikonfirmasi.
- Aplikasi belum menjadi bukti deployment operasional.
- Model bukan production-ready dan bukan sistem keputusan keselamatan.
- Hasil classification tidak membuktikan hubungan kausal.

Sumber: `docs/RESEARCH_INTERPRETATION.md`, `docs/FINAL_MODEL.md`,
`docs/OPERATIONAL_VALIDATION.md`.

## P. Klaim yang Diperbolehkan dan Dilarang

### Diperbolehkan

- Model dievaluasi pada final holdout 2025.
- Model mengklasifikasikan severity pada collision yang sudah tercatat.
- Performa antar kelas tidak merata.
- Threshold 0,50 menghasilkan trade-off precision dan recall pada kelas Fatal.
- Clustering legacy C3–C4 memberikan segmentasi karakteristik secara deskriptif.
- Aplikasi berhasil mengintegrasikan artifact final secara inference-only.

### Dilarang

- Model memprediksi apakah kecelakaan akan terjadi.
- Model memprediksi kecelakaan tahun 2026.
- Model production-ready.
- Model membuktikan penyebab atau hubungan kausal.
- Clustering merupakan prediksi severity atau tingkat bahaya.
- 10.000 record adalah dataset final research.
- Legacy classification 18 → 105 adalah model final.
- Tahun 2025 digunakan untuk training, tuning, atau selection.
- Threshold 0,50 adalah akurasi Fatal atau optimum universal.

## Q. Traceability dan Conflicts

### Traceability utama

| Area laporan | Sumber utama |
|---|---|
| Dataset dan strategi | `docs/DATA_STRATEGY.md`, `docs/DATA_UNDERSTANDING.md` |
| Preparation | `docs/DATA_PREPARATION.md` |
| Feature selection | `docs/FEATURE_SELECTION.md` |
| Modeling dan eksperimen | `docs/MODELING_PHASE5.md`, `docs/MODELING_PHASE5A.md`, `docs/MODELING_PHASE5B1.md` |
| Final model | `docs/FINAL_MODEL.md`, `results/final_model_metadata.json` |
| Final metrics | `results/phase5_2_final_holdout.csv`, `results/final_model_metadata.json` |
| Clustering | `models/final_clustering_metadata.json`, `results/clustering_k_evaluation.csv`, `docs/FINAL_RESULTS_CONSOLIDATION.md` |
| Application | `docs/APPLICATION_INTEGRATION.md`, `docs/OPERATIONAL_VALIDATION.md` |
| Interpretasi | `docs/RESEARCH_INTERPRETATION.md` |

### Konflik atau ketidaksinkronan yang ditemukan

| ID | Temuan | Dampak | Tindakan pada Phase 10.2 |
|---|---|---|---|
| KS-01 | `docs/PROJECT_STATUS.md` dan `docs/HANDOFF.md` masih menyebut current phase 8.4, sementara pekerjaan sekarang adalah Phase 10.2. `PROJECT_STATUS.md` juga mencantumkan subphase/next action Phase 10.1. | Membingungkan navigasi project, tetapi tidak mengubah fakta riset. | Dicatat; tidak diubah pada sinkronisasi ini. |
| KS-02 | Blueprint menyebut basis hasil sampai Phase 9.4, sedangkan chronology Git terbaru memuat checkpoint Phase 8.4 setelah dokumentasi Phase 10.1. | Urutan label fase tidak sepenuhnya linear. | Dicatat sebagai isu metadata; isi fakta final tetap memakai sumber final/artifact. |
| KS-03 | Beberapa dokumen lama menyebut “legacy 10K baseline” secara umum, sedangkan dokumentasi terbaru memberi label lebih spesifik “clustering legacy C3–C4”. | Terminologi dapat membutuhkan klarifikasi saat laporan ditulis. | Factsheet memakai label spesifik dan tidak mengubah dokumen lama. |
| KS-04 | `FINAL_RESULTS_CONSOLIDATION.md` menyebut cross-version scikit-learn belum terverifikasi penuh, sementara `.venv` dan requirements kini sama-sama 1.9.0. | Tidak kontradiktif: runtime/artifact alignment terverifikasi, portability lintas versi belum. | Ditulis sebagai dua status berbeda. |

Tidak ditemukan konflik pada ukuran dataset, temporal split, target, final feature
contract, final metrics, proteksi 2025, atau pemisahan final research versus
legacy artifact.

## R. Status Sinkronisasi

- Fakta penelitian final: **SYNCHRONIZED**.
- Artifact/model/dataset/results ML: **tidak diubah**.
- Metodologi temporal: **tidak diubah**.
- Konflik dokumentasi: **minor metadata/terminology conflicts dicatat**.
- File source code dan aplikasi: **tidak diubah**.
- File baru pada Phase 10.2: `docs/PHASE10_2_RESEARCH_FACTS.md`.

Status: **COMPLETED WITH DOCUMENTATION STATUS NOTES**.

Factsheet ini siap digunakan sebagai sumber internal penulisan laporan setelah
status metadata fase ditinjau. Jangan menulis angka baru, mengganti hasil final,
atau mengubah metodologi berdasarkan dokumen ini.
