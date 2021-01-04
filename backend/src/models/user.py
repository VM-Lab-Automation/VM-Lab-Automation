class User:

    def __init__(self, id, username, password_hash, email):
        self.id = id
        self.username = username
        self.email = email
        self.password_hash = password_hash
