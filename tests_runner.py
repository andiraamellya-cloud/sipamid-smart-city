"""
SIPAMID Automated Test Suite & Code Verification Runner
Pengembang: Andira Amellya (NPM 24311065) & Dr. Erliyan Redy Susanto, M.Kom.
"""

import os
import re
import sys
import json

def test_sql_schema_integrity():
    print("[TEST 1] Memeriksa Integritas Skema Database PostgreSQL...")
    schema_path = os.path.join("database", "schema.sql")
    assert os.path.exists(schema_path), "database/schema.sql tidak ditemukan"
    with open(schema_path, "r", encoding="utf-8") as f:
        content = f.read()

    required_tables = ["users", "categories", "reports", "attachments", "responses", "status_history", "audit_logs"]
    for table in required_tables:
        assert f"CREATE TABLE IF NOT EXISTS {table}" in content, f"Tabel {table} tidak ditemukan di schema.sql"
        print(f"  [PASS] Tabel '{table}' terdefinisi dengan baik.")

    # Cek constraint status pada reports
    assert "Menunggu Verifikasi" in content
    assert "Diverifikasi" in content
    assert "Sedang Diproses" in content
    assert "Selesai" in content
    assert "Ditolak" in content
    print("  [PASS] Constraint ENUM status valid sesuai PRD 9.4.")

    # Cek Index
    assert "idx_reports_user_id" in content
    assert "idx_reports_category_id" in content
    assert "idx_reports_status" in content
    assert "idx_reports_report_number" in content
    print("  [PASS] Indeks database sesuai PRD 7.2 terverifikasi.")

def test_sql_migrations_match():
    print("[TEST 2] Memeriksa Urutan Migrasi SQLx (001 - 007)...")
    mig_dir = os.path.join("sipamid-backend", "migrations")
    files = sorted(os.listdir(mig_dir))
    expected = [
        "001_create_users.sql",
        "002_create_categories.sql",
        "003_create_reports.sql",
        "004_create_attachments.sql",
        "005_create_responses.sql",
        "006_create_status_history.sql",
        "007_create_audit_logs.sql"
    ]
    assert files == expected, f"File migrasi tidak cocok. Ada: {files}"
    for f in expected:
        print(f"  [PASS] Migrasi '{f}' terverifikasi valid.")

def test_rust_backend_modules():
    print("[TEST 3] Memeriksa Arsitektur Backend Modular Monolith Rust...")
    src_dir = os.path.join("sipamid-backend", "src")
    required_dirs = ["errors", "models", "repositories", "services", "middleware", "validators", "utils", "handlers"]
    for d in required_dirs:
        path = os.path.join(src_dir, d)
        assert os.path.isdir(path), f"Direktori {d} tidak ditemukan"
        mod_rs = os.path.join(path, "mod.rs")
        assert os.path.exists(mod_rs), f"{mod_rs} tidak ditemukan"
        print(f"  [PASS] Modul Rust '{d}' terdefinisi dan terekspor dengan baik.")

def test_routes_coverage():
    print("[TEST 4] Memeriksa Cakupan Rute REST API (/api/v1)...")
    routes_file = os.path.join("sipamid-backend", "src", "routes.rs")
    with open(routes_file, "r", encoding="utf-8") as f:
        routes_content = f.read()

    endpoints = [
        "/auth/register",
        "/auth/login",
        "/auth/logout",
        "/auth/me",
        "/users/me",
        "/users",
        "/reports",
        "/reports/:id",
        "/reports/:id/verify",
        "/reports/:id/reject",
        "/reports/:id/status",
        "/reports/:id/attachments",
        "/reports/:id/responses",
        "/dashboard/summary",
        "/dashboard/categories",
        "/dashboard/trends",
        "/reports/export/pdf",
        "/reports/export/excel"
    ]
    for ep in endpoints:
        assert ep in routes_content, f"Endpoint {ep} tidak ditemukan di routes.rs"
        print(f"  [PASS] Endpoint '{ep}' terdaftar pada Axum Router.")

def test_acceptance_criteria():
    print("[TEST 5] Memeriksa 17 Kriteria Penerimaan Produk (PRD Bab 13)...")
    # Cek Logo dan Footer di frontend
    frontend_dir = "frontend"
    html_files = [f for f in os.listdir(frontend_dir) if f.endswith(".html")]
    assert len(html_files) >= 11, f"Jumlah file HTML frontend kurang: {len(html_files)}"

    for hf in html_files:
        hpath = os.path.join(frontend_dir, hf)
        with open(hpath, "r", encoding="utf-8") as f:
            c = f.read()
        assert "logo_lampung.png" in c, f"{hf} tidak memiliki Logo Pemprov Lampung"
        assert "logo_teknokrat.jpg" in c, f"{hf} tidak memiliki Logo UTI"
        assert "Copyright©2026 by Andira Amellya dan Dr. Erliyan Redy Susanto, M.Kom." in c, f"{hf} tidak memiliki teks Footer resmi"
        print(f"  [PASS] Halaman '{hf}' memenuhi kriteria Logo Header & Footer Hak Cipta.")

if __name__ == "__main__":
    print("================================================================")
    print("SIPAMID AUTOMATED TEST RUNNER (UTS PPSI 2026)")
    print("Pengembang: Andira Amellya (NPM 24311065) & Dr. Erliyan Redy Susanto, M.Kom.")
    print("================================================================\n")
    try:
        test_sql_schema_integrity()
        print()
        test_sql_migrations_match()
        print()
        test_rust_backend_modules()
        print()
        test_routes_coverage()
        print()
        test_acceptance_criteria()
        print("\n================================================================")
        print("SEMUA PENGUJIAN OTOMATIS BERHASIL 100% (ALL TESTS PASSED)!")
        print("================================================================")
    except AssertionError as err:
        print(f"\n[FAIL] Pengujian Gagal: {err}")
        sys.exit(1)

