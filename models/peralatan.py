class Peralatan:
    def __init__(self, kode_alat, nama_alat, kategori, stok_total):
        self.__kode_alat = kode_alat
        self.__nama_alat = nama_alat
        self.__kategori = kategori
        self.__stok_total = stok_total
        self.__stok_tersedia = stok_total
        self.__jumlah_rusak_ringan = 0
        self.__jumlah_rusak_berat = 0

    @property
    def kode_alat(self):
        return self.__kode_alat

    @property
    def nama_alat(self):
        return self.__nama_alat

    @property
    def kategori(self):
        return self.__kategori

    @property
    def stok_total(self):
        return self.__stok_total

    @property
    def stok_tersedia(self):
        return self.__stok_tersedia

    @property
    def jumlah_rusak_ringan(self):
        return self.__jumlah_rusak_ringan

    @property
    def jumlah_rusak_berat(self):
        return self.__jumlah_rusak_berat

    def is_tersedia(self, jumlah):
        return jumlah > 0 and self.__stok_tersedia >= jumlah

    def update_stok(self, jumlah, kondisi):
        if kondisi == "pinjam":
            self.__stok_tersedia -= jumlah
        elif kondisi == "baik":
            self.__stok_tersedia += jumlah
        elif kondisi == "rusak_ringan":
            self.__jumlah_rusak_ringan += jumlah
        elif kondisi == "rusak_berat":
            self.__jumlah_rusak_berat += jumlah

    def ubah_kondisi(self, kondisi_awal, kondisi_baru, jumlah):
        if kondisi_awal == kondisi_baru:
            return False
        if kondisi_baru not in ("baik", "rusak_ringan", "rusak_berat"):
            return False

        if kondisi_awal == "baik" and self.__stok_tersedia >= jumlah:
            self.__stok_tersedia -= jumlah
        elif kondisi_awal == "rusak_ringan" and self.__jumlah_rusak_ringan >= jumlah:
            self.__jumlah_rusak_ringan -= jumlah
        elif kondisi_awal == "rusak_berat" and self.__jumlah_rusak_berat >= jumlah:
            self.__jumlah_rusak_berat -= jumlah
        else:
            return False

        self.update_stok(jumlah, kondisi_baru)
        return True

    def set_nama(self, nama_baru):
        self.__nama_alat = nama_baru

    def set_kategori(self, kategori_baru):
        self.__kategori = kategori_baru

    def set_stok_total(self, stok_baru):
        selisih = stok_baru - self.__stok_total
        if stok_baru <= 0 or self.__stok_tersedia + selisih < 0:
            return False
        self.__stok_total = stok_baru
        self.__stok_tersedia += selisih
        return True
