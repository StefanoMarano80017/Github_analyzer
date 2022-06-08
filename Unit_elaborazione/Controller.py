from datetime import datetime
from Broker import Broker
from Unit_elaborazione import Analisi_sorgente

#La classe controller ha il compito di coordinare tutte le classi di questo package
class Controller:
    def __init__(self, token, db_file):
        self.broker = Broker.Broker(token, db_file)
        self.token = token
        self.db_file = db_file

    def get_git_data(self, date: datetime.date, lang: str, size_max):
        # eseguo query su git e salvo i dati sul db
        self.broker.do_search(date, lang, size_max)


    def get_repo(self) -> list:
        return self.broker.get_repo()

    #Viene realizzato il binding delle classi presenti in questo package con il db
    def repo_cloc(self) -> list:
        result_cloc = []
        for repo in self.broker.get_repo():
            #La chiamata al broker ha lo scopo di leggere i dati presenti nel db
            links = self.broker.get_link_repo(repo[0])
            a = Analisi_sorgente.Analyzer(group=repo[1])
            #Viene generato il summary del cloc
            cloc_result = a.cloc_files(links)
            result_cloc.append([cloc_result, repo[2], repo[3]])
        return result_cloc
