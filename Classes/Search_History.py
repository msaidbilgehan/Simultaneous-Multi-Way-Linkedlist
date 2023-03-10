

from threading import Lock


class Search_History_List_Struct(list):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__lock = Lock()

    def append(self, *args, **kwargs):
        self.__lock.acquire()
        super().append(*args, **kwargs)
        self.__lock.release()

    def __enter__(self):
        self.__lock.acquire()

    def __exit__(self, type, value, traceback):
        self.__lock.release()


class Search_History_Dict_Struct(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__lock = Lock()

    def __setitem__(self, *args, **kwargs):
        self.__lock.acquire()
        super().__setitem__(*args, **kwargs)
        self.__lock.release()

    def __delitem__(self, *args, **kwargs):
        self.__lock.acquire()
        super().__delitem__(*args, **kwargs)
        self.__lock.release()

    def __enter__(self):
        self.__lock.acquire()

    def __exit__(self, type, value, traceback):
        self.__lock.release()
