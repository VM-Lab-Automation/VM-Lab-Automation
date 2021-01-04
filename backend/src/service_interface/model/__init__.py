import service_interface.model.labs_models
import service_interface.model.auth_models
from service_interface.model import workers_models

machine_model = labs_models.machine_model
lab_details_model = labs_models.lab_details_model
create_lab_request_model = labs_models.create_lab_request_model
lab_model = labs_models.lab_model
login_request_model = auth_models.login_request_model
user_model = auth_models.user_model
state_request_model = workers_models.state_request_model
worker_model = workers_models.worker_model


def register_models(api):
    models_to_register = [
        machine_model,
        lab_details_model,
        create_lab_request_model,
        lab_model,
        login_request_model,
        user_model,
        state_request_model,
        worker_model
    ]
    for model in models_to_register:
        api.models[model.name] = model
