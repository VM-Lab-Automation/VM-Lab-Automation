import sqlite3


class DbConnection:

    def __init__(self, config):
        self.db = config['DATABASE']

    def __enter__(self):
        self.conn = sqlite3.connect(self.db)
        return self.conn

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.conn.commit()
        self.conn.close()
