from functools import wraps
from flask import request

from config.app import containers,app
from src.services.user import UserService
from src.exceptions.unknown_roles import UnknownRolesOrNotMatched
from src.utils.responses import response_error


def check_role(*role_names):
    def wrapper(f):
        @wraps(f)
        def decorator(*args, **kwargs):
            userService = containers[UserService]
            try:
                result = userService.check_user_auth(request, True)

                if result is None:
                    return response_error('token rejected', None, 403)
                uid = result
                if not userService.check_user_roles(uid, role_names):
                    raise UnknownRolesOrNotMatched(role_names)
            except Exception as e:
                app.flask_app.logger.error(e)
                return response_error('Unauthorized  access', None, 401)
            return f(uid, *args, **kwargs)

        return decorator

    return wrapper
