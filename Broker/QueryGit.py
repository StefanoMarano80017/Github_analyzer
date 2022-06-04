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
                if self.extractable_files(c[len_c - 1] ):
                    list_file.append(file_content.download_url)
        return list_file

    def extractable_files(self, str):
        # QUI TUTTE LE ESTENSIONI CHE POSSO LEGGERE
        #if str == 'py' or str == 'eee'
        #in realtà la lib pygments ne legge fin troppi più di 100 linguaggi
        #metto tutti i file da evitare poiché cnf, dati di git e così via

        if ( str == 'gitignore' or str == 'md' or str == 'svg' or str == 'jpeg' or str == 'gif'
                or str == 'doctree' or str == 'png' or str == 'cfg' or str =='txt' or str == 'ico'
                or str == 'npmignore' or str == 'gitattributes' or str == 'eslintrc' or str ==' '):
            return False
        else:
            return True
