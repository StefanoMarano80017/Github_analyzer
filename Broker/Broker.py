import github.Repository

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
        repos = self.do_git_query_repo(date, lang)
        for repo in repos:
            args = (None, repo.name)
            self.dao_repo.set_data(args)

            #creare DAO per i link dei file
            #for link in self.extract_file_repo(repo):
                    #self.dao_link_set_data(link)
        return repos

    def print_table_repo(self):
        for repo in self.dao_repo.get_data():
            print(repo)

    def select_repo(self, size_max):
        size = self.dao_repo.get_data('count_repo')
        if size > size_max:
            return self.random_select_repo(size_max)
        else:
            return self.dao_repo.get_data()

    def random_select_repo(self, size_max):
        repos = self.dao_repo.get_data()
        return random.sample(repos, size_max)

    def count_search(self, query_txt):
        return self.git_repo.count_query(query_txt)

    def extract_file_repo(self, repo:github.Repository.Repository):
        contents = repo.get_contents("")
        list_file = []

        while contents:
            file_content = contents.pop(0)
            if file_content.type == "dir":
                contents.extend(repo.get_contents(file_content.path))
            else:
                c = file_content.name.split('.')
                len_c = len(c)
                #QUI TUTTE LE ESTENSIONI CHE POSSO LEGGERE
                if c[len_c-1] == 'py':
                    list_file.append(file_content.download_url)

        return list_file