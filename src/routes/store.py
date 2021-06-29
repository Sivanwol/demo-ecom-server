from flask import request
from lagom import injectable
from marshmallow import ValidationError

from config.app import app as current_app, containers
from src.middlewares import check_role
from src.schemas.requests import RequestStoreCreate, RequestStoreUpdate, RequestStoreLocationSchema, RequestStoreHourSchema
from src.services import FileSystemService, StoreService, UserService
from src.utils.common_methods import verify_uid
from src.utils.enums import RolesTypes
from src.utils.general import Struct
from src.utils.responses import response_success, response_error
from src.utils.validations import valid_currency_code


@current_app.route(current_app.flask_app.config['API_ROUTE'].format(route="/store/<store_code>/info"))
def get_store_info(store_code, storeService: StoreService = injectable):
    storeService = containers[StoreService]
    store = storeService.get_store_by_status_code(store_code)
    if store is None:
        response_error("error store not existed", {store_code: store_code})

    return response_success(store)


@current_app.route(current_app.flask_app.config['API_ROUTE'].format(route="/store/list"))
@check_role([RolesTypes.Support.value, RolesTypes.Owner.value, RolesTypes.Accounts.value, RolesTypes.Reports.value])
def list_stores(uid, storeService: StoreService = injectable):
    stores = storeService.get_stores()
    return response_success(stores)


@current_app.route(current_app.flask_app.config['API_ROUTE'].format(route="/store/<request_uid>/create"), methods=["POST"])
@check_role([RolesTypes.Accounts.value, RolesTypes.Owner.value])
def create_store(uid, request_uid,
                 storeService: StoreService = injectable,
                 userService: UserService = injectable):
    if not request.is_json:
        return response_error("Request Data must be in json format", request.data)
    if verify_uid(userService, request_uid):
        try:
            schema = RequestStoreCreate()
            data = schema.load(request.json)
        except ValidationError as e:
            return response_error("Error on format of the params", {'params': request.json, 'errors': e.messages})

        store = storeService.create_store(request_uid, data)
        userService.update_user_store_owner(request_uid, store['info']['store_code'])
        return response_success(store)
    return response_error("Error on format of the params", {'uid': request_uid})


@current_app.route(current_app.flask_app.config['API_ROUTE'].format(route="/store/<request_uid>/<store_code>"), methods=["DELETE"])
@check_role([RolesTypes.Accounts.value, RolesTypes.Owner.value])
def delete_store(uid, request_uid, store_code,
                 storeService: StoreService = injectable,
                 userService: UserService = injectable):
    if verify_uid(userService, request_uid):
        if not storeService.store_exists(request_uid, store_code):
            response_error("store not exist", {'request_uid': request_uid, 'store_code': store_code})

        storeService.freeze_store(request_uid, store_code)
        userService.toggle_freeze_user(request_uid)
        return response_success({})
    return response_error("Error on format of the params", {'request_uid': request_uid})


@current_app.route(current_app.flask_app.config['API_ROUTE'].format(route="/store/<request_uid>/<store_code>/toggle/maintenance"),
                   methods=["PUT"])
@check_role([RolesTypes.Accounts.value, RolesTypes.Owner.value])
def toggle_store_maintenance(uid, request_uid, store_code,
                             storeService: StoreService = injectable,
                             userService: UserService = injectable):
    if verify_uid(userService, request_uid):
        if not storeService.store_exists(request_uid, store_code):
            response_error("store not exist", {'request_uid': request_uid, 'store_code': store_code})

        storeService.toggle_maintenance_store(request_uid, store_code)
        stores = storeService.get_stores()
        return response_success(stores)
    return response_error("Error on format of the params", {'request_uid': request_uid})


@current_app.route(current_app.flask_app.config['API_ROUTE'].format(route="/store/<request_uid>/<store_code>/update"), methods=["PUT"])
@check_role([RolesTypes.Support.value, RolesTypes.StoreOwner.value, RolesTypes.StoreAccount.value])
def update_store_support(uid, request_uid, store_code,
                         storeService: StoreService = injectable,
                         userService: UserService = injectable):
    if not request.is_json:
        return response_error("Request Data must be in json format", request.data)
    if verify_uid(userService, request_uid):
        has_store = storeService.store_exists(request_uid, store_code)
        if has_store is None:
            response_error("error store not existed", {'request_uid': request_uid, 'store_code': store_code})
        try:
            schema = RequestStoreUpdate()
            data = schema.load(request.json)
        except ValidationError as e:
            return response_error("Error on format of the params", {'params': request.json})
        if not valid_currency_code(data['currency_code']):
            return response_error("Error on format of the params", {'params': request.json})
        data = Struct(data)
        store = storeService.update_store_info(request_uid, store_code, data)
        return response_success(store)
    return response_error("Error on format of the params", {'request_uid': uid})


@current_app.route(current_app.flask_app.config['API_ROUTE'].format(route="/store/<request_uid>/<store_code>/locations"), methods=["POST"])
@check_role([RolesTypes.Support.value, RolesTypes.StoreOwner.value, RolesTypes.StoreAccount.value])
def update_store_location(uid, request_uid, store_code,
                          storeService: StoreService = injectable,
                          userService: UserService = injectable):
    if not request.is_json:
        return response_error("Request Data must be in json format", request.data)
    if verify_uid(userService, request_uid):
        has_store = storeService.store_exists(request_uid, store_code)
        if has_store is None:
            response_error("error store not existed", {'request_uid': uid, 'store_code': store_code})
        try:
            schema = RequestStoreLocationSchema()
            data = schema.load(request.json, many=True)
        except ValidationError as e:
            return response_error("Error on format of the params", {'params': request.json})
        data = Struct({'locations': data})
        store = storeService.update_locations(request_uid, store_code, data)
        return response_success(store)
    return response_error("Error on format of the params", {'request_uid': request_uid})


@current_app.route(current_app.flask_app.config['API_ROUTE'].format(route="/store/<request_uid>/<store_code>/hours"), methods=["POST"])
@check_role([RolesTypes.Support.value, RolesTypes.StoreOwner.value, RolesTypes.StoreAccount.value])
def update_store_hours(uid, request_uid, store_code,
                       storeService: StoreService = injectable,
                       userService: UserService = injectable):
    if not request.is_json:
        return response_error("Request Data must be in json format", request.data)
    if verify_uid(userService, request_uid):
        has_store = storeService.store_exists(request_uid, store_code)
        if has_store is None:
            response_error("error store not existed", {'request_uid': uid, 'store_code': store_code})
        try:
            schema = RequestStoreHourSchema()
            data = schema.load(request.json, many=True)
        except ValidationError as e:
            return response_error("Error on format of the params", {'params': request.json})
        data = Struct({'hours': data})
        store = storeService.update_hours(request_uid, store_code, data)
        return response_success(store)
    return response_error("Error on format of the params", {'request_uid': request_uid})
