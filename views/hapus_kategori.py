from views.menu import cetak_judul, gagal, sukses, info, input_teks, input_angka, tampil_kategori


def menu_hapus_kategori(lab):
    cetak_judul("HAPUS KATEGORI")
    tampil_kategori(lab)
    id_kategori = input_teks("ID kategori yang dihapus : ").upper()
    if id_kategori not in lab.data_kategori:
        gagal("ID kategori tidak ditemukan")
        return
    if lab.hapus_kategori(id_kategori):
        sukses("Kategori berhasil dihapus")
