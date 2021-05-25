import os

import pycountry
from config import settings
from config.api import app as current_app
from src.middlewares.check_role import check_role
from src.utils.responses import response_success


@current_app.route(settings[os.environ.get("FLASK_ENV", "development")].API_ROUTE.format(route="/store/uid/info"))
@check_role(["customer", "account", "owner"])
def get_store_info():
    countries = {}
    for country in list(pycountry.countries):
        obj = {"{}".format(country.alpha_3): country.__dict__['_fields']}
        countries.update(obj)
    return response_success(countries)


@current_app.route(settings[os.environ.get("FLASK_ENV", "development")].API_ROUTE.format(route="/store/uid/update"), methods=["PUT"])
@check_role(["account", "owner"])
def update_store_info():
    currencies = {}
    for currency in list(pycountry.currencies):
        obj = {"{}".format(currency.alpha_3): currency.__dict__['_fields']}
        currencies.update(obj)
    return response_success(currencies)


@current_app.route(settings[os.environ.get("FLASK_ENV", "development")].API_ROUTE.format(route="/store/uid/currencies"), methods=["PUT"])
@check_role(["account", "owner"])
def update_store_support_currencies():
    currencies = {}
    for currency in list(pycountry.currencies):
        obj = {"{}".format(currency.alpha_3): currency.__dict__['_fields']}
        currencies.update(obj)
    return response_success(currencies)


@current_app.route(settings[os.environ.get("FLASK_ENV", "development")].API_ROUTE.format(route="/store/uid/location"), methods=["POST"])
@check_role(["account", "owner"])
def add_store_location():
    currencies = {}
    for currency in list(pycountry.currencies):
        obj = {"{}".format(currency.alpha_3): currency.__dict__['_fields']}
        currencies.update(obj)
    return response_success(currencies)


@current_app.route(settings[os.environ.get("FLASK_ENV", "development")].API_ROUTE.format(route="/store/uid/location"), methods=["DELETE"])
@check_role(["account", "owner"])
def delete_store_location():
    currencies = {}
    for currency in list(pycountry.currencies):
        obj = {"{}".format(currency.alpha_3): currency.__dict__['_fields']}
        currencies.update(obj)
    return response_success(currencies)
