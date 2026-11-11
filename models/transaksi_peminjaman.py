from datetime import datetime, timedelta
from models.detail_peminjaman import DetailPeminjaman


class TransaksiPeminjaman:
    def __init__(
        self, id_transaksi, mahasiswa, durasi_hari=7
    ):
        self.__id_transaksi = id_transaksi
        self.__mahasiswa = mahasiswa
        self.__daftar_detail = []
        self.__tgl_pinjam = datetime.now()
        self.__durasi_hari = (
            durasi_hari  # Menyimpan durasi custom
        )
        self.__batas_kembali = self.hitung_batas_kembali()
        self.__status_transaksi = "dipinjam"

    @property
    def id_transaksi(self):
        return self.__id_transaksi

    @property
    def mahasiswa(self):
        return self.__mahasiswa

    @property
    def daftar_detail(self):
        return self.__daftar_detail

    @property
    def tgl_pinjam(self):
        return self.__tgl_pinjam

    @property
    def batas_kembali(self):
        return self.__batas_kembali

    @property
    def status_transaksi(self):
        return self.__status_transaksi

    def hitung_batas_kembali(self):
        # Menghitung batas kembali berdasarkan durasi custom (dalam hari)
        return self.__tgl_pinjam + timedelta(
            days=self.__durasi_hari
        )

    def tambah_detail(self, alat, jumlah):
        if not alat.is_tersedia(jumlah):
            return False
        detail = DetailPeminjaman(alat, jumlah)
        self.__daftar_detail.append(detail)
        alat.update_stok(jumlah, "pinjam")
        return True

    def update_status_transaksi(self):
        lunas = True
        for d in self.__daftar_detail:
            if not d.is_lunas():
                lunas = False
        if lunas:
            self.__status_transaksi = "selesai"
        else:
            self.__status_transaksi = "dipinjam"
        return self.__status_transaksi
