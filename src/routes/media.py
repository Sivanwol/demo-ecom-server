import os

import pycountry
from flask import request
from marshmallow import ValidationError

from config import settings
from config.containers import app as current_app, container
from src.exceptions import UnableCreateFolder
from src.middlewares import check_token_of_user
from src.schemas.requests import RequestMediaCreateFolderSchema
from src.services import MediaService, UserService, RoleService
from src.utils.enums import RolesTypes
from src.utils.responses import response_success, response_error


# Todo: upload media files that include the file meta data and every thing else
@current_app.route(settings[os.environ.get("FLASK_ENV", "development")].API_ROUTE.format(route="/media/uploads"), methods=["POST"])
@check_token_of_user
def upload_media():
    files = request.files.getlist("files")
    for file in files:
        pass
    return response_success([])


@current_app.route(settings[os.environ.get("FLASK_ENV", "development")].API_ROUTE.format(route="/media/folder/create"), methods=["POST"])
@check_token_of_user
def create_virtual_directory():
    mediaService = container[MediaService]
    userService = container[UserService]
    roleService = container[RoleService]
    if not request.is_json:
        return response_error("Request Data must be in json format", request.data)
    try:
        schema = RequestMediaCreateFolderSchema()
        data = schema.load(request.json)

        if data['type'] != settings[os.environ.get("FLASK_ENV", "development")].UPLOAD_SYSTEM_FOLDER:
            supportRole = roleService.get_roles([RolesTypes.Support.value, RolesTypes.Owner.value, RolesTypes.Accounts.value])
            if userService.user_has_any_role_matched(request.uid, supportRole):
                result = mediaService.create_virtual_folder(data)
                return response_success(result)
        if data['type'] != settings[os.environ.get("FLASK_ENV", "development")].UPLOAD_STORES_FOLDER_FOLDER:
            supportRole = roleService.get_roles([RolesTypes.Support.value])
            user = userService.get_user(request.uid, True)
            if userService.user_has_any_role_matched(request.uid, supportRole) or \
                (user.store_code == data['entity_id'] and type == settings[os.environ.get("FLASK_ENV", "development")].UPLOAD_STORES_FOLDER):
                result = mediaService.create_virtual_folder(data)
                return response_success(result)
        if data['type'] != settings[os.environ.get("FLASK_ENV", "development")].UPLOAD_USERS_FOLDER or request.uid == data['entity_id']:
            supportRole = roleService.get_roles([RolesTypes.Support.value])
            if userService.user_has_any_role_matched(request.uid, supportRole):
                result = mediaService.create_virtual_folder(data)
                return response_success(result)
        return response_error("No Permission Create folder", {'params': request.json})
    except ValidationError as e:
        return response_error("Error on format of the params", {'params': request.json, 'error': e.messages})
    except UnableCreateFolder as e:
        current_app.logger.error("User failed create folder", {'params': request.json, 'e': e.message})
        return response_error("Error on create folder it may try create folder under same name or internal issue", {'params': request.json})


@current_app.route(settings[os.environ.get("FLASK_ENV", "development")].API_ROUTE.format(route="/media/<entity_id>/folder/<folder_code>/delete"),
                   methods=["DELETE"])
@check_token_of_user
def delete_virtual_directory(entity_id, folder_code):
    mediaService = container[MediaService]
    userService = container[UserService]
    roleService = container[RoleService]

    def handle(type):
        media = mediaService.get_virtual_folder(folder_code, entity_id, True)
        if media is None:
            return response_error("folder not found", {'params': {entity_id, folder_code}})
        result = mediaService.delele_virtual_folder(media.code, type,entity_id)
        response_success({"delete_status": result})

    user = userService.get_user(request.uid, True)
    if entity_id == user.uid:
        return handle(settings[os.environ.get("FLASK_ENV", "development")].UPLOAD_USERS_FOLDER)
    else:
        if entity_id == 'none':
            entity_id = None
        supportRole = roleService.get_roles([RolesTypes.Support.value])
        if userService.user_has_any_role_matched(request.uid, supportRole) or user.store_code == entity_id:
            type = settings[os.environ.get("FLASK_ENV", "development")].UPLOAD_SYSTEM_FOLDER
            if entity_id is not None:
                type = settings[os.environ.get("FLASK_ENV", "development")].UPLOAD_STORES_FOLDER
            return handle(type)
    return response_error("No Permission access folder", {'params': {entity_id, folder_code}})

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
