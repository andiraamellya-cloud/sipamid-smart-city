# SIPAMID - Sistem Informasi Pengaduan Masyarakat dan Monitoring Infrastruktur Desa
### Implementasi Konsep Smart City melalui Smart Governance Desa Berbasis Rust & PostgreSQL

![Provinsi Lampung](frontend/assets/img/logo_lampung.png) &nbsp;&nbsp;&nbsp;&nbsp; ![Universitas Teknokrat Indonesia](frontend/assets/img/logo_teknokrat.jpg)

---

## Informasi Akademik
- **Mata Kuliah:** Perencanaan & Pengembangan Sistem Informasi (PPSI)
- **Tugas:** Ujian Tengah Semester (UTS PPSI) 2026 - Prompt 4 & 5
- **Nama Mahasiswa:** **Andira Amellya**
- **NPM:** **24311065**
- **Kelas:** **SI 23 A**
- **Dosen Pengampu:** **Dr. Erliyan Redy Susanto, M.Kom.**
- **Institusi:** Program Studi S1 Sistem Informasi, Fakultas Teknik dan Ilmu Komputer, Universitas Teknokrat Indonesia
- **Hak Cipta:** `Copyright©2026 by Andira Amellya dan Dr. Erliyan Redy Susanto, M.Kom.`

---

## 1. Deskripsi Proyek & Konsep Smart City
**SIPAMID** adalah platform web responsif berbasis konsep **Smart City** (pendekatan *Smart Governance* dan *Smart Village*) yang menghubungkan masyarakat desa dan pemerintah desa dalam pelaporan serta pemantauan perbaikan infrastruktur publik (seperti jalan rusak, lampu penerangan jalan mati/PJU, drainase tersumbat, penumpukan sampah liar, dan kerusakan fasilitas umum).

Sistem dirancang dengan keamanan memori tinggi dan performa asinkronus menggunakan **Rust**, framework web **Axum**, runtime **Tokio**, database toolkit **SQLx**, basis data relasional **PostgreSQL**, serta antarmuka web modern responsif **HTML5/CSS3 Bootstrap 5** yang dilengkapi visualisasi **Chart.js** dan peta spasial **Leaflet GIS (OpenStreetMap)**.

---

## 2. Struktur Direktori Proyek Lengkap

