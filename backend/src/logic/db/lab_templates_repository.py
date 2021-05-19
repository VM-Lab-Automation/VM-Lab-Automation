from logic.db.db_connection import DbConnection
from models.lab_template import LabTemplate
from sqlalchemy import Table, MetaData, Column, String, Integer, DateTime


meta = MetaData()
lab_templates = Table(
   'lab_templates', meta,
   Column('id', Integer, primary_key = True),
   Column('code_name', String),
   Column('lab_name', String)
)


class TemplateNotFoundException(Exception):
    pass


class LabTemplatesRepository:

    def __init__(self, config: dict):
        self.config = config

    def get_all(self) -> [LabTemplate]:
        with DbConnection(self.config) as con:
            result = con.execute(lab_templates.select())
            rows = result.fetchall()
            return [LabTemplate(*r) for r in rows]

    def get_by_lab_name(self, lab_name) -> LabTemplate:
        with DbConnection(self.config) as con:
            result = con.execute(lab_templates.select().where(lab_templates.c.lab_name == lab_name))
            template_row = result.fetchone()
            if template_row is None:
                raise TemplateNotFoundException()
            return LabTemplate(*template_row)
