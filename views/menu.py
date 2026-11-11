from datetime import datetime

LEBAR = 60


# ==========================================
# 1. FUNGSI UTILITAS & HELPER (TAMPILAN & INPUT)
# ==========================================


def garis(karakter="-"):
    print(karakter * LEBAR)


def cetak_judul(teks):
    print()
    garis("=")
    print(teks.center(LEBAR))
    garis("=")


def sukses(teks):
    print("[OK] " + teks)


def gagal(teks):
    print("[X]  " + teks)


def info(teks):
    print("[i]  " + teks)


def buat_baris(isi, lebar, rata):
    sel = []
    for i, nilai in enumerate(isi):
        sel.append(
            " "
            + format(str(nilai), rata[i] + str(lebar[i]))
            + " "
        )
    return "|" + "|".join(sel) + "|"


def cetak_tabel(kepala, baris, rata=None):
    if rata is None:
        rata = ["<"] * len(kepala)
    lebar = []
    for i, k in enumerate(kepala):
        terpanjang = len(k)
        for b in baris:
            terpanjang = max(terpanjang, len(str(b[i])))
        lebar.append(terpanjang)

    pemisah = (
        "+" + "+".join("-" * (w + 2) for w in lebar) + "+"
    )
    print(pemisah)
    print(buat_baris(kepala, lebar, ["^"] * len(kepala)))
    print(pemisah)
    for b in baris:
        print(buat_baris(b, lebar, rata))
    print(pemisah)


def input_teks(teks):
    while True:
        nilai = input("  " + teks).strip()
        if nilai != "":
            return nilai
        gagal("Tidak boleh kosong")


def input_angka(teks):
    while True:
        nilai = input("  " + teks).strip()
        if nilai.isdigit() and int(nilai) > 0:
            return int(nilai)
        gagal("Masukkan angka lebih dari 0")


def input_durasi(teks):
    while True:
        nilai = input("  " + teks).strip()
        if nilai.isdigit():
            durasi = int(nilai)
            if 1 <= durasi <= 7:
                return durasi
            else:
                gagal(
                    "Durasi peminjaman minimal 1 hari dan maksimal 7 hari!"
                )
        else:
            gagal("Masukkan angka yang valid")


def pilih_kondisi(teks):
    daftar = ["baik", "rusak_ringan", "rusak_berat"]
    print(f"  {teks}")
    print(
        "    [1] baik    [2] rusak_ringan    [3] rusak_berat"
    )
    while True:
        p = input("  Pilih (1-3)   : ").strip()
        if p in ("1", "2", "3"):
            return daftar[int(p) - 1]
        gagal("Pilihan tidak valid")


# ==========================================
# 2. MODUL MAHASISWA (CRUD)
# ==========================================


def tampil_mahasiswa(lab):
    cetak_judul("DAFTAR MAHASISWA")
    if len(lab.data_mahasiswa) == 0:
        info("Belum ada data mahasiswa")
        return
    baris = []
    no = 1
    for m in lab.data_mahasiswa.values():
        status = "AKTIF" if m.is_aktif() else "NONAKTIF"
        baris.append([no, m.nim, m.nama, m.no_hp, status])
        no += 1
    cetak_tabel(
        ["No", "NIM", "Nama", "No HP", "Status"],
        baris,
        [">", "<", "<", "<", "<"],
    )


def menu_tambah_mahasiswa(lab):
    cetak_judul("TAMBAH MAHASISWA")
    nim = input_teks("NIM    : ").upper()
    nama = input_teks("Nama   : ")
    no_hp = input_teks("No HP  : ")
    jumlah_awal = len(lab.data_mahasiswa)
    lab.tambah_mahasiswa(nim, nama, no_hp)
    if len(lab.data_mahasiswa) > jumlah_awal:
        sukses(f"Mahasiswa {nama} berhasil ditambahkan")


