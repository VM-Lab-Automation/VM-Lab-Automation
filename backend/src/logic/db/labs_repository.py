from logic.helpers.date_helper import DateHelper
from models.lab import Lab
from logic.db.db_connection import DbConnection


class LabsRepository:

    def __init__(self, config: dict):
        self.config = config

    def insert(self, lab: Lab):
        with DbConnection(self.config) as con:
            c = con.cursor()
            c.execute("INSERT INTO labs VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (
                str(lab.id),
                lab.name,
                lab.worker_id,
                lab.user_id,
                DateHelper.date_to_ISO_string(lab.created_date),
                lab.lab_template_id,
                DateHelper.date_to_ISO_string(lab.start_date),
                DateHelper.date_to_ISO_string(lab.expiration_date),
                lab.vm_count,
                lab.description
            ))

    def get_all(self):
        with DbConnection(self.config) as con:
            c = con.cursor()
            rows = c.execute("SELECT * FROM labs")
            return [Lab(*r) for r in rows]

    def get_all_by_user(self, user_id):
        with DbConnection(self.config) as con:
            c = con.cursor()
            rows = c.execute("SELECT * FROM labs WHERE user_id=?", str(user_id))
            return [Lab(*r) for r in rows]

    def get_by_id(self, lab_id) -> Lab:
        with DbConnection(self.config) as con:
            c = con.cursor()
            row = c.execute("SELECT * FROM labs WHERE id='{}'".format(lab_id))
            lab_row = row.fetchone()
            if lab_row is None:
                raise Exception("Lab not found")
            return Lab(*lab_row)
