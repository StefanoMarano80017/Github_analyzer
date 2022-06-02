import os
import tempfile
from pygount import SourceAnalysis
from pygount import ProjectSummary

class C_Analysis:
    def __init__(self, group):
        self.counts = {"code_count": None, "doc_count": None, "empty_count": None}
        self.group = group
        self.summary = ProjectSummary()

    def count_file(self, file, suffix: str)->list:
        temp = tempfile.NamedTemporaryFile(suffix = suffix, delete=False)
        temp.write(file)
        list = []

        try:
            c = SourceAnalysis.from_file(temp.name, self.group)
            #self.counts['code_count'] = c.code_count
            #self.counts['doc_count'] = c.documentation_count
            #self.counts['empty_count'] = c.empty_count
            self.summary.add(c)
            print(c)

        except Exception as e:
            print('Errore count file in cloc analize')
            print(e)
        finally:
            temp.close()
            os.unlink(temp.name)
            return list

