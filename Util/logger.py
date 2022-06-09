import logging

class logger:
    def __init__(self):
        path = 'Util/github_rest.log'
        logging.basicConfig(filename=path, filemode='a', level=logging.DEBUG, format='%(asctime)s - %(message)s')

    def write(self, string, mode):
        string = f"{string:^10}"
        if 'f' in mode:
            self.__write_log(string)
        if 'g' in mode:
            self.__write_gui(string)

    def __write_log(self, string):
        logging.info(string)

    def __write_gui(self, string):
        print(string)