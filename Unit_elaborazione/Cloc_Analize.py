import os
import tempfile
from pygount import SourceAnalysis
from pygount import ProjectSummary
from contextlib import contextmanager


@contextmanager
def tempinput(data, suffix):
    temp = tempfile.NamedTemporaryFile(suffix=suffix, delete=False)
    temp.write(data)
    temp.close()
    try:
        yield temp.name
    finally:
        os.unlink(temp.name)


class C_Analysis:
    def __init__(self, group):
        self.counts = {"code_count": None, "doc_count": None, "empty_count": None}
        self.group = group
        self.summary = ProjectSummary()


    def count_file(self, code, suffix:str):
        with tempinput(code, suffix) as tmp:
            try:
                c = SourceAnalysis.from_file(tmp, self.group)
                self.summary.add(c)
            except Exception as e:
                print(e)

    def get_summary(self):
        self.counts["code_count"]  = self.summary.total_code_count
        self.counts["doc_count"]   = self.summary.total_documentation_count
        self.counts["empty_count"] = self.summary.total_empty_count
        return self.counts