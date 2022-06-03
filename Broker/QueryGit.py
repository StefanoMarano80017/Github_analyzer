from github import Github
from github import Repository

from Broker import Query_Txt
from Broker import TokenUtil

TOKEN = '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'


class QueryRepo:
    def __init__(self, token):
        self.repos = None
        self.g = Github(token, per_page=100)
        self.tokenutil = TokenUtil.Token(self.g)

    def do_query_ini(self, query_id, sort='stars', order='desc'):
        # sort – string (‘stars’, ‘forks’, ‘updated’)
        # order – string (‘asc’, ‘desc’)

        query_string = Query_Txt.read_query(query_id, 'GIT')
        return self.do_query_txt(query_string, sort, order)

    def count_query(self, query_txt, sort='stars', order='desc'):
        self.tokenutil.wait_is_usable()
        count: int = self.g.search_repositories(query_txt, sort, order).totalCount
        return count

    def do_query_txt(self, query_txt, sort='stars', order='desc') -> list:
        count = self.count_query(query_txt)

        repo_list = []
        for i in range(0, round(count / 100) + 1):
            self.tokenutil.wait_is_usable()
            for repo in self.g.search_repositories(query_txt, sort, order).get_page(i):
                repo_list.append(repo)
        return repo_list

    def extract_file_repo(self, repo: Repository.Repository):
        self.tokenutil.wait_is_usable()
        contents = repo.get_contents("")
        list_file = []

        while contents:
            self.tokenutil.wait_is_usable()
            file_content = contents.pop(0)
            if file_content.type == "dir":
                contents.extend(repo.get_contents(file_content.path))
            else:
                c = file_content.name.split('.')
                len_c = len(c)
                # QUI TUTTE LE ESTENSIONI CHE POSSO LEGGERE
                if c[len_c - 1] == 'py':
                    list_file.append(file_content.download_url)

        return list_file
