import PySimpleGUI as sg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib

from Unit_elaborazione import Controller
from Util import logger

SIZE_SEARCH = 3

def get_new_window(layout, title):
    return sg.Window(title, layout, finalize=True, resizable=True, element_justification="right")

def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg


class Window_Manager:
    def __init__(self):
        sg.theme('LightGrey1')
        self.layout = [[sg.Text('Github Rest analyser'), sg.Text(size=(15, 2), key='-LINE1-')],
                        [sg.Multiline(size=(90, 20), auto_refresh=True, reroute_stdout=True, reroute_cprint=True,
                        write_only=True, key='-OUT-')],
                        [sg.Text('Inserisci un Token Github per eseguire'), sg.Text(size=(20, 1), key='-LINE2-')],
                        [sg.Input(key='-TOKEN-', size=(90, 1))],
                        [sg.Text('Scrivi la tua query o carica un db compatibile'),
                        sg.Text(size=(20, 1), key='-LINE3-')],
                        [sg.Input(key='-IN-', size=(90, 1))],
                        [sg.Text('Operazioni dati')],
                        [sg.Button('Do Query'), sg.FileBrowse('Load Data', file_types=(("File DB", "*.db"),)),
                        sg.Button('Salva Dati')],
                        [sg.Text('Elaborazioni'), sg.Text(size=(20, 1), key='-LINE4-')],
                        [sg.Button('Repos'), sg.Button('Cloc'), sg.Button('Densità')],
                        [sg.Text('Grafici'), sg.Text(size=(20, 1), key='-LINE5-')],
                        [sg.Button('Documentazione/Modificabilità'),sg.Button('Documentazione/Popolarità')],]

        self.titolo = 'prova GUI'
        self.window = sg.Window(self.titolo, self.layout, finalize=True)
        self.db_file = 'Util/db_default.db'
        self.query = None
        self.token = None
        self.controller = None
        self.query = None
        self.repos = None
        self.cloc_results = None
        self.dens_results = None
        self.log = logger.logger()
        self.log.write(
            '--------------------------------------INIZIO SESSIONE---------------------------------------------', 'f')

    def event_loop(self):
        win_graph1 = None
        win_graph2 = None
        win_salva = None
        while True:  # Event Loop
            windows, event, values = sg.read_all_windows()
            self.controller = Controller.Controller(self.token, self.db_file, self.log)

            if event == sg.WIN_CLOSED:
                if windows == win_graph1:
                    win_graph1.close()
                    win_graph1 = None
                elif windows  == win_graph2:
                    win_graph2.close()
                    win_graph2 = None
                elif windows == win_salva:
                    win_salva.close()
                    win_salva = None
                elif windows == self.window:
                    # DA METTERE ALLA FINE DEL PROGETTO
                    # if self.db_file == 'Util/db_prova.db':
                    # self.controller.close()
                    self.log.write(
                        '--------------------------------------FINE SESSIONE---------------------------------------------',
                        'f')
                    windows.close()
                    break

            if windows == self.window:
                if values['-TOKEN-']:
                    self.token = values['-TOKEN-']
                if values['-IN-']:
                    self.query = values['-IN-']
                if values['Load Data']:
                    self.db_file = values['Load Data']
                    self.repos = None
                    self.log.write('[INFO] FILE CARICATO', 'f+g')

            if event == 'Salva Dati':
                win_salva = self.__salva__window()
            elif event == 'Submit_salva':
                backup = values['-IN SALVA-']
                if backup.find(".db") != -1:
                    win_salva.close()
                    self.__salva_dati(backup)
                else:
                    win_salva.close()
                    print('[ERRORE] IL FILE DEVE AVERE ESTENSIONE .db')

            if event == 'Do Query':
                self.__do_query()
            elif event == 'Repos':
                self.log.write(
                    '--------------------------------------REPOS---------------------------------------------', 'f+g')
                self.repos = self.controller.print_repo()
            elif event == 'Cloc':
                self.log.write(
                    '------------------------------------------CALCOLO CLOC---------------------------------------',
                    'f+g')
                self.window.perform_long_operation(lambda: self.controller.repo_cloc(), '-CLOC KEY-')
            elif event == 'Densità':
                if self.cloc_results is not None:
                    self.log.write(
                        '------------------------------------------CALCOLO DENSITA DOC------------------------------------',
                        'f+g')
                    self.window.perform_long_operation(lambda: self.controller.cloc_density_graph(self.cloc_results), '-DENS KEY-')
                else:
                    self.log.write('[ERRORE] Effettuare prima il calcolo del Cloc', 'f+g')

            if event == '-CLOC KEY-':
                self.cloc_results = values['-CLOC KEY-']
            if event == '-DENS KEY-':
                self.dens_results = values['-DENS KEY-']


            if event == 'Documentazione/Modificabilità':
                if self.dens_results is not None:
                    forks = []
                    for repo in self.cloc_results:
                        forks.append(repo[2])
                    win_graph1 = self.__graph_window('Documentazione/Modificabilità','Documentazione/Modificabilità', self.dens_results, forks)
                else:
                    self.log.write('[ERRORE] Effettuare prima il calcolo delle densità', 'f+g')
            if event == 'Documentazione/Popolarità':
                if self.dens_results is not None:
                    stars = []
                    for repo in self.cloc_results:
                        stars.append(repo[1])
                    win_graph2 = self.__graph_window('Documentazione/Popolarità', 'Documentazione/Popolarità', self.dens_results, stars)
                else:
                    self.log.write('[ERRORE] Effettuare prima il calcolo delle densità', 'f+g')

    def __salva_dati(self,  backup_file):
        self.repos = self.controller.get_repo()
        if self.repos is not None:
            self.controller.backup(backup_file)
            self.db_file = backup_file
            self.controller = Controller.Controller(self.token, self.db_file, self.log)
            self.log.write('[INFO] SALVATAGGIO ESEGUITO', 'f+g')

    def __salva__window(self):
        layout = [[sg.Input(key='-IN SALVA-'), sg.Button('Submit_salva')]]
        return get_new_window(layout, 'Salva file')

    def __do_query(self):
        if self.query is not None and self.token is not None:
            self.log.write(
                '---------------------------------------------ESEGUO QUERY GIT--------------------------',
                'f+g')
            self.window.perform_long_operation(lambda: self.controller.get_git_data(self.query, SIZE_SEARCH),
                                               '-END KEY-')
            self.repos = self.controller.get_repo()
        if self.token is None:
            self.log.write('[ERRORE] MANCA IL TOKEN', 'g')
        if self.query is None:
            self.log.write('[ERRORE] MANCA LA QUERY', 'g')

    def __graph_window(self, title, descrizione, x, y):
        layout = [[sg.Text(descrizione)],
                  [sg.Canvas(key="-CANVAS-")], ]

        win_graph = get_new_window(layout, title)

        fig = matplotlib.figure.Figure(figsize=(5, 4), dpi=100)
        fig.add_subplot(111).plot(x, y, 'o')

        matplotlib.use("TkAgg")
        draw_figure(win_graph['-CANVAS-'].TKCanvas, fig)
        return win_graph