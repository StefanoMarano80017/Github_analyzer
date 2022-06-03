from Unit_elaborazione import Analisi_sorgente
from Broker import Broker


class Controller:
    def __init__(self, token, db_file):
        self.broker = Broker.Broker(token, db_file)

    def repo_cloc(self):
        # link dei file della repo
        repos = self.broker.select_repo(100)
        total_lines = 0
        for repo in repos:
            links = self.broker.get_link_repo(repo[0])
            for link in links:
                print(link[1])
                a = Analisi_sorgente.Analyzer(group=repo[1], link=link[1])
                print(a.cloc_files())