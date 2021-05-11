from firebase_admin.auth import UserNotFoundError
from firebase_admin.exceptions import FirebaseError
from flask import Flask
from flask_restful import Resource
from app.middlewares.check_token import check_token
from app.services.user import UserService
from app.utils.responses import response_error
from app.utils.user_methods import verify_uid

app = Flask(__name__)

class User(Resource):
    def __init__(self):
        self.userSerivce = UserService()

    @check_token
    def get(self, uid):
        if verify_uid(uid):
            try:
                self.userSerivce.get_user(uid)
            except ValueError:
                return response_error("Error on format of the params", {uid: uid})
            except UserNotFoundError:
                app.logger.error("User not found", {uid: uid})
                return response_error("User not found", {uid: uid})
            except FirebaseError as err:
                app.logger.error("unknown error", err)
                return response_error("unknown error", {err: err.cause})
        else:
            return response_error("Error on format of the params", {uid: uid})

    def get_extended_user_info(self, uid):
        if verify_uid(uid):
            pass
        else:
            return response_error("Error on format of the params", {uid: uid})


    def put(self, id):
        pass

    def patch(self, id):
        pass

    def delete(self, id):
        pass


class UserList(Resource):

    def get(self):
        pass

    def post(self):
        pass


