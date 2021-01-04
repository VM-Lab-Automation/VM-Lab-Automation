from models.worker import Worker
from logic.db.db_connection import DbConnection


class WorkersRepository:

    def __init__(self, config: dict):
        self.config = config

    def insert_or_update(self, worker: Worker):
        with DbConnection(self.config) as con:
            c = con.cursor()
            c.execute("INSERT OR REPLACE INTO workers VALUES(?, ?, ?, ?, ?)",(str(worker.worker_id), worker.state, worker.host, worker.api_port, worker.last_update))

    def get_all(self):
        with DbConnection(self.config) as con:
            c = con.cursor()
            rows = c.execute("SELECT * FROM workers")
            return [Worker(*r) for r in rows]

    def get_all_running(self):
        with DbConnection(self.config) as con:
            c = con.cursor()
            rows = c.execute("SELECT * FROM workers WHERE state=1")
            return [Worker(*r) for r in rows]

    def get_by_id(self, worker_id):
        with DbConnection(self.config) as con:
            c = con.cursor()
            row = c.execute("SELECT * FROM workers WHERE id='{}'".format(worker_id))
            worker_row = row.fetchone()
            if worker_row is None:
                raise Exception("Worker not found")
            return Worker(*worker_row)