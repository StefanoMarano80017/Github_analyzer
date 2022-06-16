import logging
import os
import time

path = 'Util/logs/'


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        else:
            cls._instances[cls].__init__(*args, **kwargs)
        return cls._instances[cls]


class logger(metaclass=Singleton):
    def __init__(self):
        timestr = time.strftime("%Y%m%d-%H%M%S")
        full_path = path + f"{timestr}.log"
        if not os.path.exists(path):
            os.makedirs(path)
        logging.basicConfig(filename=full_path, level=logging.INFO, format='%(asctime)s - %(message)s')

    def write(self, string, mode):
        if 'f' in mode:
            self.__write_log(string)
        if 'g' in mode:
            self.__write_gui(string)

    def __write_log(self, string):
        logging.info(string)

    def __write_gui(self, string):
        print(string)
