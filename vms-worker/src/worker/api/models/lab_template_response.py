from flask_restplus import Model, fields

lab_template_response = Model('LabTemplateResponse', {
    'codename': fields.String(),
    'path': fields.String(),
    'provider': fields.String(),
})
