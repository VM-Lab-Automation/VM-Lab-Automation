from datetime import datetime


class Lab:

    def __init__(self, id: str,
                 name: str,
                 worker_id: str,
                 user_id: int,
                 created_date: datetime,
                 lab_template_id: int,
                 start_date: datetime,
                 expiration_date: datetime,
                 description: str,
                 vm_count: int):
        self.id = id
        self.name = name
        self.worker_id = worker_id
        self.user_id = user_id
        self.created_date = created_date
        self.lab_template_id = lab_template_id
        self.start_date = start_date
        self.expiration_date = expiration_date
        self.description = description
        self.vm_count = vm_count
