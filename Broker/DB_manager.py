import os
import sqlite3


# Questa classe ha il compito di gestire il db
class DB:
    def __init__(self, db_file):
        self.db_file = db_file
        self.backup_name = None
        self.conn = None
        self.conn_alive = False

    # Viene creata la connessione
    def create_connection(self):
        try:
            self.conn = sqlite3.connect(self.db_file)
            self.conn_alive = True
        except sqlite3.Error as err:
            print("Errore! impossibile stabile connessione")
            print(err)
            self.conn_alive = False

    # Viene Chiusa la connessione
    def close_connection(self):
        self.conn_alive = False
        self.conn.close()

    # Controllo stato Connessione
    def check_conn(self):
        if not self.conn_alive:
            return self.create_connection()
        else:
            return self.conn

    # Esecuzione query sul db con o senza parametri
    def do_query(self, query: str, lista_parametri=None):
        c = None
        try:
            with self.check_conn() as con:
                c = con.cursor()
                if lista_parametri is None:
                    c.execute(query)
                else:
                    c.execute(query, lista_parametri)
        except sqlite3.Error as err:
            raise err
        return c

    # Viene generata una copia in locale nel caso l'utente voglia salvare il db
    def backup_on_file(self, backup_name: str):
        # existing DB
        ram_con = self.check_conn()
        # copy into this DB
        back_con = sqlite3.connect(backup_name)
        self.backup_name = backup_name

        try:
            with back_con:
                ram_con.backup(back_con, pages=0)
            print("backup successful")
        except sqlite3.Error as e:
            print("Errore di backup: ", e)
        finally:
            if back_con:
                back_con.close()
                ram_con.close()

    def delete_db(self):
        os.remove(self.db_file)
