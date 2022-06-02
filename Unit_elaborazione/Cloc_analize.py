from pygount import SourceAnalysis


class Cloc_Analize:
    def __init__(self, lang, estensione):
        self.lang = lang
        self.estensione = estensione
        self.documentation_count = None

    def count_from_file(self, file_path: str, group: str):
        try:
            c = SourceAnalysis.from_file(file_path, group)
            self.documentation_count = c.documentation_count
        except Exception as e:
            print(e)
