# DATA STRATEGY

## Dataset

Audit read-only pada 2026-08-27 memverifikasi dataset aktual berikut.

| Item | Verified fact |
|---|---|
| File | `data/raw/dft-road-casualty-statistics-collision-last-5-years.csv` |
| Status Git | Lokal dan di-ignore; tidak diubah pada Phase 1 |
| Ukuran | 97.669.586 byte |
| Baris | 513.801 |
| Kolom | 44 |
| Periode tanggal | 2021-01-01 s.d. 2025-12-31 |
| Tahun | 2021: 101.087; 2022: 106.004; 2023: 104.258; 2024: 100.927; 2025: 101.525 |
| Target terverifikasi | `collision_severity` |

Dokumentasi mapping lokal hanya tersedia untuk 10 kolom terpilih di `data/processed/stats19_maps.json`. Arti lain pada inventory yang tidak ditopang mapping ditandai berdasarkan nama kolom dan memerlukan konfirmasi data dictionary STATS19 resmi pada Phase 2.

## Full Dataset

Full dataset adalah kandidat dataset utama Tugas 2: seluruh 513.801 record yang tersedia pada file raw ini. Tidak ada duplicate row utuh; `collision_index` juga unik untuk semua baris. Penggunaan seluruh record tetap dapat mengecualikan record atau fitur tertentu hanya bila alasan metodologis, aturan leakage, dan jumlah yang terdampak didokumentasikan sebelum implementasi.

## Legacy 10K Baseline

| Aspek | Full dataset | Legacy 10K |
|---|---:|---:|
| Record | 513.801 | 10.000 |
| Kolom raw | 44 | 44 (output notebook) |
| Periode | 2021–2025 | 2021–2025 |
| Distribusi tahun | Sesuai populasi aktual | 2.000 per tahun |
| Fatal | 7.553 (1,470024%) | 137 (1,37%) |
| Serious | 116.813 (22,735067%) | 2.614 (26,14%) |
| Slight | 389.435 (75,794909%) | 7.249 (72,49%) |
| Sampling | Tidak ada | Acak per tahun |
| Random state | N/A | 42 |
| Tujuan | Kandidat utama Tugas 2 | Baseline/referensi legacy |

Angka 10K berasal dari output yang tersimpan di `notebooks/01_data_understanding.ipynb`, bukan dari sampling ulang pada Phase 1. Alokasi sama per tahun dan selisih distribusi target menunjukkan baseline tidak boleh disebut dataset final.

## Target

`collision_severity` terverifikasi sebagai kolom target legacy dan mempunyai tiga kode valid, seluruhnya tersedia dalam mapping lokal:

| Code | Label | Count | Percentage |
|---:|---|---:|---:|
| 1 | Fatal | 7.553 | 1,470024% |
| 2 | Serious | 116.813 | 22,735067% |
| 3 | Slight | 389.435 | 75,794909% |

Tidak ada missing ataupun kode target tak terduga. Ketimpangan kelas tinggi, khususnya kelas Fatal, adalah fakta audit; belum ada resampling atau penetapan metode penanganan pada Phase 1.

## Data Quality

- Duplicate row utuh: 0.
- `collision_index` duplikat: 0; `collision_ref_no` memiliki 2.964 baris duplikat sehingga tidak cocok sebagai primary key.
- Missing eksplisit hanya pada `location_easting_osgr`, `location_northing_osgr`, `longitude`, dan `latitude` (masing-masing 53).
- Seluruh tanggal valid dengan format `%d/%m/%Y`; seluruh waktu valid dengan format `HH:MM`.
- Tidak ada kolom konstan.
- Tidak ada kode tak terpetakan pada 10 kolom yang memiliki mapping lokal.
- Kode `-1` adalah nilai "Data missing / out of range" menurut mapping untuk kolom tertentu, bukan missing pandas. Contoh frekuensi: `junction_control` 217.897, `junction_detail` 19.982, `road_surface_conditions` 3.527.
- Kolom kode lain yang tidak memiliki mapping lokal memerlukan data dictionary sebelum validitas kategorinya dapat disimpulkan.

## Feature Inventory

`Keep`, `Drop`, dan `Review` adalah kandidat strategi, bukan feature selection final. Contoh adalah nilai aktual; `miss` adalah missing pandas; `uniq` adalah jumlah nilai non-null.

