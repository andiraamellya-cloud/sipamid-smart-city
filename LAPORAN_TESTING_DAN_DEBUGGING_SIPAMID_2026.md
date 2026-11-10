# LAPORAN PENGUJIAN DAN DEBUGGING SISTEM (TESTING & QUALITY ASSURANCE REPORT)
## SIPAMID - Sistem Informasi Pengaduan Masyarakat dan Monitoring Infrastruktur Desa
### *Implementasi Konsep Smart City melalui Smart Governance Desa Berbasis Rust & PostgreSQL*

---

### Informasi Dokumen & Pengembang
- **Mata Kuliah:** Perencanaan & Pengembangan Sistem Informasi (PPSI 2026)
- **Tugas:** Ujian Tengah Semester (UTS PPSI) - Evaluasi Testing & Debugging (Prompt 4 & 5)
- **Nama Pengembang:** **Andira Amellya**
- **NPM:** **24311065**
- **Kelas:** **SI 23 A**
- **Dosen Pengampu:** **Dr. Erliyan Redy Susanto, M.Kom.**
- **Program Studi:** S1 Sistem Informasi, Fakultas Teknik dan Ilmu Komputer, Universitas Teknokrat Indonesia
- **Tahun Dokumen:** 2026
- **Hak Cipta:** `Copyright©2026 by Andira Amellya dan Dr. Erliyan Redy Susanto, M.Kom.`

---

## 1. Ringkasan Eksekutif Pengujian (Executive Summary)

Pengujian sistem pada aplikasi **SIPAMID (Sistem Informasi Pengaduan Masyarakat dan Monitoring Infrastruktur Desa)** dilaksanakan secara menyeluruh untuk memastikan keandalan, integritas data, kepatuhan keamanan memori (*memory safety*), serta kepatuhan penuh terhadap spesifikasi teknis pada dokumen *Product Requirement Document* (PRD Versi 1.0).

Pengujian mencakup 4 (empat) pilar utama:
1. **Unit Testing**: Pengujian modul independen (utilitas keamanan enkripsi password Argon2id, token JWT claims, generator nomor tiket laporan unik, serta validator DTO input).
2. **Integration Testing dengan PostgreSQL**: Pengujian integritas skema database, foreign key constraints, transaksi atomik ACID pada pencatatan riwayat perubahan status (*status history*), dan mekanisme *connection pooling* SQLx.
3. **Functional & SOP Lifecycle Testing**: Pengujian skenario alur kerja dari sisi Masyarakat, Admin Desa, hingga Kepala Desa sesuai Standar Operasional Prosedur (SOP) transisi status pengaduan (PRD Bab 9.4).
4. **Security & Role-Based Access Control (RBAC) Testing**: Pengujian hak akses untuk mencegah eskalasi wewenang (*privilege escalation*), kebocoran data pribadi masyarakat, dan validasi berkas lampiran foto (maksimal 5 MB dengan filter MIME type).

---

## 2. Rencana & Skenario Pengujian (Test Scenarios)

### 2.1. Skenario Unit Testing (Backend Rust Utilities)

| Kode Uji | Komponen yang Diuji | Input / Kondisi | Hasil yang Diharapkan | Status |
|---|---|---|---|:---:|
| **UT-001** | Hashing Sandi Argon2id | String password mentah: `"PasswordAman2026!"` | Hash tersimpan berformat `$argon2id$v=19$`, lolos verifikasi `verify_password()`, dan menolak password yang tidak identik. | **PASSED** |
| **UT-002** | JWT Token Generator | Payload claims `user_id`, `username`, `role: "masyarakat"` | Token JWT bertipe Bearer terbentuk dengan masa kedaluwarsa valid, decoded claims identik dengan payload asli. | **PASSED** |
| **UT-003** | Validasi Token dengan Secret Berbeda | Token valid diverifikasi menggunakan secret key yang salah | Sistem menolak token dan menghasilkan error `AppError::Unauthorized`. | **PASSED** |
| **UT-004** | Generator Nomor Tiket Unik | Eksekusi `generate_unique_report_number()` | Menghasilkan kode string berformat `LAP-YYYYMM-XXXX` (15 karakter) dan unik di setiap pemanggilan. | **PASSED** |
| **UT-005** | Validator Registrasi Pengguna | DTO dengan nama kosong atau email tanpa `@` | Fungsi `validate_register_dto()` mengembalikan `AppError::ValidationError`. | **PASSED** |
| **UT-006** | Validator Form Pengaduan | Judul kurang dari 5 karakter atau lokasi kosong | Fungsi `validate_create_report_dto()` mengembalikan `AppError::ValidationError`. | **PASSED** |

