import random

from Datas.DB import DB_manager, DAOS
from Datas.Git import QueryGit


class Broker:
    def __init__(self, token: str, db_file: str, logger):
        self.token = token
        self.db_file = db_file
        self.git_repo = QueryGit.QueryRepo(token)
        self.dao_repo = DAOS.DAO_Repo(db_file)
        self.dao_links = DAOS.DAO_link(db_file)
        self.dao_stats = DAOS.DAO_stats(db_file)
        self.log = logger

    """
        RICERCA SU GIT
    """

    def do_git_search(self, query_string: str, size_max):
        # eseguo una query su git
        try:
            repos = self.__select_repo(query_string, size_max)
            if repos is not None:
                self.__repos_to_db(repos)
        except Exception as e:
            raise e

    def __do_git_query_repo(self, query_string: str):
        # fork > 0 & star > 0
        # created:2017-05-31 stars:>0 forks:>0 language:Java
        query_txt = query_string + " stars:>0 forks:>0"
        self.log.write("[Query] " + query_txt, 'f+g')
        # return list[repo]
        return self.git_repo.do_query_txt(query_txt)

    def __do_git_query_link(self, repo) -> list:
        return self.git_repo.extract_file_repo(repo)

    def __select_repo(self, query_string: str, size_max):
        # eseguo query su git con un limite al numero di repository
        count = self.git_repo.count_query(query_string)

        if count > size_max:
            repos = self.git_repo.do_query_txt(query_string)
            return random.sample(repos, size_max)
        else:
            return self.git_repo.do_query_txt(query_string)

    """
        INTERFACCIA COL DB
    """

    def get_repo(self):
        try:
            return self.dao_repo.get_data()
        except Exception as e:
            raise e

    def get_link_repo(self, id_repo: str):
        try:
            links_raw = self.dao_links.get_data('select_link_id', (id_repo,))
            links = []
            for link_raw in links_raw:
                li = list(link_raw)
                links.append([li[1], li[3]])
            return links
        except Exception as e:
            raise e

    def __repos_to_db(self, repos: list):
        self.log.write(
            "-----------------------------------SALVATAGGIO IN DB IN CORSO-------------------------------------------",
            "f+g")
        for repo in repos:
            # query DB salvataggio repo
            args = (repo.id, repo.full_name, repo.stargazers_count, repo.forks_count)
            self.dao_repo.set_data(args)

            # query DB salvataggio link repo
            for link in self.__do_git_query_link(repo):
                self.dao_links.set_data((None, link[0], repo.id, link[1]))
        self.log.write(
            "-----------------------------------SALVATAGGIO IN DB TERMINATO-------------------------------------------",
            "f+g")

    def stats_to_db(self, args):
        try:
            self.dao_stats.set_data(args)
        except Exception as e:
            raise "errore dato stats" + str(e)

    def get_elab(self, Elab_name):
        try:
            return self.dao_links.get_data('select_stats', (Elab_name,))
        except Exception as e:
            raise 'Errore Dao stats' + str(e)

    def delete_db(self):
        db = DB_manager.DB(self.db_file)
        db.delete_db()

    def backup(self, backup_file):
        db = DB_manager.DB(self.db_file)
        db.backup_on_file(backup_file)
