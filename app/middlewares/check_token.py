from functools import wraps

from firebase_admin import auth
from flask import request

from app.utils.common_methods import verify_response
from app.utils.responses import response_error


def check_token(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        response = verify_response()
        if response is None:
            if not request.headers.get('authorization'):
                return response_error('No token provided', None, 400)
            try:
                user = auth.verify_id_token(request.headers['authorization'])
                request.user = user
            except:
                return response_error('Invalid token provided', None, 400)
        else:
            return response
        return f(*args, **kwargs)

    return wrap
