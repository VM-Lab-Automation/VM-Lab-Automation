from flask import request
from werkzeug.exceptions import Unauthorized

from logic.helpers.tokens_helper import TokensHelper


def authorize(tokens_helper: TokensHelper):
    def decorator(f):
        def wrapper(*args, **kws):
            if not 'Authorization' in request.headers:
                raise Unauthorized()

            user = None
            data = request.headers['Authorization']
            token = str.replace(str(data), 'Bearer ', '')
            try:
                user = tokens_helper.decode_auth_token(token)
            except:
                raise Unauthorized()

            if 'user_id' in f.__code__.co_varnames:
                return f(user_id=user, *args, **kws)
            else:
                return f(*args, **kws)

        return wrapper

    return decorator
