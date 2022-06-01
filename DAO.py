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

    def set_data(self, args, query_id="insert_repo") -> None:

        self.db.check_conn()
        query_tabella = Query_Txt.read_query("create_repo", 'DB')
        query_set = Query_Txt.read_query(query_id, 'DB')

        try:
            self.db.do_query(query_tabella)
            self.db.do_query(query_set, args)
        except Exception as e:
            raise e
        finally:
            self.db.close_connection()

    def get_data(self, query_id="select_repo", args = None):

        self.db.check_conn()
        query_txt = Query_Txt.read_query(query_id, 'DB')

        repos = []
        try:
            if args is None:
                for row in self.db.do_query(query_txt):
                    repos.append(row)
            else:
                for row in self.db.do_query(query_txt, args):
                    repos.append(row)
        except Exception as e:
            e = "DAO exception" + e
            print(e)

        return repos
