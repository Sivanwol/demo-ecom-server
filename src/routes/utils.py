import pycountry
from config.app import app as current_app
from src.utils.responses import response_success


@current_app.route(current_app.flask_app.config['API_ROUTE'].format(route="/utils/countries"))
def get_countries():
    countries = {}
    for country in list(pycountry.countries):
        obj = {"{}".format(country.alpha_3): country.__dict__['_fields']}
        countries.update(obj)
    return response_success(countries)


@current_app.route(current_app.flask_app.config['API_ROUTE'].format(route="/utils/currencies"))
def get_currencies():
    currencies = {}
    for currency in list(pycountry.currencies):
        obj = {"{}".format(currency.alpha_3): currency.__dict__['_fields']}
        currencies.update(obj)
    return response_success(currencies)
