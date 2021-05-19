from sqlalchemy import *



class ConnectionFactory:
    def __init__(self, config):
        self.engine = create_engine(config['DATABASE_CONNECTION_STRING'])

    def create_connection(self):
        return self.engine.connect()

class DbConnection:

    def __init__(self, config):
        self.connection_factory = ConnectionFactory(config)

    def __enter__(self):
        self.conn = self.connection_factory.create_connection()
        return self.conn

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.conn.close()