---

### 2.2. Skenario Integration Testing dengan PostgreSQL (Database & Transaksi)

| Kode Uji | Skenario Integrasi | Kueri / Tindakan SQLx | Hasil yang Diharapkan | Status |
|---|---|---|---|:---:|
| **IT-001** | Eksekusi Migrasi SQLx Terpadu | Menjalankan migrasi `001_create_users.sql` s/d `007_create_audit_logs.sql` | Seluruh 7 tabel terbuat tanpa konflik tipe data; ekstensi `uuid-ossp` aktif. | **PASSED** |
| **IT-002** | Constraint Unik Username & Email | Insert pengguna dengan username/email duplikat | Database melempar error code `23505` (`unique_violation`), repository menangkap dan mengembalikan pesan ramah pengguna. | **PASSED** |
| **IT-003** | Relasi Foreign Key `ON DELETE RESTRICT` | Menghapus pengguna yang telah memiliki pengaduan terdaftar | Operasi ditolak oleh PostgreSQL untuk melindungi keutuhan jejak audit pengaduan masyarakat. | **PASSED** |
| **IT-004** | Transaksi Atomik Perubahan Status | Update status pada tabel `reports` dan insert riwayat ke `status_history` dalam satu `tx` | Jika salah satu kueri gagal, seluruh transaksi di-*rollback*; tidak ada data setengah tersimpan. | **PASSED** |
| **IT-005** | Indeks Kolom Pencarian Cepat | Indeks pada `report_number`, `user_id`, `category_id`, `status`, dan `created_at` | Kueri filter pengaduan skala besar menggunakan *Index Scan* (waktu respons < 50ms). | **PASSED** |

---

### 2.3. Skenario Functional Testing & Alur Kerja (SOP Pengaduan Desa)

| Kode Uji | Skenario Pengujian | Aktor | Langkah Pengujian & Validasi | Status |
|---|---|---|---|:---:|
| **FT-001** | Registrasi & Login Warga | Masyarakat | Mengisi formulir registrasi desa, login ke portal warga, memeriksa sesi token JWT. | **PASSED** |
| **FT-002** | Pembuatan Laporan Infrastruktur | Masyarakat | Mengunggah foto bukti fisik jalan berlubang, memilih kategori, menandai koordinat Leaflet GIS (Latitude & Longitude), mengirim laporan. Tiket `LAP-202611-XXXX` terbit dengan status awal `Menunggu Verifikasi`. | **PASSED** |
| **FT-003** | Verifikasi Laporan Masuk | Admin Desa | Memeriksa kelayakan foto dan deskripsi; menekan tombol **Setujui Verifikasi**. Status berubah menjadi `Diverifikasi`. | **PASSED** |
| **FT-004** | Penolakan Laporan dengan Catatan | Admin Desa | Menolak laporan yang tidak valid dengan menyertakan alasan penolakan wajib (PRD FR-016). Status berubah menjadi `Ditolak`. | **PASSED** |
| **FT-005** | Pengerjaan Lapangan & Penyelesaian | Admin Desa | Mengubah status dari `Diverifikasi` &rarr; `Sedang Diproses`, lalu dari `Sedang Diproses` &rarr; `Selesai` setelah perbaikan fisik rampung. | **PASSED** |
| **FT-006** | Pengiriman Tanggapan Resmi | Admin Desa | Memberikan pesan instruksi teknis kepada warga pelapor melalui `/reports/:id/responses`. Pesan tampil di halaman detail pelapor. | **PASSED** |
| **FT-007** | Pemantauan Dashboard Eksekutif | Kepala Desa | Membuka dashboard pimpinan; memantau grafik donat kategori kerusakan, persentase tuntas (100%), dan peta sebaran titik masalah desa. | **PASSED** |
| **FT-008** | Rekapitulasi & Ekspor Laporan | Admin / Kades | Melakukan penyaringan periode dan mengunduh berkas CSV / Excel, serta mencetak dokumen kop resmi desa print-ready (PDF). | **PASSED** |

---

### 2.4. Skenario Security & Role-Based Access Control (RBAC) Testing

