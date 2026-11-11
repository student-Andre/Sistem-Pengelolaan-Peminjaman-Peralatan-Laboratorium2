import os
from datetime import datetime

from models import (
    Kategori,
    Mahasiswa,
    Peralatan,
    TransaksiPeminjaman,
    LogActivity,
)

from controllers.file_manager import FileManager
from data_dummy import (
    buat_kategori,
    isi_peralatan,
    isi_mahasiswa,
    isi_transaksi,
)


class SistemLaboratorium:
    def __init__(self, daftar_kategori=None):
        self.__data_mahasiswa = {}
        self.__data_peralatan = {}
        self.__data_kategori = {}
        self.__data_transaksi = {}
        self.__logs = []
        self.data_dir = "data"

        # 1. Pastikan folder data ada
        FileManager.pastikan_folder_ada(self.data_dir)

        # 2. Cek apakah seluruh file utama (termasuk transaksi & detail) sudah lengkap dan tidak kosong
        path_mhs = os.path.join(
            self.data_dir, "mahasiswa.txt"
        )
        path_kat = os.path.join(
            self.data_dir, "kategori.txt"
        )
        path_alt = os.path.join(self.data_dir, "alat.txt")
        path_trx = os.path.join(
            self.data_dir, "transaksi.txt"
        )
        path_det = os.path.join(
            self.data_dir, "detail_transaksi.txt"
        )

        file_belum_lengkap = (
            not os.path.exists(path_mhs)
            or os.path.getsize(path_mhs) == 0
            or not os.path.exists(path_kat)
            or os.path.getsize(path_kat) == 0
            or not os.path.exists(path_alt)
            or os.path.getsize(path_alt) == 0
            or not os.path.exists(path_trx)
            or os.path.getsize(path_trx) == 0
            or not os.path.exists(path_det)
            or os.path.getsize(path_det) == 0
        )

        if file_belum_lengkap:
            print(
                "[Info] Data file teks belum lengkap atau kosong. Mengisi data awal dari data_dummy.py..."
            )

            # Masukkan kategori awal
            if daftar_kategori:
                for k in daftar_kategori:
                    self.__data_kategori[k.id_kategori] = k
                self.simpan_data_kategori()
            else:
                for k in buat_kategori():
                    self.__data_kategori[k.id_kategori] = k
                self.simpan_data_kategori()

            # Panggil fungsi dummy untuk mengisi seluruh file teks secara otomatis (termasuk transaksi)
            isi_peralatan(self)
            isi_mahasiswa(self)
            isi_transaksi(self)

            # Catat log awal bahwa sistem diinisialisasi dari dummy
            self.catat_log(
                "Sistem diinisialisasi dengan data dummy awal."
            )
            print(
                "[Info] Data awal (Mahasiswa, Kategori, Alat, Transaksi, Detail) berhasil disimpan permanen!"
            )
        else:
            if daftar_kategori:
                for k in daftar_kategori:
                    self.__data_kategori[k.id_kategori] = k
            self.muat_semua_data()

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

    def muat_semua_data(self):
        """Memuat seluruh data dari folder data/ ke dalam memori aplikasi."""
        # 1. Memuat Data Mahasiswa dari mahasiswa.txt
        # Format file: NIM|nama|no_hp
        data_mhs = FileManager.muat_file("mahasiswa.txt")
        for idx, line in data_mhs:
            parts = line.split("|")
            if len(parts) >= 3:
                nim, nama, no_hp = (
                    parts[0].strip(),
                    parts[1].strip(),
                    parts[2].strip(),
                )
                self.__data_mahasiswa[nim] = Mahasiswa(
                    nim, nama, no_hp
                )
            else:
                print(
                    f"[Peringatan] Format tidak valid pada mahasiswa.txt baris {idx}, baris dilewati."
                )
        # 2. Load Kategori (Format: id_kategori|nama_kategori)
        data_kat = FileManager.muat_file("kategori.txt")
        for idx, line in data_kat:
            parts = line.split("|")
            if len(parts) >= 2:
                id_kat, nama_kat = (
                    parts[0].strip(),
                    parts[1].strip(),
                )
                self.__data_kategori[id_kat] = Kategori(
                    id_kat, nama_kat
                )
            else:
                print(
                    f"[Peringatan] Format tidak valid pada kategori.txt baris {idx}, baris dilewati."
                )

        # 3. Load Alat (Format: kode_alat|nama_alat|id_kategori|stok_total|stok_tersedia)
        data_alt = FileManager.muat_file("alat.txt")
        for idx, line in data_alt:
            parts = line.split("|")
            if len(parts) >= 5:
                (
                    kode,
                    nama,
                    id_kat,
                    stok_total,
                    stok_tersedia,
                ) = (
                    parts[0].strip(),
                    parts[1].strip(),
                    parts[2].strip(),
                    int(parts[3].strip()),
                    int(parts[4].strip()),
                )
                kategori = self.__data_kategori.get(id_kat)
                if kategori:
                    alat = Peralatan(
                        kode, nama, kategori, stok_total
                    )
                    # Sesuaikan jika class Peralatan memiliki atribut stok tersedia tersendiri
                    self.__data_peralatan[kode] = alat
            else:
                print(
                    f"[Peringatan] Format tidak valid pada alat.txt baris {idx}, baris dilewati."
                )

        # 4. Load Transaksi Peminjaman (Format: id_transaksi|nim|tgl_pinjam|batas_kembali|status_transaksi)
        data_trx = FileManager.muat_file("transaksi.txt")
        for idx, line in data_trx:
            parts = line.split("|")
            if len(parts) >= 5:
                (
                    id_trx,
                    nim,
                    tgl_pinjam,
                    batas_kembali,
                    status_trx,
                ) = (
                    parts[0].strip(),
                    parts[1].strip(),
                    parts[2].strip(),
                    parts[3].strip(),
                    parts[4].strip(),
                )
                mhs = self.__data_mahasiswa.get(nim)
                if mhs:
                    # Inisialisasi objek transaksi (sesuaikan parameter dengan class Anda)
                    transaksi = TransaksiPeminjaman(
                        id_trx, mhs
                    )
                    transaksi.tgl_pinjam = tgl_pinjam
                    transaksi.batas_kembali = batas_kembali
                    transaksi.status_transaksi = status_trx
                    self.__data_transaksi[id_trx] = (
                        transaksi
                    )
            else:
                print(
                    f"[Peringatan] Format tidak valid pada transaksi.txt baris {idx}, baris dilewati."
                )

        # 5. Load Detail Transaksi (Format: id_transaksi|kode_alat|jumlah_pinjam|status_detail|kondisi_kembali|tgl_kembali)
        data_det = FileManager.muat_file(
            "detail_transaksi.txt"
        )
        for idx, line in data_det:
            parts = line.split("|")
            if len(parts) >= 6:
                (
                    id_trx,
                    kode_alat,
                    jumlah,
                    status_det,
                    kondisi,
                    tgl_kmb,
                ) = (
                    parts[0].strip(),
                    parts[1].strip(),
                    int(parts[2].strip()),
                    parts[3].strip(),
                    parts[4].strip(),
                    parts[5].strip(),
                )
                transaksi = self.__data_transaksi.get(
                    id_trx
                )
                alat = self.__data_peralatan.get(kode_alat)

                if transaksi and alat:
                    # Masukkan detail ke dalam transaksi yang sesuai
                    transaksi.tambah_detail_muat(
                        alat,
                        jumlah,
                        status_det,
                        kondisi,
                        tgl_kmb,
                    )
            else:
                print(
                    f"[Peringatan] Format tidak valid pada detail_transaksi.txt baris {idx}, baris dilewati."
                )
        # (Nanti Anda bisa menambahkan pemuatan alat.txt dan transaksi.txt di sini dengan pola serupa)

    def simpan_data_mahasiswa(self):
        """Menyimpan seluruh dictionary mahasiswa ke file mahasiswa.txt"""
        daftar_str = []
        for mhs in self.__data_mahasiswa.values():
            baris = f"{mhs.nim}|{mhs.nama}|{mhs.no_hp}"
            daftar_str.append(baris)
        FileManager.simpan_file("mahasiswa.txt", daftar_str)

    def simpan_data_kategori(self):
        """Menyimpan seluruh data kategori ke file kategori.txt"""
        daftar_str = []
        for kat in self.__data_kategori.values():
            baris = f"{kat.id_kategori}|{kat.nama_kategori}"
            daftar_str.append(baris)
        FileManager.simpan_file("kategori.txt", daftar_str)

    def simpan_data_alat(self):
        """Menyimpan seluruh data peralatan ke file alat.txt"""
        daftar_str = []
        for alat in self.__data_peralatan.values():
            # Sesuaikan dengan atribut yang ada pada class Peralatan Anda
            baris = f"{alat.kode_alat}|{alat.nama_alat}|{alat.kategori.id_kategori}|{alat.stok_total}|{alat.stok_tersedia if hasattr(alat, 'stok_tersedia') else alat.stok_total}"
            daftar_str.append(baris)
        FileManager.simpan_file("alat.txt", daftar_str)

    def simpan_data_transaksi(self):
        """Menyimpan seluruh data transaksi ke file transaksi.txt"""
        daftar_str = []
        for trx in self.__data_transaksi.values():
            # Format: id_transaksi|nim|tgl_pinjam|batas_kembali|status_transaksi
            baris = f"{trx.id_transaksi}|{trx.mahasiswa.nim}|{trx.tgl_pinjam}|{trx.batas_kembali}|{trx.status_transaksi}"
            daftar_str.append(baris)
        FileManager.simpan_file("transaksi.txt", daftar_str)

    def simpan_data_detail_transaksi(self):
        """Menyimpan seluruh detail transaksi ke file detail_transaksi.txt"""
        daftar_str = []
        for trx in self.__data_transaksi.values():
            for detail in trx.daftar_detail:
                # Format: id_transaksi|kode_alat|jumlah_pinjam|status_detail|kondisi_kembali|tgl_kembali
                tgl_kmb = (
                    detail.tanggal_kembali
                    if detail.tanggal_kembali
                    else "-"
                )
                kondisi = (
                    detail.kondisi_kembali
                    if detail.kondisi_kembali
                    else "-"
                )
                status_det = (
                    detail.status 
                    if hasattr(detail, 'status') 
                    else "dipinjam"
                )
                
                baris = f"{trx.id_transaksi}|{detail.alat.kode_alat}|{detail.jumlah_pinjam}|{status_det}|{kondisi}|{tgl_kmb}"
                daftar_str.append(baris)
        FileManager.simpan_file(
            "detail_transaksi.txt", daftar_str
        )

    def tambah_mahasiswa(self, nim, nama, no_hp):
        if nim in self.__data_mahasiswa:
            print("[X]  NIM sudah terdaftar")
            return False

        self.__data_mahasiswa[nim] = Mahasiswa(
            nim, nama, no_hp
        )

        # Simpan perubahan secara permanen ke file teks
        self.simpan_data_mahasiswa()
        self.catat_log(f"Tambah mahasiswa {nama} ({nim})")
        return True

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

        # Perbarui file teks setelah penghapusan
        self.simpan_data_mahasiswa()
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

        # Perbarui file teks setelah pengeditan
        self.simpan_data_mahasiswa()
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

        # Simpan permanen ke file kategori.txt
        self.simpan_data_kategori()

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

        # Simpan permanen ke file kategori.txt
        self.simpan_data_kategori()

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

        # Simpan permanen ke file kategori.txt
        self.simpan_data_kategori()

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

        # Simpan permanen ke file alat.txt
        self.simpan_data_alat()

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

        # Simpan permanen ke file alat.txt
        self.simpan_data_alat()

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

        # Simpan permanen ke file alat.txt
        self.simpan_data_alat()

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

        # Simpan otomatis ke file teks secara permanen (Transaksi, Detail, dan Stok Alat)
        self.simpan_data_transaksi()
        self.simpan_data_detail_transaksi()
        self.simpan_data_alat()  # Memperbarui stok alat yang berkurang

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

                    # Simpan otomatis perubahan status ke file teks
                    self.simpan_data_transaksi()
                    self.simpan_data_detail_transaksi()
                    self.simpan_data_alat()  # Memperbarui stok alat jika kondisi baik kembali tersedia

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
        """Menambahkan log aktivitas baru dan menyimpannya secara permanen."""
        log_baru = LogActivity(aktivitas)
        self.__logs.append(log_baru)

        # Opsional: Jika ingin log tersimpan ke file 'log.txt' secara permanen
        daftar_str = [log.get_log() for log in self.__logs]
        FileManager.simpan_file("log.txt", daftar_str)
