import jwt
from datetime import datetime, timedelta

from logger import get_logger

logger = get_logger(__name__)


class TokenError(Exception):
    pass


class SecretKeyError(Exception):
    pass


class TokensHelper:

    def __init__(self, config: dict):
        self.token = config['JWT_SECRET']

    def get_secret_key(self):
        key = self.token
        if key == '':
            logger.critical("Unable to find secret key. Please set JWT_SECRET environmental variable")
            raise SecretKeyError()
        return key

    def decode_auth_token(self, auth_token):
        try:
            payload = jwt.decode(auth_token, self.get_secret_key())
            return int(payload['sub'])
        except jwt.ExpiredSignatureError:
            raise TokenError('Signature expired.')
        except jwt.InvalidTokenError:
            raise TokenError('Invalid token.')
        except:
            raise TokenError('Unknown error while decoding token.')

    def encode_auth_token(self, user_id: int):
        payload = {
            'exp': datetime.utcnow() + timedelta(days=1),
            'iat': datetime.utcnow(),
            'sub': user_id
        }
        return str(jwt.encode(
            payload,
            self.get_secret_key(),
            algorithm='HS256'
        ), encoding='utf-8')
