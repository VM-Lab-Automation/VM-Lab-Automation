from flask_restplus import fields, Model

machine_model = Model("Machine model", {
    "id": fields.String(),
    "name": fields.String(),
    "status": fields.String(),
    "rdp_address": fields.String(),
    "ssh_address": fields.String(),
    "login": fields.String(),
    "password": fields.String()
})

lab_details_model = Model("Lab details model", {
    "lab_id": fields.String(),
    "status": fields.String(),
    "lab_name": fields.String(),
    "machines": fields.List(fields.Nested(machine_model))
})

create_lab_request_model = Model("Create lab request", {
    "lab_name": fields.String(description="Lab name", required=True),
    "lab_type": fields.String(description="Lab type", required=True),
    "start_date": fields.String(description="Start date", required=True),
    "expiration_date": fields.String(description="Expiration date", required=True),
    "description": fields.String(description="Description", required=True),
    "machines": fields.List(fields.String(), description="Machines name")
})

lab_model = Model("Lab model", {
    "id": fields.String(),
    "name": fields.String(),
    "worker_id": fields.String(),
    "created_date": fields.DateTime(dt_format="iso8601"),
    "lab_type": fields.String(),
    "start_date": fields.DateTime(dt_format="iso8601"),
    "expiration_date": fields.DateTime(dt_format="iso8601"),
    "description": fields.String(),
    "vm_count": fields.Integer(),
    "status": fields.String()
})

