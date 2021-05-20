import json
import os

from firebase_admin.auth import UserNotFoundError
from firebase_admin.exceptions import FirebaseError
from config import settings
from config.api import app as current_app
from src.middlewares.check_token import check_token
from src.services.roels import RolesService
from src.services.user import UserService
from src.utils.responses import response_error, response_success
from src.utils.common_methods import verify_uid

roleSerivce = RolesService()
userService = UserService()
print(settings[os.environ.get("FLASK_ENV", "development")].API_ROUTE.format(route="/health"))


@current_app.route(settings[os.environ.get("FLASK_ENV", "development")].API_ROUTE.format(route="/health"))
def get_health():
    return {"status": "OK"}


@check_token
@current_app.route(settings[os.environ.get("FLASK_ENV", "development")].API_ROUTE.format(route="/user/<uid>"))
def get(uid):
    if verify_uid(uid):
        try:
            response = {'user': None, 'extend_info': None}
            response.user = userService.get_user(uid)
            response.extend_info = userService.get_extend_user_info(uid)
            return response_success(response)
        except ValueError:
            return response_error("Error on format of the params", {uid: uid})
        except UserNotFoundError:
            current_app.logger.error("User not found", {uid: uid})
            return response_error("User not found", {uid: uid})
        except FirebaseError as err:
            current_app.logger.error("unknown error", err)
            return response_error("unknown error", {err: err.cause})
    return response_error("Error on format of the params", {uid: uid})


@check_token
@current_app.route(settings[os.environ.get("FLASK_ENV", "development")].API_ROUTE.format(route="/user/<uid>"), methods=["POST"])
def sync_user_create(uid):
    if verify_uid(uid):
        try:
            response = {'user': json.dumps(userService.get_user(uid).__dict__['_data'], indent=4), 'extend_info': None}
            roles = roleSerivce.get_roles(['customer'])
            userService.sync_user(uid, roles)
            response['extend_info'] = userService.get_extend_user_info(uid).to_dict()
            return response_success(response)
        except ValueError:
            return response_error("Error on format of the params", {uid: uid})
        except UserNotFoundError:
            current_app.logger.error("User not found", {uid: uid})
            return response_error("User not found", {uid: uid})
        except FirebaseError as err:
            current_app.logger.error("unknown error", err)
            return response_error("unknown error", {err: err.cause})
    return response_error("Error on format of the params", {uid: uid})
