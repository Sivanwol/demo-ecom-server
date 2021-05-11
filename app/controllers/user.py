from firebase_admin.auth import UserNotFoundError
from firebase_admin.exceptions import FirebaseError
from flask import Flask
from flask_restful import Resource

from app import registry
from app.controllers.schemas.user_schema import UserResponseSchema
from app.middlewares.check_token import check_token
from app.services.user import UserService
from app.utils.responses import response_error, response_success
from app.utils.common_methods import verify_uid

app = Flask(__name__)


class User(Resource):
    def __init__(self):
        self.userService = UserService()

    @check_token
    @registry.handles('/user/<uid>', methods=['GET'], response_body_schema=UserResponseSchema)
    def get(self, uid):
        if verify_uid(uid):
            try:
                response = {'user': None, 'extend_info': None}
                response.user = self.userService.get_user(uid)
                response.extend_info = self.userService.get_extend_user_info(uid)
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
    @registry.handles('/user/<uid>', methods=['POST'], response_body_schema=UserResponseSchema)
    def sync_user_create(self, uid):
        if verify_uid(uid):
            try:
                response = {'user': None, 'extend_info': None}
                response.user = self.userService.get_user(uid)
                self.userService.sync_user(uid)
                response.extend_info = self.userService.get_extend_user_info(uid)
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

    def get(self):
        pass

    def post(self):
        pass
