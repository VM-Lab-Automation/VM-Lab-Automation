from logic.db.db_connection import DbConnection
from models.lab_template import LabTemplate


class TemplateNotFoundException(Exception):
    pass


class LabTemplatesRepository:

    def __init__(self, config: dict):
        self.config = config

    def get_all(self) -> [LabTemplate]:
        with DbConnection(self.config) as con:
            c = con.cursor()
            rows = c.execute("SELECT * FROM lab_templates ")
            return [LabTemplate(*r) for r in rows]

    def get_by_lab_name(self, lab_name) -> LabTemplate:
        with DbConnection(self.config) as con:
            c = con.cursor()
            rows = c.execute("SELECT * FROM lab_templates WHERE lab_name='%s' LIMIT 1" % lab_name)
            template_row = rows.fetchone()
            if template_row is None:
                raise TemplateNotFoundException()
            return LabTemplate(*template_row)
