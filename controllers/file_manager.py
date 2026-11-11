import os


class FileManager:
    """
    Class terpusat untuk menangani operasi I/O file teks (Read & Write)
    menggunakan open(), with, dan try-except.
    """

    @staticmethod
    def pastikan_folder_ada(folder_path="data"):
        """Membuat folder data otomatis jika belum ada tanpa error."""
        if not os.path.exists(folder_path):
            try:
                os.makedirs(folder_path)
            except Exception as e:
                print(
                    f"[Error] Gagal membuat folder {folder_path}: {e}"
                )

    @staticmethod
    def muat_file(nama_file, folder_path="data"):
        """
        Membaca baris-baris data dari file teks.
        - Menggunakan 'with open()' dan 'try-except'.
        - Otomatis membuat file kosong jika file belum ada.
        - Mengembalikan list tuple: [(nomor_baris, isi_baris_bersih), ...]
        """
        FileManager.pastikan_folder_ada(folder_path)
        path = os.path.join(folder_path, nama_file)

        hasil_baris = []
        try:
            with open(path, "r", encoding="utf-8") as f:
                for idx, line in enumerate(f, 1):
                    line = line.strip()
                    # Lewati baris kosong
                    if not line:
                        continue
                    hasil_baris.append((idx, line))

        except FileNotFoundError:
            # Jika file belum ada, buat file baru secara otomatis
            try:
                with open(path, "w", encoding="utf-8") as f:
                    pass
            except Exception as e:
                print(
                    f"[Error] Gagal membuat file baru {nama_file}: {e}"
                )

        except Exception as e:
            print(
                f"[Error] Terjadi kesalahan saat membaca {nama_file}: {e}"
            )

        return hasil_baris

    @staticmethod
    def simpan_file(
        nama_file, daftar_data_str, folder_path="data"
    ):
        """
        Menulis ulang (overwrite) data ke file teks secara permanen.
        - daftar_data_str adalah list berisi string yang sudah diformat (|).
        - Menggunakan 'with open()' dan 'try-except'.
        """
        FileManager.pastikan_folder_ada(folder_path)
        path = os.path.join(folder_path, nama_file)

        try:
            with open(path, "w", encoding="utf-8") as f:
                for baris in daftar_data_str:
                    f.write(str(baris).strip() + "\n")
        except Exception as e:
            print(
                f"[Error] Gagal menyimpan data ke {nama_file}: {e}"
            )

    @staticmethod
    def tambah_baris_file(
        nama_file, baris_data_str, folder_path="data"
    ):
        """
        Menambahkan satu baris data di akhir file (mode append) - Berguna untuk log aktivitas.
        """
        FileManager.pastikan_folder_ada(folder_path)
        path = os.path.join(folder_path, nama_file)

        try:
            with open(path, "a", encoding="utf-8") as f:
                f.write(str(baris_data_str).strip() + "\n")
        except Exception as e:
            print(
                f"[Error] Gagal menambahkan data ke {nama_file}: {e}"
            )
