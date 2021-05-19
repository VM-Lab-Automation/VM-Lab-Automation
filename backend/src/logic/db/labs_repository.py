from logic.helpers.date_helper import DateHelper
from models.lab import Lab
from logic.db.db_connection import DbConnection
from sqlalchemy import Table, MetaData, Column, String, Integer, DateTime

meta = MetaData()
labs = Table(
    'labs', meta,
    Column('id', String, primary_key=True),
    Column('name', String),
    Column('worker_id', String),
    Column('user_id', Integer),
    Column('created_date', DateTime),
    Column('lab_template_id', Integer),
    Column('start_date', DateTime),
    Column('expiration_date', DateTime),
    Column('description', String),
    Column('vm_count', Integer),
)


class LabsRepository:

    def __init__(self, config: dict):
        self.config = config

    def insert(self, lab: Lab):
        with DbConnection(self.config) as con:
            con.execute(labs.insert().values(id=str(lab.id),
                                             name=lab.name,
                                             worker_id=lab.worker_id,
                                             user_id=lab.user_id,
                                             created_date=lab.created_date,
                                             lab_template_id=lab.lab_template_id,
                                             start_date=lab.start_date,
                                             expiration_date=lab.expiration_date,
                                             vm_count=lab.vm_count,
                                             description=lab.description))

    def get_all(self):
        with DbConnection(self.config) as con:
            result = con.execute(labs.select())
            rows = result.fetchall()
            return [Lab(*r) for r in rows]

    def get_all_by_user(self, user_id):
        with DbConnection(self.config) as con:
            result = con.execute(labs.select().where(labs.c.user_id == str(user_id)))
            rows = result.fetchall()
            return [Lab(*r) for r in rows]

    def get_by_id(self, lab_id) -> Lab:
        with DbConnection(self.config) as con:
            result = con.execute(labs.select().where(labs.c.id == lab_id))
            lab_row = result.fetchone()
            if lab_row is None:
                raise Exception("Lab not found")
            return Lab(*lab_row)
