import time

from github import Github


class Token:

    def __init__(self, token):
        self.waiting_time = 60
        self.git = Github(token)

    def wait_is_usable(self):
        try:
            if not self.__is_usuable:
                print("Token expired, aspetta per " + str(self.waiting_time) + " secondi")
                time.sleep(self.waiting_time)
        except Exception as e:
            print(e)

    def __is_usuable(self):

        rate = self.git.get_rate_limit()
        left = rate.search.remaining
        if left > 5:
            return True
        else:
            return False