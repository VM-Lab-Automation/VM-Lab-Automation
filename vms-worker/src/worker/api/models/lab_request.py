from flask_restplus import Model, fields

lab_request = Model('LabRequest', {
    'lab_id': fields.String(required=True),
    'lab_template': fields.String(required=True),
    'vm_count': fields.Integer(required=True),
    'start_date': fields.DateTime(required=True),
    'expiration_date': fields.DateTime(required=True)
})
