import datetime

from Broker import Broker


def main():
    data = datetime.date(2016, 4, 5)
    b = Broker.Broker(token='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', db_file='prova.db')

    b.repos_to_db(data, 'java')

    b.print_table_link()


if __name__ == '__main__':
    main()
