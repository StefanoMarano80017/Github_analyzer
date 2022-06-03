import sqlite3


class DB:
    db_file: str

    def __init__(self, db_file):
        self.db_file = db_file
        self.conn = None
        self.conn_alive = False

    def create_connection(self):
        try:
            self.conn = sqlite3.connect(self.db_file)
            self.conn_alive = True
        except Exception as e:
            print("Errore! impossibile stabile connessione")
            self.conn_alive = False

    def close_connection(self):
        self.conn_alive = False
        self.conn.close()

    def check_conn(self):
        if not self.conn_alive:
            return self.create_connection()
        else:
            return self.conn

    def do_query(self, query: str, lista_parametri=None):
        c = None
        try:
            with self.check_conn() as con:
                c = con.cursor()
                if lista_parametri is None:
                    c.execute(query)
                else:
                    c.execute(query, lista_parametri)
        except Exception as e:
            print(e)

        return c

    # probabilmente inutile, utili solo le query
    def create_table(self):
        c = self.conn.cursor()

        create_table_repos = "CREATE TABLE IF NOT EXISTS project(" \
                             "id INTEGER PRIMARY KEY AUTOINCREMENT," \
                             "name text NOT NULL );"

        create_table_user = "CREATE TABLE IF NOT EXISTS user ( " \
                            "id int(20) AUTO_INCREMENT PRIMARY KEY, " \
                            "name varchar(256), " \
                            "email varchar(256), " \
                            "CONSTRAINT namem UNIQUE (name, email) " \
                            ") ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;"

        create_table_user_alias = "CREATE TABLE IF NOT EXISTS user_alias ( " \
                                  "user_id int(20), " \
                                  "alias_id int(20), " \
                                  "CONSTRAINT a UNIQUE (user_id) " \
                                  ") ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;"

        c.execute(create_table_repos)
        # c.execute(create_table_user)
        # c.execute(create_table_user_alias)
