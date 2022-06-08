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
                      [sg.Input(key='-IN-', size=(60,1)), sg.FileBrowse('Load Data'), sg.Button('Search Data')],
                      [sg.Text('Elaborazioni'), sg.Text(size=(15, 1), key='-LINE4-')],
                      [sg.Button('Save Data'),sg.Button('Exit')]]

        self.titolo = 'prova GUI'
        self.window = sg.Window(self.titolo, self.layout)
        self.db_file= ':memory:' #di default carico i dati in RAM
        self.query = None
        self.token = None
        self.repos = []
        self.links = []
        self.controller = None

    def event_loop(self):
        while True:  # Event Loop
            event, values = self.window.read()
            print(event, values)

            if values['-TOKEN-'] != '':
                self.token = values['-TOKEN-']
            if event in (sg.WIN_CLOSED, 'Exit'):
                break
            if event == 'Search Data':
                self.__load_data(values)

        self.window.close()


    def __load_data(self, values):
        #Controllo validità della query o del path e ritorno true

        if values['-IN-'] == values['Load Data']:
            self.controller = Controller.Controller(self.token, self.db_file)
            print('----Analizzo le repo nel File')
            self.repos = self.controller.get_repo()
            if self.repos is not None:
                for repo in self.repos:
                    print(repo)

        elif self.token is None:
            cprint('INSERISCE UN TOKEN PER ESEGUIRE UNA QUERY', text_color='red')
        else:
            print('inserita query')


