import json
import os

from firebase_admin.auth import UserNotFoundError
from firebase_admin.exceptions import FirebaseError
from flask import request
from marshmallow import ValidationError
from config import settings
from config.containers import app as current_app, container
from src.middlewares import check_role, check_token_register_firebase_user, check_token_of_user
from src.schemas.requests import UserRolesList, CreateStoreStaffUser, UpdateUserInfo
from src.schemas import UserSchema
from src.services import FileSystemService, RoleService, StoreService, UserService
from src.utils.enums import RolesTypes
from src.utils.general import Struct
from src.utils.responses import response_error, response_success, response_success_paging
from src.utils.common_methods import verify_uid
from src.utils.validations import vaild_per_page, valid_user_list_by_permissions, valid_currency_code, valid_country_code, valid_user_list_params


@current_app.route(settings[os.environ.get("FLASK_ENV", "development")].API_ROUTE.format(route="/user/<uid>"))
def get(uid):
    userService = container[UserService]
    if verify_uid(userService, uid):
        try:
            firebase_response = {
                'display_name': '',
                'disabled': False
            }
            firebase_user_object = userService.get_firebase_user(uid)
            firebase_response['display_name'] = firebase_user_object.display_name
            firebase_response['disabled'] = firebase_user_object.disabled
            response = {
                'user_meta': firebase_response,
                'user_data': userService.get_user(uid)
            }
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


@current_app.route(settings[os.environ.get("FLASK_ENV", "development")].API_ROUTE.format(route="/user/list"))
@check_token_of_user
def get_users():
    userService = container[UserService]
    per_page = request.args.get('per_page', type=int)
    page = request.args.get('page', type=int)
    if not vaild_per_page(per_page) and isinstance(page, int):
        return response_error("Error on support per page or page number invalid", {'per_page': 'per_page', page: page}, 400)
    is_platform = False
    if request.args.get('filter_platform', type=int):
        is_platform = True

    is_inactive = False
    if request.args.get('filter_inactive', type=int):
        is_inactive = True

    show_store_users = False
    if request.args.get('filter_store_users', type=int) and request.args.get('filter_store_users', type=int) == 1:
        show_store_users = True

    filters = {
        'names': [],
        'emails': [],
        'stores': [],
        'countries': [],
        'store_users': show_store_users,
        'platform': is_platform,
    }

    if request.args.get('filter_stores') is not None and request.args.get('filter_stores') != 'None':
        filters['stores'] = request.args.get('filter_stores').split(',')

    if request.args.get('filter_emails') is not None and request.args.get('filter_emails') != 'None':
        filters['emails'] = request.args.get('filter_emails').split(',')

    if request.args.get('filter_countries') is not None and request.args.get('filter_countries') != 'None':
        filters['countries'] = request.args.get('filter_countries').split(',')

    if request.args.get('filter_names') is not None and request.args.get('filter_names') != 'None':
        filters['names'] = request.args.get('filter_names').split(',')
    order_by = []

    if request.args.get('order_by') is not None and request.args.get('order_by') != 'None' and request.args.get('order_by') != '':
        for order in request.args.get('order_by').split(','):
            temp = order.split('|')
            order_by.append({
                'field': temp[0],
                'sort': temp[1]
            })
    result = valid_user_list_params(filters, order_by)
    if not result and isinstance(result, (bool)):
        return response_error("Error on incorrect params", {'filters': filters, 'orders': order_by}, 400)
    filters = result['filters']
    orders = result['orders']

    result = valid_user_list_by_permissions(userService, request.uid, filters)
    if not result:
        return response_error("restricted access to some of the filter params", {'filters': filters, 'orders': orders}, 400)
    if not isinstance(result, (bool)):
        filters['platform'] = result['platform']
        filters['stores'] = result['stores']
        show_store_users = result['store_users']

    result = userService.get_users(filters, orders, int(per_page), int(page), is_inactive, show_store_users)
    schema = UserSchema()
    return response_success_paging(schema.dump(result.items, many=True), result.total, result.pages, result.has_next, result.has_prev)


