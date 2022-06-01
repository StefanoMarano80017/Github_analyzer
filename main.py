import Broker
import datetime
import DB_manager

def main():

    data = datetime.date(2017, 5, 31)
    broker = Broker.Broker('', 'prova.db')
    broker.repos_to_db(data, 'java')

    db = DB_manager.DB('prova.db')
    db.create_connection()

    for row in db.do_query("Select * from project"):
        print(row)

if __name__ == '__main__':
    main()
