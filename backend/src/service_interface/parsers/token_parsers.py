from flask_restplus import reqparse

token_parser = reqparse.RequestParser()
token_parser.add_argument('token', type=str, required=True, help='User token')
