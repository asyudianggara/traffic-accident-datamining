# Documentation Gaps and Open Audit Items

**Tanggal audit:** 25 Agustus 2026
**Scope:** documentation, provenance, reproducibility, dan evidence RPL.
**Aturan:** dokumen ini tidak mengubah model atau hasil eksperimen.

## P0 — Sebelum laporan classification disebut lengkap

### 1. CSV evaluasi classification lama tidak konsisten dengan artifact final (MASIH TERBUKA)

`models/final_classification_metadata.json` menyatakan pipeline 18 fitur → 105 encoded dengan
Accuracy 0,6385, Macro Precision 0,3802, Macro Recall 0,4008, Macro F1 0,3862, Weighted F1 0,6496.

Namun `results/final_test_results.csv` menyatakan Accuracy 0,6375 dan Macro F1 0,3985.
`results/final_classification_report.csv` dan `results/final_confusion_matrix.*` mengikuti output
lama. Source `final_model_evaluation.py` menggunakan 21 fitur (longitude, latitude, + lainnya),
sehingga **bukan** kontrak final 18 fitur.

Dampak: report/confusion matrix/feature-importance PNG lama **tidak** boleh dikutip sebagai hasil
final 18 fitur. Metadata final + notebook 03 boleh dikutip sebagai angka sah (lihat penutupan #1a).

### 1a. Per-class report 18 fitur (DITUTUP — ditemukan)

Laporan per kelas untuk pipeline 18 fitur **ditemukan** di `notebooks/03_classification.ipynb`
(baris 1071–1073): Fatal P0,07/R0,14/F10,10, Serious P0,28/R0,32/F10,30, Slight P0,79/R0,74/F10,76
(support 28/453/1519). Angka ini konsisten dengan aggregate metadata final
(macro ≈ 0,38 / 0,40 / 0,3867). Catatan: laporan ini **belum** diekspor ke CSV final; hanya ada di
notebook. Rekomendasi: ekspor ke `results/final_classification_report_18feat.csv` bila diizinkan
maintainer (tanpa mengubah model).

### 2. Feature importance final 18 fitur belum memiliki output audit kuat

`results/final_feature_importance.png` dibuat oleh evaluator lama 21 fitur. Belum ada CSV feature
importance yang mengikat nilai ke `preprocessor.get_feature_names_out()` dari preprocessor final 105 fitur.
Jangan menyebut dummy OHE sebagai fitur asli.

## P1 — Reproducibility dan source of truth

### 3. Kontrak fitur diulang di banyak file

Daftar 18 fitur diulang di `app.py`, `finalize_models.py`, `clustering_c2_c3.py`, `clustering_c4.py`,
dan notebook. Assertion/count membantu, tetapi tetap membuka risiko drift.

### 4. Script tuning historis masih 21 fitur

`step4_hyperparameter_tuning.py` dan `results/best_hyperparameters.json` merepresentasikan
Scenario D 21 fitur, bukan model final 18 fitur.

### 5. Evaluator lama memiliki nama yang tampak final

`final_model_evaluation.py` menulis `final_*` CSV/PNG padahal 21 fitur. Risiko operasional;
perlakukan sebagai historical/stale.

### 6. Belum ada manifest provenance

Belum ada file yang mencatat checksum dataset/artifact, commit Git pembuat output, waktu pembuatan,
dan versi Python/scikit-learn sebagai manifest per-artifact.

### 7. Dataset raw tidak masuk repository

`.gitignore` meng-ignore `data/raw/`. Baik untuk ukuran repo, tetapi reviewer butuh dataset &
sumber resmi terpisah untuk reproducibility.

## P2 — Metodologi dan akademik

### 8. Citation dataset belum formal

Source menyebut DfT/STATS19 dan nama file, tetapi belum ada URL unduhan resmi, tanggal akses,
lisensi, dan variable-version citation formal.

### 9. Alasan pemilihan 18 fitur belum menjadi decision record

Source membuktikan daftar dan exclusion checks, tetapi belum ada dokumen formal yang menjelaskan
trade-off interpretabilitas, ketersediaan saat prediksi, dan leakage untuk setiap fitur.

### 10. Generalisasi sample belum dianalisis

Sampling 2.000/tahun menyeimbangkan jumlah antar tahun, tetapi laporan belum menjelaskan dampaknya
terhadap representasi wilayah, distribusi severity, dan generalisasi ke populasi penuh 513.801 baris.

### 11. Evaluasi statistik tambahan belum dibuktikan

Belum ada calibration analysis, confidence interval test formal, fairness/subgroup analysis, atau
analisis error per tahun/wilayah. Jangan diasumsikan sudah dilakukan.

### 12. Cluster ID bukan label intrinsik

Cluster ID 0/1 adalah nomor K-Means. Profil menunjukkan rural/high-speed dan urban/lower-speed,
tetapi tidak membuktikan sebab-akibat dan tidak menjadikan cluster sebagai severity class.

## P3 — RPL dan presentasi

### 13. Diagram formal RPL belum tersedia

Belum ditemukan use-case, activity, sequence, component, deployment, atau data-flow diagram formal.
README/app menjelaskan pipeline secara naratif.

### 14. Test case matrix belum dipersistenkan

Evidence smoke test/AppTest tersedia, tetapi belum ada dokumen test case dengan ID, precondition,
input, expected result, actual result, dan timestamp.

### 15. Data dictionary 44 kolom belum formal

Notebook 01 membuktikan 44 nama kolom dan mapping sebagian field. Belum ada kamus data formal untuk
semua kolom, definisi bisnis, special values, dan status penggunaan.

### 16. Audit log perubahan belum sinkron

`README.md`, `README_APP.md`, dan `app.py` memiliki perubahan lokal yang akan di-commit saat
finalisasi dokumentasi. Tidak ada force push dilakukan.

## Hal yang sudah dinilai baik

- target tidak masuk feature set clustering;
- `number_of_casualties` dan respons polisi tidak masuk fitur final;
- identifier/kode administratif utama tidak dipilih;
- preprocessor classification dan clustering dipisahkan;
- classification preprocessor fit pada training set;
- clustering memakai 18 fitur dan 108 encoded;
- PCA ditempatkan sesudah K-Means untuk visualisasi;
- legacy joblib di-ignore dan tidak direferensikan aplikasi;
- per-class report 18 fitur tersedia di notebook 03 (konsisten dengan metadata);
- aplikasi memiliki metadata checks dan smoke/functional evidence.

## Rekomendasi urutan penutupan gap

1. Tetapkan satu source evaluasi 18 fitur (metadata + notebook 03 sudah cukup sebagai angka);
   ekspor per-class ke CSV final bila diizinkan.
2. Tandai atau pindahkan evaluator 21 fitur ke lokasi historical agar tidak menulis nama `final_*`.
3. Tambahkan manifest provenance tanpa menyimpan raw dataset atau secret.
4. Tambahkan citation/data dictionary dan decision record feature selection.
5. Tambahkan test case matrix serta diagram RPL.
6. Lakukan audit final read-only dan dokumentasikan commit release.

## Hal yang sengaja tidak dilakukan

- tidak menjalankan K-Means, PCA, training, tuning, atau evaluasi test set baru;
- tidak mengubah model, notebook, app, C1–C4 result, atau feature list;
- tidak menghapus legacy artifact atau output lama;
- tidak membuat commit atau push Git (ditangani pada tahap finalisasi);
- tidak mengubah angka yang ada pada CSV/metadata final.