def menu_status_mahasiswa(lab):
    cetak_judul("UBAH STATUS MAHASISWA")
    nim = input_teks("NIM : ").upper()
    mhs = lab.data_mahasiswa.get(nim)
    if mhs is None:
        gagal("NIM tidak ditemukan")
        return
    status = "AKTIF" if mhs.is_aktif() else "NONAKTIF"
    info(f"{mhs.nama} saat ini {status}")
    print("    [1] Aktifkan    [2] Nonaktifkan")
    pilih = input("  Pilih : ").strip()
    if pilih == "1":
        mhs.set_status_aktif(True)
        lab.catat_log(
            f"Mahasiswa {mhs.nama} ({nim}) diaktifkan"
        )
        sukses("Status diubah menjadi AKTIF")
    elif pilih == "2":
        mhs.set_status_aktif(False)
        lab.catat_log(
            f"Mahasiswa {mhs.nama} ({nim}) dinonaktifkan"
        )
        sukses("Status diubah menjadi NONAKTIF")
    else:
        gagal("Pilihan tidak valid")


def menu_hapus_mahasiswa(lab):
    cetak_judul("HAPUS MAHASISWA")
    nim = input_teks("NIM yang dihapus : ").upper()
    if nim not in lab.data_mahasiswa:
        gagal("NIM tidak ditemukan")
        return
    if lab.hapus_mahasiswa(nim):
        sukses("Mahasiswa berhasil dihapus")


def menu_cari_mahasiswa(lab):
    cetak_judul("CARI MAHASISWA")
    keyword = input_teks(
        "Kata kunci (NIM / Nama / No HP) : "
    )
    hasil = lab.cari_mahasiswa(keyword)
    print()
    if len(hasil) > 0:
        info(f"Ditemukan {len(hasil)} mahasiswa")
        baris = []
        no = 1
        for m in hasil:
            status = "AKTIF" if m.is_aktif() else "NONAKTIF"
            baris.append(
                [no, m.nim, m.nama, m.no_hp, status]
            )
            no += 1
        cetak_tabel(
            ["No", "NIM", "Nama", "No HP", "Status"],
            baris,
            [">", "<", "<", "<", "<"],
        )
    else:
        info("Mahasiswa tidak ditemukan")


# ==========================================
# 3. MODUL KATEGORI ALAT (CRUD)
# ==========================================


def tampil_kategori(lab):
    baris = []
    for k in lab.data_kategori.values():
        baris.append([k.id_kategori, k.nama_kategori])
    cetak_tabel(["ID", "Nama Kategori"], baris)


# ==========================================
# 4. MODUL PERALATAN & KONDISI (CRUD)
# ==========================================


def tabel_alat(daftar):
    daftar_terurut = sorted(
        daftar,
        key=lambda a: (
            a.kategori.nama_kategori,
            a.nama_alat,
        ),
    )

    baris = []
    for a in daftar_terurut:
        dipinjam = (
            a.stok_total
            - a.stok_tersedia
            - a.jumlah_rusak_ringan
            - a.jumlah_rusak_berat
        )
        baris.append(
            [
                a.kode_alat,
                a.nama_alat,
                a.kategori.nama_kategori,
                a.stok_total,
                a.stok_tersedia,
                dipinjam,
                a.jumlah_rusak_ringan,
                a.jumlah_rusak_berat,
            ]
        )
    cetak_tabel(
        [
            "Kode",
            "Nama Alat",
            "Kategori",
            "Total",
            "Ada",
            "Pinjam",
            "RR",
            "RB",
        ],
        baris,
        ["<", "<", "<", ">", ">", ">", ">", ">"],
    )
    print(
        "Ada = tersedia, RR = rusak ringan, RB = rusak berat"
    )


def tampil_alat(lab, daftar=None):
    if daftar is None:
        daftar = list(lab.data_peralatan.values())
    if len(daftar) == 0:
        info("Data alat tidak ditemukan")
        return
    tabel_alat(daftar)


def menu_cari_alat(lab):
    cetak_judul("CARI ALAT")
    keyword = input_teks(
        "Kata kunci (nama/kode/kategori) : "
    )
    hasil = lab.cari_alat_fleksibel(keyword)
    print()
    if len(hasil) > 0:
        info(f"Ditemukan {len(hasil)} alat")
    tampil_alat(lab, hasil)


def menu_tambah_alat(lab):
    cetak_judul("TAMBAH ALAT")
    tampil_kategori(lab)
    kode = input_teks("Kode alat   : ").upper()
    nama = input_teks("Nama alat   : ")
    id_kategori = input_teks("ID kategori : ").upper()
    stok = input_angka("Stok        : ")
    jumlah_awal = len(lab.data_peralatan)
    lab.tambah_alat(kode, nama, id_kategori, stok)
    if len(lab.data_peralatan) > jumlah_awal:
        sukses(f"Alat {nama} berhasil ditambahkan")


