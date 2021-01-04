from flask_restplus import fields, Model

state_request_model = Model("POST worker state", {
    "worker_id": fields.String(description="Worker id", required=True),
    "host": fields.String(description="External address of worker", required=True),
    "port": fields.String(description="Port that worker is exposing api", required=True),
    "state": fields.Integer(description="Worker state (1 = RUNNING, 2 = NOT_RUNNING)", required=True),
})
worker_model = Model("Worker model", {
    "state": fields.Integer(),
    "worker_id": fields.String(),
    "host": fields.String(),
    "api_port": fields.String(),
    "last_update": fields.DateTime(dt_format="iso8601"),
})
