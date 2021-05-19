from sqlalchemy import MetaData, String, Table, Column, Integer, DateTime, exists
from sqlalchemy.orm import Session

from logic.db.db_connection import DbConnection
from models.worker import Worker

meta = MetaData()

workers = Table(
   'workers', meta,
   Column('id', String, primary_key = True),
   Column('state', Integer),
   Column('host', String),
   Column('port', String),
   Column('last_updated', DateTime),
)


class WorkerNotFoundException(Exception):
    pass


class WorkersRepository:

    def __init__(self, config: dict):
        self.config = config

    def insert_or_update(self, worker: Worker):
        with DbConnection(self.config) as con:
            with Session(con) as session:
                vals = dict(state=worker.state,
                            host=worker.host,
                            port=worker.api_port,
                            last_updated=worker.last_update)
                ret = session.query(exists().where(workers.c.id == worker.worker_id)).scalar()
                if ret:
                    session.execute(workers.update().where(workers.c.id == worker.worker_id).values(**vals))
                else:
                    session.execute(workers.insert().values(id=worker.worker_id, **vals))
                session.commit()

    def get_all(self):
        with DbConnection(self.config) as con:
            result = con.execute(workers.select())
            rows = result.fetchall()
            return [Worker(*r) for r in rows]

    def get_all_running(self):
        with DbConnection(self.config) as con:
            result = con.execute(workers.select().where(workers.c.state == 1))
            rows = result.fetchall()
            print(rows)
            return [Worker(*r) for r in rows]

    def get_by_id(self, worker_id):
        with DbConnection(self.config) as con:
            result = con.execute(workers.select().where(workers.c.id == worker_id))
            worker_row = result.fetchone()
            if worker_row is None:
                raise WorkerNotFoundException("Worker not found")
            return Worker(*worker_row)
