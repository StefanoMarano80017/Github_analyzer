import QueryGit
import DAO
import datetime
import random

class Broker:
    def __init__(self, token: str, db_file: str):
        self.token = token
        self.db_file = db_file
        self.git_repo = QueryGit.QueryRepo(token)
        self.dao_repo = DAO.DAO_Repo(db_file)

    def do_git_query_repo(self, date: datetime.date, lang: str):
        # fork > 0 & star > 0
        # created:2017-05-31 stars:>0 forks:>0 language:Java
        query_txt = "created:" + str(date) + " stars:>0 forks:>0 language:" + lang
        print(query_txt)
        return self.git_repo.do_query_txt(query_txt)

    def repos_to_db(self, date: datetime.date, lang: str):
        for repo in self.do_git_query_repo(date, lang):
            args = (None, repo.name)
            self.dao_repo.set_data(args)

    def print_table_repo(self):
        for repo in self.dao_repo.get_data():
            print(repo)

    def select_repo(self, size_max):
        size = self.dao_repo.get_data('count_repo')
        if size > size_max:
            return self.random_select_repo(size, size_max)
        else:
            return self.dao_repo.get_data()

    def random_select_repo(self, size, size_max):
        repos = self.dao_repo.get_data()
        return random.sample(repos, size_max)
