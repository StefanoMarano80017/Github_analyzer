import os
import sqlite3


# Questa classe ha il compito di gestire il db
class DB:
    def __init__(self, db_file):
        self.db_file = db_file
        self.backup_name = None
        self.__conn = None


    def check_conn(self):
        try:
            self.__conn.cursor()
            return self.__conn
        except Exception as ex:
            return self.__create_connection()


    def __create_connection(self):
        try:
            self.__conn = sqlite3.connect(self.db_file)
            return self.__conn
        except sqlite3.Error as err:
            raise Exception('[ERRORE] db: ' + str(err))


    # Esecuzione query sul db con o senza parametri
    def do_query(self, query: str, lista_parametri=None):
        c = None
        try:
            with self.check_conn() as conn:
                c = conn.cursor()
                if lista_parametri is None:
                    c.execute(query)
                else:
                    c.execute(query, lista_parametri)
        except sqlite3.Error as err:
            raise err
        finally:
            return c

    # Viene generata una copia in locale nel caso l'utente voglia salvare il db
    def backup_on_file(self, backup_name: str):
        try:
            backup_conn = sqlite3.connect(backup_name)
            db_conn = self.check_conn()
            db_conn.backup(backup_conn, pages=0)
        except sqlite3.Error:
            raise "Errore di backup"

    def delete_db(self):
        os.remove(self.db_file)

