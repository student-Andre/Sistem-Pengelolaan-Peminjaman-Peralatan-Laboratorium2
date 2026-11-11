from models import Kategori

def buat_kategori():
    return [
        Kategori("K01", "Perangkat Jaringan"),
        Kategori("K02", "IoT dan Mikrokontroler"),
        Kategori("K03", "Komputer dan Aksesori"),
        Kategori("K04", "Multimedia dan Audio Visual"),
    ]


def isi_peralatan(lab):
    # K01: Perangkat Jaringan
    lab.tambah_alat("A001", "Router MikroTik", "K01", 10)
    lab.tambah_alat("A002", "Switch Managed 24-Port", "K01", 5)

    # K02: IoT dan Mikrokontroler
    lab.tambah_alat("A003", "ESP32 NodeMCU", "K02", 15)
    lab.tambah_alat("A004", "Arduino Uno Rev3", "K02", 20)

    # K03: Komputer dan Aksesori
    lab.tambah_alat("A005", "PC Server Workstation", "K03", 4)
    lab.tambah_alat("A006", "Webcam HD 1080p", "K03", 8)

    # K04: Multimedia dan Audio Visual
    lab.tambah_alat("A007", "Proyektor HDMI", "K04", 3)
    lab.tambah_alat("A008", "VR Headset", "K04", 2)
    
def isi_mahasiswa(lab):
    lab.tambah_mahasiswa("M001", "Ahmad Fauzi", "081234567890")
    lab.tambah_mahasiswa("M002", "Siti Rahma", "081298765432")
    lab.tambah_mahasiswa("M003", "Budi Santoso", "081345678901")
    lab.tambah_mahasiswa("M004", "Dewi Lestari", "081567890123")


def isi_transaksi(lab):
    # Ahmad Fauzi meminjam Router MikroTik (2) dan ESP32 (1)
    lab.buat_transaksi("M001", {"A001": 2, "A003": 1})

    # Siti Rahma meminjam Arduino Uno (3)
    lab.buat_transaksi("M002", {"A004": 3})

    # Budi Santoso meminjam Proyektor HDMI (1) dan Webcam HD (2)
    lab.buat_transaksi("M003", {"A007": 1, "A006": 2})