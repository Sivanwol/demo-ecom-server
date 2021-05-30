import os

from flask import request
from marshmallow import ValidationError

from config import settings
from config.api import app as current_app
from src.middlewares.check_role import check_role
from src.schemas.requests.store import RequestStoreCreate, RequestStoreUpdate, RequestStoreLocationSchema, RequestStoreHoursUpdate, RequestStoreHourSchema
from src.services.store import StoreService
from src.services.user import UserService
from src.utils.common_methods import verify_uid
from src.utils.enums import RolesTypes
from src.utils.general import Struct
from src.utils.responses import response_success, response_error
from src.utils.validations import valid_currency

storeService = StoreService()
userService = UserService()


@current_app.route(settings[os.environ.get("FLASK_ENV", "development")].API_ROUTE.format(route="/store/<store_code>/info"))
def get_store_info(store_code):
    store = storeService.get_store_by_status_code(store_code)
    if store is None:
        response_error("error store not existed", {store_code: store_code})

    return response_success(store)


@current_app.route(settings[os.environ.get("FLASK_ENV", "development")].API_ROUTE.format(route="/store/list"))
@check_role([RolesTypes.Support.value, RolesTypes.Owner.value, RolesTypes.Accounts.value, RolesTypes.Reports.value])
def list_stores():
    stores = storeService.get_stores()
    return response_success(stores.data)


@current_app.route(settings[os.environ.get("FLASK_ENV", "development")].API_ROUTE.format(route="/store/<uid>/create"), methods=["POST"])
@check_role([RolesTypes.Accounts.value, RolesTypes.Owner.value])
def create_store(uid):
    if not request.is_json:
        return response_error("Request Data must be in json format", request.data)
    if verify_uid(uid):
        try:
            schema = RequestStoreCreate()
            data = schema.load(request.json)
        except ValidationError as e:
            return response_error("Error on format of the params", {'params': request.json, 'errors': e.messages})

        store = storeService.create_store(uid, data.data)
        userService.update_user_store_owner(uid, store['info']['store_code'])
        return response_success(store)
    return response_error("Error on format of the params", {'uid': uid})


@current_app.route(settings[os.environ.get("FLASK_ENV", "development")].API_ROUTE.format(route="/store/<uid>/<store_code>"), methods=["DELETE"])
@check_role([RolesTypes.Accounts.value, RolesTypes.Owner.value])
def delete_store(uid, store_code):
    if verify_uid(uid):
        if not storeService.store_exists(uid, store_code):
            response_error("store not exist", {uid: uid, store_code: store_code})

        storeService.freeze_store(uid, store_code)
        userService.toggle_freeze_user(uid)
        return response_success({})
    return response_error("Error on format of the params", {uid: uid})


@current_app.route(settings[os.environ.get("FLASK_ENV", "development")].API_ROUTE.format(route="/store/<uid>/<store_code>/toggle/maintenance"), methods=["PUT"])
@check_role([RolesTypes.Accounts.value, RolesTypes.Owner.value])
def toggle_store_maintenance(uid, store_code):
    if verify_uid(uid):
        if not storeService.store_exists(uid, store_code):
            response_error("store not exist", {uid: uid, store_code: store_code})

        storeService.toggle_maintenance_store(uid, store_code)
        stores = storeService.get_stores()
        return response_success(stores.data)
    return response_error("Error on format of the params", {uid: uid})


@current_app.route(settings[os.environ.get("FLASK_ENV", "development")].API_ROUTE.format(route="/store/<uid>/<store_code>/update"), methods=["PUT"])
@check_role([RolesTypes.Support.value, RolesTypes.StoreOwner.value, RolesTypes.StoreAccount.value])
def update_store_support(uid, store_code):
    if not request.is_json:
        return response_error("Request Data must be in json format", request.data)
    if verify_uid(uid):
        has_store = storeService.store_exists(uid, store_code)
        if has_store is None:
            response_error("error store not existed", {uid: uid, store_code: store_code})
        try:
            schema = RequestStoreUpdate()
            data = schema.load(request.json)
        except ValidationError as e:
            return response_error("Error on format of the params", {'params': request.json})
        if not valid_currency(data.data['currency_code']):
            return response_error("Error on format of the params", {'params': request.json})
        data = Struct(data.data)
        store = storeService.update_store_info(uid, store_code, data)
        return response_success(store)
    return response_error("Error on format of the params", {uid: uid})


@current_app.route(settings[os.environ.get("FLASK_ENV", "development")].API_ROUTE.format(route="/store/<uid>/<store_code>/locations"), methods=["POST"])
@check_role([RolesTypes.Support.value, RolesTypes.StoreOwner.value, RolesTypes.StoreAccount.value])
def update_store_location(uid, store_code):
    if not request.is_json:
        return response_error("Request Data must be in json format", request.data)
    if verify_uid(uid):
        has_store = storeService.store_exists(uid, store_code)
        if has_store is None:
            response_error("error store not existed", {uid: uid, store_code: store_code})
        try:
            schema = RequestStoreLocationSchema()
            data = schema.load(request.json, many=True)
        except ValidationError as e:
            return response_error("Error on format of the params", {'params': request.json})
        data = Struct({'locations': data.data})
        store = storeService.update_locations(uid, store_code, data)
        return response_success(store)
    return response_error("Error on format of the params", {uid: uid})


@current_app.route(settings[os.environ.get("FLASK_ENV", "development")].API_ROUTE.format(route="/store/<uid>/<store_code>/hours"), methods=["POST"])
@check_role([RolesTypes.Support.value, RolesTypes.StoreOwner.value, RolesTypes.StoreAccount.value])
def update_store_hours(uid, store_code):
    if not request.is_json:
        return response_error("Request Data must be in json format", request.data)
    if verify_uid(uid):
        has_store = storeService.store_exists(uid, store_code)
        if has_store is None:
            response_error("error store not existed", {uid: uid, store_code: store_code})
        try:
            schema = RequestStoreHourSchema()
            data = schema.load(request.json, many=True)
        except ValidationError as e:
            return response_error("Error on format of the params", {'params': request.json})
        data = Struct({'hours': data.data})
        store = storeService.update_hours(uid, store_code, data)
        return response_success(store)
    return response_error("Error on format of the params", {uid: uid})

