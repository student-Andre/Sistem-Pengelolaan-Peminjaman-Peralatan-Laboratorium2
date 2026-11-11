from views.menu import cetak_judul, gagal, sukses, info, input_teks, input_angka, tampil_kategori


def menu_tambah_kategori(lab):
    cetak_judul("TAMBAH KATEGORI")
    tampil_kategori(lab)
    id_kategori = input_teks("ID kategori baru : ").upper()
    nama = input_teks("Nama kategori    : ")
    if lab.tambah_kategori(id_kategori, nama):
        sukses(f"Kategori {nama} berhasil ditambahkan")
