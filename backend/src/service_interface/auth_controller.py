from flask import request
from flask_restplus import Resource, Namespace
from werkzeug.exceptions import Unauthorized

from logger import get_logger
from logic.auth_service import NotAuthenticated
from logic.db.users_repository import UserNotFoundException
from logic.helpers.tokens_helper import TokenError
from service_interface import di
from service_interface.decorators.auth_decorator import authorize
from service_interface.model import login_request_model, user_model

api = Namespace('auth', description='Auth related operations')

logger = get_logger(__name__)


@api.route('/login')
class Auth(Resource):

    @api.expect(login_request_model)
    def post(self):
        user = request.json['username']
        password = request.json['password']
        try:
            return {
                'token': di.auth_service.login(user, password)
            }
        except (TokenError, NotAuthenticated, UserNotFoundException) as e:
            logger.info('User {} wasn\'t authenticated. Reason: {}'.format(user, str(e)))
            raise Unauthorized("Incorrect user or password")
        except Exception as e:
            logger.info('Error while authorizing {}: {}'.format(user, str(e)))
            raise Unauthorized("Unable to authenticate at the moment.")


@api.route('/user')
class CurrentUser(Resource):

    @api.marshal_with(user_model)
    @authorize(di.tokens_helper)
    def get(self, user_id):
        return di.auth_service.get_user(user_id)
