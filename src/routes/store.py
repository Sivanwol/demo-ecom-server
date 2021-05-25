import os

import pycountry
from config import settings
from config.api import app as current_app
from src.middlewares.check_role import check_role
from src.middlewares.check_token import check_token
from src.services.store import StoreService
from src.services.user import UserService
from src.utils.common_methods import verify_uid
from src.utils.enums import RolesTypes
from src.utils.responses import response_success, response_error

storeService = StoreService()
userService = UserService()


# Todo: add logic to get store info
@current_app.route(settings[os.environ.get("FLASK_ENV", "development")].API_ROUTE.format(route="/store/<uid>/<store_code>/info"))
@check_token
def get_store_info(uid, store_code):
    if verify_uid(uid):
        store = storeService.get_store(uid, store_code)
        if store is None:
            response_error("error store not existed", {uid: uid, store_code: store_code})

        return response_success(storeService.get_store(uid, store_code))
    return response_error("Error on format of the params", {uid: uid})


# Todo: add logic to update store info
@current_app.route(settings[os.environ.get("FLASK_ENV", "development")].API_ROUTE.format(route="/store/list"))
@check_role([RolesTypes.Support, RolesTypes.Owner, RolesTypes.Accounts, RolesTypes.Reports])
def list_stores():
    return response_success(storeService.get_stores())


# Todo: add logic to update store info
@current_app.route(settings[os.environ.get("FLASK_ENV", "development")].API_ROUTE.format(route="/store/<uid>/<store_code>/update"), methods=["PUT"])
@check_role([RolesTypes.Support, RolesTypes.StoreOwner, RolesTypes.StoreAccount])
def update_store_info(uid, store_code):
    currencies = {}
    for currency in list(pycountry.currencies):
        obj = {"{}".format(currency.alpha_3): currency.__dict__['_fields']}
        currencies.update(obj)
    return response_success(currencies)


# Todo: add logic to update store supported currencies
@current_app.route(settings[os.environ.get("FLASK_ENV", "development")].API_ROUTE.format(route="/store/<uid>/<store_code>/currencies"), methods=["PUT"])
@check_role([RolesTypes.Support, RolesTypes.StoreOwner, RolesTypes.StoreAccount])
def update_store_support_currencies(uid, store_code):
    currencies = {}
    for currency in list(pycountry.currencies):
        obj = {"{}".format(currency.alpha_3): currency.__dict__['_fields']}
        currencies.update(obj)
    return response_success(currencies)


# Todo: add logic to create store location
@current_app.route(settings[os.environ.get("FLASK_ENV", "development")].API_ROUTE.format(route="/store/<uid>/<store_code>/location"), methods=["POST"])
@check_role([RolesTypes.Support, RolesTypes.StoreOwner, RolesTypes.StoreAccount])
def add_store_location(uid, store_code):
    currencies = {}
    for currency in list(pycountry.currencies):
        obj = {"{}".format(currency.alpha_3): currency.__dict__['_fields']}
        currencies.update(obj)
    return response_success(currencies)


# Todo: add logic to delete store location
@current_app.route(settings[os.environ.get("FLASK_ENV", "development")].API_ROUTE.format(route="/store/<uid>/<store_code>/location/<location_id>"),
                   methods=["DELETE"])
@check_role([RolesTypes.Support, RolesTypes.StoreOwner, RolesTypes.StoreAccount])
def delete_store_location(uid, store_code, location_id):
    currencies = {}
    for currency in list(pycountry.currencies):
        obj = {"{}".format(currency.alpha_3): currency.__dict__['_fields']}
        currencies.update(obj)
    return response_success(currencies)


# Todo: add logic to create opening hours
@current_app.route(settings[os.environ.get("FLASK_ENV", "development")].API_ROUTE.format(route="/store/<uid>/<store_code>/hours/<location_id>"),
                   methods=["POST"])
@check_role([RolesTypes.Support, RolesTypes.StoreOwner, RolesTypes.StoreAccount])
def add_store_hours(uid, store_code, location_id):
    currencies = {}
    for currency in list(pycountry.currencies):
        obj = {"{}".format(currency.alpha_3): currency.__dict__['_fields']}
        currencies.update(obj)
    return response_success(currencies)


# Todo: add logic to delete opening hours
@current_app.route(settings[os.environ.get("FLASK_ENV", "development")].API_ROUTE.format(route="/store/<uid>/<store_code>/hours/<location_id>"),
                   methods=["DELETE"])
@check_role([RolesTypes.Support, RolesTypes.StoreOwner, RolesTypes.StoreAccount])
def delete_store_hours(uid, store_code, location_id):
    currencies = {}
    for currency in list(pycountry.currencies):
        obj = {"{}".format(currency.alpha_3): currency.__dict__['_fields']}
        currencies.update(obj)
    return response_success(currencies)
