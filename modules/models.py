"""
Hotel Reservation System - Data Models (OOP)
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class Kamar:
    """Class representing a hotel room"""
    nomor_kamar: str
    tipe: str          # Standard, Deluxe, Suite
    harga_per_malam: float
    kapasitas: int
    fasilitas: str
    status: str = "Tersedia"   # Tersedia, Terisi, Maintenance

    def to_dict(self) -> dict:
        return {
            "nomor_kamar": self.nomor_kamar,
            "tipe": self.tipe,
            "harga_per_malam": self.harga_per_malam,
            "kapasitas": self.kapasitas,
            "fasilitas": self.fasilitas,
            "status": self.status,
        }

    @staticmethod
    def from_dict(d: dict) -> "Kamar":
        return Kamar(
            nomor_kamar=str(d["nomor_kamar"]),
            tipe=str(d["tipe"]),
            harga_per_malam=float(d["harga_per_malam"]),
            kapasitas=int(d["kapasitas"]),
            fasilitas=str(d["fasilitas"]),
            status=str(d.get("status", "Tersedia")),
        )


@dataclass
class Tamu:
    """Class representing a hotel guest"""
    id_tamu: str
    nama: str
    nik: str
    telepon: str
    email: str
    alamat: str
    tanggal_daftar: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d"))

    def to_dict(self) -> dict:
        return {
            "id_tamu": self.id_tamu,
            "nama": self.nama,
            "nik": self.nik,
            "telepon": self.telepon,
            "email": self.email,
            "alamat": self.alamat,
            "tanggal_daftar": self.tanggal_daftar,
        }

    @staticmethod
    def from_dict(d: dict) -> "Tamu":
        return Tamu(
            id_tamu=str(d["id_tamu"]),
            nama=str(d["nama"]),
            nik=str(d["nik"]),
            telepon=str(d["telepon"]),
            email=str(d["email"]),
            alamat=str(d["alamat"]),
            tanggal_daftar=str(d.get("tanggal_daftar", datetime.now().strftime("%Y-%m-%d"))),
        )


@dataclass
class Reservasi:
    """Class representing a hotel reservation"""
    id_reservasi: str
    id_tamu: str
    nama_tamu: str
    nomor_kamar: str
    tipe_kamar: str
    tanggal_checkin: str
    tanggal_checkout: str
    jumlah_malam: int
    harga_per_malam: float
    total_biaya: float
    status: str = "Reservasi"   # Reservasi, Check-In, Check-Out, Batal
    tanggal_reservasi: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M"))
    catatan: str = ""

    def to_dict(self) -> dict:
        return {
            "id_reservasi": self.id_reservasi,
            "id_tamu": self.id_tamu,
            "nama_tamu": self.nama_tamu,
            "nomor_kamar": self.nomor_kamar,
            "tipe_kamar": self.tipe_kamar,
            "tanggal_checkin": self.tanggal_checkin,
            "tanggal_checkout": self.tanggal_checkout,
            "jumlah_malam": self.jumlah_malam,
            "harga_per_malam": self.harga_per_malam,
            "total_biaya": self.total_biaya,
            "status": self.status,
            "tanggal_reservasi": self.tanggal_reservasi,
            "catatan": self.catatan,
        }

    @staticmethod
    def from_dict(d: dict) -> "Reservasi":
        return Reservasi(
            id_reservasi=str(d["id_reservasi"]),
            id_tamu=str(d["id_tamu"]),
            nama_tamu=str(d["nama_tamu"]),
            nomor_kamar=str(d["nomor_kamar"]),
            tipe_kamar=str(d["tipe_kamar"]),
            tanggal_checkin=str(d["tanggal_checkin"]),
            tanggal_checkout=str(d["tanggal_checkout"]),
            jumlah_malam=int(d["jumlah_malam"]),
            harga_per_malam=float(d["harga_per_malam"]),
            total_biaya=float(d["total_biaya"]),
            status=str(d.get("status", "Reservasi")),
            tanggal_reservasi=str(d.get("tanggal_reservasi", "")),
            catatan=str(d.get("catatan", "")),
        )
