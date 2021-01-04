from flask import request
from flask_restplus import Resource, Namespace

from service_interface import di
from service_interface.model import worker_model, state_request_model

api = Namespace('workers', description='Workers related operations')


@api.route('')
class Workers(Resource):

    @api.marshal_list_with(worker_model)
    def get(self):
        return di.worker_service.get_workers()

    @api.expect(state_request_model)
    def post(self):
        worker_id = str(request.json['worker_id'])
        host = request.json['host']
        port = request.json['port']
        state = int(request.json['state'])
        di.worker_service.update_state(worker_id, state, host, port)
