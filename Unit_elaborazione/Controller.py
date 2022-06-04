from Broker import Broker
from Unit_elaborazione import Analisi_sorgente


class Controller:
    def __init__(self, token, db_file):
        self.broker = Broker.Broker(token, db_file)

    def repo_cloc(self) -> list:
        result_cloc = []
        repos = self.broker.select_repo(100)

        for repo in repos:
            links = self.broker.get_link_repo(repo[0])
            a = Analisi_sorgente.Analyzer(group=repo[1])
            result_cloc.append(a.cloc_files(links))

        return result_cloc