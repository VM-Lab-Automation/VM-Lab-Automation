from datetime import datetime
from io import BytesIO

from worker.logger import get_logger

from worker.lab_templates import LabTemplatesRepository
from worker.labs.lab import Lab, create_lab
from worker.labs.lab_status import LabStatus
from worker.labs.labs_repository import LabsRepository


class Worker:
    def __init__(self, id, host, port, labs_repository: LabsRepository, lab_templates_repository: LabTemplatesRepository):
        self.port = port
        self.host = host
        self.id = id
        self.labs_repository = labs_repository
        self.lab_templates_repository = lab_templates_repository

    def create_lab(self, lab_id: str, lab_template_codename: str, vm_count: int, start_date: datetime, expiration_date: datetime):
        template = self.lab_templates_repository.get(lab_template_codename)
        lab = create_lab(template,
                         lab_id,
                         vm_count=vm_count,
                         start_date=start_date,
                         expiration_date=expiration_date,
                         status=LabStatus.PREPARING)
        if start_date <= datetime.now():
            lab.start()

    def lab(self, lab_id) -> Lab:
        return self.labs_repository.get(lab_id)

    def labs(self, lab_ids=None) -> [Lab]:
        if lab_ids is None:
            return self.labs_repository.all()
        return self.labs_repository.get_many(lab_ids)

    def logs(self, id) -> str:
        return self.labs_repository.get(id).logs()

    def userdata(self, id) -> BytesIO:
        return self.labs_repository.get(id).get_userdata()

    def lab_templates(self):
        return self.lab_templates_repository.get_all()