def menu_ubah_kondisi(lab):
    cetak_judul("UBAH KONDISI ALAT")
    kode = input_teks("Kode alat : ").upper()
    alat = lab.data_peralatan.get(kode)
    if alat is None:
        gagal("Kode alat tidak ditemukan")
        return
    tampil_alat(lab, [alat])
    awal = pilih_kondisi("Kondisi awal:")
    baru = pilih_kondisi("Kondisi baru:")
    jumlah = input_angka("Jumlah        : ")
    if alat.ubah_kondisi(awal, baru, jumlah):
        lab.catat_log(
            f"{kode}: {jumlah} unit dari {awal} menjadi {baru}"
        )
        sukses("Kondisi berhasil diubah")
        tampil_alat(lab, [alat])
    else:
        gagal(
            "Gagal mengubah kondisi (cek jumlah atau kondisi)"
        )


def menu_hapus_alat(lab):
    cetak_judul("HAPUS ALAT")
    kode = input_teks("Kode alat yang dihapus : ").upper()
    if kode not in lab.data_peralatan:
        gagal("Kode alat tidak ditemukan")
        return
    if lab.hapus_alat(kode):
        sukses("Alat berhasil dihapus")


# ==========================================
# 5. MODUL TRANSAKSI
# ==========================================


def tampil_satu_transaksi(trx):
    status = trx.status_transaksi.upper()
    if (
        trx.status_transaksi == "dipinjam"
        and datetime.now() > trx.batas_kembali
    ):
        status += " (TERLAMBAT)"
    print(
        f"{trx.id_transaksi}  -  {trx.mahasiswa.nama} ({trx.mahasiswa.nim})"
    )
    print(f"Status        : {status}")
    print(
        f"Tgl pinjam    : {trx.tgl_pinjam.strftime('%d-%m-%Y %H:%M')}"
    )
    print(
        f"Batas kembali : {trx.batas_kembali.strftime('%d-%m-%Y')}"
    )
    baris = []
    for d in trx.daftar_detail:
        sisa = d.jumlah_pinjam - d.jumlah_dikembalikan
        baris.append(
            [
                d.alat.kode_alat,
                d.alat.nama_alat,
                d.jumlah_pinjam,
                d.jumlah_dikembalikan,
                sisa,
                d.kondisi_kembali,
            ]
        )
    cetak_tabel(
        [
            "Kode",
            "Nama Alat",
            "Pinjam",
            "Kembali",
            "Sisa",
            "Kondisi Kembali",
        ],
        baris,
        ["<", "<", ">", ">", ">", "<"],
    )


def tampil_transaksi(lab):
    cetak_judul("DAFTAR TRANSAKSI")
    if len(lab.data_transaksi) == 0:
        info("Belum ada transaksi")
        return
    for trx in lab.data_transaksi.values():
        tampil_satu_transaksi(trx)
        print()


def menu_buat_transaksi(lab):
    cetak_judul("BUAT TRANSAKSI PEMINJAMAN")
    nim = input_teks("NIM peminjam : ").upper()
    if nim not in lab.data_mahasiswa:
        gagal("Mahasiswa tidak ditemukan")
        return

    # Input custom durasi peminjaman (menggunakan input_angka agar valid > 0)
    print()
    durasi = input_durasi(
        "Durasi peminjaman (hari) (Maks 7 Hari): "
    )

    print()
    tampil_alat(lab)
    info(
        "Isi kode alat satu per satu, kosongkan kode jika sudah selesai"
    )
    pinjam = {}
    while True:
        kode = input("  Kode alat    : ").strip().upper()
        if kode == "":
            break
        if kode not in lab.data_peralatan:
            gagal("Kode alat tidak ada")
            continue
        jumlah = input_angka("Jumlah       : ")
        pinjam[kode] = pinjam.get(kode, 0) + jumlah

    # Kirim parameter durasi ke method buat_transaksi
    trx = lab.buat_transaksi(nim, pinjam, durasi)
    if trx is not None:
        print()
        sukses(
            f"Transaksi berhasil dibuat (Batas kembali: {durasi} hari)"
        )
        tampil_satu_transaksi(trx)


