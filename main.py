import Broker
import datetime

def main():

    data = datetime.date(2019, 3, 1)
    Broker.repos_to_db('prova.db', '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', data, "java")

    db = DB_manager.DB('prova.db')
    db.create_connection()

    for row in db.do_query("Select * from project"):
        print(row)

if __name__ == '__main__':
    main()
