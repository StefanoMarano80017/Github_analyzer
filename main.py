import Broker
import datetime
import DB_manager

def main():

    data = datetime.date(2017, 5, 31)
    broker = Broker.Broker('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', 'prova.db')

    for repo in broker.random_select_repo(150, 4):
        print(repo)
if __name__ == '__main__':
    main()
