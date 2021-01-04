from flask import Flask
from flask_cors import CORS
from flask_restplus import Api

from di import DIContainer
from logic.workers import worker_observer
from service_interface.model import register_models
import os

app = Flask("Virtual lab manager")
app.config.from_object('config.{}Config'.format(os.getenv('FLASK_ENV').capitalize()))

CORS(app)

authorizations = {
    'Bearer Auth': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    }
}
api = Api(app, doc='/api/', security='Bearer Auth', authorizations=authorizations)

register_models(api)

di = DIContainer(app.config)

from service_interface.lab_controller import api as lab_ns
from service_interface.workers_controller import api as worker_ns
from service_interface.lab_types_controller import api as lab_types_ns
from service_interface.auth_controller import api as auth_ns

api.add_namespace(auth_ns, '/api/auth')
api.add_namespace(lab_ns, '/api/labs')
api.add_namespace(worker_ns, '/api/workers')
api.add_namespace(lab_types_ns, '/api/lab-types')

workers_observer_thread = worker_observer.start_workers_observer_thread(di.worker_repository)
