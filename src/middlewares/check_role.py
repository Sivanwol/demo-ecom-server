from functools import wraps

from firebase_admin import auth
from flask import request

from src.exceptions.unknown_roles import UnknownRolesOrNotMatched
from src.services.roels import RolesService
from src.services.user import UserService
from src.utils.common_methods import verify_response
from src.utils.responses import response_error

roleSerivce = RolesService()
userService = UserService()


def check_role(*role_names):
    def wrapper(f):
        @wraps(f)
        def decorator(*args, **kwargs):
            response = verify_response()
            if response is None:
                try:
                    uid = request.uid
                    if not roleSerivce.check_roles(role_names) or not userService.check_user_roles(uid, role_names):
                        raise UnknownRolesOrNotMatched(role_names)
                except:
                    return response_error('Unauthorized  access', None, 401)
            else:
                return response
            return f(*args, **kwargs)
        return wrapper
