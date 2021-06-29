import os

from flask import request, make_response
from marshmallow import ValidationError
from lagom import injectable
from config.app import app as current_app, containers
from src.exceptions import UnableCreateFolder
from src.middlewares import check_token_of_user
from src.schemas import MediaFileSchema
from src.schemas.requests import RequestMediaCreateFolderSchema, RequestMediaCreateFile
from src.services import MediaService, UserService, RoleService, FileSystemService, StoreService
from src.utils.enums import RolesTypes
from src.utils.responses import response_success, response_error


@current_app.route(current_app.flask_app.config['API_ROUTE'].format(route="/media/<entity_code>/uploads"), methods=["POST"])
@check_token_of_user
def upload_media(uid,
                 entity_code,
                 fileSystemService: FileSystemService = injectable,
                 mediaService: MediaService = injectable,
                 userService: UserService = injectable,
                 roleService: RoleService = injectable):
    try:
        schema = RequestMediaCreateFile()
        data = schema.load(request.form)
        if not mediaService.virtual_folder_exists(data['folder_code'], None if entity_code.lower() == 'none' else entity_code):
            return response_error("Folder not existed", {'params': request.json})

        is_system_file = False
        is_store_file = False
        is_user_file = False
        if data['is_system_file'] and not data['is_store_file']:
            is_system_file = True

        if not data['is_system_file'] and data['is_store_file']:
            is_store_file = True

        if not is_system_file and not is_store_file:
            is_user_file = True
        if is_system_file:
            roles = [RolesTypes.Support.value, RolesTypes.Owner.value, RolesTypes.Accounts.value]
            if not userService.user_has_any_role_matched(uid, roles):
                return response_error("Permission Error", None, 403)
        if is_store_file:
            roles = [RolesTypes.Support.value]
            user = userService.get_user(request.uid, True)
            if not userService.user_has_any_role_matched(uid, roles) or user.store_code != data['entity_id']:
                return response_error("Permission Error", None, 403)
        if is_user_file:
            supportRole = roleService.get_roles([RolesTypes.Support.value])
            if userService.user_has_any_role_matched(uid, supportRole) or uid != data['entity_id']:
                return response_error("Permission Error", None, 403)
        if not mediaService.virtual_folder_exists(data['folder_code'], data['folder_code'] if data['folder_code'] != 'None' else None):
            return response_error("Upload location not existed")
    except ValidationError as e:
        return response_error("Error on format of the params", {'params': request.json, 'error': e.messages})
    files = request.files.getlist("files")
    if len(files) == 0:
        return response_error("no upload files found")
    files = fileSystemService.save_temporary_upload_files(files)
    if len(files) == 0:
        return response_error("Files that uploaded no meet with server limitations")
    data['entity_code'] = entity_code
    files = mediaService.register_uploaded_files(uid, files, data, is_system_file, is_store_file, is_user_file)
    # any task need do after need assign here to the task que
    mediaService.post_process_files_uploads(files)
    # end assign code
    schema = MediaFileSchema()
    response = schema.dump(files, many=True)
    return response_success(response)


@current_app.route(current_app.flask_app.config['API_ROUTE'].format(route="/media/<entity_id>/<file_code>/update"), methods=["PUT"])
@check_token_of_user
def upload_media_file_metadata(uid, entity_id, file_code,
                               mediaService: MediaService = injectable,
                               userService: UserService = injectable,
                               roleService: RoleService = injectable):
    pass


@current_app.route(current_app.flask_app.config['API_ROUTE'].format(route="/media/file/<file_code>/toggle/publish"), methods=["PUT"])
@check_token_of_user
def toggle_published_files(uid, file_code,
                           mediaService: MediaService = injectable,
                           userService: UserService = injectable,
                           roleService: RoleService = injectable):
    media = mediaService.get_file(file_code)
    if not media:
        return response_error("no file found")

    is_system_file = media['is_system_file']
    is_store_file = media['is_store_file']
    is_user_file = False
    if not media['is_system_file'] and not media['is_store_file']:
        is_user_file = True

    if is_system_file:
        roles = [RolesTypes.Support.value, RolesTypes.Owner.value, RolesTypes.Accounts.value]
        if not userService.user_has_any_role_matched(uid, roles):
            return response_error("Permission Error", None, 403)
    if is_store_file:
        roles = [RolesTypes.Support.value]
        user = userService.get_user(uid, True)
        if not userService.user_has_any_role_matched(uid, roles) or user.store_code != media['entity_code']:
            return response_error("Permission Error", None, 403)
    if is_user_file:
        supportRole = roleService.get_roles([RolesTypes.Support.value])
        if userService.user_has_any_role_matched(uid, supportRole) or uid != media['entity_code']:
            return response_error("Permission Error", None, 403)
    media = mediaService.toggle_file_publish(file_code)
    if not media:
        return response_error("internal Error, ,model not found", None, 500)
    return response_success(media)


