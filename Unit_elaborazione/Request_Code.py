import requests

# Con questa classe vengono gestiti i download delle raw github
class extract_code:
    #Costruttore della classe in cui viene passato il link
    def __init__(self, link):
        self.link = link

    # Il metodo che effettua il download dei link
    def get_page(self):
        try:
           #Metodo della libreria requests per il download dei singolo file di una repository
            return requests.get(self.link)
        except requests.exceptions.Timeout as e:
            # Gestione errore in caso di timeout
            print(e.response.text)
        except requests.exceptions.TooManyRedirects as e:
            #Gestione errore in caso di troppe redirezioni delle pagine
            print(e.response.text)
        except requests.exceptions.RequestException as e:
            #Gestione errore catastrofico. Uscita dal programma
            raise SystemExit(e)

    #Metodo della classe per ottenere il codice del file appena scaricato
    def get_content(self):
        file = self.get_page()
        try:
            return file.content
        except Exception as e:
            print('errore get content page')
            print(e)
