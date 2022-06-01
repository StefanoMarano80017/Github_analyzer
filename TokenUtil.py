import time


class Token:

    def __init__(self, token):
        self.waiting_time = 3600
        self.token = token

    def _is_usuable(self):
        # checks that a token has requests left
        try:
            left = self.token.rate_limiting[0]
        except:
            raise "TokenUtil, impossibile ricavare token"

        if left:
            check = left > 50
        else:
            check = False

        return check

    def wait_is_usable(self):
        if not self._is_usuable:
            print("Token expired, aspetta per " + str(self.waiting_time) + " seconds")
            time.sleep(self.waiting_time)
