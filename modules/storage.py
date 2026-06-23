"""
Hotel Reservation System - Data Storage Manager (CSV-based)
"""
import csv
import os
import uuid
from datetime import datetime
from typing import List, Optional

import pandas as pd

from modules.models import Kamar, Tamu, Reservasi

DATA_DIR = "data"
KAMAR_FILE = os.path.join(DATA_DIR, "kamar.csv")
TAMU_FILE = os.path.join(DATA_DIR, "tamu.csv")
RESERVASI_FILE = os.path.join(DATA_DIR, "reservasi.csv")

KAMAR_FIELDS = ["nomor_kamar", "tipe", "harga_per_malam", "kapasitas", "fasilitas", "status"]
TAMU_FIELDS = ["id_tamu", "nama", "nik", "telepon", "email", "alamat", "tanggal_daftar"]
RESERVASI_FIELDS = [
    "id_reservasi", "id_tamu", "nama_tamu", "nomor_kamar", "tipe_kamar",
    "tanggal_checkin", "tanggal_checkout", "jumlah_malam", "harga_per_malam",
    "total_biaya", "status", "tanggal_reservasi", "catatan"
]


def init_storage():
    """Initialize CSV files if they don't exist"""
    os.makedirs(DATA_DIR, exist_ok=True)

    if not os.path.exists(KAMAR_FILE):
        with open(KAMAR_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=KAMAR_FIELDS)
            writer.writeheader()
        _seed_kamar()

    if not os.path.exists(TAMU_FILE):
        with open(TAMU_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=TAMU_FIELDS)
            writer.writeheader()

    if not os.path.exists(RESERVASI_FILE):
        with open(RESERVASI_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=RESERVASI_FIELDS)
            writer.writeheader()


def _seed_kamar():
    """Seed initial room data"""
    kamar_awal = [
        Kamar("101", "Standard", 350000, 2, "AC, TV, WiFi, Kamar Mandi"),
        Kamar("102", "Standard", 350000, 2, "AC, TV, WiFi, Kamar Mandi"),
        Kamar("103", "Standard", 350000, 2, "AC, TV, WiFi, Kamar Mandi"),
        Kamar("201", "Deluxe", 550000, 2, "AC, TV, WiFi, Kamar Mandi, Balkon, Mini Bar"),
        Kamar("202", "Deluxe", 550000, 2, "AC, TV, WiFi, Kamar Mandi, Balkon, Mini Bar"),
        Kamar("203", "Deluxe", 550000, 3, "AC, TV, WiFi, Kamar Mandi, Balkon, Mini Bar"),
        Kamar("301", "Suite", 900000, 4, "AC, TV, WiFi, Kamar Mandi Mewah, Ruang Tamu, Dapur Mini, Balkon Luas"),
        Kamar("302", "Suite", 900000, 4, "AC, TV, WiFi, Kamar Mandi Mewah, Ruang Tamu, Dapur Mini, Balkon Luas"),
    ]
    for k in kamar_awal:
        simpan_kamar(k)


# ─────────────── KAMAR ───────────────

def baca_semua_kamar() -> List[Kamar]:
    if not os.path.exists(KAMAR_FILE):
        return []
    df = pd.read_csv(KAMAR_FILE, dtype=str)
    return [Kamar.from_dict(row) for _, row in df.iterrows()]


def simpan_kamar(kamar: Kamar):
    kamar_list = baca_semua_kamar()
    kamar_list = [k for k in kamar_list if k.nomor_kamar != kamar.nomor_kamar]
    kamar_list.append(kamar)
    with open(KAMAR_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=KAMAR_FIELDS)
        writer.writeheader()
        for k in sorted(kamar_list, key=lambda x: x.nomor_kamar):
            writer.writerow(k.to_dict())


