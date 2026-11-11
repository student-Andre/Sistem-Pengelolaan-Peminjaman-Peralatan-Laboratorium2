from controllers import SistemLaboratorium
from data_dummy import buat_kategori, isi_peralatan, isi_mahasiswa, isi_transaksi
from views import jalankan_menu


if __name__ == "__main__":
    lab = SistemLaboratorium(buat_kategori())
    isi_peralatan(lab)
    isi_mahasiswa(lab)
    isi_transaksi(lab)
    jalankan_menu(lab)