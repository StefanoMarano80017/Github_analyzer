import random

from Datas.DB import DB_manager, DAOS
from Datas.Git import QueryGit


class Broker:
    def __init__(self, token: str, db_file: str, logger):
        self.__token = token
        self.__db_file = db_file
        self.__git_repo = QueryGit.QueryRepo(token)
        self.__dao_repo = DAOS.DAO_Repo(db_file)
        self.__dao_links = DAOS.DAO_link(db_file)
        self.__dao_stats = DAOS.DAO_stats(db_file)
        self.__log = logger

    """
        RICERCA SU GIT
    """

    def do_git_search(self, query_string: str, size_max):
        # eseguo una query su git
        repos = self.__select_repo(query_string, size_max)
        if repos is not None:
            self.__repos_to_db(repos)


    def __do_git_query_link(self, repo) -> list:
        return self.__git_repo.extract_file_repo(repo)

    def __select_repo(self, query_string: str, size_max):
        # eseguo query su git con un limite al numero di repository
        count = self.__git_repo.count_query(query_string)
        self.__log.write('[INFO] Ricerca git in corso', 'g')
        if count > size_max:
            repos = self.__git_repo.do_query_txt(query_string)
            return random.sample(repos, size_max)
        else:
            return self.__git_repo.do_query_txt(query_string)

    """
        INTERFACCIA COL DB
    """

    def get_repo(self):
        return self.__dao_repo.get_data()

    def get_link_repo(self, id_repo: str):
        links_raw = self.__dao_links.get_data('select_link_id', (id_repo,))
        links = []
        for link_raw in links_raw:
            li = list(link_raw)
            links.append([li[1], li[3]])
        return links


    def __repos_to_db(self, repos: list):
        self.__log.write("[INFO] Salvataggio in DB", "f+g")
        for repo in repos:
            self.__log.write("[INFO] Salvataggio contenuto repo", "g")
            # query DB salvataggio repo
            args = (repo.id, repo.full_name, repo.stargazers_count, repo.forks_count)
            self.__dao_repo.set_data(args)

            # query DB salvataggio link repo
            for link in self.__do_git_query_link(repo):
                self.__dao_links.set_data((None, link[0], repo.id, link[1]))

        self.__log.write("[INFO] Salvataggio terminato", "f+g")

    def stats_to_db(self, stats:list, tag:str):
        for res in stats:
            self.__dao_stats.set_data(args=(0, tag, str(res)))

    def get_elab(self, Elab_name:str):
        return self.__dao_stats.get_data('select_stats', (Elab_name,))


    def delete_db(self):
        db = DB_manager.DB(self.__db_file)
        db.delete_db()

    def backup(self, backup_file):
        db = DB_manager.DB(self.__db_file)
        db.backup_on_file(backup_file)