@current_app.route(current_app.flask_app.config['API_ROUTE'].format(route="/media/file/<file_code>"), methods=["GET"])
@check_token_of_user
def download_media_file(uid, file_code,
                        mediaService: MediaService = injectable,
                        userService: UserService = injectable,
                        roleService: RoleService = injectable):
    media = mediaService.get_file(file_code, True)
    if not media:
        return response_error("no file found")

    is_system_file = media.is_system_file
    is_store_file = media.is_store_file
    is_user_file = False
    if not is_system_file and not is_store_file:
        is_user_file = True

    if is_system_file:
        roles = [RolesTypes.Support.value, RolesTypes.Owner.value, RolesTypes.Accounts.value]
        if not userService.user_has_any_role_matched(uid, roles):
            return response_error("Permission Error", None, 403)
    if is_store_file:
        roles = [RolesTypes.Support.value]
        user = userService.get_user(uid, True)
        if not userService.user_has_any_role_matched(uid, roles) or user.store_code != media.entity_code:
            return response_error("Permission Error", None, 403)
    if is_user_file:
        supportRole = roleService.get_roles([RolesTypes.Support.value])
        if userService.user_has_any_role_matched(uid, supportRole) or uid != media.entity_code:
            return response_error("Permission Error", None, 403)
    return media.download_file()


@current_app.route(current_app.flask_app.config['API_ROUTE'].format(route="/media/folder/create"), methods=["POST"])
@check_token_of_user
def create_virtual_directory(uid,
                             mediaService: MediaService = injectable,
                             userService: UserService = injectable,
                             roleService: RoleService = injectable):
    if not request.is_json:
        return response_error("Request Data must be in json format", request.data)
    try:
        schema = RequestMediaCreateFolderSchema()
        data = schema.load(request.json)

        is_system_folder = False
        is_store_folder = False
        if data['is_system_folder'] and not data['is_store_folder']:
            is_system_folder = True

        if not data['is_system_folder'] and data['is_store_folder']:
            is_store_folder = True

        if data['is_system_folder'] and data['is_store_folder']:
            return response_error("No Permission Create folder that both system and store folder type", {'params': request.json})
        if is_system_folder:
            roles = [RolesTypes.Support.value, RolesTypes.Owner.value, RolesTypes.Accounts.value]
            if userService.user_has_any_role_matched(uid, roles):
                result = mediaService.create_virtual_folder(uid, data, is_system_folder, is_store_folder)
                return response_success(result)
        if is_store_folder:
            roles = [RolesTypes.Support.value]
            user = userService.get_user(uid, True)
            if userService.user_has_any_role_matched(uid, roles) or user.store_code == data['entity_code']:
                result = mediaService.create_virtual_folder(uid, data, is_system_folder, is_store_folder)
                return response_success(result)
        if not is_system_folder and not is_store_folder:
            supportRole = roleService.get_roles([RolesTypes.Support.value])
            if userService.user_has_any_role_matched(uid, supportRole) or request.uid == data['entity_code']:
                result = mediaService.create_virtual_folder(uid, data, is_system_folder, is_store_folder)
                return response_success(result)
        return response_error("No Permission Create folder", {'params': request.json}, 403)
    except ValidationError as e:
        return response_error("Error on format of the params", {'params': request.json, 'error': e.messages})
    except UnableCreateFolder as e:
        current_app.logger.error("User failed create folder", {'params': request.json, 'e': e.message})
        return response_error("Error on create folder it may try create folder under same name or internal issue", {'params': request.json})


@current_app.route(current_app.flask_app.config['API_ROUTE'].format(route="/media/<entity_id>/folder/<folder_code>/delete"),
                   methods=["DELETE"])
@check_token_of_user
def delete_virtual_directory(uid, entity_id, folder_code,
                             mediaService: MediaService = injectable,
                             userService: UserService = injectable,
                             roleService: RoleService = injectable):
    def handle(type):
        media = mediaService.get_virtual_folder(folder_code, entity_id, True)
        if media is None:
            return response_error("folder not found", {'params': {entity_id, folder_code}})
        result = mediaService.delele_virtual_folder(media.code, type, entity_id)
        response_success({"delete_status": result})

    user = userService.get_user(request.uid, True)
    if entity_id == user.uid:
        return handle(current_app.flask_app.config['UPLOAD_USERS_FOLDER'])
    else:
        if entity_id == 'none':
            entity_id = None
        supportRole = roleService.get_roles([RolesTypes.Support.value])
        if userService.user_has_any_role_matched(request.uid, supportRole) or user.store_code == entity_id:
            type = current_app.flask_app.config['UPLOAD_SYSTEM_FOLDER']
            if entity_id is not None:
                type = current_app.flask_app.config['UPLOAD_STORES_FOLDER']
            return handle(type)
    return response_error("No Permission access folder", {'params': {entity_id, folder_code}}, 403)


