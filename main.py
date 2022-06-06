import datetime
import time

from Unit_elaborazione import Controller


def main():
    start_time = time.time()
    data = datetime.date(2019, 3, 12)
    c = Controller.Controller(token='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', db_file=':memory:')
    c.get_git_data(data, 'java')
    print("--- %s seconds ---" % (time.time() - start_time))


if __name__ == '__main__':
    main()
