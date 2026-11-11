from datetime import datetime


class LogActivity:
    def __init__(self, aktivitas):
        self.__timestamp = datetime.now()
        self.__aktivitas = aktivitas

    def get_log(self):
        waktu = self.__timestamp.strftime("%d-%m-%Y %H:%M:%S")
        return f"[{waktu}] {self.__aktivitas}"
