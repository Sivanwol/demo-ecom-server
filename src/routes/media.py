import os

import pycountry
from flask import request

from config import settings
from config.containers import app as current_app
from src.middlewares.check_token import check_token_of_user
from src.services.filesystem import FileSystemService
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
@current_app.route(settings[os.environ.get("FLASK_ENV", "development")].API_ROUTE.format(route="/media/<entity_id>/<type>/folder/create"), methods=["POST"])
@check_token_of_user
def create_virtual_directory(entity_id, type, fileSystemService: FileSystemService):
    path = fileSystemService.getFolderPath(entity_id, type)
    if path is None:
        return response_error("Error on format of the params", {type, entity_id})
    # uploaded_files = request.files.getlist('files')
    parent_folder = request.json['parent_folder']
    create_folder = request.json['folder']
    if parent_folder is None:
        path = fileSystemService.getFolderPath(entity_id, type, create_folder)
    else:
        path = fileSystemService.getFolderPath(entity_id, type, os.path.join(parent_folder, create_folder))
    fileSystemService.create_folder(path)


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
