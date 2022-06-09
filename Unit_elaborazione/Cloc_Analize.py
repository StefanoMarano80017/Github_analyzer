import os
import tempfile
from contextlib import contextmanager

from pygount import ProjectSummary
from pygount import SourceAnalysis


# Funzione che effettua la gestione di contesto per i file temporanei
@contextmanager
def tempinput(data, suffix):
    suffix = "." + suffix
    temp = tempfile.NamedTemporaryFile(suffix=suffix, delete=False)
    temp.write(data)
    temp.close()
    try:
        yield temp.name
    finally:
        # Con questa chiamata il sistema operativo dealloca il file dal filesystem
        os.unlink(temp.name)


# Questa classe ha il compito di effettuare l'analisi del codice
class C_Analysis:
    def __init__(self, group):
        """
        Il parametro group è un ID per la repository
        Il parametro summary viene salvato il risultato del parser cloc
        ProjectSummary() è un API fornita dalla libreria pygount per la gestione dei resoconti di un progetto
        """
        self.group = group
        self.summary = ProjectSummary()

    def count_file(self, data, suffix: str):
        with tempinput(data, suffix) as tmp:
            try:
                """
                SourceAnalysis.from_file() è una funzione dell'API fornita dalla libreria pygount per l'analisi del codice 
                """
                c = SourceAnalysis.from_file(tmp, self.group)
                self.summary.add(c)
                #print(c)
                #qui logger
            except Exception as e:
                raise e

    def get_summary(self) -> list:
        return [self.summary.total_code_count, self.summary.total_documentation_count, self.summary.total_empty_count]
