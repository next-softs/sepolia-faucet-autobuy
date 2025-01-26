from utils.file_manager import txt_to_list

class Account:
    def __init__(self, private_key):
        self.private_key = private_key

class Accounts:
    def __init__(self):
        self.accounts = []

    def loads_accs(self):
        private_keys = txt_to_list("private_keys")

        for i, private_key in enumerate(private_keys):
            self.accounts.append(Account(private_key=private_key))
