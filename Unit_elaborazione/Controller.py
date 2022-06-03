import Analisi_sorgente
from Broker import Broker


class Controller:
    def __init__(self, token, db_file):
        self.broker = Broker.Broker(token, db_file)

    def repo_cloc(self):
        # link dei file della repo
        repos = self.broker.select_repo(100)
        for repo in repos:
            self.broker.get_link_repo(repo)