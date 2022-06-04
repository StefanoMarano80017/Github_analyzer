import datetime
import os
from Broker import Broker
from Unit_elaborazione import Controller

def main():
    b = Broker.Broker(token='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', db_file='Util/prova.db')
    c = Controller.Controller(token='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', db_file='Util/prova.db')

    #b.print_table_link()

    c.repo_cloc()
    print('fine elaborazione')

    #links = b.get_link_repo('60104635')
    #for link in links:
     #    print(type(link[1]))

if __name__ == '__main__':
    main()


