import os

import pycountry
from flask import request
from marshmallow import ValidationError

from config import settings
from config.containers import app as current_app, container
from src.exceptions import UnableCreateFolder
from src.middlewares import check_token_of_user
from src.schemas.requests import RequestMediaCreateFolderSchema
from src.services import MediaService
from src.utils.responses import response_success, response_error


# Todo: upload media files that include the file meta data and every thing else
@current_app.route(settings[os.environ.get("FLASK_ENV", "development")].API_ROUTE.format(route="/media/uploads"), methods=["POST"])
@check_token_of_user
def upload_media():
    files = request.files.getlist("files")
    for file in files:
        pass
    return response_success([])


# Todo: create folder
@current_app.route(settings[os.environ.get("FLASK_ENV", "development")].API_ROUTE.format(route="/media/folder/create"), methods=["POST"])
@check_token_of_user
def create_virtual_directory():
    mediaService = container[MediaService]
    if not request.is_json:
        return response_error("Request Data must be in json format", request.data)
    try:
        schema = RequestMediaCreateFolderSchema()
        data = schema.load(request.json)
        result = mediaService.create_virtual_folder(data, False)
        return response_success(result)
    except ValidationError as e:
        return response_error("Error on format of the params", {'params': request.json})
    except UnableCreateFolder as e:
        current_app.logger.error("User failed create folder", {'params': request.json, 'e': e.message})
        return response_error("Error on create folder it may try create folder under same name or internal issue", {'params': request.json})


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
