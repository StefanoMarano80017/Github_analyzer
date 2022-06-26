from github import BadCredentialsException
from github import Github
from github import RateLimitExceededException
from github import Repository

from QueryGit import TokenUtil


# Classe che effettua la query su Github
class QueryRepo:
    def __init__(self, token):
        self.repos = None
        self.g = Github(token, per_page=100)
        self.tokenutil = TokenUtil.Token(token)

    # Contatore query
    def count_query(self, query_txt, sort='stars', order='desc'):
        self.tokenutil.wait_is_usable()
        count: int = self.g.search_repositories(query_txt, sort, order).totalCount
        return count

    # Metodo che esegue la query e salva le singole repository
    def do_query_txt(self, query_txt, sort='stars', order='desc') -> list:
        try:
            count = self.count_query(query_txt)
            repo_list = []
            for i in range(0, round(count / 100) + 1):
                # Valutazione Token
                self.tokenutil.wait_is_usable()
                # Viene creata una lista di repository
                for repo in self.g.search_repositories(query_txt, sort, order).get_page(i):
                    repo_list.append(repo)
            return repo_list
        except BadCredentialsException as e:
            raise 'token errato'
        except RateLimitExceededException as e:
            raise 'limite'

    # Creazione lista dei file di una repository
    def extract_file_repo(self, repo: Repository.Repository):
        # Controllo token
        self.tokenutil.wait_is_usable()
        contents = repo.get_contents("")
        list_file = []

        while contents:
            self.tokenutil.wait_is_usable()
            file_content = contents.pop(0)
            if file_content.type == "dir":
                contents.extend(repo.get_contents(file_content.path))
            elif file_content.type == "file":
                c = file_content.name.split('.')
                len_c = len(c)
                if self.__extractable_files(c[len_c - 1]):
                    list_file.append([file_content.download_url, c[len_c - 1]])
        return list_file

    @staticmethod
    def __extractable_files(strs):
        # QUI TUTTE LE ESTENSIONI CHE POSSO LEGGERE
        # if str == 'py' or str == 'eee'
        # in realtà la lib pygments legge più di 100 linguaggi
        # metto tutti i file da evitare cnf, dati di git e così via

        if (
                strs == 'gitignore' or strs == 'md' or strs == 'svg' or strs == 'jpeg' or strs == 'jpg' or strs == 'gif' or strs == 'PNG'
                or strs == 'doctree' or strs == 'png' or strs == 'cfg' or strs == 'txt' or strs == 'ico'
                or strs == 'npmignore' or strs == 'gitattributes' or strs == 'eslintrc'
                or strs == 'csv' or strs == 'runtime' or strs == 'ref' or strs == 'set' or strs == 'xlsx'
                or strs == 'runtime' or strs == 'pdf' or strs == 'log' or strs == 'prototxt' or strs == 'mat'
                or strs == 'lock' or strs == 'gitmodules' or strs == 'eps' or strs == 'properties' or strs == 'props'
                or strs == 'DS_store' or strs == 'classpath' or strs == 'LICENSE' or strs == 'prefs' or strs == 'clang-format'
                or strs == 'gradle' or strs == 'bat' or strs == 'pro' or strs == 'fs' or strs == 'conf' or strs == 'kl'
                or strs == 'bp' or strs == 'flags' or strs == 'accept' or strs == 'ini' or strs == 'deny'
                or strs == 'te' or strs == 'arff' or strs == 'mp4' or strs == 'mp3' or strs == 'sql' or strs == 'flat'
                or strs == None or (len(strs) > 6)):
            return False
        else:
            return True
