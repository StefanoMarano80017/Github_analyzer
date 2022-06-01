from abc import abstractmethod

import DB_manager
import Query_Txt


class DAO_Astratto:

    @abstractmethod
    def set_data(self, query_id, item: object):
        pass

    @abstractmethod
    def get_data(self, query_id):
        pass


class DAO_Repo(DAO_Astratto):
    def __init__(self, db_file):
        self.db_file = db_file
        self.db = DB_manager.DB(self.db_file)

    def set_data(self, item, args, query_id="prova") -> None:

        self.db.check_conn()

        #query_tabella = Query_Txt.read_query(query_id, 'DB')
        query_set = Query_Txt.read_query(query_id, 'DB')

        # Qui codice per settare parametri della query
        # usa cur.execute("insert into test(d, ts) values (?, ?)", (today, now))
        # lista = [nome = repo.name, id = repo.id ....e così via]
        # eseguo query, deve essere un insert di un singolo elemento

        try:
            self.db.create_table()
            self.db.do_query(query_set, args)
        except Exception as e:
            raise e
        finally:
            self.db.close_connection()

    def get_data(self, query_id="nome default"):
        self.db.check_conn()

        query_txt = "Select * from project"
        repos = []
        try:
            for row in self.db.do_query(query_txt):
                repos.append(row)
        except Exception as e:
            print(e)

        return repos
