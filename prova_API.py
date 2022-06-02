from pygount import SourceAnalysis
import os
import tempfile
from contextlib import contextmanager
import requests

@contextmanager
def tempinput(data):
        temp = tempfile.NamedTemporaryFile(suffix='.py', delete=False)
        temp.write(data)
        temp.close()
        try:
            yield temp.name
        finally:
            os.unlink(temp.name)


def prova_loc():

    link = 'https://raw.githubusercontent.com/SOM-Research/Gitana/master/gitana/gitana.py'
    f = requests.get(link)

    with tempinput(f.content) as tp:
        try:
            c = SourceAnalysis.from_file(tp, 'prova')
            print(c.code_count)
            print(c.documentation_count)
            print(c.empty_count)
        except Exception as e:
            print(e)