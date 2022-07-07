import time

from github import Github


# Questa classe ha il compito di gestire il rate limit di Github
class Token:
    def __init__(self, token):
        # Tempo da attendere nel caso in cui le richieste superano il numero massimo
        self.waiting_time = 60
        # Token di GitHub
        self.git = Github(token)

    # Metodo della classe che implementa la gestione de rate limit
    def wait_is_usable(self):
        try:
            # Controllo sul limite delle richieste
            if not self.__is_usuable:
                print("Token expired, aspetta per " + str(self.waiting_time) + " secondi")
                # Se si supera le richieste nel minuto aspetta waiting_time
                time.sleep(self.waiting_time)
        except Exception as e:
            raise e

    # metodo della classe che controlla il limite delle richieste
    def __is_usuable(self):
        # Imposto limite max delle richieste
        rate = self.git.get_rate_limit()
        # Calcolo richieste residue
        left = rate.search.remaining
        if left > 5:
            return True
        else:
            return False
