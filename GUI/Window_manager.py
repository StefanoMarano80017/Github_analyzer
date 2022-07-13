import PySimpleGUI as sg

from GUI import windows
from Util import logger, Query_Txt

SIZE_DEFAULT = int(Query_Txt.read_query('SIZE_SEARCH', 'GUI'))
DB_DEFAULT = Query_Txt.read_query('DEFAULT_DB_FILE', 'GUI')


class Event_Processor():
    def __init__(self, controller):
        sg.theme('LightGrey1')
        self.log = logger.logger()
        self.win_utente = windows.Utente_window()
        self.win_salva = None
        self.win_graph = list()
        self.win_salva_graph = None
        self.controller = controller

        self.inputs = None
        self.RepoList = None
        self.Elab_results = {}

    def __create_win_dati(self):
        return windows.Salva_window('Salva Dati')

    def __create_win_graph(self, tipo, title, desc_x, desc_y, x, y):
        self.win_graph.append(windows.graph_window(tipo, title, desc_x, desc_y, x, y))


    def event_loop(self):
        while True:
            # eventi utente
            if self.win_utente is not None:
                opt = self.win_utente.Notifica()
                self.inputs = self.win_utente.GetStato()

                if self.inputs['db'] is None:
                    self.inputs['db'] = DB_DEFAULT

                self.controller.set_param(self.inputs['token'], self.inputs['db'])

                match opt:
                    case 'Do Query':
                        self.__do_query()
                    case 'Repos':
                        self.__repos()
                    case 'Cloc':
                        self.__elabs('source_analyzer', '-CLOC KEY-')
                    case 'Densità':
                        self.__elabs('density_analyzer', '-DENS KEY-')
                    case 'Salva Dati':
                        self.win_salva = self.__create_win_dati()
                    case 'Documentazione/Modificabilità':
                        forks = list()
                        for repo in self.controller.Get_repos():
                            forks.append(repo[3])
                        self.__density_graph(forks, 'doc/mod', 'Grafico Documentazione/Modificabilità', 'forks')
                    case 'Documentazione/Popolarità':
                        stars = list()
                        for repo in self.controller.Get_repos():
                            stars.append(repo[2])
                        self.__density_graph(stars, 'doc/pop', 'Grafico Documentazione/Popolarità', 'stars')
                    case '-END KEY-':
                        self.log.write('[INFO] Query terminata', 'f+g')
                        self.RepoList = self.controller.Get_repo_list()
                        self.__repos()
                    case '-CLOC KEY-':
                        self.Elab_results['source_analyzer'] = self.controller.Get_stats('source_analyzer')
                        self.log.write('[INFO] Elaborazione terminata', 'f+g')
                        self.__print_elab('source_analyzer')

                    case '-DENS KEY-':
                        self.Elab_results['density_analyzer'] = self.controller.Get_stats('density_analyzer')
                        self.log.write('[INFO] Elaborazione terminata', 'f+g')
                        self.__print_elab('density_analyzer')

                    case sg.WIN_CLOSED:
                        self.win_utente.close()

            # eventi salva dati
            if self.win_salva is not None:
                match self.win_salva.Notifica():
                    case 'Submit_salva':
                        backup = self.win_salva.GetStato()
                        self.__salva_dati(backup['backup'])
                        self.win_salva.close()
                        self.win_salva = None
                    case sg.WIN_CLOSED:
                        self.win_salva.close()
                        self.win_salva = None

            # eventi graph
            if self.win_graph is not None:
                for graph in self.win_graph:
                    match graph.Notifica():
                        case 'Salva Graph':
                            self.win_salva_graph = self.__create_win_dati()
                        case sg.WIN_CLOSED:
                            graph.close()

            if self.win_salva_graph is not None:
                match self.win_salva_graph.Notifica():
                    case 'Submit_salva':
                        backup = self.win_salva.GetStato()
                        if backup != ' ':
                            fig = self.win_salva.GetFig()
                            fig.savefig(backup)
                        else:
                            self.log.write('[ERRORE] path immagine grafico vuoto', 'g')
                        self.win_salva_graph.close()
                        self.win_salva_graph = None
                    case sg.WIN_CLOSED:
                        self.win_salva_graph.close()
                        self.win_salva_graph = None

            self.inputs = None

    def __do_query(self):
        if self.inputs['token'] is not None and self.inputs['query'] is not None:
            self.log.write(
                '[INFO] Eseguo query: ' + self.inputs['query'], 'f+g')
            try:
                print(self.inputs['query'])
                print(SIZE_DEFAULT)

                win = self.win_utente.GetWin()
                win.perform_long_operation(lambda: self.controller.get_git_data(self.inputs['query'], SIZE_DEFAULT),
                                           '-END KEY-')

            except Exception as e:
                self.log.write('[ERRORE] ' + str(e), 'g')
        else:
            if self.inputs['token'] is None:
                self.log.write('[ERRORE] MANCA IL TOKEN', 'g')
            if self.inputs['query'] is None:
                self.log.write('[ERRORE] MANCA LA QUERY', 'g')

    def __repos(self):
        try:
            self.RepoList = self.controller.Get_repo_list()
            if self.RepoList is not None:
                self.log.write('[INFO] Repos in: ' + self.inputs['db'], 'g')
                for repo in self.RepoList:
                    self.log.write(repo[0], 'g')
            else:
                self.log.write('[ERRORE] Il file non contiene repository', 'g')
        except Exception as e:
            self.log.write('[ERRORE] ' + str(e), 'g')

    def __elabs(self, ElabName, key):
        self.log.write('[INFO] Inizio elab: ' + ElabName, 'f+g')
        if self.RepoList is None:
            self.RepoList = self.controller.Get_repo_list()

        try:
            win = self.win_utente.GetWin()
            win.perform_long_operation(lambda: self.controller.DoElaborazione(ElabName, self.RepoList), key)
        except Exception as e:
            self.log.write('[ERRORE] ' + str(e),'f+g')

    def __print_elab(self, elab_name):
        if elab_name not in self.Elab_results:
            self.log.write('[ERRORE] errore elaborazione', 'g')
        else:
            if self.Elab_results[elab_name] is not None:
                for res in self.Elab_results[elab_name]:
                    self.log.write(res, 'f+g')
            else:
                self.log.write('[ERRORE] Elaborazione nulla', 'f+g')

    def __density_graph(self, y, tipo, titolo, desc_y):
        if 'density_analyzer' not in self.Elab_results:
            self.Elab_results['density_analyzer'] = self.controller.Get_stats('density_analyzer')

        if self.Elab_results['density_analyzer'] is not None:
            x = self.Elab_results['density_analyzer']
            self.__create_win_graph(tipo, titolo, 'Densità Doc', desc_y, x, y)
        else:
            self.log.write('[ERRORE] eseguire un elaborazione di densità', 'g')

    def __salva_dati(self, backup_file):
        self.controller.backup(backup_file)
        self.controller.set_param(self.inputs['token'], backup_file)
        self.log.write('[INFO] SALVATAGGIO ESEGUITO', 'f+g')
