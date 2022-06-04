import datetime
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

    def do_git_query_repo(self, date: datetime.date, lang: str):
        # fork > 0 & star > 0
        # created:2017-05-31 stars:>0 forks:>0 language:Java
        query_txt = "created:" + str(date) + " stars:>0 forks:>0 language:" + lang
        print(query_txt)
        # return list[repo]
        return self.git_repo.do_query_txt(query_txt)

    def do_git_query_link(self, repo) -> list:
        return self.git_repo.extract_file_repo(repo)

    def repos_to_db(self, date: datetime.date, lang: str):
        print("----salvataggio in DB-------")
        repos = self.do_git_query_repo(date, lang)
        for repo in repos:
            # query DB salvataggio repo
            print('salvo repo')
            args = (repo.id, repo.full_name)
            self.dao_repo.set_data(args)

            # query DB salvataggio link repo
            for link in self.do_git_query_link(repo):
                self.dao_links.set_data((None, link, repo.id))

    def print_table_repo(self):
        for repo in self.dao_repo.get_data():
            print(repo)

    def select_repo(self, size_max):
        count = self.dao_repo.get_data('count_repo')
        size = count[0][0]
        if size > size_max:
            return self.random_select_repo(size_max)
        else:
            return self.dao_repo.get_data()

    def random_select_repo(self, size_max):
        repos = self.dao_repo.get_data()
        return random.sample(repos, size_max)

    def count_search(self, query_txt):
        return self.git_repo.count_query(query_txt)

    def select_link(self, repo):
        return self.dao_links.get_data(repo.id)

    def print_table_link(self):
        for link in self.dao_links.get_data():
            print(link)

    def get_link_repo(self, id_repo:str):
        args = (id_repo, )
        links_raw = self.dao_links.get_data('select_link_id', args)
        links = []
        for link_raw in links_raw:
            links.append(link_raw[0])

        return links