| Kode Uji | Skenario Pengujian | Role Aktor | Target Endpoint / Fitur | Hasil Evaluasi Keamanan | Status |
|---|---|---|---|---|:---:|
| **ST-001** | Akses Tidak Terotorisasi | Anonim (Tanpa Token) | `GET /api/v1/reports` | Ditolak: `401 Unauthorized`. | **PASSED** |
| **ST-002** | Eskalasi Hak Akses ke Admin | Warga (Masyarakat) | `POST /api/v1/reports/:id/verify` | Ditolak oleh middleware RBAC: `403 Forbidden`. | **PASSED** |
| **ST-003** | Isolasi Data Antar-Warga | Warga A | `GET /api/v1/reports/:id_milik_warga_B` | Ditolak: `403 Forbidden: Anda tidak memiliki izin untuk melihat rincian laporan pengaduan ini`. | **PASSED** |
| **ST-004** | Pembatasan Upload File | Pengguna | Unggah berkas `.exe` atau gambar > 5MB | Ditolak: `400 Bad Request` (Hanya format JPG/JPEG/PNG & batas ukuran 5MB diizinkan). | **PASSED** |

---

## 3. Daftar Bug / Error Log yang Ditemukan & Solusi Perbaikannya

Selama tahapan inspeksi mendalam, uji coba kompilasi statis kode Rust, dan eksekusi integrasi endpoint, ditemukan sejumlah *defect* dan *bug* kritis. Berikut rincian log kesalahan beserta perbaikan komprehensif yang telah diterapkan:

### Bug #1: *Inverted Middleware Execution Order in Tower/Axum* (Kritis)
- **Komponen Terdampak:** `sipamid-backend/src/routes.rs`
- **Tingkat Keparahan:** **Kritis (Critical - Blocker)**
- **Gejala / Error Log:**
  ```text
  HTTP/1.1 401 Unauthorized
  {"status":"error","code":401,"message":"Sesi otentikasi tidak ditemukan"}
  ```
  Permintaan ke seluruh endpoint khusus Admin (seperti `/api/v1/reports/:id/verify` dan `/api/v1/users`) selalu ditolak dengan status 401 Unauthorized, meskipun klien mengirimkan header `Authorization: Bearer <valid_admin_token>`.
- **Akar Masalah (Root Cause):**
  Pada arsitektur framework Tower/Axum, pemanggilan `.layer(A).layer(B)` mengevaluasi middleware dari arah luar ke dalam (*bottom-to-top* / *reverse order*). Pada implementasi awal:
  ```rust
  // KODE SEBELUM PERBAIKAN:
  let admin_routes = Router::new()
      ...
      .layer(from_fn_with_state(config.clone(), auth_middleware))
      .layer(axum::middleware::from_fn(require_admin));
  ```
  Akibatnya, fungsi `require_admin` dieksekusi **sebelum** `auth_middleware`. Karena `auth_middleware` belum berjalan, objek `AuthContext` belum disuntikkan ke dalam `request.extensions()`, sehingga `require_admin` selalu menganggap sesi kosong.
- **Solusi Perbaikan (Fix Applied):**
  Mengubah urutan layer sehingga `auth_middleware` membungkus sub-router (`outer`), lalu `require_admin` menjadi layer `inner`:
  ```rust
  // KODE SETELAH PERBAIKAN:
  let admin_routes = Router::new()
      ...
      .layer(axum::middleware::from_fn(require_admin))
      .layer(from_fn_with_state(config.clone(), auth_middleware));
  ```
  Dengan urutan ini, otentikasi JWT diproses terlebih dahulu sebelum otorisasi peran admin dievaluasi.

---

### Bug #2: *Borrow Checker Lifetime Conflict in Request Extensions* (Kritis)
- **Komponen Terdampak:** `sipamid-backend/src/middleware/role.rs`
- **Tingkat Keparahan:** **Kritis (Compilation Error)**
- **Gejala / Error Log:**
  ```text
  error[E0505]: cannot move out of `request` because it is borrowed
    --> src/middleware/role.rs:21:16
     |
  13 |     let auth = request.extensions().get::<AuthContext>()...
     |                ------- borrow of `request` occurs here
  ...
  21 |     Ok(next.run(request).await)
     |                 ^^^^^^^ move out of `request` occurs here
  ```
- **Akar Masalah (Root Cause):**
  Variabel `auth` meminjam referensi `&request.extensions()`. Compiler Rust mendeteksi bahwa kepemilikan `request` hendak dipindahkan ke pemanggilan `next.run(request)` saat pinjaman memori belum dilepaskan.
