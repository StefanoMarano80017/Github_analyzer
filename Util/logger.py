import logging
import os
import time
from prettytable import PrettyTable

path = 'Util/logs/'

class logger:
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

