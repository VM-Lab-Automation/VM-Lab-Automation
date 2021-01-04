from flask_restplus import reqparse

status_parser = reqparse.RequestParser()
status_parser.add_argument('lab_ids', type=str, required=True, help='Ids of labs', action='append')
