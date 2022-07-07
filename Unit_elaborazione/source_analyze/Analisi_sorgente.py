from Unit_elaborazione.AbstractElaborazione import AbstractElaborazione
from Unit_elaborazione.source_analyze import Cloc_Analize, Request_Code


# Classe che analizza il codice sorgente di tutti i file di una repository
class source_analyzer(AbstractElaborazione):

    def __init__(self, ElabName='source_analyzer'):
        super().__init__(ElabName)
        self.cloc = None

    def GetName(self) -> str:
        return self.name

    # Interfaccia comune per le elaborazioni
    def DoElaborazione(self, RepoList: list) -> list:
        results = list()
        dens_results = list()
        for repo in RepoList:
            self.cloc = Cloc_Analize.C_Analysis(repo[0][0])
            results.append(self.__cloc_files(repo[1]))

        return results

    # Metodo della classe che analizza i link della repository
    def __cloc_files(self, links: list) -> list:
        for link in links:
            if link is not None:
                self.__cloc_file(link[0], link[1])
        # return [self.summary.total_code_count, self.summary.total_documentation_count, self.summary.total_empty_count]
        return self.cloc.get_summary()

    # Metodo della classe che effettua la richiesta del singolo file della repository
    def __cloc_file(self, link: str, suffix: str):
        try:
            req = Request_Code.extract_code(link)
            self.cloc.count_file(req.get_content(), suffix)
        except Exception as e:
            raise '[ERRORE] Cloc' + str(e)


class density_analyzer(source_analyzer):
    def __init__(self, ElabName='density_analyzer'):
        super().__init__(ElabName)

    def GetName(self) -> str:
        return self.name

    def DoElaborazione(self, RepoList: list) -> list:

        dens_results = list()
        density = 0

        for res in super(density_analyzer, self).DoElaborazione(RepoList):
            try:
                total_lines = res[0] + res[1] + res[2]
                density = (res[1] / total_lines) * 100
            except ZeroDivisionError:
                density = 0
            finally:
                density = round(density, 2)
                dens_results.append(density)

        return dens_results
