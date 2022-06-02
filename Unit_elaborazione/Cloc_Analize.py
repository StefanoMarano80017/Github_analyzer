import os
import tempfile
from contextlib import contextmanager
from pygount import SourceAnalysis


@contextmanager
def tempinput(data, suffix: str):
    temp = tempfile.NamedTemporaryFile(suffix, delete=False)
    temp.write(data)
    temp.close()
    try:
        yield temp.name
    finally:
        os.unlink(temp.name)


class C_Analysis:
    def __init__(self, suffix, group):
        self.documentation_count = None
        self.group = group

    def count_file(self, data, suffix):
        with tempinput(data, suffix) as path:
            try:
                c = SourceAnalysis.from_file(path, self.group)
                print(c.code_count)
                print(c.documentation_count)
                print(c.empty_count)
            except Exception as e:
                print('Errore count file in cloc analize')
                print(e)
