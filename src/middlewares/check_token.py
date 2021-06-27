from functools import wraps

from flask import request

from config.app import containers
from src.services.user import UserService
from src.utils.responses import response_error


def check_token_of_user(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        userService = containers[UserService]
        uid = None
        result = userService.check_user_auth(request, True)
        if result is None:
            return response_error('token rejected', None, 403)
        uid = result

        return f(uid, *args, **kwargs)

    return decorator


def check_token_register_firebase_user(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        userService = containers[UserService]
        uid = None
        result = userService.check_user_auth(request, False)
        if result is None:
            return response_error('token rejected', None, 403)
        uid = result
        return f(uid, *args, **kwargs)

    return decorator