| Feature | Type; contoh | miss; uniq | Kandidat dan alasan |
|---|---|---:|---|
| `collision_index` | str; `202517M102225` | 0; 513.801 | DROP — identifier unik |
| `collision_year` | int64; `2025` | 0; 5 | REVIEW — untuk split/monitoring; bukan otomatis fitur model |
| `collision_ref_no` | str; `17M102225` | 0; 510.837 | DROP — identifier, tidak unik penuh |
| `location_easting_osgr` | float64; `449804.0` | 53; 245.276 | REVIEW — koordinat; privacy/overfit dan redundan dengan longitude |
| `location_northing_osgr` | float64; `519612.0` | 53; 263.601 | REVIEW — koordinat; privacy/overfit dan redundan dengan latitude |
| `longitude` | float64; `-1.23119` | 53; 437.862 | REVIEW — geografis; pertimbangkan bersama easting/northing, bukan semua |
| `latitude` | float64; `54.56929` | 53; 412.450 | REVIEW — geografis; pertimbangkan bersama easting/northing, bukan semua |
| `police_force` | int64; `17` | 0; 44 | REVIEW — administratif/geographic proxy |
| `collision_severity` | int64; `3` | 0; 3 | KEEP AS TARGET — outcome yang diprediksi |
| `number_of_vehicles` | int64; `1` | 0; 19 | REVIEW — kandidat numerik; validitas bergantung waktu prediksi |
| `number_of_casualties` | int64; `1` | 0; 26 | DROP — outcome setelah kecelakaan/potential leakage |
| `date` | str; `15/02/2025` | 0; 1.826 | REVIEW — turunkan fitur waktu, jangan gunakan raw date langsung |
| `day_of_week` | int64; `7` | 0; 7 | KEEP CANDIDATE — kategorikal; mapping tersedia |
| `time` | str; `19:15` | 0; 1.440 | REVIEW — turunkan jam/siklus waktu setelah pipeline diset |
| `local_authority_district` | int64; `-1` | 0; 15 | REVIEW — administratif; cek definisi/kode sentinel |
| `local_authority_ons_district` | str; `E06000002` | 0; 370 | REVIEW — administratif/high cardinality |
| `local_authority_highway` | str; `E06000002` | 0; 211 | REVIEW — administratif/high cardinality |
| `local_authority_highway_current` | str; `E06000002` | 0; 208 | REVIEW — kemungkinan versi/duplikasi administratif |
| `first_road_class` | int64; `6` | 0; 7 | KEEP CANDIDATE — kategorikal; mapping tersedia; sentinel `-1` ada 6 |
| `first_road_number` | int64; `0` | 0; 3.616 | REVIEW — high cardinality; berpotensi geographic proxy |
| `road_type` | int64; `6` | 0; 6 | KEEP CANDIDATE — kategorikal; mapping tersedia |
| `speed_limit` | int64; `30` | 0; 7 | KEEP CANDIDATE — numerik/ordinal; validasi coding pada Phase 2 |
| `junction_detail_historic` | int64; `-1` | 0; 11 | DROP — historical/duplicate candidate |
| `junction_detail` | int64; `16` | 0; 8 | KEEP CANDIDATE — kategorikal; mapping tersedia; sentinel `-1` ada 19.982 |
| `junction_control` | int64; `4` | 0; 6 | KEEP CANDIDATE — kategorikal; mapping tersedia; sentinel `-1` ada 217.897 |
| `second_road_class` | int64; `6` | 0; 9 | REVIEW — road-context; dokumentasi kode lokal tidak lengkap |
| `second_road_number` | int64; `0` | 0; 3.356 | REVIEW — high cardinality/geographic proxy |
| `pedestrian_crossing_human_control_historic` | int64; `-1` | 0; 5 | DROP — historical/duplicate candidate |
| `pedestrian_crossing_physical_facilities_historic` | int64; `-1` | 0; 8 | DROP — historical/duplicate candidate |
| `pedestrian_crossing` | int64; `0` | 0; 10 | REVIEW — candidate kategorikal; dokumentasi kode lokal tidak lengkap |
| `light_conditions` | int64; `4` | 0; 6 | KEEP CANDIDATE — kategorikal; mapping tersedia; sentinel `-1` ada 34 |
| `weather_conditions` | int64; `1` | 0; 10 | KEEP CANDIDATE — kategorikal; mapping tersedia; sentinel `-1` ada 12 |
| `road_surface_conditions` | int64; `1` | 0; 7 | KEEP CANDIDATE — kategorikal; mapping tersedia; sentinel `-1` ada 3.527 |
| `special_conditions_at_site` | int64; `-1` | 0; 10 | REVIEW — candidate kategorikal; codebook required |
| `carriageway_hazards_historic` | int64; `-1` | 0; 8 | DROP — historical/duplicate candidate |
| `carriageway_hazards` | int64; `0` | 0; 14 | REVIEW — candidate kategorikal; codebook required |
| `urban_or_rural_area` | int64; `1` | 0; 4 | KEEP CANDIDATE — kategorikal; mapping tersedia; sentinel `-1` ada 8 |
| `did_police_officer_attend_scene_of_accident` | int64; `1` | 0; 3 | DROP — berpotensi dicatat setelah kejadian/potential leakage |
| `trunk_road_flag` | int64; `2` | 0; 3 | REVIEW — candidate kategorikal; codebook required |
| `lsoa_of_accident_location` | str; `E01012092` | 0; 35.630 | REVIEW — lokasi high cardinality/privacy/geographic proxy |
| `enhanced_severity_collision` | int64; `3` | 0; 6 | DROP — severity-derived/potential target leakage |
| `collision_injury_based` | int64; `1` | 0; 2 | DROP — injury/outcome-derived/potential leakage |
| `collision_adjusted_severity_serious` | float64; `0.0` | 0; 25.538 | DROP — severity-adjusted/outcome-derived/potential leakage |
| `collision_adjusted_severity_slight` | float64; `1.0` | 0; 25.539 | DROP — severity-adjusted/outcome-derived/potential leakage |

