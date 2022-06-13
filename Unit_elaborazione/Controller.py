from Broker import Broker
from Unit_elaborazione import Analisi_sorgente


# La classe controller ha il compito di coordinare le funzioni di analisi sui repository
class Controller:
    def __init__(self, token, db_file, logger):
        self.broker = None
        self.token = token
        self.db_file = db_file
        self.log = logger

    def get_git_data(self, query_string: str, size_max):
        # eseguo query su git e salvo i dati sul db
        self.broker = Broker.Broker(self.token, self.db_file, self.log)
        try:
            self.broker.do_search(query_string, size_max)
        except Exception as e:
            self.log.write('[ERRORE] ' + str(e), 'g')
        finally:
            self.broker = None

    def get_repo(self) -> list:
        # ottengo i dati dal db
        self.broker = Broker.Broker(self.token, self.db_file, self.log)
        repos = None
        try:
            repos = self.broker.get_repo()
        except Exception as e:
            self.log.write('[ERRORE] ' + str(e), 'g')
        finally:
            self.broker = None
            return repos

    def print_repo(self):
        self.broker = Broker.Broker(self.token, self.db_file, self.log)
        try:
            self.broker.print_table_repo()
        except Exception as err:
            if str(err) == 'no such table: repos':
                self.log.write('[ERRORE] Non sono presenti repos', 'g')
            else:
                self.log.write('[ERRORE] Impossibile lettura repos', 'g')

        self.broker = None

    def get_link(self, id):
        self.broker = Broker.Broker(self.token, self.db_file, self.log)
        links = self.broker.get_link_repo(id)
        self.broker = None
        return links

    def repo_cloc(self):
        result_cloc = []
        self.broker = Broker.Broker(self.token, self.db_file, self.log)
        try:
            for repo in self.broker.get_repo():
                # La chiamata al broker ha lo scopo di leggere i dati presenti nel db
                links = self.broker.get_link_repo(repo[0])
                a = Analisi_sorgente.Analyzer(group=repo[1])
                # Viene effettuata l'analisi della repository e aggiunta alla lista
                cloc_result = a.cloc_files(links)
                result_cloc.append([cloc_result, repo[2], repo[3]])
                string = "[CLOC] Name: {name:^36} LOC: {loc:<6} LOD: {lod:<6}".format(name=repo[1], loc=cloc_result[0], lod=cloc_result[1])
                self.log.write(string, 'f+g')
                #total_lines = cloc_result[0] + cloc_result[1] + cloc_result[2]
                #self.broker.stats_to_db((repo[0], cloc_result[0], cloc_result[1], total_lines))
            self.broker = None
            return result_cloc
        except Exception as e:
            if str(e) == 'no such table: repos':
                self.log.write('[ERRORE] Non sono presenti repos da elaborare', 'g')
            if str(e) == 'no such table: links':
                self.log.write('[ERRORE] Non è possibile ricavare il codice sorgente', 'g')
            self.broker = None
            return None

    def cloc_density_graph(self, list_raw):
        li_r = []
        for li in list_raw:
            try:
                total_lines = li[0][0] + li[0][1] + li[0][2]
                density = (li[0][1] / total_lines) * 100
            except ZeroDivisionError:
                density = 0
            finally:
                density = round(density, 2)
                li_r.append(density)
                string = "[DENSITY CLOC] Density: {dens:^4} Stars: {stars:<6} forks: {forks:<6}".format(dens=density, stars=li[1], forks=li[2])
                self.log.write(string, 'f+g')
        return li_r

    def close(self):
        self.broker = Broker.Broker(self.token, self.db_file, self.log)
        self.broker.delete_db()
        self.broker = None

    def backup(self, backup_file):
        self.broker = Broker.Broker(self.token, self.db_file, self.log)
        self.broker.backup(backup_file)
        self.broker = None
