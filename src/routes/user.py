import json
import os

from firebase_admin.auth import UserNotFoundError
from firebase_admin.exceptions import FirebaseError
from flask import request

from config import settings
from config.api import app as current_app
from src.middlewares.check_role import check_role
from src.middlewares.check_token import check_token
from src.schemas.user_schema import FirebaseUserSchema
from src.serializers.create_platform_user import CreatePlatformUser
from src.services.roles import RolesService
from src.services.store import StoreService
from src.services.user import UserService
from src.utils.enums import RolesTypes
from src.utils.responses import response_error, response_success
from src.utils.common_methods import verify_uid

roleSerivce = RolesService()
userService = UserService()
storeService = StoreService()


@current_app.route(settings[os.environ.get("FLASK_ENV", "development")].API_ROUTE.format(route="/user/<uid>"))
def get(uid):
    if verify_uid(uid):
        try:
            response = {
                'user_meta': None,
                'user_data': None
            }
            firebaseUserSchema = FirebaseUserSchema()
            firebase_response = {
                'display_name': '',
                'disabled': False
            }
            firebase_user_object = userService.get_firebase_user(uid)
            firebase_response['display_name'] = firebase_user_object.display_name
            firebase_response['disabled'] = firebase_user_object.disabled

            response['user_meta'] = firebaseUserSchema.dump(firebase_response)
            response['user_data'] = userService.get_user(uid)
            # response['extend_info']['roles'] = role_schema.dump(user.roles)
            return response_success(response)
        except ValueError:
            current_app.logger.error("User not found", {uid: uid})
            return response_error("Error on format of the params", {uid: uid})
        except UserNotFoundError:
            return response_error("User not found", {uid: uid}, 404)
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
            if not user or user.is_pass_tutorial:
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


@current_app.route(settings[os.environ.get("FLASK_ENV", "development")].API_ROUTE.format(route="/user/<uid>/<store_code>"), methods=["POST"])
@check_token
def sync_store_user_create(uid, store_code):
    if verify_uid(uid):
        try:
            store = storeService.get_store(uid, store_code, True)
            if store is None:
                return response_error("Store not found", {store_code: store_code})
            roles = roleSerivce.get_roles([RolesTypes.StoreCustomer.value])
            return response_success(get_user_object(uid, roles, False))
        except ValueError:
            return response_error("Error on format of the params", {uid: uid})
        except UserNotFoundError:
            current_app.logger.error("User not found", {uid: uid})
            return response_error("User not found", {uid: uid})
        except FirebaseError as err:
            current_app.logger.error("unknown error", err)
            return response_error("unknown error", {err: err.cause})
    return response_error("Error on format of the params", {uid: uid})


@current_app.route(settings[os.environ.get("FLASK_ENV", "development")].API_ROUTE.format(route="/user/<uid>"), methods=["POST"])
@check_role([RolesTypes.Accounts.value, RolesTypes.Owner.value])
def sync_platform_user_create(uid):
    if request.is_json:
        return response_error("Request Data must be in json format", request.data)
    if verify_uid(uid):
        try:
            body = request.json()
            bodyObj = {"role_names": ', '.join(body['role_names'])}
            data = CreatePlatformUser(**bodyObj)
            if roleSerivce.check_roles(data.role_names):
                return response_error("One or more of fields are invalid", request.data)

            roles = roleSerivce.get_roles(data.role_names)
            return response_success(get_user_object(uid, roles, True))
        except ValueError:
            return response_error("Error on format of the params", {uid: uid})
        except UserNotFoundError:
            current_app.logger.error("User not found", {uid: uid})
            return response_error("User not found", {uid: uid})
        except FirebaseError as err:
            current_app.logger.error("unknown error", err)
            return response_error("unknown error", {err: err.cause})
    return response_error("Error on format of the params", {uid: uid})


def get_user_object(uid, role_names, is_platform_user):
    response = {'user': json.dumps(userService.get_firebase_user(uid).__dict__['_data'], indent=4), 'extend_info': None}
    roles = roleSerivce.get_roles(role_names)
    userService.sync_firebase_user(uid, roles, is_platform_user)
    response['extend_info'] = userService.get_user(uid)
    return response
