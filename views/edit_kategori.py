from views.menu import cetak_judul, gagal, sukses, info, input_teks, input_angka, tampil_kategori


def menu_edit_kategori(lab):
    cetak_judul("EDIT KATEGORI")
    tampil_kategori(lab)
    id_kategori = input_teks("ID kategori yang diedit : ").upper()
    kategori = lab.data_kategori.get(id_kategori)
    if kategori is None:
        gagal("ID kategori tidak ditemukan")
        return
    nama_baru = input_teks(f"Nama baru [{kategori.nama_kategori}] : ")
    if lab.edit_kategori(id_kategori, nama_baru):
        sukses("Kategori berhasil diubah")
