# Blueprint Laporan Final

## Tujuan

Blueprint ini menjadi kerangka penyusunan laporan akademik final berdasarkan
hasil yang telah dikunci sampai Phase 9.4. Blueprint bukan hasil eksperimen baru
dan tidak mengubah dataset, model, artifact, results, atau aplikasi.

## Struktur laporan yang disarankan

### 1. Halaman judul

Cantumkan judul penelitian, nama Asyudi Anggara, NIM F552630019, institusi,
mata kuliah, dan tahun penyusunan.

### 2. Abstrak

Ringkas masalah, sumber data STATS19, pendekatan classification dan clustering,
hasil utama, serta keterbatasan. Jangan menyebut model sebagai production-ready
atau sistem prediksi kecelakaan sebelum event.

### 3. Pendahuluan

Jelaskan latar belakang, tujuan, ruang lingkup, pertanyaan riset, dan kontribusi
proyek. Pertanyaan riset harus dibatasi pada post-event severity classification
dan clustering deskriptif.

### 4. Landasan teori

Bahas data mining, supervised classification, Random Forest, class imbalance,
threshold decision rule, unsupervised clustering, K-Means, preprocessing,
evaluasi temporal, dan leakage prevention.

### 5. Analisis kebutuhan dan rancangan sistem

Dokumentasikan aktor/use case, alur data, kontrak input-output, arsitektur
pipeline, dan batasan penggunaan aplikasi. Jelaskan bahwa aplikasi inference-only.

### 6. Data understanding

Gunakan `docs/DATA_STRATEGY.md` dan `docs/DATA_UNDERSTANDING.md` sebagai sumber.
Cantumkan:

- dataset STATS19 513.801 baris × 44 kolom;
- periode 2021–2025;
- distribusi target Fatal, Serious, Slight;
- missingness dan sentinel values;
- temuan deskriptif tanpa klaim kausal.

### 7. Data preparation

Gunakan `docs/DATA_PREPARATION.md`. Jelaskan target, 18 predictor final,
identifier/outcome exclusions, imputasi, encoding, kategori unknown, numeric
handling, dan train-only fitting.

### 8. Feature selection dan leakage control

Gunakan `docs/FEATURE_SELECTION.md`. Jelaskan alasan peran fitur, exclusion
identifier/post-event/outcome-derived, serta bahwa predictive association tidak
otomatis berarti hubungan sebab-akibat.

### 9. Metodologi classification

Gunakan `docs/MODELING_PHASE5.md` dan `docs/FINAL_MODEL.md`. Sajikan kronologi:

1. training/eksperimen 2021–2023: 311.349 baris;
2. validation 2024: 100.927 baris;
3. refit development 2021–2024: 412.276 baris;
4. final holdout 2025: 101.525 baris.

Final candidate adalah Random Forest balanced, 18 fitur input, 149 encoded
features, dan threshold Fatal 0,50. Tegaskan bahwa 2025 tidak dipakai untuk
fit, selection, tuning, atau threshold choice.

### 10. Metodologi clustering

Gunakan dokumentasi C2–C4 dan `docs/FINAL_RESULTS_CONSOLIDATION.md`. Jelaskan
pipeline terpisah, 18→108 encoded features, K-Means `k=2`, serta bahwa cluster
bersifat deskriptif dan bukan severity.

### 11. Hasil classification

Sumber angka: `results/final_model_metadata.json`,
`results/phase5_2_final_holdout.csv`, dan `docs/FINAL_MODEL.md`.

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

Interpretasikan ketidakseimbangan metrik dan threshold trade-off secara hati-hati.
Jangan hanya menggunakan accuracy sebagai bukti keberhasilan.

### 12. Hasil clustering

Sajikan evaluasi `k=2..6`, alasan pemilihan `k=2`, ukuran cluster, profil fitur,
dan PCA sebagai visualisasi. Jangan memberikan label severity pada cluster.

### 13. Implementasi dan validasi aplikasi

Gunakan `docs/APPLICATION_INTEGRATION.md` dan
`docs/OPERATIONAL_VALIDATION.md`. Cantumkan artifact
`models/final_research_model.joblib`, 18 input, 149 encoded features, class
mapping 1/2/3, threshold, probability output, dan inference-only behavior.

### 14. Interpretasi, keterbatasan, dan risiko

Gunakan `docs/RESEARCH_INTERPRETATION.md`. Bahas minoritas Fatal, temporal
shift, generalisasi wilayah, codebook, domain-range validation, dependency
compatibility, post-event timing, dan larangan klaim kausal/production.

### 15. Kesimpulan dan pekerjaan lanjutan

Simpulkan bahwa model adalah final candidate penelitian dengan kemampuan
terbatas dan trade-off pada Fatal. Pekerjaan lanjutan harus mencakup validasi
domain, pembekuan codebook/dependency, definisi use case, acceptance criteria,
dan review operasional sebelum deployment.

### 16. Daftar pustaka dan lampiran

Tambahkan sumber resmi STATS19/DfT, referensi metode, data dictionary/codebook,
tabel metrik, confusion matrix, profil cluster, traceability, dan screenshot
aplikasi bila diperlukan. Sumber yang belum tersedia di repository harus diberi
status belum terdokumentasi, bukan diisi dengan asumsi.

## Matriks sumber utama

| Bagian laporan | Sumber repository |
|---|---|
| Strategi data | `docs/DATA_STRATEGY.md` |
| Data understanding | `docs/DATA_UNDERSTANDING.md` |
| Preparation | `docs/DATA_PREPARATION.md` |
| Feature selection | `docs/FEATURE_SELECTION.md` |
| Modeling | `docs/MODELING_PHASE5.md`, `docs/MODELING_PHASE5A.md`, `docs/MODELING_PHASE5B1.md` |
| Final model | `docs/FINAL_MODEL.md`, `results/final_model_metadata.json` |
| Operational validation | `docs/OPERATIONAL_VALIDATION.md` |
| Application | `docs/APPLICATION_INTEGRATION.md` |
| Interpretation | `docs/RESEARCH_INTERPRETATION.md` |
| Consolidated results | `docs/FINAL_RESULTS_CONSOLIDATION.md` |

## Checklist sebelum laporan final

- [ ] Semua angka memakai sumber final yang benar.
- [ ] Legacy 10K/18→105 diberi label historis.
- [ ] Final research 513.801 raw rows dan 18→149 dibedakan jelas.
- [ ] Split temporal dan proteksi holdout 2025 dijelaskan.
- [ ] Metrik Fatal tidak disembunyikan.
- [ ] Tidak ada klaim kausal atau production-ready.
- [ ] Clustering tidak disamakan dengan severity.
- [ ] Keterbatasan dan unresolved decisions dicantumkan.
- [ ] Daftar pustaka dan provenance dilengkapi sebelum submission.
