from views.menu import cetak_judul, gagal, sukses, info, input_teks, input_angka, tampil_kategori
from views.menu import tampil_alat


def menu_edit_alat(lab):
    cetak_judul("EDIT ALAT")
    kode = input_teks("Kode alat yang diedit : ").upper()
    alat = lab.data_peralatan.get(kode)
    if alat is None:
        gagal("Kode alat tidak ditemukan")
        return
    tampil_alat(lab, [alat])
    print()
    tampil_kategori(lab)
    info("Kosongkan input jika tidak ingin mengubah")
    nama = input(f"  Nama alat            [{alat.nama_alat}] : ").strip()
    id_kategori = input(f"  ID kategori          [{alat.kategori.id_kategori}] : ").strip().upper()
    stok_txt = input(f"  Stok total           [{alat.stok_total}] : ").strip()
    stok = None
    if stok_txt != "":
        if not (stok_txt.isdigit() and int(stok_txt) > 0):
            gagal("Stok harus angka lebih dari 0")
            return
        stok = int(stok_txt)
    if lab.edit_alat(kode, nama, id_kategori, stok):
        sukses("Data alat berhasil diubah")
        tampil_alat(lab, [alat])
