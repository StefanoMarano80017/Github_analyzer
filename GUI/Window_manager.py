import PySimpleGUI as sg
import sys

class Window_Manager:
    def __init__(self):
        sg.theme('BluePurple')
        self.layout = [[sg.Text('Your typed chars appear here:'), sg.Text(size=(15, 1), key='-OUTPUT-')],
                      [sg.Input(key='-IN-')],
                      [sg.Button('Search Data'), sg.Button('Save Data'),  sg.FileBrowse('Load Data'),  sg.Button('Exit')]]

        self.titolo = 'prova GUI'
        self.window = self.__start()
        self.db_file= ':memory:' #di default carico i dati in RAM
        self.query = None
        self.token = None

    def __start(self):
        return sg.Window(self.titolo, self.layout)

    def event_loop(self):
        while True:  # Event Loop
            event, values = self.window.read()
            print(event, values, self.db_file)

            if event == sg.WIN_CLOSED or 'Exit':
                break
            if event:
                self.db_file = values[1]

        self.window.close()