## Sampling Legacy

- Lokasi: `notebooks/01_data_understanding.ipynb`, `notebooks/03_classification.ipynb`, `clustering_c2_c3.py`, dan `clustering_c4.py`.
- Metode: filter tahun 2021–2025, lalu `groupby("collision_year").sample(n=2000, random_state=42)` dan reset index.
- Ukuran: 2.000/tahun, total 10.000.
- Stratifikasi sampling: tidak ada; `collision_severity` bukan variabel stratifikasi sampling.
- Setelah sampling: notebook classification menurunkan `hour` dan `month`, melakukan decoding, lalu `train_test_split(test_size=0.20, random_state=42, stratify=y)`; script clustering melakukan preprocessing, evaluasi `k=2..6`, dan C4 profiling/PCA.
- Waktu pertama sampling dilakukan: TIDAK DAPAT DIVERIFIKASI dari checkpoint.

## Full Dataset Strategy

### Dataset master

Pertahankan CSV raw sebagai master immutable. Phase 2 harus membaca dari path ini, mencatat ukuran, jumlah baris/kolom, periode, dan checksum file pada manifest eksperimen. Jangan menulis salinan processed besar kecuali transformasi telah disetujui dan memiliki kebutuhan reproducibility yang jelas.

### Train/Test Strategy

| Option | Design | Trade-off |
|---|---|---|
| A | Random stratified 80/20 dengan `random_state` terdokumentasi | Sebanding dengan legacy tetapi berisiko optimistic bila pola temporal berubah |
| B | Outer temporal holdout: latih/develop 2021–2024, uji final 2025; validasi internal pada data train dengan split waktu atau stratified CV yang ditetapkan | Lebih representatif untuk generalisasi ke waktu mendatang, tetapi distribusi tahun bisa berubah |
| Recommended | B, jika tujuan prediksi memakai informasi yang tersedia saat kejadian dan generalisasi ke tahun berikutnya penting | Keputusan final menunggu konfirmasi use case/dosen dan audit fitur waktu |

Semua opsi menggunakan seluruh baris yang memenuhi aturan kualitas: baris test tidak dibuang, hanya dipisahkan dari fitting. Tidak ada sampling 10K untuk dataset final.

## Preprocessing Strategy

- Derive `hour` dari `time` dan fitur kalender yang disetujui dari `date` di dalam pipeline, kemudian tidak memasukkan raw timestamp/identifier sebagai prediktor.
- Fit imputer, encoder, scaler, dan semua transformasi hanya pada data training; terapkan transformasi yang sama ke validation/test.
- Untuk koordinat, putuskan terlebih dahulu apakah feature geografis dipakai. Jika dipakai, pilih satu representasi koordinat, ukur dampak 53 missing, dan fit imputasi pada train saja; jika tidak, drop seluruh pasangan geografis secara konsisten.
- Perlakukan kode sentinel seperti `-1` sebagai kategori explicit `Missing/Out of range`, bukan nilai numerik yang diskalakan. Konfirmasi semua codebook yang belum ada sebelum transformasi.
- Numerik kandidat: validasi domain/range dan gunakan imputer median serta scaling hanya bila algoritma berikutnya memerlukannya. Kategorikal kandidat: imputer most-frequent/explicit missing dan one-hot atau encoder lain harus dipilih setelah audit cardinality.
- Untuk high-cardinality administratif/geografis, jangan otomatis one-hot; keputusan menunggu analisis leakage, privacy, dan generalization.

