from abc import abstractmethod

from Broker import DB_manager
from Broker import Query_Txt


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
            print(args)
            self.db.do_query(query_tabella)
            self.db.do_query(query_set, args)
        finally:
            self.db.close_connection()

    def get_data(self, query_id="select_repo", args=None):

        self.db.check_conn()
        query_txt = Query_Txt.read_query(query_id, 'DB')
        repos = []
        if args is None:
            for row in self.db.do_query(query_txt):
                repos.append(row)
        else:
            for row in self.db.do_query(query_txt, args):
                repos.append(row)
        return repos


class DAO_link(DAO_Astratto):
    def __init__(self, db_file):
        self.db_file = db_file
        self.db = DB_manager.DB(self.db_file)

    def get_data(self, query_id='select_link', args=None) -> list:
        self.db.check_conn()
        query_txt = Query_Txt.read_query(query_id, 'DB')
        links = []
        if args is None:
            for row in self.db.do_query(query_txt):
                links.append(row)
        else:
            for row in self.db.do_query(query_txt, args):
                links.append(row)
        return links

    def set_data(self, args, query_id="insert_link"):
        self.db.check_conn()
        query_tabella = Query_Txt.read_query("create_links", 'DB')
        query_set = Query_Txt.read_query(query_id, 'DB')

        try:
            self.db.do_query(query_tabella)
            self.db.do_query(query_set, args)
        finally:
            self.db.close_connection()