@current_app.route(settings[os.environ.get("FLASK_ENV", "development")].API_ROUTE.format(route="/user/<uid>/toggle_active"), methods=["PUT"])
@check_role([RolesTypes.Accounts.value, RolesTypes.Owner.value])
def user_toggle_active(uid):
    userService = container[UserService]
    if verify_uid(userService, uid):
        try:
            userService.toggle_freeze_user(uid)
            return response_success({})
        except ValueError:
            current_app.logger.error("User not found", {uid: uid})
            return response_error("Error on format of the params", {uid: uid})
        except UserNotFoundError:
            return response_error("User not found", {uid: uid}, 404)
        except FirebaseError as err:
            current_app.logger.error("unknown error", err)
            return response_error("unknown error", {err: err.cause})
    return response_error("Error on format of the params", {uid: uid})


@current_app.route(settings[os.environ.get("FLASK_ENV", "development")].API_ROUTE.format(route="/user/platform/list/<per_page>/<page>"), methods=["GET"])
@check_role([RolesTypes.Accounts.value, RolesTypes.Owner.value, RolesTypes.Support.value])
def get_platform_users(per_page, page):
    userService = container[UserService]
    if not vaild_per_page(per_page):
        return response_error("Error on support per page", {per_page: per_page})
    filter = {'names': request.args.getlist('filter_fullname')}
    result = userService.query_platform_users(filter, per_page, page)
    return response_success_paging(result.items, result.total, result.pages, result.has_next, result.has_prev)


@current_app.route(settings[os.environ.get("FLASK_ENV", "development")].API_ROUTE.format(route="/user/store/<store_code>/list/<per_page>/<page>"),
                   methods=["GET"])
@check_role([RolesTypes.Support.value, RolesTypes.StoreAccount.value, RolesTypes.StoreOwner.value, RolesTypes.StoreSupport.value])
def get_store_users(store_code, per_page, page, userService: UserService, storeService: StoreService):
    if not vaild_per_page(per_page):
        return response_error("Error on support per page", {per_page: per_page})
    uid = request.uid
    if not storeService.store_exists(uid, store_code):
        response_error("store not exist", {uid: uid, store_code: store_code})
    filter = {'names': request.args.getlist('filter_fullname')}
    result = userService.query_store_users(store_code, filter, per_page, page)
    return response_success_paging(result.items, result.total, result.pages, result.has_next, result.has_prev)


@current_app.route(settings[os.environ.get("FLASK_ENV", "development")].API_ROUTE.format(route="/user/<uid>/passed_tutorial"), methods=["PUT"])
@check_token_of_user
def mark_user_passed_tutorial(uid):
    userService = container[UserService]
    if verify_uid(userService, uid):
        try:
            userService.mark_user_passed_tutorial(uid)
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


@current_app.route(settings[os.environ.get("FLASK_ENV", "development")].API_ROUTE.format(route="/user/update"), methods=["PUT"])
@check_token_of_user
def update_user_info():
    userService = container[UserService]
    if not request.is_json:
        return response_error("Request Data must be in json format", request.data)
    try:
        schema = UpdateUserInfo()
        data = schema.load(request.json)
    except ValidationError as e:
        return response_error("Error on format of the params", {'params': request.json})
    data = Struct(data)
    if not valid_currency_code(data.currency) or not valid_country_code(data.country):
        return response_error("Error on format of the params", {'params': request.json})
    uid = request.uid
    userService.update_user_info(uid, data)
    return response_success({})


@current_app.route(settings[os.environ.get("FLASK_ENV", "development")].API_ROUTE.format(route="/user/<uid>/update"), methods=["PUT"])
@check_role([RolesTypes.Support.value, RolesTypes.StoreSupport.value])
def update_user_info_by_support_user(uid):
    userService = container[UserService]
    if not request.is_json:
        return response_error("Request Data must be in json format", request.data)
    if verify_uid(userService, uid):
        if userService.user_has_role_matched(request.uid, [RolesTypes.StoreSupport.value]):
            user = userService.get_user(uid, True)
            requester_user = userService.get_user(request.uid, True)
            if user.store_code != requester_user.store_code:
                return response_error("Error support store user not matched with user (not in same store)", {'params': request.json})

        try:
            schema = UpdateUserInfo()
            data = schema.load(request.json)
        except ValidationError as e:
            return response_error("Error on format of the params", {'params': request.json})
        data = Struct(data)
        if not valid_currency_code(data.currency) or not valid_country_code(data.country):
            return response_error("Error on format of the params", {'params': request.json})
        userService.update_user_info(uid, data)
        return response_success({})
    return response_error("Error on format of the params", {'uid': uid})


