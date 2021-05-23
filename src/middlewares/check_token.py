from functools import wraps

from flask import request

from src.services.user import UserService
from src.utils.common_methods import verify_response
userService = UserService()


def check_token(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        response = verify_response()
        if response is None:
            return userService.check_user_auth(request)
        else:
            return response
        return f(*args, **kwargs)
    return check_token
