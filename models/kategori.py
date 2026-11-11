class Kategori:
    def __init__(self, id_kategori, nama_kategori):
        self.__id_kategori = id_kategori
        self.__nama_kategori = nama_kategori

    @property
    def id_kategori(self):
        return self.__id_kategori

    @property
    def nama_kategori(self):
        return self.__nama_kategori

    def get_info(self):
        return f"{self.__id_kategori} - {self.__nama_kategori}"

    def set_nama(self, nama_baru):
        self.__nama_kategori = nama_baru
