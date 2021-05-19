from logic.db.db_connection import DbConnection
from models.machine import Machine
from sqlalchemy import Table, MetaData, Column, String

meta = MetaData()
machines = Table(
    'machines', meta,
    Column('id', String, primary_key=True),
    Column('lab_id', String),
    Column('default_name', String),
    Column('display_name', String),
)


class MachinesRepository:

    def __init__(self, config: dict):
        self.config = config

    def insert(self, machine: Machine):
        with DbConnection(self.config) as con:
            con.execute(machines.insert().values(id=str(machine.id),
                                                 lab_id=str(machine.lab_id),
                                                 default_name=machine.default_name,
                                                 display_name=machine.display_name))

    def get_by_lab_id(self, lab_id) -> [Machine]:
        with DbConnection(self.config) as con:
            result = con.execute(machines.select().where(machines.c.lab_id == lab_id))
            rows = result.fetchall()
            return [Machine(*r) for r in rows]
