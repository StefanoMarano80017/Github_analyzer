import concurrent.futures

import PySimpleGUI as sg

from GUI import windows
from Util import logger, Query_Txt

SIZE_DEFAULT = Query_Txt.read_query('SIZE_SEARCH', 'GUI')
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
        self.Elab_results = dict()

    def __create_win_dati(self):
        return windows.Salva_window('Salva Dati')

    def __create_win_graph(self, tipo, title, descrizione, x, y):
        self.win_graph.append(windows.graph_window(tipo, title, descrizione, x, y))

    def __long_function(self, ElabName, RepoList):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            thread = executor.submit(self.controller.DoElaborazione(ElabName, RepoList))
            self.Elab_results[ElabName] = thread.result()

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
                        self.__cloc()
                    case 'Densità':
                        self.__dens()
                    case 'Salva Dati':
                        self.win_salva = self.__create_win_dati()
                    case 'Documentazione/Modificabilità':
                        forks = list()
                        for repo in self.controller.Get_repos():
                            forks.append(repo[3])
                        self.__density_graph(forks)
                    case 'Documentazione/Popolarità':
                        stars = list()
                        for repo in self.controller.Get_repos():
                            stars.append(repo[2])
                        self.__density_graph(stars)
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
                '---------------------------------------------ESEGUO QUERY GIT--------------------------',
                'f+g')
            try:
                win = self.win_utente.GetWin()
                win.perform_long_operation(lambda: self.controller.get_git_data(self.inputs['query'], SIZE_DEFAULT),
                                           '-END KEY-')
                self.RepoList = self.controller.Get_repo_list()
            except Exception as e:
                print(e)
        else:
            if self.inputs['token'] is None:
                self.log.write('[ERRORE] MANCA IL TOKEN', 'g')
            if self.inputs['query'] is None:
                self.log.write('[ERRORE] MANCA LA QUERY', 'g')

    def __repos(self):
        try:
            for repo in self.controller.Get_repos():
                print(repo)
            self.RepoList = self.controller.Get_repo_list()
        except Exception as e:
            self.log.write('[ERRORE] ' + str(e), 'g')

    def __cloc(self):
        self.log.write('------------------------------------INIZIO CALCOLO CLOC-----------------------------------',
                       'f+g')
        if self.RepoList is None:
            self.RepoList = self.controller.Get_repo_list()
        self.__long_function('source_analyzer', self.RepoList)
        self.log.write('------------------------------------FINE CALCOLO CLOC-----------------------------------',
                       'f+g')
        self.__print_elab('source_analyzer')

    def __dens(self):
        self.log.write('------------------------------------INIZIO CALCOLO DENS-----------------------------------',
                       'f+g')
        if self.RepoList is None:
            self.RepoList = self.controller.Get_repo_list()
        self.__long_function('density_analyzer', self.RepoList)
        self.log.write('------------------------------------FINE CALCOLO DENS-----------------------------------',
                       'f+g')
        self.__print_elab('density_analyzer')

    def __print_elab(self, elab_name):
        for res in self.Elab_results[elab_name]:
            print(res)

    def __density_graph(self, y):
        if self.inputs['elabs']['-DENS KEY-'] is not None:

            x = self.inputs['-DENS KEY-']
            self.__create_win_graph('mod/doc', 'Documentazione/Modificabilità', ' ', x, y)
        else:
            self.log.write('[ERRORE] eseguire un elaborazione di densità', 'g')

    def __salva_dati(self, backup_file):
        self.controller.backup(backup_file)
        self.controller.set_param(self.inputs['token'], backup_file)
        self.log.write('[INFO] SALVATAGGIO ESEGUITO', 'f+g')