@current_app.route(current_app.flask_app.config['API_ROUTE'].format(route="/media/<entity_id>/file/<file_code>/delete"), methods=["DELETE"])
@check_token_of_user
def delete_files(uid, entity_id, file_code,
                 mediaService: MediaService = injectable,
                 userService: UserService = injectable,
                 roleService: RoleService = injectable):
    media = mediaService.get_file(file_code)

    if not media:
        return response_error("no file found")
    is_valid = False
    is_system_folder = False
    is_store_folder = False
    if media['is_system_file'] and not media['is_store_file']:
        is_system_folder = True

    if not media['is_system_file'] and media['is_store_file']:
        is_store_folder = True

    if media['is_system_file'] and media['is_store_file']:
        return response_error("No Permission Create folder that both system and store folder type", {'params': {entity_id, file_code}})
    if is_system_folder:
        roles = [RolesTypes.Support.value, RolesTypes.Owner.value, RolesTypes.Accounts.value]
        if userService.user_has_any_role_matched(uid, roles):
            is_valid = True
    if is_store_folder:
        roles = [RolesTypes.Support.value]
        user = userService.get_user(uid, True)
        if userService.user_has_any_role_matched(uid, roles) or user.store_code == entity_id:
            is_valid = True
    if not is_system_folder and not is_store_folder:
        supportRole = roleService.get_roles([RolesTypes.Support.value])
        if userService.user_has_any_role_matched(uid, supportRole) or request.uid == entity_id:
            is_valid = True
    if is_valid:
        mediaService.delete_file(file_code)
        return response_success({})
    return response_error("No Permission access folder", {'params': {entity_id, file_code}}, 403)


# Todo: get users files and folders
@current_app.route(current_app.flask_app.config['API_ROUTE'].format(route="/media/list"), methods=["GET"])
@check_token_of_user
def get_media_list(uid,
                   mediaService: MediaService = injectable,
                   userService: UserService = injectable,
                   storeService: StoreService = injectable,
                   roleService: RoleService = injectable):
    is_system = False
    is_store = False
    from_folder_code = None
    entity_code = str(None)
    parent_level = 1
    only_folder = None
    is_valid = False
    if request.args.get('from_folder_code') is not None and request.args.get('from_folder_code') != '':
        from_folder_code = request.args.get('from_folder_code')
        parent_level = request.args.get('parent_level', type=int)
        if not mediaService.virtual_folder_exists(from_folder_code):
            return response_error("folder not found", {'params': request.json})

    if request.args.get('is_system', type=int) is not None:
        is_system = True if request.args.get('is_system', type=int) == 1 else False
    if request.args.get('is_store', type=int) is not None:
        is_store = True if request.args.get('is_store', type=int) == 1 else False
    if request.args.get('only_folder', type=int) is not None:
        only_folder = True if request.args.get('only_folder', type=int) == 1 else False
    if is_system and is_store:
        return response_error("Cant get both system folder and store please pick", {'params': request.args})
    if not is_system:
        if request.args.get('entity_code') is not None and request.args.get('entity_code') != '':
            entity_code = request.args.get('entity_code').lower()
            if is_store:
                if not storeService.store_exists(entity_code):
                    return response_error("store not found", {'params': request.args})

            if not is_store:
                if not userService.user_exists(entity_code):
                    return response_error("user not found", {'params': request.args})
        else:
            return response_error("missing params", {'params': request.args})
    else:
        roles = [RolesTypes.Support.value, RolesTypes.Owner.value, RolesTypes.Accounts.value]
        if userService.user_has_any_role_matched(uid, roles):
            is_valid = True
    if is_store:
        roles = [RolesTypes.Support.value]
        user = userService.get_user(uid, True)
        if userService.user_has_any_role_matched(uid, roles) or user.store_code == entity_code:
            is_valid = True
    if not is_system and not is_store:
        supportRole = roleService.get_roles([RolesTypes.Support.value])
        if userService.user_has_any_role_matched(uid, supportRole) or request.uid == entity_code:
            is_valid = True

    if is_valid:
        result = mediaService.get_list(uid, entity_code, is_system, is_store, from_folder_code, parent_level, only_folder)
        return response_success(result)
    return response_error("No Permission access folder", {'params': request.json}, 403)