def hapus_kamar(nomor_kamar: str) -> bool:
    kamar_list = baca_semua_kamar()
    original_len = len(kamar_list)
    kamar_list = [k for k in kamar_list if k.nomor_kamar != nomor_kamar]
    if len(kamar_list) == original_len:
        return False
    with open(KAMAR_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=KAMAR_FIELDS)
        writer.writeheader()
        for k in kamar_list:
            writer.writerow(k.to_dict())
    return True


def cari_kamar(nomor_kamar: str) -> Optional[Kamar]:
    for k in baca_semua_kamar():
        if k.nomor_kamar == nomor_kamar:
            return k
    return None


def update_status_kamar(nomor_kamar: str, status: str):
    kamar = cari_kamar(nomor_kamar)
    if kamar:
        kamar.status = status
        simpan_kamar(kamar)


# ─────────────── TAMU ───────────────

def baca_semua_tamu() -> List[Tamu]:
    if not os.path.exists(TAMU_FILE):
        return []
    df = pd.read_csv(TAMU_FILE, dtype=str)
    return [Tamu.from_dict(row) for _, row in df.iterrows()]


def simpan_tamu(tamu: Tamu):
    tamu_list = baca_semua_tamu()
    tamu_list = [t for t in tamu_list if t.id_tamu != tamu.id_tamu]
    tamu_list.append(tamu)
    with open(TAMU_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=TAMU_FIELDS)
        writer.writeheader()
        for t in tamu_list:
            writer.writerow(t.to_dict())


def hapus_tamu(id_tamu: str) -> bool:
    tamu_list = baca_semua_tamu()
    original_len = len(tamu_list)
    tamu_list = [t for t in tamu_list if t.id_tamu != id_tamu]
    if len(tamu_list) == original_len:
        return False
    with open(TAMU_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=TAMU_FIELDS)
        writer.writeheader()
        for t in tamu_list:
            writer.writerow(t.to_dict())
    return True


def cari_tamu(id_tamu: str) -> Optional[Tamu]:
    for t in baca_semua_tamu():
        if t.id_tamu == id_tamu:
            return t
    return None


def generate_id_tamu() -> str:
    tamu_list = baca_semua_tamu()
    if not tamu_list:
        return "T001"
    nums = []
    for t in tamu_list:
        try:
            nums.append(int(t.id_tamu[1:]))
        except Exception:
            pass
    return f"T{max(nums) + 1:03d}" if nums else "T001"


# ─────────────── RESERVASI ───────────────

def baca_semua_reservasi() -> List[Reservasi]:
    if not os.path.exists(RESERVASI_FILE):
        return []
    df = pd.read_csv(RESERVASI_FILE, dtype=str)
    return [Reservasi.from_dict(row) for _, row in df.iterrows()]


def simpan_reservasi(reservasi: Reservasi):
    res_list = baca_semua_reservasi()
    res_list = [r for r in res_list if r.id_reservasi != reservasi.id_reservasi]
    res_list.append(reservasi)
    with open(RESERVASI_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=RESERVASI_FIELDS)
        writer.writeheader()
        for r in res_list:
            writer.writerow(r.to_dict())


def cari_reservasi(id_reservasi: str) -> Optional[Reservasi]:
    for r in baca_semua_reservasi():
        if r.id_reservasi == id_reservasi:
            return r
    return None


def reservasi_aktif_kamar(nomor_kamar: str) -> Optional[Reservasi]:
    for r in baca_semua_reservasi():
        if r.nomor_kamar == nomor_kamar and r.status in ("Reservasi", "Check-In"):
            return r
    return None


def generate_id_reservasi() -> str:
    res_list = baca_semua_reservasi()
    today = datetime.now().strftime("%Y%m")
    prefix = f"RSV{today}"
    nums = []
    for r in res_list:
        if r.id_reservasi.startswith(prefix):
            try:
                nums.append(int(r.id_reservasi[len(prefix):]))
            except Exception:
                pass
    next_num = max(nums) + 1 if nums else 1
    return f"{prefix}{next_num:03d}"
