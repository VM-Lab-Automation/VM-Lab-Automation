class Lab:

    def __init__(self, id, name, worker_id, user_id, created_date, lab_template_id, start_date, expiration_date, vm_count, description):
        self.id = id
        self.name = name
        self.worker_id = worker_id
        self.created_date = created_date
        self.user_id = user_id
        self.lab_template_id = lab_template_id
        self.start_date = start_date
        self.expiration_date = expiration_date
        self.vm_count = vm_count
        self.description = description
