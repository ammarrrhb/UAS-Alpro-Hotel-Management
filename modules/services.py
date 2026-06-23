"""
Hotel Reservation System - Business Logic Module
"""
from datetime import datetime, date
from typing import Optional, Tuple

from modules.models import Kamar, Tamu, Reservasi
from modules import storage


def hitung_lama_menginap(checkin: date, checkout: date) -> int:
    delta = (checkout - checkin).days
    return max(delta, 1)


def hitung_total_biaya(harga_per_malam: float, jumlah_malam: int) -> float:
    return harga_per_malam * jumlah_malam


def buat_reservasi(
    id_tamu: str,
    nomor_kamar: str,
    tanggal_checkin: date,
    tanggal_checkout: date,
    catatan: str = "",
) -> Tuple[bool, str, Optional[Reservasi]]:
    """
    Create a new reservation.
    Returns (success, message, reservasi_obj)
    """
    # Validate guest
    tamu = storage.cari_tamu(id_tamu)
    if not tamu:
        return False, f"Tamu dengan ID '{id_tamu}' tidak ditemukan.", None

    # Validate room
    kamar = storage.cari_kamar(nomor_kamar)
    if not kamar:
        return False, f"Kamar '{nomor_kamar}' tidak ditemukan.", None

    if kamar.status != "Tersedia":
        return False, f"Kamar {nomor_kamar} sedang {kamar.status}. Tidak dapat direservasi.", None

    # Validate dates
    if tanggal_checkin >= tanggal_checkout:
        return False, "Tanggal check-out harus setelah tanggal check-in.", None

    if tanggal_checkin < date.today():
        return False, "Tanggal check-in tidak boleh di masa lalu.", None

    # Check existing active reservation for room
    existing = storage.reservasi_aktif_kamar(nomor_kamar)
    if existing:
        return False, f"Kamar {nomor_kamar} sudah memiliki reservasi aktif (ID: {existing.id_reservasi}).", None

    jumlah_malam = hitung_lama_menginap(tanggal_checkin, tanggal_checkout)
    total_biaya = hitung_total_biaya(kamar.harga_per_malam, jumlah_malam)

    reservasi = Reservasi(
        id_reservasi=storage.generate_id_reservasi(),
        id_tamu=id_tamu,
        nama_tamu=tamu.nama,
        nomor_kamar=nomor_kamar,
        tipe_kamar=kamar.tipe,
        tanggal_checkin=str(tanggal_checkin),
        tanggal_checkout=str(tanggal_checkout),
        jumlah_malam=jumlah_malam,
        harga_per_malam=kamar.harga_per_malam,
        total_biaya=total_biaya,
        status="Reservasi",
        catatan=catatan,
    )

    storage.simpan_reservasi(reservasi)
    storage.update_status_kamar(nomor_kamar, "Terisi")

    return True, f"Reservasi berhasil dibuat! ID Reservasi: {reservasi.id_reservasi}", reservasi


def proses_checkin(id_reservasi: str) -> Tuple[bool, str]:
    """
    Process check-in for a reservation.
    """
    reservasi = storage.cari_reservasi(id_reservasi)
    if not reservasi:
        return False, f"Reservasi '{id_reservasi}' tidak ditemukan."

    if reservasi.status != "Reservasi":
        return False, f"Reservasi ini tidak dapat di-check-in. Status saat ini: {reservasi.status}"

    reservasi.status = "Check-In"
    storage.simpan_reservasi(reservasi)
    storage.update_status_kamar(reservasi.nomor_kamar, "Terisi")

    return True, f"Check-In berhasil! Tamu {reservasi.nama_tamu} menempati Kamar {reservasi.nomor_kamar}."


def proses_checkout(id_reservasi: str) -> Tuple[bool, str, Optional[Reservasi]]:
    """
    Process check-out for a reservation.
    Returns (success, message, reservasi with final bill)
    """
    reservasi = storage.cari_reservasi(id_reservasi)
    if not reservasi:
        return False, f"Reservasi '{id_reservasi}' tidak ditemukan.", None

    if reservasi.status != "Check-In":
        return False, f"Reservasi ini tidak dapat di-checkout. Status saat ini: {reservasi.status}", None

    reservasi.status = "Check-Out"
    storage.simpan_reservasi(reservasi)
    storage.update_status_kamar(reservasi.nomor_kamar, "Tersedia")

    return True, f"Check-Out berhasil! Total tagihan: Rp {reservasi.total_biaya:,.0f}", reservasi


def batalkan_reservasi(id_reservasi: str) -> Tuple[bool, str]:
    """
    Cancel a reservation.
    """
    reservasi = storage.cari_reservasi(id_reservasi)
    if not reservasi:
        return False, f"Reservasi '{id_reservasi}' tidak ditemukan."

    if reservasi.status not in ("Reservasi",):
        return False, f"Reservasi dengan status '{reservasi.status}' tidak dapat dibatalkan."

    reservasi.status = "Batal"
    storage.simpan_reservasi(reservasi)
    storage.update_status_kamar(reservasi.nomor_kamar, "Tersedia")

    return True, f"Reservasi {id_reservasi} berhasil dibatalkan."


def get_statistik() -> dict:
    """Get dashboard statistics"""
    kamar_list = storage.baca_semua_kamar()
    tamu_list = storage.baca_semua_tamu()
    res_list = storage.baca_semua_reservasi()

    total_kamar = len(kamar_list)
    kamar_tersedia = sum(1 for k in kamar_list if k.status == "Tersedia")
    kamar_terisi = sum(1 for k in kamar_list if k.status == "Terisi")

    total_tamu = len(tamu_list)
    total_reservasi = len(res_list)
    reservasi_aktif = sum(1 for r in res_list if r.status in ("Reservasi", "Check-In"))
    checkin_hari_ini = sum(
        1 for r in res_list
        if r.status == "Check-In" and r.tanggal_checkin == str(date.today())
    )
    checkout_hari_ini = sum(
        1 for r in res_list
        if r.status == "Check-Out" and r.tanggal_checkout == str(date.today())
    )

    total_pendapatan = sum(r.total_biaya for r in res_list if r.status == "Check-Out")

    return {
        "total_kamar": total_kamar,
        "kamar_tersedia": kamar_tersedia,
        "kamar_terisi": kamar_terisi,
        "total_tamu": total_tamu,
        "total_reservasi": total_reservasi,
        "reservasi_aktif": reservasi_aktif,
        "checkin_hari_ini": checkin_hari_ini,
        "checkout_hari_ini": checkout_hari_ini,
        "total_pendapatan": total_pendapatan,
        "occupancy_rate": (kamar_terisi / total_kamar * 100) if total_kamar > 0 else 0,
    }
