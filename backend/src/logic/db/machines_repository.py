from logic.db.db_connection import DbConnection
from models.machine import Machine


class MachinesRepository:

    def __init__(self, config: dict):
        self.config = config

    def insert(self, machine: Machine):
        with DbConnection(self.config) as con:
            c = con.cursor()
            c.execute("INSERT INTO machines VALUES(?, ?, ?, ?)", (
                str(machine.id),
                str(machine.lab_id),
                machine.default_name,
                machine.display_name
            ))

    def get_by_lab_id(self, lab_id) -> [Machine]:
        with DbConnection(self.config) as con:
            c = con.cursor()
            rows = c.execute("SELECT * FROM machines WHERE lab_id='%s'" % lab_id)
            return [Machine(*r) for r in rows]
