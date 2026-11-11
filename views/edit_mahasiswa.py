from views.menu import cetak_judul, gagal, sukses, info, input_teks, input_angka, tampil_kategori


def menu_edit_mahasiswa(lab):
    cetak_judul("EDIT MAHASISWA")
    nim = input_teks("NIM yang diedit : ").upper()
    mhs = lab.data_mahasiswa.get(nim)
    if mhs is None:
        gagal("NIM tidak ditemukan")
        return
    info("Kosongkan input jika tidak ingin mengubah")
    nama = input(f"  Nama  [{mhs.nama}] : ").strip()
    no_hp = input(f"  No HP [{mhs.no_hp}] : ").strip()
    if no_hp and not no_hp.isdigit():
        gagal("No HP harus berupa angka")
        return
    if nama == "" and no_hp == "":
        info("Tidak ada perubahan")
        return
    if lab.edit_mahasiswa(nim, nama, no_hp):
        sukses("Data mahasiswa berhasil diubah")
