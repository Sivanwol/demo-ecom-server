import os

import pycountry
from config import settings
from config.api import app as current_app
from src.middlewares.check_token import check_token_of_user
from src.utils.responses import response_success


# Todo: add logic to uploads media
@current_app.route(settings[os.environ.get("FLASK_ENV", "development")].API_ROUTE.format(route="/media/uploads"), methods=["POST"])
@check_token_of_user
def upload_media():
    countries = {}
    for country in list(pycountry.countries):
        obj = {"{}".format(country.alpha_3): country.__dict__['_fields']}
        countries.update(obj)
    return response_success(countries)

