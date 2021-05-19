from flask_restplus import Resource, Namespace
from flask import request, send_file
from werkzeug.exceptions import Unauthorized

from logic.helpers.date_helper import DateHelper
from models.lab_create_request import LabCreateRequest
from service_interface import di
from service_interface.decorators.auth_decorator import authorize
from service_interface.model import lab_model, create_lab_request_model, lab_details_model
from service_interface.parsers import token_parser

api = Namespace('labs', description='Lab related operations')


@api.route('')
class Labs(Resource):

    @api.marshal_list_with(lab_model)
    @authorize(di.tokens_helper)
    def get(self, user_id):
        return di.labs_service.get_labs_by_user(user_id)

    @api.expect(create_lab_request_model, validate=True)
    @authorize(di.tokens_helper)
    def post(self, user_id):
        lab_name = request.json['lab_name']
        lab_template = request.json['lab_type']
        start_date = DateHelper.datetime_from_ISO_string(request.json['start_date'])
        expiration_date = DateHelper.datetime_from_ISO_string(request.json['expiration_date'])
        machines = request.json['machines']
        description = request.json['description']
        lab_request = LabCreateRequest(lab_name, lab_template, start_date, expiration_date, machines, description, user_id)
        result = di.labs_service.create_lab(lab_request)
        return str(result)


@api.route('/<lab_id>')
class LabDetails(Resource):

    @api.marshal_with(lab_details_model)
    @authorize(di.tokens_helper)
    def get(self, lab_id):
        return di.labs_service.get_lab_details(lab_id)


@api.route('/<string:lab_id>/machine_files')
class LabFiles(Resource):

    @api.expect(token_parser)
    def get(self, lab_id):
        args = token_parser.parse_args()
        try:
            di.tokens_helper.decode_auth_token(args.token)
        except Exception:
            raise Unauthorized()

        return send_file(di.labs_service.get_lab_files(lab_id),
                         attachment_filename='{}.zip'.format(lab_id),
                         as_attachment=True)


@api.route('/<lab_id>/machine/<vm_id>/start')
class LabMachineRestart(Resource):

    @authorize(di.tokens_helper)
    def put(self, lab_id, vm_id):
        di.labs_service.restart_lab_machine(lab_id, vm_id)
