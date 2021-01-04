from worker.api.models.lab_request import lab_request
from worker.api.models.lab_template_response import lab_template_response

lab_request = lab_request
lab_template_response = lab_template_response


def register_models(api):
    api.models[lab_request.name] = lab_request
    api.models[lab_template_response.name] = lab_template_response
