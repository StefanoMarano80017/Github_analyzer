import PySimpleGUI as sg
from Unit_elaborazione import Controller

cprint = sg.cprint

class Window_Manager:
    def __init__(self):
        sg.theme('BluePurple')
        self.layout = [[sg.Text('Github Rest analyser'), sg.Text(size=(15, 2), key='-LINE1-')],
                      [sg.Multiline(size=(82,20), auto_refresh=True, reroute_stdout=True, reroute_cprint=True, write_only=True, key='-OUT-')],
                      [sg.Text('Inserisci un Token Github per eseguire'), sg.Text(size=(15, 1), key='-LINE2-')],
                      [sg.Input(key='-TOKEN-', size=(85, 1))],
                      [sg.Text('Scrivi la tua query o carica un db compatibile'), sg.Text(size=(15, 1), key='-LINE3-')],
                      [sg.Input(key='-IN-', size=(60,1)), sg.Button('Add Data')],
                      [sg.Text('Elaborazioni'), sg.Text(size=(15, 1), key='-LINE4-')],
                      [sg.FileBrowse('Load Data', file_types=(("File DB", "*.db"),)), sg.Button('Repos'),sg.Button('Exit')]]

        self.titolo = 'prova GUI'
        self.window = sg.Window(self.titolo, self.layout)
        self.db_file= 'Util/db_prova.db' #di default carico i dati in RAM
        self.query = None
        self.token = None
        self.controller = None
        self.query = None
        self.repos = []

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

            self.controller = Controller.Controller(self.token, self.db_file)
            if event == 'Add Data':
                if self.query is not None and self.token is not None:
                    print("Eseguo query git, attendere")
                    self.window.perform_long_operation(lambda: self.controller.get_git_data(self.query, 3), '-END KEY-')
            elif event == 'Repos':
                self.window['-OUT-'].Update('')
                self.repos = self.controller.get_repo()
                for repo in self.repos:
                    print(repo)

            if event == '-END KEY-':
                    print('Inserimento dati nel db terminato')

            if event in (sg.WIN_CLOSED, 'Exit'):
                self.window.close()

