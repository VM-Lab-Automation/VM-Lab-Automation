from flask_restplus import Resource, Namespace

from service_interface import di

api = Namespace('lab-types', description='Lab types')


@api.route('')
class LabTypes(Resource):

    def get(self):
        return di.lab_templates_service.get_templates_name()
