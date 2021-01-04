from werkzeug.exceptions import BadRequest

from worker.api.models import register_models, lab_request, lab_template_response
from flask_restplus import Resource, Api
from flask import request, jsonify, send_file

from worker.api.parsers import bulk_status_params_parser
import datetime

from worker.utils.date_helper import parse_date
from worker.worker import Worker


def parse_iso_datetime_or_throw(datetimestr):
    try:
        return parse_date(datetimestr)
    except Exception as e:
        raise BadRequest(str(e))


def register_endpoints(api: Api, worker: Worker):
    register_models(api)

    @api.route('/stats')
    class Index(Resource):
        def get(self):
            return {
                'id': worker.id
            }

    @api.route('/lab')
    class CreateLab(Resource):
        @api.expect(lab_request)
        def post(self):
            job_id = request.json['lab_id']
            lab_type = request.json['lab_template']
            vm_amount = int(request.json['vm_count'])
            start_date = parse_iso_datetime_or_throw(request.json['start_date'])
            expiration_date = parse_iso_datetime_or_throw(request.json['expiration_date'])

            worker.create_lab(job_id, lab_type, vm_amount, start_date, expiration_date)
            return job_id

    @api.route('/labs/<string:id>/status')
    class LabStatus(Resource):
        def get(self, id):
            lab = worker.lab(id)
            return jsonify(lab.status())

    @api.route('/labs/status')
    @api.expect(bulk_status_params_parser)
    class LabsStatus(Resource):
        def get(self):
            args = bulk_status_params_parser.parse_args()
            ids = args['lab_ids']
            labs = worker.labs(ids)
            return jsonify([l.status(include_machines=False) for l in labs])

    @api.route('/<string:lab_id>/logs')
    class Logs(Resource):
        def get(self, lab_id):
            return jsonify({'logs': worker.logs(lab_id)})

    @api.route('/labs/<string:lab_id>/machine/<string:machine_name>/start')
    class StartMachine(Resource):
        def put(self, lab_id, machine_name):
            worker.lab(lab_id).start_machine(machine_name)

    @api.route('/labs/<string:lab_id>/machine_files')
    class MachineFiles(Resource):
        def get(self, lab_id):
            userdata = worker.lab(lab_id).get_userdata()
            return send_file(userdata, attachment_filename='{}.zip'.format(lab_id), as_attachment=True)

    @api.route('/lab-templates')
    class LabTemplates(Resource):
        @api.marshal_list_with(lab_template_response)
        def get(self):
            return worker.lab_templates()
