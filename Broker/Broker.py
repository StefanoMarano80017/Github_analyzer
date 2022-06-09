import random

from Broker import DAOS
from Broker import QueryGit


class Broker:
    def __init__(self, token: str, db_file: str):
        self.token = token
        self.db_file = db_file
        self.git_repo = QueryGit.QueryRepo(token)
        self.dao_repo = DAOS.DAO_Repo(db_file)
        self.dao_links = DAOS.DAO_link(db_file)

    def __do_git_query_repo(self, query_string: str):
        # fork > 0 & star > 0
        # created:2017-05-31 stars:>0 forks:>0 language:Java
        query_txt = query_string + " stars:>0 forks:>0"
        print(query_txt)
        # return list[repo]
        return self.git_repo.do_query_txt(query_txt)

    def __do_git_query_link(self, repo) -> list:
        return self.git_repo.extract_file_repo(repo)

    def do_search(self, query_string: str, size_max):
        # eseguo una query su git e poi salvo su db
        repos = self.__select_repo(query_string, size_max)
        self.__repos_to_db(repos)

    def __repos_to_db(self, repos: list):
        print("----salvataggio in DB-------")
        for repo in repos:
            # query DB salvataggio repo
            args = (repo.id, repo.full_name, repo.stargazers_count, repo.forks_count)
            self.dao_repo.set_data(args)

            # query DB salvataggio link repo
            for link in self.__do_git_query_link(repo):
                self.dao_links.set_data((None, link[0], repo.id, link[1]))

    def __select_repo(self, query_string: str, size_max):
        # eseguo query su git con un limite al numero di repository
        print("--------------------Query git in corso----------------------------")
        repos = self.__do_git_query_repo(query_string)

        if len(repos) > size_max:
            return random.sample(repos, size_max)
        elif len(repos) is None:
            raise "Query Git errore"
        else:
            return repos

    def get_repo(self):
        return self.dao_repo.get_data()

    def get_link_repo(self, id_repo: str):
        links_raw = self.dao_links.get_data('select_link_id', (id_repo,))
        links = []
        if len(links_raw) is not None:
            for link_raw in links_raw:
                li = list(link_raw)
                links.append([li[1], li[3]])
            return links
        else:
            raise "Exception, db link vuoto"

    def print_table_link(self):
        # metodo per il debug
        for link in self.dao_links.get_data():
            print(link)

    def print_table_repo(self):
        # metodo per il debugg
        for repo in self.dao_repo.get_data():
            print(repo)
