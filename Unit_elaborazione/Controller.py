from Datas import Broker
from Unit_elaborazione.AbstractElaborazione import AbstractElaborazione

class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        else:
            cls._instances[cls].__init__(*args, **kwargs)
        return cls._instances[cls]


# La classe controller ha il compito di coordinare le funzioni di analisi sui repository
class Controller(metaclass=Singleton):
    def __init__(self, token=None, db_file=None, logger=None):
        self.broker = None
        self.token = token
        self.db_file = db_file
        self.log = logger
        self.ElabList = list()


    """
        OPERAZIONI DI GESTIONE ELABORAZIONI
    """
    def set_param(self, token:str, db:str):
        self.token = token
        self.db_file = db

    def AttachElab(self, Elab: AbstractElaborazione):
        if Elab is not None:
            self.ElabList.append(Elab)
        else:
            raise 'Elab is None'

    def DoElaborazione(self, ElabName, RepoList) -> list:
        if ElabName is not None:
            for Elab in self.ElabList:
                if Elab.GetName() == ElabName:
                    return Elab.DoElaborazione(RepoList)
            raise "ELab inesistente"
        else:
            raise "Elabname None"

    """
        OPERAZIONI DI GESTIONE DATI 
    """
    def Get_repo_list(self):

        RepoList = list()
        with ContextBroker(self.token, self.db_file, self.log) as b:
            repos = b.get_repo()
            if repos is not None:
                for repo in repos:
                    links = b.get_link_repo(repo[0])
                    RepoList.append([repo, links])
                return RepoList
            else:
                return None


    def Get_repos(self):
        with ContextBroker(self.token, self.db_file, self.log) as b:
            return b.get_repo()

    # eseguo query su git e salvo i dati sul db
    def get_git_data(self, query_string: str, size_max):
        with ContextBroker(self.token, self.db_file, self.log) as b:
            try:
                b.do_search(query_string, size_max)
            except Exception as e:
                if str(e) == 'token errato':
                    self.log.write('[ERRORE] Token di accesso errato', 'g')
                if str(e) == 'limite':
                    self.log.write('[ERRORE] Rate Limit superato, attendere del tempo', 'g')
                if str(e) == "name 'github' is not defined":
                    self.log.write('[ERRORE] Impossibile collegarsi a Github', 'g')
                else:
                    self.log.write('[ERRORE] ' + str(e), 'g')


    def __stats_to_db(self, tag, data, repo_id = 0):
        with ContextBroker(self.token, self.db_file, self.log) as b:
            args = (None, repo_id, tag, data)
            b.stats_to_db(args)

    """
        OPERAZIONI DI GESTIONE FILE
    """
    def close(self):
        try:
            with ContextBroker(self.token, self.db_file, self.log) as b:
                b.delete_db()
        except Exception as e:
            self.log.write('[ERRORE] problemi in chiusura file' + str(e), 'f+g')

    def backup(self, backup_file):
        try:
            with ContextBroker(self.token, self.db_file, self.log) as b:
                b.backup(backup_file)
        except Exception as e:
            self.log.write('[ERRORE] problemi in salvataggio file' + str(e), 'f+g')


"""
    CONTEXT MANAGER BROKER PER IL MULTI THREADING
"""
class ContextBroker():
    def __init__(self, token, db_file, log):
        self.__token = token
        self.__db = db_file
        self.__log = log
        self.broker = None

    def __enter__(self):
        self.broker = Broker.Broker(self.__token, self.__db, self.__log)
        return self.broker

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.broker = None