- **Solusi Perbaikan (Fix Applied):**
  Mengisolasi peminjaman ekstensi di dalam blok terpisah (*scoped borrow*) dan mengklon nilai string `role`:
  ```rust
  // KODE SETELAH PERBAIKAN:
  let role = {
      let auth = request
          .extensions()
          .get::<AuthContext>()
          .ok_or_else(|| AppError::Unauthorized("Sesi otentikasi tidak ditemukan".to_string()))?;
      auth.claims.role.clone()
  }; // Pinjaman memori request berakhir di sini secara aman

  if role != "admin" {
      return Err(AppError::Forbidden("Akses ditolak: Endpoint ini hanya untuk Admin Desa".to_string()));
  }

  Ok(next.run(request).await)
  ```

---

### Bug #3: *Metode `is_unique_violation` Deprecated pada SQLx 0.7* (Tinggi)
- **Komponen Terdampak:** `src/repositories/user_repo.rs` & `src/repositories/category_repo.rs`
- **Tingkat Keparahan:** **Tinggi (Compatibility Error)**
- **Gejala / Error Log:**
  ```text
  error[E0599]: no method named `is_unique_violation` found for reference `&Box<dyn DatabaseError>`
    --> src/repositories/user_repo.rs:26:28
     |
  26 |     if db_err.is_unique_violation() {
     |               ^^^^^^^^^^^^^^^^^^^ method not found
  ```
- **Akar Masalah (Root Cause):**
  Pada rilis SQLx 0.7, helper `is_unique_violation()` dirombak dan tidak lagi tersedia langsung pada tipe antarmuka `DatabaseError`.
- **Solusi Perbaikan (Fix Applied):**
  Menggunakan pencocokan kode standar internasional PostgreSQL SQLState untuk pelanggaran batasan unik (*unique constraint violation*), yaitu kode `"23505"`:
  ```rust
  // KODE SETELAH PERBAIKAN:
  if let sqlx::Error::Database(ref db_err) = e {
      if db_err.code().as_deref() == Some("23505") {
          return AppError::BadRequest("Username atau Email sudah terdaftar dalam sistem.".to_string());
      }
  }
  ```

---

### Bug #4: *Kompilasi Gagal Akibat Makro `sqlx::query!` Tanpa Database Aktif* (Sedang)
- **Komponen Terdampak:** `src/handlers/dashboard.rs`
- **Tingkat Keparahan:** **Sedang (Build Time Failure)**
- **Gejala / Error Log:**
  ```text
  error: DATABASE_URL must be set, or run 'cargo sqlx prepare'
    --> src/handlers/dashboard.rs:37:16
     |
  37 |     let rows = sqlx::query!( ... ).fetch_all(&state.pool).await?;
     |                ^^^^^^^^^^^^^
  ```
- **Akar Masalah (Root Cause):**
  Makro `sqlx::query!` (dengan tanda seru) memaksa compiler melakukan validasi sintaks SQL langsung ke server PostgreSQL aktif saat proses kompilasi binary dijalankan. Jika compiler dijalankan pada mesin tanpa PostgreSQL berjalan, kompilasi langsung terhenti.
- **Solusi Perbaikan (Fix Applied):**
  Mengubah pemanggilan ke `sqlx::query(...)` runtime dengan pengambilan nilai kolom eksplisit `Row::get`:
  ```rust
  // KODE SETELAH PERBAIKAN:
  let rows = sqlx::query(
      r#"
      SELECT r.report_number, u.name as reporter_name, c.name as category_name,
             r.title, r.location, r.status, TO_CHAR(r.created_at, 'YYYY-MM-DD HH24:MI:SS') as date
      FROM reports r
      JOIN users u ON r.user_id = u.id
      JOIN categories c ON r.category_id = c.id
      ORDER BY r.created_at DESC
      "#
  )
  .fetch_all(&state.pool)
  .await?;
  ```
  Solusi ini menjamin backend dapat dikompilasi dan dibangun (*build*) secara portabel dalam lingkungan Docker maupun pipeline CI/CD.

---

### Bug #5: *UnicodeDecodeError Akibat Berkas Temporary Windows pada Pengujian Frontend* (Rendah)
- **Komponen Terdampak:** `frontend/`
- **Tingkat Keparahan:** **Rendah (Test Environment Anomaly)**
- **Gejala / Error Log:**
  ```text
  UnicodeDecodeError: 'utf-8' codec can't decode byte 0x8d in position 71: invalid start byte
  File: frontend/~$index.html
  ```
- **Akar Masalah (Root Cause):**
  Aplikasi editor di Windows menghasilkan file sementara berformat biner dengan awalan `~$` pada saat membuka file web.
- **Solusi Perbaikan (Fix Applied):**
  Menjalankan skrip sanitasi pembersihan file sampah berawalan `~*` dan memastikan hanya berkas murni `.html`, `.css`, dan `.js` yang diproses oleh test suite dan static server.

---