## Leakage Prevention

Keluarkan target dari input dan blok kolom outcome/adjusted severity: `number_of_casualties`, `enhanced_severity_collision`, `collision_injury_based`, `collision_adjusted_severity_serious`, dan `collision_adjusted_severity_slight`. Blok identifier. Perlakukan `did_police_officer_attend_scene_of_accident` sebagai excluded hingga urutan ketersediaan data dibuktikan. Review waktu ketersediaan `number_of_vehicles`, lokasi, dan field administratif terhadap use case sebelum modeling.

## Imbalance Strategy

Fakta awal adalah Fatal 1,47%. Tidak ada oversampling/undersampling pada Phase 1. Phase berikutnya harus mempertahankan distribusi target dalam split yang relevan, melaporkan precision/recall/F1 per kelas dan macro metric, serta membandingkan class weighting atau resampling hanya di training folds jika diperlukan dan disetujui.

## Reproducibility

- Gunakan satu konfigurasi versioned untuk path data, schema, target, feature candidates, exclusions, split, seed, dan dependency version.
- Rekam checksum SHA-256 raw, jumlah record sebelum/sesudah setiap filter, dan alasan filter pada manifest eksperimen.
- Tetapkan seed untuk split dan estimator; simpan split identifiers/aturan temporal, bukan sample acak tersembunyi.
- Jangan overwrite baseline legacy; setiap output full dataset nanti harus memakai nama/directori yang berbeda.

## Performance Considerations

CSV 97,7 MB dengan 513.801 baris masih dapat diaudit sekali di memori lokal, tetapi hindari multiple copy dataframe. Gunakan `usecols`, dtype eksplisit, dan chunked scan untuk EDA yang tidak membutuhkan seluruh frame. Pertimbangkan encoder sparse bila algoritma mendukungnya; jangan menerapkan one-hot dense secara membabi buta pada fitur high-cardinality. Profil memori wajib dilakukan sebelum eksperimen full dataset.

## Risks

- Imbalance target dapat menyamarkan kinerja kelas Fatal bila hanya memakai accuracy.
- Outcome-derived fields dapat menghasilkan leakage berat.
- Field historis/administratif/geografis dapat redundant, berubah antar tahun, atau menurunkan generalisasi.
- Mapping lokal belum mencakup seluruh field kode; codebook resmi belum terverifikasi pada checkout.
- `collision_ref_no` bukan key unik; gunakan `collision_index` hanya untuk traceability/split record, bukan fitur.

## Decisions

1. Full dataset 513.801 baris adalah kandidat master Tugas 2; baseline 10K hanya referensi legacy.
2. Tidak ada sampling, cleaning permanen, feature selection final, training, atau artifact baru pada Phase 1.
3. `collision_severity` adalah target kandidat terverifikasi; outcome-derived field diblok dari kandidat input.
4. Strategi split temporal direkomendasikan secara kondisional; keputusan final bergantung use case yang dikonfirmasi.
5. Phase 2 harus melengkapi data dictionary dan audit domain sebelum menetapkan feature set.

## Open Questions

1. Apa definisi use case prediction yang diharapkan dosen: sebelum kejadian, saat kejadian, atau analisis pascakejadian?
2. Apakah split temporal 2025 sebagai final test sesuai kebutuhan penilaian, atau dosen mewajibkan holdout acak?
3. Apakah field geografis dan administratif boleh dipakai, dan bagaimana batas privacy/generalization-nya?
4. Di mana data dictionary resmi untuk seluruh kode STATS19 dan definisi field historical/adjusted severity?

## Next Phase

PHASE 2 – DATA UNDERSTANDING: lengkapi data dictionary, domain audit, visual/EDA yang disetujui, dan finalisasi spesifikasi input serta aturan kualitas. Jangan mulai modeling sampai instruksi eksplisit berikutnya.
