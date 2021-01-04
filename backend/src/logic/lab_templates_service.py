from logic.db.lab_templates_repository import LabTemplatesRepository
from models.lab_template import LabTemplate


class LabTemplatesService:
    def __init__(self, templates_repository: LabTemplatesRepository):
        self.templates_repository = templates_repository

    def get_templates_name(self) -> [str]:
        templates = self.templates_repository.get_all()
        templates_lab_names = list(map(lambda template: template.lab_name, templates))
        return templates_lab_names

    def get_template_by_lab_name(self, lab_name) -> LabTemplate:
        return self.templates_repository.get_by_lab_name(lab_name)

    def get_all(self) -> [LabTemplate]:
        return self.templates_repository.get_all()