def menu_cari_transaksi(lab):
    cetak_judul("CARI TRANSAKSI")
    keyword = input_teks(
        "Kata kunci (ID Transaksi / NIM / Nama) : "
    )
    hasil = lab.cari_transaksi(keyword)
    print()
    if len(hasil) > 0:
        info(f"Ditemukan {len(hasil)} transaksi")
        print()
        for trx in hasil:
            tampil_satu_transaksi(trx)
            print()
    else:
        info("Transaksi tidak ditemukan")


def menu_pengembalian(lab):
    cetak_judul("PROSES PENGEMBALIAN")
    id_trx = input_teks("ID transaksi : ").upper()
    trx = lab.data_transaksi.get(id_trx)
    if trx is None:
        gagal("Transaksi tidak ditemukan")
        return
    print()
    tampil_satu_transaksi(trx)
    if trx.status_transaksi == "selesai":
        info("Transaksi ini sudah selesai")
        return
    kode = input_teks(
        "Kode alat yang dikembalikan : "
    ).upper()
    jumlah = input_angka("Jumlah                      : ")
    kondisi = pilih_kondisi("Kondisi saat kembali:")
    if lab.proses_pengembalian(
        id_trx, kode, jumlah, kondisi
    ):
        print()
        sukses("Pengembalian berhasil dicatat")
        tampil_satu_transaksi(trx)
    else:
        gagal(
            "Pengembalian gagal (cek kode alat dan jumlah)"
        )


# ==========================================
# 6. MODUL LOG AKTIVITAS
# ==========================================


def tampil_log(lab):
    cetak_judul("LOG AKTIVITAS")
    if len(lab.logs) == 0:
        info("Log masih kosong")
        return
    no = 1
    for log in lab.logs:
        print(f"{no:>3}. {log.get_log()}")
        no += 1


def menu_statistik_peminjaman(lab):
    cetak_judul("STATISTIK PEMINJAMAN LABORATORIUM")
    stat = lab.get_statistik_peminjaman()

    # Tampilkan Ringkasan Status Transaksi
    print(" [ RINGKASAN STATUS TRANSAKSI ]")
    print(
        f"   - Transaksi Masih Aktif  : {stat['trx_aktif']}"
    )
    print(
        f"   - Transaksi Telah Selesai: {stat['trx_selesai']}"
    )
    print()

    # Tampilkan Mahasiswa Paling Sering Meminjam
    print(" [ MAHASISWA PALING SERING MEMINJAM ]")
    if len(stat["mhs_teraktif"]) > 0:
        baris_mhs = []
        for i, m in enumerate(
            stat["mhs_teraktif"][:5], 1
        ):  # Ambil top 5
            baris_mhs.append(
                [
                    i,
                    m["nim"],
                    m["nama"],
                    f"{m['total_trx']} kali",
                ]
            )
        cetak_tabel(
            [
                "No",
                "NIM",
                "Nama Mahasiswa",
                "Frekuensi Pinjam",
            ],
            baris_mhs,
            [">", "<", "<", ">"],
        )
    else:
        info("Belum ada data peminjaman mahasiswa.")
    print()

    # Tampilkan Alat yang Paling Sering Dipinjam
    print(" [ ALAT PALING SERING DIPINJAM ]")
    if len(stat["alat_terlaris"]) > 0:
        baris_alat = []
        for i, a in enumerate(
            stat["alat_terlaris"][:5], 1
        ):  # Ambil top 5
            baris_alat.append(
                [i, a["nama"], f"{a['total']!s} unit"]
            )
        cetak_tabel(
            ["No", "Nama Alat", "Total Dipinjam"],
            baris_alat,
            [">", "<", ">"],
        )
    else:
        info("Belum ada data peminjaman alat.")


# ==========================================
# 7. MENU UTAMA & NAVIGASI TERSTRUKTUR (CRUD)
# ==========================================


