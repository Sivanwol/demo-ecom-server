import os
import pathlib
import shutil
from uuid import uuid4

from flask import Flask

from config.setup import app
from src.utils.enums import MediaAssetsType
from src.utils.validations import media_type_valid


class FileSystemService:
    def __init__(self, app: Flask, settingsService):
        self.logger = app.logger
        self.settingsService = settingsService

    def file_existed(self, src) -> bool:
        file = pathlib.Path(src)
        if file.exists() and file.is_file():
            return True
        return False

    def acutal_folder_existed(self, src) -> bool:
        folder = pathlib.Path(src)
        if folder.exists() and folder.is_dir():
            return True
        return False

    def acutal_file_existed(self, src) -> bool:
        file = pathlib.Path(src)
        if file.exists() and file.is_file():
            return True
        return False

    def remove_file(self, src):
        if self.file_existed(src):
            os.unlink(src)

    def remove_folder(self, src):
        try:
            self.logger.info('delete folder %s' % src)
            shutil.rmtree(src)
        except OSError as e:
            print("Error: %s : %s" % (src, e.strerror))
            self.logger.error("Error: %s : %s" % (src, e.strerror), {
                'path': src,
                'error': e.strerror
            })

    def get_folder_list(self, src):
        folders = []
        for dirname, dirnames, filenames in os.walk(src):
            # print path to all subdirectories first.
            for subdirname in dirnames:
                folders.append(os.path.join(dirname, subdirname))
        return folders

    def get_folder_path(self, type, entity_id, sub_folder=None):
        upload_path = None
        if media_type_valid(type):
            upload_path = os.path.join(app.config['UPLOAD_FOLDER'],
                                       type,
                                       entity_id)
            if sub_folder is not None:
                upload_path = os.path.join(app.config['UPLOAD_FOLDER'],
                                           type, entity_id, sub_folder)
        return upload_path

    def folder_exists(self, type, entity_id=None, sub_folder=None) -> bool:
        if not media_type_valid(type) or (sub_folder is not None and entity_id is None):
            return False

        upload_path = os.path.join(app.config['UPLOAD_FOLDER'],
                                   type)
        if sub_folder is not None and entity_id is not None:
            upload_path = os.path.join(app.config['UPLOAD_FOLDER'],
                                       type, entity_id, sub_folder)
        result = self.acutal_folder_existed(upload_path)
        self.logger.info('checking %s folder existed (%s)' % (type, result))
        return result

    def temp_move_file(self, temp_file_location, dest_path):
        shutil.move(temp_file_location, dest_path)

    def system_folder_exists(self, sub_folder=None) -> bool:
        upload_path = os.path.join(app.config['UPLOAD_FOLDER'])
        if sub_folder is not None:
            upload_path = os.path.join(app.config['UPLOAD_FOLDER'], sub_folder)
        result = self.acutal_folder_existed(upload_path)
        self.logger.info('checking system folder existed (%s)' % result)
        return result

    def create_folder(self, src, sub_path=None, force_create=False):
        src = os.path.join(app.config['UPLOAD_FOLDER'], src)
        if sub_path is not None:
            src = os.path.join(src, sub_path)
        if not self.acutal_folder_existed(src):
            if force_create:
                self.remove_folders(src)
            try:
                self.logger.info("create folder (%s)" % src)
                os.mkdir(src)
            except OSError as e:
                print("Error: %s : %s" % (src, e.strerror))
                self.logger.error("Error: %s : %s" % (src, e.strerror), {
                    'path': src,
                    'error': e.strerror
                })

    def create_user_folder_initialize(self, entity_id):
        upload_path = os.path.join(app.config['UPLOAD_FOLDER'],
                                   app.config['UPLOAD_USERS_FOLDER'],
                                   entity_id)
        if not self.acutal_folder_existed(upload_path):
            self.logger.info('initialize user folder %s (entity id: %s )' % (upload_path, entity_id))
            self.create_folder(upload_path, None)

    def create_user_folder(self, entity_id, code, sub_path=None):
        upload_path = os.path.join(app.config['UPLOAD_FOLDER'],
                                   app.config['UPLOAD_USERS_FOLDER'],
                                   entity_id, code)
        self.logger.info('create user folder %s (entity id: %s ,code: %s )' % (upload_path, entity_id, code))
        self.create_folder(upload_path, sub_path)

    def create_store_folder_initialize(self, entity_id):
        upload_path = os.path.join(app.config['UPLOAD_FOLDER'],
                                   app.config['UPLOAD_STORES_FOLDER'],
                                   entity_id)
        if not self.acutal_folder_existed(upload_path):
            self.logger.info('initialize store folder %s (entity id: %s )' % (upload_path, entity_id))
            self.create_folder(upload_path, None)

    def create_store_folder(self, entity_id, code, sub_path=None):
        upload_path = os.path.join(app.config['UPLOAD_FOLDER'],
                                   app.config['UPLOAD_STORES_FOLDER'],
                                   entity_id, code)
        self.logger.info('create store folder %s (entity id: %s ,code: %s )' % (upload_path, entity_id, code))
        self.create_folder(upload_path, sub_path)

    def identify_file_type(self, file_ext):
        docs = ['doc', 'txt', 'xls', 'docx', 'xlsx', 'odt', 'pdf']
        video = ['avi', 'mp4']
        image = ['jpg', 'jpeg', 'gif', 'png']
        if file_ext in docs:
            return MediaAssetsType.Document
        if file_ext in video:
            return MediaAssetsType.Video
        if file_ext in image:
            return MediaAssetsType.Image

    def save_temporary_upload_files(self, files):
        upload_path = os.path.join(app.config['UPLOAD_FOLDER'],
                                   app.config['UPLOAD_TEMP_FOLDER'])
        response = []
        allow_ext = self.settingsService.getItem('UPLOAD_ALLOW_FILES_TYPES').decode("utf-8")
        allow_ext = allow_ext.split(',')
        for file in files:
            extension = os.path.splitext(file.filename)[1].replace(".", "")
            file.seek(0, os.SEEK_END)
            file_length = file.tell()
            if extension in allow_ext:
                file_name = f'{uuid4()}.{extension}'
                file_location = os.path.join(upload_path, file_name)
                file.save(file_location)
                response.append({
                    'file_location': file_location,
                    'file_name': file.filename,
                    'file_ext': extension,
                    'file_type': self.identify_file_type(extension),
                    'file_original_name': file.filename,
                    'file_size': file_length
                })
        return response