@current_app.route(settings[os.environ.get("FLASK_ENV", "development")].API_ROUTE.format(route="/user/staff/<store_code>"), methods=["POST"])
@check_role([RolesTypes.Support.value, RolesTypes.StoreSupport.value, RolesTypes.StoreOwner.value])
def create_store_stuff(store_code):
    userService = container[UserService]
    roleSerivce = container[RoleService]
    fileSystemService = container[FileSystemService]
    if not request.is_json:
        return response_error("Request Data must be in json format", request.data)
    try:
        schema = CreateStoreStaffUser()
        data = schema.load(request.json)
    except ValidationError as e:
        return response_error("Error on format of the params", {'params': request.json})

    if userService.user_has_any_role_matched(request.uid, [RolesTypes.StoreSupport.value, RolesTypes.StoreOwner.value]):
        requester_user = userService.get_user(request.uid, True)
        if store_code != requester_user.store_code:
            return response_error("Error support store user not matched with user (not in same store)", {'params': request.json})
    data = Struct(data)
    if not roleSerivce.check_roles(data.roles):
        return response_error("One or more of fields are invalid", {'params': request.json})

    try:
        roles = roleSerivce.get_roles(data.roles)
        return response_success(userService.create_user(data.email, data.fullname, data.password, roles, store_code))
    except ValueError:
        return response_error("Error on format of the params", request.data)
    except UserNotFoundError:
        current_app.logger.error("User not found", request.data)
        return response_error("User not found", request.data)
    except FirebaseError as err:
        current_app.logger.error("unknown error", err)
        return response_error("unknown error", {err: err.cause})


@current_app.route(settings[os.environ.get("FLASK_ENV", "development")].API_ROUTE.format(route="/user/<uid>"), methods=["POST"])
@check_role([RolesTypes.Accounts.value, RolesTypes.Owner.value])
def sync_platform_user_create(uid):
    userService = container[UserService]
    roleSerivce = container[RoleService]
    if not request.is_json:
        return response_error("Request Data must be in json format", request.data)
    if verify_uid(userService, uid):
        try:
            body = request.json()
            bodyObj = {"role_names": ', '.join(body['role_names'])}
            try:
                schema = UserRolesList()
                data = schema.load(bodyObj)
            except ValidationError as e:
                return response_error("Error on format of the params", {'params': request.json})
            if roleSerivce.check_roles(data.role_names):
                return response_error("One or more of fields are invalid", request.data)
            return response_success(sync_user_from_firebase_user(uid, data.role_names, True, False))
        except ValueError:
            return response_error("Error on format of the params", {uid: uid})
        except UserNotFoundError:
            current_app.logger.error("User not found", {uid: uid})
            return response_error("User not found", {uid: uid})
        except FirebaseError as err:
            current_app.logger.error("unknown error", err)
            return response_error("unknown error", {err: err.cause})
    return response_error("Error on format of the params", {uid: uid})


@current_app.route(settings[os.environ.get("FLASK_ENV", "development")].API_ROUTE.format(route="/user/<uid>/bind/<store_code>"), methods=["POST"])
@check_token_register_firebase_user
def sync_store_user_create(uid, store_code):
    userService = container[UserService]
    storeService = container[StoreService]
    if not verify_uid(userService, uid):
        try:
            has_store = storeService.store_exists(uid, store_code)
            if has_store is None:
                response_error("error store not existed", {uid: uid, store_code: store_code})
            return response_success(
                sync_user_from_firebase_user(uid, [RolesTypes.StoreCustomer.value], False, store_code))
        except ValueError:
            return response_error("Error on format of the params", {uid: uid})
        except UserNotFoundError:
            current_app.logger.error("User not found", {uid: uid})
            return response_error("User not found", {uid: uid})
        except FirebaseError as err:
            current_app.logger.error("unknown error", err)
            return response_error("unknown error", {err: err.cause})
    return response_error("Error user exist", {uid: uid})


def sync_user_from_firebase_user(uid, role_names, is_platform_user, store_code=None, new_user=True):
    userService = container[UserService]
    roleSerivce = container[RoleService]
    user_object = userService.get_firebase_user(uid).__dict__['_data']
    response = {'user': json.dumps(user_object, indent=4), 'extend_info': None}
    roles = roleSerivce.get_roles(role_names)
    email = user_object['email']
    fullname = user_object['displayName']
    userService.sync_firebase_user(uid, roles, email, fullname, is_platform_user, store_code, new_user)
    response['extend_info'] = userService.get_user(uid)
    return response
