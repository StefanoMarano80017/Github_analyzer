import QueryGit
import DAO
import datetime

class Broker:
    def __init__(self, token:str , db_file:str):
        self.token = token
        self.db_file = db_file
        self.git_repo = QueryGit.QueryRepo(token)
        self.dao_repo = DAO.DAO_Repo(db_file)

    def do_git_query_repo(self, date:datetime.date, lang:str):
        # fork > 0 & star > 0
        # created:2017-05-31 stars:>0 forks:>0 language:Java
        query_txt = "created:" + str(date) + " stars:>0 forks:>0 language:" + lang
        print(query_txt)
        return self.git_repo.do_query_txt(query_txt)

    def repos_to_db(self, date:datetime.date, lang:str):
        for repo in self.do_git_query_repo(date, lang):
            args = (None, repo.name)
            self.dao_repo.set_data(args)
