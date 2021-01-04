class LabCreateRequest:

    def __init__(self, lab_name, lab_template_name, start_date, expiration_date, machines, description, user_id):
        self.lab_name = lab_name
        self.lab_template_name = lab_template_name
        self.start_date = start_date
        self.expiration_date = expiration_date
        self.machines = machines
        self.description = description
        self.user_id = user_id
