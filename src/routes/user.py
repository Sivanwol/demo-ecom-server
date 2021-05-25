import json
import os

from firebase_admin.auth import UserNotFoundError
from firebase_admin.exceptions import FirebaseError
from config import settings
from config.api import app as current_app
from src.middlewares.check_role import check_role
from src.middlewares.check_token import check_token
from src.services.roels import RolesService
from src.services.user import UserService
from src.utils.enums import RolesTypes
from src.utils.responses import response_error, response_success
from src.utils.common_methods import verify_uid

roleSerivce = RolesService()
userService = UserService()


@current_app.route(settings[os.environ.get("FLASK_ENV", "development")].API_ROUTE.format(route="/health"))
def get_health():
    return {"status": "OK"}


@check_token
@current_app.route(settings[os.environ.get("FLASK_ENV", "development")].API_ROUTE.format(route="/user/<uid>"))
def get(uid):
    if verify_uid(uid):
        try:
            response = {'user': {
                'display_name': '',
                'disabled': False
            }, 'extend_info': None}
            firebase_user_object = userService.get_firebase_user(uid)
            response['user']['display_name'] = firebase_user_object.display_name
            response['user']['disabled'] = firebase_user_object.disabled
            response['extend_info'] = userService.get_user(uid)
            # response['extend_info']['roles'] = role_schema.dump(user.roles)
            return response_success(response)
        except ValueError:
            current_app.logger.error("User not found", {uid: uid})
            return response_error("Error on format of the params", {uid: uid})
        except UserNotFoundError:
            return response_error("User not found", {uid: uid})
        except FirebaseError as err:
            current_app.logger.error("unknown error", err)
            return response_error("unknown error", {err: err.cause})
    return response_error("Error on format of the params", {uid: uid})


@current_app.route(settings[os.environ.get("FLASK_ENV", "development")].API_ROUTE.format(route="/user/passed_tutorial/<uid>/<store_code>"), methods=["PUT"])
@check_token
def mark_user_passed_tutorial(uid, store_code):
    if verify_uid(uid):
        try:
            user = userService.get_user(uid)
            if not user:
                return response_error("User not found", {uid: uid})
            userService.mark_user_passed_tutorial(uid, store_code)
            return response_success({})
        except ValueError:
            current_app.logger.error("User not found", {uid: uid})
            return response_error("Error on format of the params", {uid: uid})
        except UserNotFoundError:
            return response_error("User not found", {uid: uid})
        except FirebaseError as err:
            current_app.logger.error("unknown error", err)
            return response_error("unknown error", {err: err.cause})
    return response_error("Error on format of the params", {uid: uid})


@check_token
@current_app.route(settings[os.environ.get("FLASK_ENV", "development")].API_ROUTE.format(route="/user/<uid>/<store_code>"), methods=["POST"])
def sync_user_create(uid, store_code):
    if verify_uid(uid):
        try:
            response = {'user': json.dumps(userService.get_firebase_user(uid).__dict__['_data'], indent=4), 'extend_info': None}
            roles = roleSerivce.get_roles(['customer'])
            userService.sync_user(uid, roles, store_code)
            response['extend_info'] = userService.get_user(uid).to_dict()
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


# Todo: add logic to create store
@current_app.route(settings[os.environ.get("FLASK_ENV", "development")].API_ROUTE.format(route="/user/create_store/<uid>"), methods=["POST"])
@check_role([RolesTypes.Owner, RolesTypes.Accounts])
def create_store(uid):
    if verify_uid(uid):
        try:
            response = {'user': json.dumps(userService.get_firebase_user(uid).__dict__['_data'], indent=4), 'extend_info': None}
            roles = roleSerivce.get_roles(['customer'])
            userService.sync_user(uid, roles)
            response['extend_info'] = userService.get_user(uid).to_dict()
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



# Todo: add logic to Delete store
@current_app.route(settings[os.environ.get("FLASK_ENV", "development")].API_ROUTE.format(route="/user/create_store/<uid>"), methods=["DELETE"])
@check_role([RolesTypes.Owner, RolesTypes.Accounts])
def delete_store(uid):
    if verify_uid(uid):
        try:
            response = {'user': json.dumps(userService.get_firebase_user(uid).__dict__['_data'], indent=4), 'extend_info': None}
            roles = roleSerivce.get_roles(['customer'])
            userService.sync_user(uid, roles)
            response['extend_info'] = userService.get_user(uid).to_dict()
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
