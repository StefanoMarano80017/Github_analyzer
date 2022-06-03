import requests


class extract_code:
    def __init__(self, link):
        self.link = link

    def get_page(self):
        # link = 'https://raw.githubusercontent.com/SOM-Research/Gitana/master/gitana/gitana.py'
        try:
            return requests.get(self.link)
        except Exception as e:
            print('eccezione requests')
            print(e)

    def get_content(self):
        file = self.get_page()
        try:
            return file.content
        except Exception as e:
            print('errore get content page')
            print(e)