## 4. Evaluasi 17 Kriteria Penerimaan Produk (PRD Bab 13)

Hasil audit terhadap seluruh Acceptance Criteria yang disyaratkan dalam dokumen PRD:

| No | Kriteria Penerimaan PRD | Hasil yang Diharapkan | Hasil Pengujian Aktual | Status |
|---|---|---|---|:---:|
| 1 | **Registrasi** | Masyarakat dapat membuat akun baru | Form registrasi warga memvalidasi NIK, email, username, dan hashing kata sandi. | **LULUS** |
| 2 | **Login** | Pengguna dapat masuk sesuai peran (role) | Berhasil login multi-role (Masyarakat, Admin Desa, Kepala Desa) dengan JWT. | **LULUS** |
| 3 | **Pengaduan** | Masyarakat dapat mengirim laporan | Form pengaduan menyimpan data judul, deskripsi, kategori, dan lokasi. | **LULUS** |
| 4 | **Upload Foto** | Menerima bukti foto valid (max 5MB) | Validasi MIME type JPG/PNG dan kapasitas file berjalan akurat. | **LULUS** |
| 5 | **Nomor Laporan** | Sistem menerbitkan kode tiket unik | Menerbitkan nomor unik format `LAP-YYYYMM-XXXX`. | **LULUS** |
| 6 | **Verifikasi** | Admin desa dapat memverifikasi laporan | Status beralih menjadi `Diverifikasi` tercatat di audit trail. | **LULUS** |
| 7 | **Penolakan** | Admin dapat menolak disertai alasan | Penolakan mewajibkan isian alasan dan terekam di riwayat. | **LULUS** |
| 8 | **Monitoring** | Status laporan dapat dipantau masyarakat | Warga dapat melihat status real-time melalui nomor tiket atau riwayat. | **LULUS** |
| 9 | **Riwayat Status** | Perubahan status tersimpan kronologis | Tersimpan atomik di tabel `status_history`. | **LULUS** |
| 10 | **Tanggapan** | Admin desa dapat memberi respons | Tanggapan resmi muncul pada halaman pelapor. | **LULUS** |
| 11 | **Dashboard** | Statistik pengaduan tersaji informatif | KPI card, Chart.js kategori & tren, serta peta GIS berfungsi normal. | **LULUS** |
| 12 | **Laporan** | Rekapitulasi dapat diunduh | Fitur ekspor Excel (CSV) dan pratinjau cetak PDF berfungsi sempurna. | **LULUS** |
| 13 | **Keamanan** | Pengguna tidak dapat bypass hak akses | RBAC menolak akses ilegal dengan status HTTP `401` dan `403`. | **LULUS** |
| 14 | **Database** | Data tersimpan konsisten di PostgreSQL | Skema ACID dengan foreign key dan indeks terverifikasi. | **LULUS** |
| 15 | **Identitas Header** | Logo Pemda Lampung & UTI tampil proporsional | **Logo Pemprov Lampung** & **Logo UTI** hadir pada header seluruh halaman web. | **LULUS** |
| 16 | **Footer Wajib** | Teks hak cipta resmi wajib tampil | Seluruh halaman menampilkan teks: `Copyright©2026 by Andira Amellya dan Dr. Erliyan Redy Susanto, M.Kom.` | **LULUS** |
| 17 | **Responsif** | Tampilan ramah smartphone, tablet, PC | Menggunakan layout grid fleksibel Bootstrap 5. | **LULUS** |

---

## 5. Kesimpulan & Rekomendasi

1. **Hasil Pengujian Keseluruhan:**  
   Seluruh 5 (lima) modul pengujian otomatis berhasil dijalankan dengan tingkat kelulusan **100% (All Tests Passed)**. Seluruh *defect* yang terdeteksi pada *middleware routing*, *borrow checker*, *macro SQLx*, dan *database error mapping* telah diperbaiki dan diverifikasi tuntas.
2. **Kesiapan Sistem (System Readiness):**  
   Source code aplikasi **SIPAMID** telah memenuhi seluruh standar akademik UTS PPSI 2026 dan siap dijalankan baik melalui mode lokal tanpa dependensi (*Smart Client-Side Fallback*), container *Docker Compose*, maupun kompilasi mandiri backend *Rust Axum* bersama basis data *PostgreSQL*.

---
*Laporan ini disusun secara resmi sebagai bagian dari luaran dokumen evaluasi mutu perangkat lunak pada Ujian Tengah Semester (UTS) Perencanaan & Pengembangan Sistem Informasi (PPSI) Tahun Akademik 2026.*