```text
UTS PPSI_Andira Amellya_24311065_SI 23A/
├── PRD_SIPAMID_Smart_City_Rust_PostgreSQL_2026.pdf   # Dokumen Resmi PRD SIPAMID
├── README.md                                          # Dokumentasi Utama Proyek
├── docker-compose.yml                                 # Orkestrasi Docker (PostgreSQL + Rust Backend)
├── database/                                          # Skrip Basis Data PostgreSQL
│   ├── schema.sql                                     # Skema Database Terpadu
│   ├── seed.sql                                       # Data Awal Pengujian (Users, Kategori, Laporan)
│   └── migrations/                                    # Migrasi Database Sesuai PRD 6.4
│       ├── 001_create_users.sql
│       ├── 002_create_categories.sql
│       ├── 003_create_reports.sql
│       ├── 004_create_attachments.sql
│       ├── 005_create_responses.sql
│       ├── 006_create_status_history.sql
│       └── 007_create_audit_logs.sql
├── sipamid-backend/                                   # Backend Rust Axum Modular Monolith
│   ├── Cargo.toml                                     # Dependensi Rust (Axum, Tokio, SQLx, Argon2, JWT)
│   ├── Dockerfile                                     # Multi-stage Container Rust
│   ├── .env.example                                   # Template Konfigurasi Lingkungan
│   ├── .env                                           # Konfigurasi Aktif
│   ├── README.md                                      # Dokumentasi Teknis Backend
│   ├── uploads/                                       # Penyimpanan Bukti Foto Pengaduan (Max 5MB)
│   ├── tests/                                         # Test Suite Integrasi & Unit Rust
│   │   └── api_tests.rs
│   ├── migrations/                                    # Migrasi SQLx Backend
│   └── src/
│       ├── main.rs                                    # Entry Point & Tokio Async Server
│       ├── lib.rs                                     # Library Exporter
│       ├── config.rs                                  # Handler Environment & Konfigurasi
│       ├── database.rs                                # Inisialisasi PgPool & SQLx Migration
│       ├── routes.rs                                  # Routing REST API (/api/v1) & Static Server
│       ├── errors/
│       │   ├── mod.rs
│       │   └── app_error.rs                           # Penanganan Error Terpusat & HTTP StatusCode
│       ├── models/
│       │   ├── mod.rs
│       │   ├── user.rs                                # Entity & DTO Pengguna (Auth, Profile)
│       │   ├── category.rs                            # Entity & DTO Kategori Infrastruktur
│       │   ├── report.rs                              # Entity & DTO Laporan & Lampiran Foto
│       │   ├── response.rs                            # Entity & DTO Tanggapan Admin
│       │   ├── status_history.rs                      # Entity Audit Status Perubahan Laporan
│       │   └── audit_log.rs                           # Entity Log Aktivitas Sistem
│       ├── repositories/
│       │   ├── mod.rs
│       │   ├── user_repo.rs                           # Operasi Database Tabel users
│       │   ├── category_repo.rs                       # Operasi Database Tabel categories
│       │   ├── report_repo.rs                         # Operasi Database Tabel reports & attachments
│       │   └── response_repo.rs                       # Operasi Database Tabel responses
│       ├── services/
│       │   ├── mod.rs
│       │   ├── auth_service.rs                        # Logika Bisnis Otentikasi & Registrasi
│       │   ├── report_service.rs                      # Logika Bisnis & SOP Validasi Status Pengaduan
│       │   └── dashboard_service.rs                   # Komputasi Statistik & Rekapitulasi Data
│       ├── middleware/
│       │   ├── mod.rs
│       │   ├── auth.rs                                # Ekstraktor & Verifikasi JWT Claims
│       │   └── role.rs                                # RBAC (Admin Desa, Kades, Masyarakat)
│       ├── validators/
│       │   ├── mod.rs
│       │   ├── auth_validator.rs                      # Validasi Kredensial & Format Input
│       │   └── report_validator.rs                    # Validasi Isian Pengaduan
│       └── utils/
│           ├── mod.rs
│           ├── password.rs                            # Enkripsi Sandi Berstandar Argon2id
│           ├── jwt.rs                                 # Pembuatan & Dekode Token JWT
│           └── report_number.rs                       # Generator Nomor Tiket Unik (LAP-YYYYMM-XXXX)
└── frontend/                                          # Antarmuka Pengguna Responsif Bootstrap 5
    ├── assets/
    │   ├── css/
    │   │   └── style.css                              # Desain Tema Smart City Lampung & Teknokrat
    │   ├── js/
    │   │   ├── app.js                                 # State Management, REST API & LocalStorage Fallback
    │   │   ├── charts.js                              # Visualisasi Chart.js Dashboard
    │   │   └── map.js                                 # Peta Interaktif Leaflet.js Infrastruktur Desa
    │   └── img/
    │       ├── logo_lampung.png                       # Logo Resmi Pemerintah Provinsi Lampung
    │       └── logo_teknokrat.jpg                     # Logo Resmi Universitas Teknokrat Indonesia
    ├── index.html                                     # Portal Publik Beranda & Cek Tiket Cepat
    ├── login.html                                     # Halaman Masuk Multi-Role Pengguna
    ├── register.html                                  # Halaman Pendaftaran Akun Warga Baru
    ├── dashboard-masyarakat.html                      # Dashboard Pengaduan Warga Desa
    ├── buat-pengaduan.html                            # Form Pengaduan + Pin Peta + Upload Foto
    ├── riwayat-pengaduan.html                         # Riwayat & Pelacakan Progres Laporan Saya
    ├── detail-pengaduan.html                          # Detail Pengaduan, Foto, Audit Trail & Tanggapan
    ├── profil.html                                    # Pengaturan Profil & Ganti Kata Sandi
    ├── admin-dashboard.html                           # Dashboard Operasional Balai Desa
    ├── admin-pengaduan.html                           # Kelola Status & Verifikasi Pengaduan Masuk
    ├── admin-kategori.html                            # Master Pengelolaan Kategori Infrastruktur
    ├── admin-users.html                               # Manajemen Pengguna & Perangkat Desa
    ├── admin-laporan.html                             # Rekapitulasi, Ekspor Excel (CSV) & Cetak PDF
    └── kades-dashboard.html                           # Executive Dashboard Monitoring Kepala Desa
```

---

## 3. Fitur Utama & Kepatuhan Spesifikasi PRD

1. **Identitas Visual Resmi**:
   - Bagian **Header** pada setiap halaman menampilkan secara proporsional **Logo Pemerintah Provinsi Lampung** dan **Logo Universitas Teknokrat Indonesia**.
   - Bagian **Footer** pada setiap halaman secara konsisten menampilkan teks wajib:  
     `Copyright©2026 by Andira Amellya dan Dr. Erliyan Redy Susanto, M.Kom.`