def tampil_menu(lab):
    transaksi_aktif = 0
    for trx in lab.data_transaksi.values():
        if trx.status_transaksi == "dipinjam":
            transaksi_aktif += 1

    daftar_menu = [
        (
            "DATA MAHASISWA",
            [
                ("1", "Lihat daftar mahasiswa"),
                ("2", "Cari mahasiswa"),  # <-- Menu baru
                ("3", "Tambah mahasiswa"),
                ("4", "Edit mahasiswa"),
                ("5", "Ubah status mahasiswa"),
                ("6", "Hapus mahasiswa"),
            ],
        ),
        (
            "DATA KATEGORI ALAT",
            [
                (
                    "7",
                    "Lihat daftar kategori",
                ),  # <-- Nomor bergeser
                ("8", "Tambah kategori"),
                ("9", "Edit kategori"),
                ("10", "Hapus kategori"),
            ],
        ),
        (
            "DATA PERALATAN",
            [
                ("11", "Lihat daftar alat"),
                ("12", "Cari alat"),
                ("13", "Tambah alat"),
                ("14", "Edit alat"),
                ("15", "Ubah kondisi alat"),
                ("16", "Hapus alat"),
            ],
        ),
        (
            "TRANSAKSI",
            [
                ("17", "Buat peminjaman"),
                ("18", "Proses pengembalian"),
                ("19", "Lihat daftar transaksi"),
                ("20", "Cari transaksi"),
            ],
        ),
        (
            "LAINNYA",
            [
                ("21", "Log aktivitas"),
                ("22", "Statistik peminjaman"),
                ("0", "Keluar"),
            ],
        ),
    ]

    isi = LEBAR - 2
    batas = "+" + "=" * isi + "+"
    print()
    print(batas)
    print(
        "|"
        + "SISTEM PEMINJAMAN PERALATAN LABORATORIUM".center(
            isi
        )
        + "|"
    )
    print(batas)
    ringkasan = (
        f"Mahasiswa: {len(lab.data_mahasiswa)}    Alat: {len(lab.data_peralatan)}"
        f"    Transaksi aktif: {transaksi_aktif}"
    )
    print("|" + ringkasan.center(isi) + "|")
    print("+" + "-" * isi + "+")
    for judul, isi_menu in daftar_menu:
        print(
            "| " + format(judul, "<" + str(isi - 1)) + "|"
        )
        for nomor, nama in isi_menu:
            print(
                "|    "
                + format(
                    f"[{nomor:>2}] {nama}",
                    "<" + str(isi - 3),
                )
                + "|"
            )
        print("+" + "-" * isi + "+")


def jalankan_menu(lab):
    from views.tambah_kategori import menu_tambah_kategori
    from views.edit_kategori import menu_edit_kategori
    from views.hapus_kategori import menu_hapus_kategori
    from views.edit_mahasiswa import menu_edit_mahasiswa
    from views.edit_alat import menu_edit_alat

    while True:
        tampil_menu(lab)
        pilih = input("  Pilih menu : ").strip()

        if pilih == "1":
            tampil_mahasiswa(lab)
        elif pilih == "2":
            menu_cari_mahasiswa(
                lab
            )  # <-- Handler menu baru
        elif pilih == "3":
            menu_tambah_mahasiswa(lab)
        elif pilih == "4":
            menu_edit_mahasiswa(lab)
        elif pilih == "5":
            menu_status_mahasiswa(lab)
        elif pilih == "6":
            menu_hapus_mahasiswa(lab)
        elif pilih == "7":
            cetak_judul("KATEGORI ALAT")
            tampil_kategori(lab)
        elif pilih == "8":
            menu_tambah_kategori(lab)
        elif pilih == "9":
            menu_edit_kategori(lab)
        elif pilih == "10":
            menu_hapus_kategori(lab)
        elif pilih == "11":
            cetak_judul("DAFTAR ALAT")
            tampil_alat(lab)
        elif pilih == "12":
            menu_cari_alat(lab)
        elif pilih == "13":
            menu_tambah_alat(lab)
        elif pilih == "14":
            menu_edit_alat(lab)
        elif pilih == "15":
            menu_ubah_kondisi(lab)
        elif pilih == "16":
            menu_hapus_alat(lab)
        elif pilih == "17":
            menu_buat_transaksi(lab)
        elif pilih == "18":
            menu_pengembalian(lab)
        elif pilih == "19":
            tampil_transaksi(lab)
        elif pilih == "20":
            menu_cari_transaksi(lab)
        elif pilih == "21":
            tampil_log(lab)
        elif pilih == "22":
            menu_statistik_peminjaman(lab)
        elif pilih == "0":
            print()
            info("Terima kasih, program selesai.")
            break
        else:
            gagal("Menu tidak ada")
