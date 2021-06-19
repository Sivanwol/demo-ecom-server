import os

import pycountry
from config import settings
from config.api import app as current_app
from src.middlewares.check_token import check_token_of_user
from src.utils.responses import response_success


# Todo: upload media files that include the file meta data and every thing else
@current_app.route(settings[os.environ.get("FLASK_ENV", "development")].API_ROUTE.format(route="/media/uploads"), methods=["POST"])
@check_token_of_user
def upload_media():
    countries = {}
    for country in list(pycountry.countries):
        obj = {"{}".format(country.alpha_3): country.__dict__['_fields']}
        countries.update(obj)
    return response_success(countries)


# Todo: create folder
@current_app.route(settings[os.environ.get("FLASK_ENV", "development")].API_ROUTE.format(route="/media/<uid>/folder/create"), methods=["POST"])
@check_token_of_user
def create_virtual_directory():
    pass


# Todo: delete folder (will be do any child entity will be mark for deletion (once it set use have N hours to prevent if not will delete if prevent will
#  remove the mark )
@current_app.route(settings[os.environ.get("FLASK_ENV", "development")].API_ROUTE.format(route="/media/<uid>/folder/delete"), methods=["DELETE"])
@check_token_of_user
def delete_virtual_directory():
    pass


# Todo: delete folder (will be do any child entity will be mark for deletion (once it set use have N hours to prevent if not will delete if prevent will
#  remove the mark )
@current_app.route(settings[os.environ.get("FLASK_ENV", "development")].API_ROUTE.format(route="/media/<uid>/<file_io>"), methods=["DELETE"])
@check_token_of_user
def delete_files():
    pass


# Todo: move folder to dest folder
@current_app.route(settings[os.environ.get("FLASK_ENV", "development")].API_ROUTE.format(route="/media/<uid>/folder/move"), methods=["PUT"])
@check_token_of_user
def move_virtual_directory():
    pass


# Todo: get users files
@current_app.route(settings[os.environ.get("FLASK_ENV", "development")].API_ROUTE.format(route="/media/<uid>/files"), methods=["GET"])
@check_token_of_user
def get_user_files():
    pass


# Todo: get users files on a folder
@current_app.route(settings[os.environ.get("FLASK_ENV", "development")].API_ROUTE.format(route="/media/<uid>/files/<folder_id>"), methods=["GET"])
@check_token_of_user
def get_user_files_from_folder():
    pass


# Todo: will download a folder (will zip and send to client) or just send the file depend what the entity_id
@current_app.route(settings[os.environ.get("FLASK_ENV", "development")].API_ROUTE.format(route="/media/<uid>/download/<entity_id>"), methods=["GET"])
@check_token_of_user
def download_files():
    pass
