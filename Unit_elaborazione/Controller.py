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
        self.__token = token
        self.__db_file = db_file
        self.__log = logger
        self.__ElabList = list()

    """
        OPERAZIONI DI GESTIONE ELABORAZIONI
    """

    def set_param(self, token: str, db: str):
        self.__token = token
        self.__db_file = db

    def AttachElab(self, Elab:AbstractElaborazione):
        if Elab is not None:
            self.__ElabList.append(Elab)
        else:
            raise Exception('Elab is None')

    def DoElaborazione(self, ElabName:str, RepoList):
        if ElabName is not None:
            for Elab in self.__ElabList:
                if Elab.GetName() == ElabName:
                    res = Elab.DoElaborazione(RepoList)
                    self.__log.write('[INFO] Salvataggio elab', 'g')
                    self.__stats_to_db(res=res, tag=ElabName)
                    return res
            raise Exception('ELaborazione Inesistente')
        else:
            raise Exception('Nome Elaborazione Nullo')

    """
        OPERAZIONI DI GESTIONE DATI 
    """

    def Get_repo_list(self):
        RepoList = list()
        with ContextBroker(self.__token, self.__db_file, self.__log) as b:
            repos = b.get_repo()
            if repos is not None:
                for repo in repos:
                    links = b.get_link_repo(repo[0])
                    RepoList.append([repo, links])
                return RepoList
            else:
                return None

    def Get_repos(self):
        with ContextBroker(self.__token, self.__db_file, self.__log) as b:
            return b.get_repo()

    # eseguo query su git e salvo i dati sul db
    def get_git_data(self, query_string: str, size_max):
        with ContextBroker(self.__token, self.__db_file, self.__log) as b:
            try:
                query_string = query_string + 'stars:>1 forks:>1'
                b.do_git_search(query_string, size_max)
            except Exception as e:
                if str(e) == 'token errato':
                    self.__log.write('[ERRORE] Token di accesso errato', 'g')
                if str(e) == 'limite':
                    self.__log.write('[ERRORE] Rate Limit superato, attendere del tempo', 'g')
                if str(e) == "name 'github' is not defined":
                    self.__log.write('[ERRORE] Impossibile collegarsi a Github', 'g')


    def __stats_to_db(self, res, tag):
        with ContextBroker(self.__token, self.__db_file, self.__log) as b:
            b.stats_to_db(stats=res, tag=tag)

    def Get_stats(self, Elab_name:str )->list:
        with ContextBroker(self.__token, self.__db_file, self.__log) as b:
            res_list = list()
            for r in b.get_elab(Elab_name):
                res_list.append(r[0])
            return res_list

    """
        OPERAZIONI DI GESTIONE FILE
    """

    def close(self):
        try:
            with ContextBroker(self.__token, self.__db_file, self.__log) as b:
                b.delete_db()
        except Exception as e:
            raise Exception('[ERRORE] problemi in chiusura file' + str(e))

    def backup(self, backup_file):
        try:
            with ContextBroker(self.__token, self.__db_file, self.__log) as b:
                b.backup(backup_file)
        except Exception as e:
            raise Exception('[ERRORE] problemi in salvataggio file' + str(e))


"""
    CONTEXT MANAGER BROKER PER IL MULTI THREADING
"""
class ContextBroker():
    def __init__(self, token, db_file, log):
        self.__token = token
        self.__db = db_file
        self.__log = log
        self.__broker = None

    def __enter__(self):
        self.__broker = Broker.Broker(self.__token, self.__db, self.__log)
        return self.__broker

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__broker = None