# Sistem Pengelolaan Peminjaman Peralatan Laboratorium

Aplikasi berbasis terminal (Python, Pemrograman Berorientasi Objek) untuk mengelola data mahasiswa, peralatan laboratorium, dan transaksi peminjaman, dibuat berdasarkan UML Class Diagram kelompok.

## Anggota Kelompok

**Kelompok 1**

| Nama | NIM |
|---|---|
| Andre Puji Saputro | K3525020 |
| Dimas Alif Ardiansyah | K3525004 |
| Justin Patrick Lineker | K3525030 |

## Deskripsi Sistem

Sistem membantu petugas laboratorium mencatat siapa meminjam alat apa, kapan harus kembali, dan bagaimana kondisi alat saat dikembalikan.

**Fitur dasar**

- Kelola mahasiswa: tambah, hapus, ubah status aktif/nonaktif, lihat daftar.
- Kelola peralatan: tambah, hapus, lihat daftar berikut kategori dan stok, ubah kondisi alat (baik, rusak ringan, rusak berat).
- Transaksi peminjaman: satu transaksi dapat berisi beberapa alat. Peminjaman ditolak bila alat tidak tersedia atau mahasiswa tidak aktif.
- Pengembalian: dapat sebagian-sebagian, dengan kondisi alat saat kembali. Alat rusak tidak kembali ke stok tersedia. Status transaksi otomatis menjadi `selesai` bila semua alat sudah kembali.
- Penghapusan mahasiswa atau alat ditolak bila masih terkait transaksi yang belum selesai.
- Data dummy: kategori dan peralatan sudah terisi saat aplikasi dibuka (lihat `data_dummy.py`). Mahasiswa dan transaksi diinput pengguna.

**Tantangan**

| Tantangan | Fitur | Menu |
|---|---|---|
| A. Pencarian fleksibel | Cari alat berdasarkan kode, sebagian nama, atau kategori | 9 |
| B. Statistik peminjaman | Alat paling sering dipinjam, mahasiswa paling sering meminjam, jumlah transaksi selesai dan aktif | 16 |
| C. Pemeliharaan peralatan | Alat rusak berat masuk daftar pemeliharaan, setelah diperbaiki kembali ke stok tersedia | 15 |
| D. Log activities | Riwayat aktivitas tersimpan di list, format `[YYYY-MM-DD HH:MM] ...` | 14 |

**Penerapan OOP**

| Konsep | Penerapan |
|---|---|
| Encapsulation | Atribut private (`__nama`) dengan `@property` pada semua class |
| Association | `DetailPeminjaman` ke `Peralatan` |
| Aggregation | `Peralatan` ke `Kategori`, `TransaksiPeminjaman` ke `Mahasiswa` |
| Composition | `TransaksiPeminjaman` membuat dan memiliki `DetailPeminjaman` |
| Dependency | `SistemLaboratorium` mengelola semua class lain |

## Struktur Program

```
lab_peminjaman/
├── README.md
├── main.py                     # titik awal aplikasi
├── data_dummy.py               # kategori dan peralatan awal
├── models/                     # class data sesuai UML
│   ├── __init__.py
│   ├── kategori.py
│   ├── mahasiswa.py
│   ├── log_activity.py
│   ├── peralatan.py
│   ├── detail_peminjaman.py
│   └── transaksi_peminjaman.py
├── controllers/                # logika sistem
│   ├── __init__.py
│   ├── sistem_laboratorium.py  # class SistemLaboratorium
│   └── statistik.py            # perhitungan statistik (tantangan B)
├── views/                      # tampilan menu di terminal
│   ├── __init__.py
│   └── menu.py
├── tests/                      # pengujian
│   ├── skenario_pengujian.py   # 6 skenario wajib + tantangan A-D
│   └── benchmark_skala.py      # pengukuran skala 10.000 alat / 20.000 mahasiswa
└── docs/                       # dokumentasi
    ├── uml_class_diagram.png
    ├── analisis_uml.md
    ├── skenario_pengujian.md
    └── analisis_skalabilitas.md
```

Class sesuai UML ada di `models/` (6 class) dan `controllers/sistem_laboratorium.py` (`SistemLaboratorium`).

## Cara Menjalankan

Kebutuhan: Python 3.8 atau lebih baru. Tidak memerlukan library tambahan.

```bash
# jalankan aplikasi (dari dalam folder lab_peminjaman)
python main.py

# jalankan pengujian 6 skenario wajib + tantangan
python tests/skenario_pengujian.py

# jalankan pengukuran skalabilitas
python tests/benchmark_skala.py
```

Di Windows gunakan `python` atau `py`; di Linux/macOS bisa `python3`.

Alur singkat memakai aplikasi: tambah mahasiswa (menu 1), lihat alat (menu 8), buat peminjaman (menu 11), proses pengembalian (menu 12), lihat transaksi (menu 13).

## Dokumentasi

- [Analisis UML](docs/analisis_uml.md)
- [Skenario pengujian dan hasilnya](docs/skenario_pengujian.md)
- [Analisis skalabilitas](docs/analisis_skalabilitas.md)

## Pembagian Kontribusi Anggota

> Bagian ini perlu diisi kelompok sesuai pembagian kerja yang sebenarnya.

| Anggota | NIM | Kontribusi |
|---|---|---|
| Andre Puji Saputro | K3525020 | _view dan controller_ |
| Dimas Alif Ardiansyah | K3525004 | _main.py, data dummy dan models(mahasiswa sampai transaksi peminjaman)_ |
| Justin Patrick Lineker | K3525030 | _models (init hingga log activity)_ |

Contoh pekerjaan yang bisa dicantumkan: perancangan UML, class di `models/`, class `SistemLaboratorium`, menu dan tampilan (`views/`), fitur tantangan A-D, pengujian skenario, analisis skalabilitas, penulisan README dan dokumentasi.
