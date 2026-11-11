from datetime import datetime

from models import (
    Kategori,
    Mahasiswa,
    Peralatan,
    TransaksiPeminjaman,
    LogActivity,
)


class SistemLaboratorium:
    def __init__(self, daftar_kategori=None):
        self.__data_mahasiswa = {}
        self.__data_peralatan = {}
        self.__data_kategori = {}
        self.__data_transaksi = {}
        self.__logs = []

        if daftar_kategori:
            for k in daftar_kategori:
                self.__data_kategori[k.id_kategori] = k

    @property
    def data_mahasiswa(self):
        return self.__data_mahasiswa

    @property
    def data_kategori(self):
        return self.__data_kategori

    @property
    def data_peralatan(self):
        return self.__data_peralatan

    @property
    def data_transaksi(self):
        return self.__data_transaksi

    @property
    def logs(self):
        return self.__logs

    def tambah_mahasiswa(self, nim, nama, no_hp):
        if nim in self.__data_mahasiswa:
            print("[X]  NIM sudah terdaftar")
            return
        self.__data_mahasiswa[nim] = Mahasiswa(
            nim, nama, no_hp
        )
        self.catat_log(f"Tambah mahasiswa {nama} ({nim})")

    def hapus_mahasiswa(self, nim):
        if nim not in self.__data_mahasiswa:
            return False
        for trx in self.__data_transaksi.values():
            if (
                trx.mahasiswa.nim == nim
                and trx.status_transaksi == "dipinjam"
            ):
                print(
                    "[X]  Mahasiswa masih punya peminjaman yang belum selesai"
                )
                return False
        nama = self.__data_mahasiswa[nim].nama
        del self.__data_mahasiswa[nim]
        self.catat_log(f"Hapus mahasiswa {nama} ({nim})")
        return True

    def edit_mahasiswa(self, nim, nama_baru, no_hp_baru):
        mhs = self.__data_mahasiswa.get(nim)
        if mhs is None:
            print("[X]  NIM tidak ditemukan")
            return False
        if nama_baru:
            mhs.set_nama(nama_baru)
        if no_hp_baru:
            mhs.set_no_hp(no_hp_baru)
        self.catat_log(f"Edit mahasiswa {mhs.nama} ({nim})")
        return True

    def cari_mahasiswa(self, keyword):
        keyword = keyword.lower()
        hasil = []
        for mhs in self.data_mahasiswa.values():
            if (
                keyword in mhs.nim.lower()
                or keyword in mhs.nama.lower()
                or keyword in mhs.no_hp.lower()
            ):
                hasil.append(mhs)
        return hasil

    def tambah_kategori(self, id_kategori, nama):
        if id_kategori in self.__data_kategori:
            print("[X]  ID kategori sudah ada")
            return False
        for k in self.__data_kategori.values():
            if k.nama_kategori.lower() == nama.lower():
                print("[X]  Nama kategori sudah ada")
                return False
        self.__data_kategori[id_kategori] = Kategori(
            id_kategori, nama
        )
        self.catat_log(
            f"Tambah kategori {nama} ({id_kategori})"
        )
        return True

    def edit_kategori(self, id_kategori, nama_baru):
        kategori = self.__data_kategori.get(id_kategori)
        if kategori is None:
            print("[X]  Kategori tidak ditemukan")
            return False
        for k in self.__data_kategori.values():
            if (
                k is not kategori
                and k.nama_kategori.lower()
                == nama_baru.lower()
            ):
                print("[X]  Nama kategori sudah ada")
                return False
        lama = kategori.nama_kategori
        kategori.set_nama(nama_baru)
        self.catat_log(
            f"Edit kategori {id_kategori}: {lama} menjadi {nama_baru}"
        )
        return True

    def hapus_kategori(self, id_kategori):
        kategori = self.__data_kategori.get(id_kategori)
        if kategori is None:
            return False
        for alat in self.__data_peralatan.values():
            if alat.kategori.id_kategori == id_kategori:
                print(
                    "[X]  Kategori masih dipakai oleh alat "
                    + alat.nama_alat
                )
                return False
        del self.__data_kategori[id_kategori]
        self.catat_log(
            f"Hapus kategori {kategori.nama_kategori} ({id_kategori})"
        )
        return True

    def edit_alat(
        self, kode, nama_baru, id_kategori_baru, stok_baru
    ):
        alat = self.__data_peralatan.get(kode)
        if alat is None:
            print("[X]  Kode alat tidak ditemukan")
            return False
        kategori = None
        if id_kategori_baru:
            kategori = self.__data_kategori.get(
                id_kategori_baru
            )
            if kategori is None:
                print("[X]  Kategori tidak ditemukan")
                return False
        if (
            stok_baru is not None
            and not alat.set_stok_total(stok_baru)
        ):
            print(
                "[X]  Stok total baru lebih kecil dari jumlah alat yang sedang dipinjam"
            )
            return False
        if nama_baru:
            alat.set_nama(nama_baru)
        if kategori is not None:
            alat.set_kategori(kategori)
        self.catat_log(
            f"Edit alat {alat.nama_alat} ({kode})"
        )
        return True

    def tambah_alat(self, kode, nama, id_kategori, stok):
        if id_kategori not in self.__data_kategori:
            print("[X]  Kategori tidak ditemukan")
            return
        if kode in self.__data_peralatan:
            print("[X]  Kode alat sudah ada")
            return
        kategori = self.__data_kategori[id_kategori]
        self.__data_peralatan[kode] = Peralatan(
            kode, nama, kategori, stok
        )
        self.catat_log(
            f"Tambah alat {nama} ({kode}) stok {stok}"
        )

    def hapus_alat(self, kode):
        if kode not in self.__data_peralatan:
            return False
        for trx in self.__data_transaksi.values():
            if trx.status_transaksi == "dipinjam":
                for detail in trx.daftar_detail:
                    if detail.alat.kode_alat == kode:
                        print(
                            "[X]  Alat masih ada di peminjaman yang belum selesai"
                        )
                        return False
        nama = self.__data_peralatan[kode].nama_alat
        del self.__data_peralatan[kode]
        self.catat_log(f"Hapus alat {nama} ({kode})")
        return True

    def buat_transaksi(
        self, nim, list_alat_pinjam, durasi_hari=7
    ):
        mhs = self.__data_mahasiswa.get(nim)
        if mhs is None or not mhs.is_aktif():
            print(
                "[X]  Mahasiswa tidak ditemukan atau tidak aktif"
            )
            return None
        if len(list_alat_pinjam) == 0:
            print("[X]  Alat yang dipinjam masih kosong")
            return None

        for kode, jumlah in list_alat_pinjam.items():
            alat = self.__data_peralatan.get(kode)
            if alat is None or not alat.is_tersedia(jumlah):
                print(f"[X]  Alat {kode} tidak tersedia")
                return None

        id_trx = "TRX" + str(
            len(self.__data_transaksi) + 1
        ).zfill(3)

        # Kirim durasi_hari ke constructor TransaksiPeminjaman
        transaksi = TransaksiPeminjaman(
            id_trx, mhs, durasi_hari
        )
        for kode, jumlah in list_alat_pinjam.items():
            transaksi.tambah_detail(
                self.__data_peralatan[kode], jumlah
            )

        self.__data_transaksi[id_trx] = transaksi
        self.catat_log(
            f"Transaksi {id_trx} dibuat oleh {mhs.nama} (Durasi: {durasi_hari} hari)"
        )
        return transaksi

    def cari_transaksi(self, keyword):
        keyword = keyword.lower()
        hasil = []
        for trx in self.data_transaksi.values():
            if (
                keyword in trx.id_transaksi.lower()
                or keyword in trx.mahasiswa.nim.lower()
                or keyword in trx.mahasiswa.nama.lower()
            ):
                hasil.append(trx)
        return hasil

    def proses_pengembalian(
        self, id_transaksi, kode_alat, jumlah, kondisi
    ):
        transaksi = self.__data_transaksi.get(id_transaksi)
        if transaksi is None:
            return False

        for detail in transaksi.daftar_detail:
            if detail.alat.kode_alat == kode_alat:
                berhasil = detail.proses_pengembalian(
                    jumlah, kondisi, datetime.now()
                )
                if berhasil:
                    status = (
                        transaksi.update_status_transaksi()
                    )
                    self.catat_log(
                        f"{id_transaksi}: {kode_alat} x{jumlah} kembali ({kondisi}), status {status}"
                    )
                return berhasil
        return False

    def cari_alat_fleksibel(self, keyword):
        keyword = keyword.lower()
        hasil = []
        for alat in self.__data_peralatan.values():
            if (
                keyword in alat.nama_alat.lower()
                or keyword in alat.kode_alat.lower()
                or keyword
                in alat.kategori.nama_kategori.lower()
            ):
                hasil.append(alat)
        return hasil

    def get_statistik_peminjaman(self):
        # 1. Menghitung jumlah transaksi aktif dan selesai
        trx_aktif = 0
        trx_selesai = 0
        for trx in self.data_transaksi.values():
            if trx.status_transaksi.lower() == "dipinjam":
                trx_aktif += 1
            elif trx.status_transaksi.lower() == "selesai":
                trx_selesai += 1

        # 2. Menghitung alat yang paling sering dipinjam berdasarkan detail transaksi
        frekuensi_alat = {}
        for trx in self.data_transaksi.values():
            for d in trx.daftar_detail:
                kode_alat = d.alat.kode_alat
                nama_alat = d.alat.nama_alat
                jumlah = d.jumlah_pinjam
                if kode_alat not in frekuensi_alat:
                    frekuensi_alat[kode_alat] = {
                        "nama": nama_alat,
                        "total": 0,
                    }
                frekuensi_alat[kode_alat]["total"] += jumlah

        # Urutkan alat berdasarkan total peminjaman terbanyak
        alat_terlaris = sorted(
            frekuensi_alat.values(),
            key=lambda x: x["total"],
            reverse=True,
        )

        # 3. Menghitung mahasiswa yang paling sering meminjam
        frekuensi_mhs = {}
        for trx in self.data_transaksi.values():
            nim = trx.mahasiswa.nim
            nama = trx.mahasiswa.nama
            if nim not in frekuensi_mhs:
                frekuensi_mhs[nim] = {
                    "nama": nama,
                    "nim": nim,
                    "total_trx": 0,
                }
            frekuensi_mhs[nim]["total_trx"] += 1

        # Urutkan mahasiswa berdasarkan jumlah transaksi terbanyak
        mhs_teraktif = sorted(
            frekuensi_mhs.values(),
            key=lambda x: x["total_trx"],
            reverse=True,
        )

        return {
            "trx_aktif": trx_aktif,
            "trx_selesai": trx_selesai,
            "alat_terlaris": alat_terlaris,
            "mhs_teraktif": mhs_teraktif,
        }

    def catat_log(self, aktivitas):
        self.__logs.append(LogActivity(aktivitas))
