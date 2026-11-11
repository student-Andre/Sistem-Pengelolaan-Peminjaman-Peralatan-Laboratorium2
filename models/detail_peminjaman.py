class DetailPeminjaman:
    def __init__(self, alat, jumlah_pinjam):
        self.__alat = alat
        self.__jumlah_pinjam = jumlah_pinjam
        self.__jumlah_dikembalikan = 0
        self.__kondisi_kembali = "-"
        self.__tanggal_kembali = None

    @property
    def alat(self):
        return self.__alat

    @property
    def jumlah_pinjam(self):
        return self.__jumlah_pinjam

    @property
    def jumlah_dikembalikan(self):
        return self.__jumlah_dikembalikan

    @property
    def kondisi_kembali(self):
        return self.__kondisi_kembali

    @property
    def tanggal_kembali(self):
        return self.__tanggal_kembali

    def proses_pengembalian(self, jumlah, kondisi, tgl):
        if kondisi not in ("baik", "rusak_ringan", "rusak_berat"):
            return False
        sisa = self.__jumlah_pinjam - self.__jumlah_dikembalikan
        if jumlah <= 0 or jumlah > sisa:
            return False

        self.__jumlah_dikembalikan += jumlah
        self.__kondisi_kembali = kondisi
        self.__tanggal_kembali = tgl
        self.__alat.update_stok(jumlah, kondisi)
        return True

    def is_lunas(self):
        return self.__jumlah_dikembalikan == self.__jumlah_pinjam
