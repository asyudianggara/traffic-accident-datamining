# Interpretasi Riset dan Keterbatasan

## Tujuan interpretasi

Dokumen ini menjelaskan apa yang dapat dan tidak dapat disimpulkan dari hasil
classification dan clustering. Interpretasi dibatasi pada data STATS19 Inggris
periode 2021–2025, kontrak 18 fitur, dan hasil evaluasi yang telah dibekukan.

Model final adalah **final candidate penelitian**, bukan sistem produksi atau
sistem keputusan keselamatan.

## Pertanyaan riset yang didukung

1. Seberapa baik karakteristik collision yang tersedia pada record menjelaskan
   perbedaan `collision_severity`?
2. Apakah model dapat mengenali kelas Fatal, Serious, dan Slight pada holdout
   temporal 2025?
3. Apakah terdapat kelompok karakteristik collision yang berbeda secara
   deskriptif berdasarkan 18 fitur tanpa memakai severity sebagai input?

Pertanyaan ini bersifat prediktif dan deskriptif. Hasilnya tidak membuktikan
hubungan sebab-akibat.

## Desain evaluasi

- Training/eksperimen awal: 2021–2023, 311.349 baris.
- Validation untuk strategi imbalance dan threshold: 2024, 100.927 baris.
- Setelah keputusan final: refit pada development 2021–2024, 412.276 baris.
- Final holdout: 2025, 101.525 baris.

Tahun 2025 tidak digunakan untuk fitting, feature selection, threshold tuning,
hyperparameter tuning, maupun model selection.

## Interpretasi model classification

Random Forest balanced dengan threshold Fatal 0,50 menghasilkan pada holdout
2025:

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

Macro F1 dan weighted F1 yang berbeda menunjukkan bahwa performa tidak merata
antar kelas. Kelas dominan Slight berkontribusi besar terhadap metrik berbobot,
sedangkan performa Fatal tetap lemah. Fatal recall 0,329663 berarti sebagian
kasus Fatal terdeteksi pada holdout, tetapi banyak kasus Fatal tetap terlewat.
Fatal precision 0,057524 berarti sebagian besar prediksi Fatal adalah false
positive. Karena itu output model memerlukan interpretasi hati-hati dan tidak
boleh dianggap sebagai kepastian.

Threshold 0,50 meningkatkan Fatal precision dan Fatal F1 dibanding aturan
argmax pada eksperimen yang telah ditetapkan, tetapi menurunkan Fatal recall.
Ini adalah trade-off kebijakan klasifikasi, bukan bukti bahwa threshold tersebut
optimal untuk semua use case.

## Interpretasi clustering

Clustering menggunakan pipeline terpisah dengan 18 fitur dan 108 encoded
features. K-Means `k=2` menghasilkan kelompok yang bersifat deskriptif, terutama
terkait perbedaan konteks urban/rural dan speed limit pada profil yang tersedia.

Cluster 0 dan Cluster 1 bukan label Fatal, Serious, atau Slight. Nomor cluster
tidak memiliki arti ordinal, tidak menunjukkan tingkat bahaya, dan tidak boleh
digunakan sebagai target keselamatan.

## Batasan metodologis

- Dataset berasal dari Inggris dan generalisasi ke wilayah lain belum diuji.
- Target merupakan severity pada collision yang sudah terjadi; model bukan
  prediksi risiko sebelum kecelakaan terjadi.
- Kelas Fatal sangat minoritas sehingga precision dan recall-nya tidak stabil
  untuk semua konteks penggunaan.
- Holdout 2025 adalah satu periode temporal; hasil belum membuktikan kestabilan
  lintas tahun, wilayah, atau perubahan kebijakan pencatatan.
- Fitur geografis dan administratif dikeluarkan karena kebijakan geografis,
  missingness, dan risiko generalisasi belum difinalkan.
- Codebook resmi untuk sebagian kode kategori belum dibekukan dalam repository.
- Tidak ada validasi domain-range terpisah untuk seluruh input inference.
- Kompatibilitas artifact lintas versi scikit-learn belum terverifikasi penuh.
- Probability adalah skor model, bukan probabilitas kausal, confidence klinis,
  atau jaminan hasil individual.
- Clustering memiliki kualitas pemisahan yang terbatas dan hanya bersifat
  eksploratif/deskriptif.

## Klaim yang tidak didukung

Hasil ini tidak mendukung klaim bahwa model dapat:

- memprediksi apakah kecelakaan akan terjadi;
- menentukan penyebab kecelakaan;
- memberikan keputusan keselamatan otomatis;
- menggantikan investigator atau otoritas lalu lintas;
- menjamin performa pada wilayah, tahun, atau codebook yang berbeda;
- mengartikan cluster sebagai severity atau tingkat bahaya.

## Kesimpulan riset

Model final candidate menunjukkan kemampuan terbatas untuk membedakan severity
dengan trade-off kuat pada kelas Fatal. Hasil paling tepat dipakai sebagai bukti
eksperimen pada dataset dan periode yang ditentukan, bukan sebagai klaim kesiapan
operasional. Penggunaan lanjutan memerlukan validasi domain-range, pembekuan
codebook dan dependency, definisi use case/timing, serta acceptance criteria
yang disetujui.

Sumber angka utama: `docs/FINAL_MODEL.md` dan
`results/final_model_metadata.json`. Sumber desain operational:
`docs/OPERATIONAL_VALIDATION.md`.
