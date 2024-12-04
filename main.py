import os

class NetworkPwner:
    def __init__(self):
        self.user = os.system('whoami')
        self.networks = []
        print(self.user)


NetworkPwner()