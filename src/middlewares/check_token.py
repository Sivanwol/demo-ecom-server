from functools import wraps

from flask import request

from config.containers import container
from src.services.user import UserService
from src.utils.common_methods import verify_response



def check_token_of_user(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        userService = container[UserService]
        response = verify_response()
        if response is None:
            result =  userService.check_user_auth(request, True)
            if result is not None:
                return result

        return f(*args, **kwargs)

    return decorator


def check_token_register_firebase_user(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        userService = app[UserService]
        response = verify_response()
        if response is None:
            result =  userService.check_user_auth(request, False)
            if result is not None:
                return result
        return f(*args, **kwargs)

    return decorator
