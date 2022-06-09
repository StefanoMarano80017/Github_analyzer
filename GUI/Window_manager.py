import PySimpleGUI as sg
from Unit_elaborazione import Controller
from Util import logger

cprint = sg.cprint

        #  tasto creare file
        #  query su 'RAM'


class Window_Manager:
    def __init__(self):
        # Creazione stile pagina con relativi bottoni
        sg.theme('BluePurple')
        self.layout = [[sg.Text('Github Rest analyser'), sg.Text(size=(15, 2), key='-LINE1-')],
                       [sg.Multiline(size=(90, 20), auto_refresh=True, reroute_stdout=True, reroute_cprint=True,
                                     write_only=True, key='-OUT-')],
                       [sg.Text('Inserisci un Token Github per eseguire'), sg.Text(size=(15, 1), key='-LINE2-')],
                       [sg.Input(key='-TOKEN-', size=(85, 1))],
                       [sg.Text('Scrivi la tua query o carica un db compatibile'),
                        sg.Text(size=(15, 1), key='-LINE3-')],
                       [sg.Input(key='-IN-', size=(60, 1))],
                       [sg.Text('Operazioni dati')],
                       [sg.Button('Do Query'), sg.FileBrowse('Load Data', file_types=(("File DB", "*.db"),)), sg.Button('Salva Dati')],
                       [sg.Text('Elaborazioni'), sg.Text(size=(15, 1), key='-LINE4-')],
                       [sg.Button('Repos'), sg.Button('Cloc'), sg.Button('Exit')]]

        self.titolo = 'prova GUI'
        self.window = sg.Window(self.titolo, self.layout)
        self.db_file = 'Util/db_prova.db'
        self.query = None
        self.token = None
        self.controller = None
        self.query = None
        self.repos = None
        self.log = logger.logger()

    def event_loop(self):
        while True:  # Event Loop
            event, values = self.window.read()
            self.window.refresh()

            if values['-TOKEN-']:
                self.token = values['-TOKEN-']
            if values['-IN-']:
                self.query = values['-IN-']
            if values['Load Data']:
                self.db_file = values['Load Data']
                self.repos = None

            self.controller = Controller.Controller(self.token, self.db_file, self.log)
            if event == 'Salva Dati':
                if self.repos is not None:
                    self.controller.backup('nuovo.db')
                    self.db_file = 'NUOVA db'
                    self.controller = Controller.Controller(self.token, self.db_file, self.log)
                else:
                    self.log.write('[ERRORE] NESSUN DATO DA SALVARE', 'g')

            if event == 'Do Query':
                if self.query is not None and self.token is not None:
                    self.log.write('---------------------------------------------ESEGUO QUERY GIT--------------------------', 'f+g')
                    self.window.perform_long_operation(lambda: self.controller.get_git_data(self.query, 3), '-END KEY-')
                    self.repos = self.controller.get_repo()
                if self.token is None:
                    self.log.write('[ERRORE] MANCA IL TOKEN', 'g')
                if self.query is None:
                    self.log.write('[ERRORE] MANCA LA QUERY', 'g')

            if event == 'Cloc':
                #if self.repos is not None:
                self.log.write('------------------------------------------CALCOLO CLOC---------------------------------------', 'f+g')
                self.window.perform_long_operation(lambda: self.controller.repo_cloc(), '-CLOC KEY-')

            if event == 'CLOC KEY':
                for cloc in event['CLOC KEY']:
                    print(cloc)

            if event == 'Repos':
                self.window['-OUT-'].Update('')
                self.log.write('--------------------------------------REPOS---------------------------------------------', 'f+g')
                self.repos = self.controller.print_repo()

            if event == '-END KEY-':
                print('Inserimento dati nel db terminato')

            if event in (sg.WIN_CLOSED, 'Exit'):
                # DA METTERE ALLA FINE DEL PROGETTO
                #if self.db_file == 'Util/db_prova.db':
                    #self.controller.close()

                self.log.write('--------------------------------------FINE SESSIONE---------------------------------------------', 'f+g')
                self.window.close()

