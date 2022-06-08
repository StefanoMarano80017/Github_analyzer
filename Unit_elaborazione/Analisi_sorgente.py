from Unit_elaborazione import Cloc_Analize
from Unit_elaborazione import Request_Code

#Classe che analizza il codice sorgente di tutti i file di una repository
class Analyzer:
    def __init__(self, group: str):
        # Il parametro group identifica un insieme di file di un singola repository
        self.group = group
        #Instanza della classe C_Analysis
        self.cloc = Cloc_Analize.C_Analysis(group)

    #Metodo della classe
    def cloc_files(self, links: list) -> list:
        for link in links:
            self.cloc_file(link[0], link[1])
        # return [self.summary.total_code_count, self.summary.total_documentation_count, self.summary.total_empty_count]
        return self.cloc.get_summary()

    #Metodo della classe che effettua
    def cloc_file(self, link: str, suffix: str):
        try:
            req = Request_Code.extract_code(link)
            return self.cloc.count_file(req.get_content(), suffix)
        except Exception as e:
            print('errore cloc_file')
            print(e)
