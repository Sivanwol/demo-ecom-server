from functools import wraps
from flask import request

from config.containers import app,container
from src.services.user import UserService
from src.exceptions.unknown_roles import UnknownRolesOrNotMatched
from src.utils.common_methods import verify_response
from src.utils.responses import response_error


def check_role(*role_names):
    def wrapper(f):
        @wraps(f)
        def decorator(*args, **kwargs):
            userService = container[UserService]
            response = verify_response()
            uid = None
            if response is None:
                try:
                    res = userService.check_user_auth(request, True)
                    if res is not None:
                        uid = res

                    if not userService.check_user_roles(uid, role_names):
                        raise UnknownRolesOrNotMatched(role_names)
                except Exception as e:
                    app.flask_app.logger.error(e)
                    return response_error('Unauthorized  access', None, 401)
            return f(uid,*args, **kwargs)
        return decorator
    return wrapper
