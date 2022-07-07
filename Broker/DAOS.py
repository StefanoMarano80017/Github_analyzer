from abc import abstractmethod

from Broker import DB_manager
from Broker import Query_Txt


# Viene generata una classe astratta per facilitare la costruzioni di più operazioni CRUD diverse
class DAO_Astratto:

    @abstractmethod
    def set_data(self, query_id, item: object):
        pass

    @abstractmethod
    def get_data(self, query_id):
        pass


# Questa è la classe DAO e si occupa di gestire le operazioni CRUD sul db
class DAO_Repo(DAO_Astratto):
    def __init__(self, db_file):
        self.db_file = db_file
        self.db = DB_manager.DB(self.db_file)

    # Con questo metodo viene implementato il create repo, ovvero, l'insert repo
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

    # Con questo metodo viene implementato il read repo, ovvero, l'operazione di select repo
    def get_data(self, query_id="select_repo", args=None):
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
            return repos
        except Exception as e:
            raise e


class DAO_link(DAO_Astratto):
    def __init__(self, db_file):
        self.db_file = db_file
        self.db = DB_manager.DB(self.db_file)

    # Con questo metodo viene implementato il read link, ovvero, l'operazione di select link
    def get_data(self, query_id='select_link', args=None) -> list:
        self.db.check_conn()
        query_txt = Query_Txt.read_query(query_id, 'DB')
        links = []
        try:
            if args is None:
                for row in self.db.do_query(query_txt):
                    links.append(row)
            else:
                for row in self.db.do_query(query_txt, args):
                    links.append(row)
            return links
        except Exception as e:
            raise e

    # Con questo metodo viene implementato il create link, ovvero, l'insert link
    def set_data(self, args, query_id="insert_link"):
        self.db.check_conn()
        query_tabella = Query_Txt.read_query("create_links", 'DB')
        query_set = Query_Txt.read_query(query_id, 'DB')

        try:
            self.db.do_query(query_tabella)
            self.db.do_query(query_set, args)
        except Exception as e:
            raise e
        finally:
            self.db.close_connection()


class DAO_stats(DAO_Astratto):
    def __init__(self, db_file):
        self.db_file = db_file
        self.db = DB_manager.DB(self.db_file)

    def set_data(self, args, query_id='insert_stats'):
        self.db.check_conn()
        query_tabella = Query_Txt.read_query("create_stats", 'DB')
        query_set = Query_Txt.read_query(query_id, 'DB')

        try:
            self.db.do_query(query_tabella)
            self.db.do_query(query_set, args)
        except Exception as e:
            raise e
        finally:
            self.db.close_connection()

    def get_data(self, query_id='select_stats', args=None):
        self.db.check_conn()
        query_txt = Query_Txt.read_query(query_id, 'DB')
        links = []
        try:
            if args is None:
                for row in self.db.do_query(query_txt):
                    links.append(row)
            else:
                for row in self.db.do_query(query_txt, args):
                    links.append(row)
            return links
        except Exception as e:
            raise e
