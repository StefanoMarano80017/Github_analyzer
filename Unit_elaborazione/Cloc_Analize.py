import os
import tempfile
from contextlib import contextmanager

from pygount import ProjectSummary
from pygount import SourceAnalysis

#Funzione che effettua la gestione di contesto
@contextmanager
def tempinput(data, suffix):
    #Generazione estensione
    suffix = "." + suffix
    #Creazione file temporaneo
    temp = tempfile.NamedTemporaryFile(suffix=suffix, delete=False)
    #Scrittura file temporaneo
    temp.write(data)
    #Chiusura file temporaneo
    temp.close()
    try:
        yield temp.name
    finally:
        #Con questa chiamata il sistema operativo dealloca il file dal file system
        os.unlink(temp.name)

#Questa classe ha il compito di effettuare l'analisi del codice
class C_Analysis:
    def __init__(self, group):
        #Il parametro group identifica un insieme di file di un singola repository
        self.group = group
        #Il parametro summary viene salvato il risultato del parser cloc
        #ProjectSummary() è un API fornita dalla libreria pygount per la gestione dei resoconti di un progetto
        self.summary = ProjectSummary()

    def count_file(self, data, suffix: str):
        #Creazione e apertura file
        with tempinput(data, suffix) as tmp:
            try:
                #SourceAnalysis.from_file() è una funzione dell'API fornita dalla libreria pygount per l'elaborazione
                c = SourceAnalysis.from_file(tmp, self.group)
                self.summary.add(c)
            except Exception as e:
                print(e)

    def get_summary(self) -> list:
        return [self.summary.total_code_count, self.summary.total_documentation_count, self.summary.total_empty_count]
