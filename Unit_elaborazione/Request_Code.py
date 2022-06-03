import requests


class extract_code:
    def get_page(self, link: str):
        # link = 'https://raw.githubusercontent.com/SOM-Research/Gitana/master/gitana/gitana.py'
        try:
            return requests.get(link)
        except Exception as e:
            print('eccezione requests')
            print(e)

    def get_content(self, link: str):
        file = self.get_page(link)
        try:
            return file.content
        except Exception as e:
            print('errore get content page')
            print(e)
