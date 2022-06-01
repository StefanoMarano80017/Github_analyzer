from github import Github
import Query_Txt
import TokenUtil

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

    def do_query_txt(self, query_txt, sort='stars', order='desc') -> list:
        self.tokenutil.wait_is_usable()
        count: int = self.g.search_repositories(query_txt, sort, order).totalCount

        repo_list = []
        for i in range(0, round(count/100)+1):
            self.tokenutil.wait_is_usable()
            for repo in self.g.search_repositories(query_txt, sort, order).get_page(i):
                repo_list.append(repo)
        return repo_list