2. **Keamanan & Otorisasi**:
   - Algoritma hashing kata sandi **Argon2id** (PRD 5.1).
   - Otorisasi berbasis peran (**Role-Based Access Control** / RBAC):
     * **Masyarakat**: Registrasi, Buat Pengaduan, Upload Foto, Pantau Status Laporan Pribadi.
     * **Admin Desa**: Verifikasi Laporan, Perbarui Status, Kirim Tanggapan Resmi, Kelola Kategori & Pengguna.
     * **Kepala Desa**: Dashboard Eksekutif, Pantau Kinerja Penanganan, Unduh Rekapitulasi Laporan.
3. **Standar Operasional Prosedur (SOP) Perubahan Status** (PRD 9.4):
   - `Menunggu Verifikasi` &rarr; `Diverifikasi` (Disetujui admin)
   - `Menunggu Verifikasi` &rarr; `Ditolak` (Wajib disertai alasan penolakan dan dicatat dalam audit trail)
   - `Diverifikasi` &rarr; `Sedang Diproses` (Pengerjaan fisik lapangan dimulai)
   - `Sedang Diproses` &rarr; `Selesai` (Infrastruktur tuntas diperbaiki)
   - Setiap perubahan status dicatat secara atomik dalam transaksi basis data ke tabel `status_history`.
4. **Monitoring Spasial (Smart City GIS)**:
   - Integrasi peta interaktif **Leaflet.js + OpenStreetMap** untuk menandai lokasi kerusakan fisik secara visual.

---

## 4. Cara Menjalankan Aplikasi

### Opsi 1: Menjalankan Antarmuka Frontend Secara Langsung (Zero Configuration)
Frontend SIPAMID telah dilengkapi dengan lapisan data pintar (*Smart Fallback Layer*) menggunakan `LocalStorage` dan simulasi REST API. Anda dapat langsung menguji seluruh fitur antarmuka tanpa perlu menginstal compiler atau database:
1. Buka folder `frontend/`.
2. Klik ganda file `index.html` pada browser modern (Google Chrome, Edge, Firefox, Safari).
3. Anda dapat langsung mencoba registrasi, login cepat dengan role akun pengujian, mengirim pengaduan dengan titik peta, verifikasi admin, hingga mencetak laporan eksekutif.

### Opsi 2: Menjalankan Menggunakan Docker Compose (Satu Perintah)
Pastikan Docker dan Docker Compose telah terpasang pada komputer Anda:
```bash
docker compose up --build
```
- Basis data PostgreSQL akan otomatis aktif pada port `5432`.
- Backend Rust Axum akan dikompilasi dan melayani API serta frontend pada port `8080`.
- Akses website di: `http://localhost:8080`.

### Opsi 3: Menjalankan Manual Backend Rust & PostgreSQL
1. **Inisialisasi Database PostgreSQL**:
   ```sql
   CREATE DATABASE sipamid_db;
   ```
   Eksekusi file skrip inisialisasi:
   ```bash
   psql -U postgres -d sipamid_db -f database/schema.sql
   psql -U postgres -d sipamid_db -f database/seed.sql
   ```
2. **Kompilasi & Jalankan Backend**:
   ```bash
   cd sipamid-backend
   cargo test
   cargo run --release
   ```
   Server aktif dan melayani antarmuka pada `http://127.0.0.1:8080`.

---

## 5. Kredensial Akun Pengujian (Demo Akun)

| Peran (Role) | Username | Password | Deskripsi Pengguna |
|---|---|---|---|
| **Warga / Masyarakat** | `andira` | `password123` | Andira Amellya (NPM 24311065) - Pelapor |
| **Warga / Masyarakat** | `budi_santoso` | `password123` | Budi Santoso - Warga Dusun 1 |
| **Admin Balai Desa** | `admin_desa` | `password123` | Petugas Verifikator & Teknis Operasional |
| **Kepala Desa** | `kades_desa` | `password123` | Bapak H. Supriyanto (Kepala Desa Natar) |

---

## 6. Hak Cipta & Lisensi
Copyright©2026 by Andira Amellya dan Dr. Erliyan Redy Susanto, M.Kom.  
Program Studi Sistem Informasi, Universitas Teknokrat Indonesia.  
Hak Cipta Dilindungi Undang-Undang.

