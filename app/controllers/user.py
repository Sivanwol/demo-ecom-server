from firebase_admin.auth import UserNotFoundError
from firebase_admin.exceptions import FirebaseError
from flask import Flask
from flask_restful import Resource

from app.utils.rebar_utils import RebarUtils
from app.controllers.schemas.user_schema import UserResponseSchema
from app.middlewares.check_token import check_token
from app.services.user import UserService
from app.utils.responses import response_error, response_success
from app.utils.common_methods import verify_uid

app = Flask(__name__)

rebar = RebarUtils()
userService = UserService()

@check_token
@rebar.registry.handles(rule='/user/<uid>', method='GET', response_body_schema=UserResponseSchema())
def get( uid):
    if verify_uid(uid):
        try:
            response = {'user': None, 'extend_info': None}
            response.user = userService.get_user(uid)
            response.extend_info = userService.get_extend_user_info(uid)
            return response_success(response)
        except ValueError:
            return response_error("Error on format of the params", {uid: uid})
        except UserNotFoundError:
            app.logger.error("User not found", {uid: uid})
            return response_error("User not found", {uid: uid})
        except FirebaseError as err:
            app.logger.error("unknown error", err)
            return response_error("unknown error", {err: err.cause})
    return response_error("Error on format of the params", {uid: uid})

@check_token
@rebar.registry.handles(rule='/user/<uid>', method='POST', response_body_schema=UserResponseSchema())
def sync_user_create(uid):
    if verify_uid(uid):
        try:
            response = {'user': None, 'extend_info': None}
            response.user = userService.get_user(uid)
            userService.sync_user(uid)
            response.extend_info = userService.get_extend_user_info(uid)
            return response_success(response)
        except ValueError:
            return response_error("Error on format of the params", {uid: uid})
        except UserNotFoundError:
            app.logger.error("User not found", {uid: uid})
            return response_error("User not found", {uid: uid})
        except FirebaseError as err:
            app.logger.error("unknown error", err)
            return response_error("unknown error", {err: err.cause})
    return response_error("Error on format of the params", {uid: uid})


class UserList(Resource):
    @check_token
    def get(self):
        pass

