import os
import tempfile
from contextlib import contextmanager

from pygount import ProjectSummary
from pygount import SourceAnalysis


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
        self.group = group
        self.summary = ProjectSummary()

    def count_file(self, code, suffix: str):
        with tempinput(code, suffix) as tmp:
            try:
                c = SourceAnalysis.from_file(tmp, self.group)
                self.summary.add(c)
            except Exception as e:
                print(e)

    def get_summary(self) -> list:
        return [self.summary.total_code_count, self.summary.total_documentation_count, self.summary.total_empty_count]
