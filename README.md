# 🏨 Hotel Telkoms — Sistem Reservasi Hotel

Sistem manajemen reservasi hotel berbasis Python + Streamlit dengan tampilan UI modern.

## 📋 Fitur Lengkap

| No | Fitur | Status |
|----|-------|--------|
| 1 | Login Admin (autentikasi) | ✅ |
| 2 | Kelola Data Kamar (CRUD) | ✅ |
| 3 | Kelola Data Tamu | ✅ |
| 4 | Reservasi Kamar | ✅ |
| 5 | Proses Check-In | ✅ |
| 6 | Proses Check-Out + Invoice | ✅ |
| 7 | Perhitungan Biaya Menginap | ✅ |
| 8 | Riwayat Reservasi | ✅ |
| 9 | Penyimpanan CSV | ✅ |
| 10 | Validasi Input & Error Handling | ✅ |
| 11 | Fungsi Terpisah (Modular) | ✅ |
| 12 | List/Dictionary untuk Data | ✅ |
| 13 | OOP (Class Kamar, Tamu, Reservasi) | ✅ |

## 🗂️ Struktur Proyek

```
hotel_system/
├── app.py                  # Main Streamlit app (UI + routing)
├── requirements.txt        # Dependencies
├── data/                   # CSV data storage
│   ├── kamar.csv
│   ├── tamu.csv
│   └── reservasi.csv
└── modules/
    ├── __init__.py
    ├── models.py           # OOP: Class Kamar, Tamu, Reservasi
    ├── storage.py          # CRUD operations (CSV-based)
    ├── services.py         # Business logic (reservasi, check-in, dll)
    └── auth.py             # Autentikasi admin
```

## 🚀 Cara Menjalankan

### 1. Jalankan Aplikasi
```bash
streamlit run app.py
```

### 2. Buka Browser
Otomatis terbuka di `http://localhost:8501`

## 🔐 Akun Login

| Username | Password | Role |
|----------|----------|------|
| `admin` | `hotel123` | Administrator |
| `manager` | `manager456` | Manager Hotel |
| `resepsionis` | `resep789` | Resepsionis |

## 💡 Alur Penggunaan

1. **Login** → Masuk dengan akun admin
2. **Tambah Tamu** → Daftarkan data tamu via menu Kelola Tamu
3. **Buat Reservasi** → Pilih tamu + kamar + tanggal di menu Reservasi
4. **Check-In** → Konfirmasi kedatangan tamu
5. **Check-Out** → Proses kepulangan + cetak invoice
6. **Riwayat** → Lihat semua histori transaksi

## 📊 Data Kamar Default

| No. Kamar | Tipe | Harga/Malam |
|-----------|------|-------------|
| 101–103 | Standard | Rp 350.000 |
| 201–203 | Deluxe | Rp 550.000 |
| 301–302 | Suite | Rp 900.000 |
