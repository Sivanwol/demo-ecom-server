import os
import pathlib
import shutil
from logging import Logger

from config import settings
from src.utils.validations import media_type_valid


class FileSystemService:
    def __init__(self, logger: Logger):
        self.logger = logger

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

    def remove_folders(self, src):
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
            upload_path = os.path.join(settings[os.environ.get("FLASK_ENV", "development")].UPLOAD_FOLDER,
                                       type,
                                       entity_id)
            if sub_folder is not None:
                upload_path = os.path.join(settings[os.environ.get("FLASK_ENV", "development")].UPLOAD_FOLDER,
                                           type, entity_id, sub_folder)
        return upload_path

    def folder_exists(self, type, entity_id=None, sub_folder=None) -> bool:
        if not media_type_valid(type) or (sub_folder is not None and entity_id is None):
            return False

        upload_path = os.path.join(settings[os.environ.get("FLASK_ENV", "development")].UPLOAD_FOLDER,
                                   type)
        if sub_folder is not None and entity_id is not None:
            upload_path = os.path.join(settings[os.environ.get("FLASK_ENV", "development")].UPLOAD_FOLDER,
                                       type, entity_id, sub_folder)
        result = self.acutal_folder_existed(upload_path)
        self.logger.info('checking %s folder existed (%s)' % (type, result))
        return result

    def system_folder_exists(self, sub_folder=None) -> bool:
        upload_path = os.path.join(settings[os.environ.get("FLASK_ENV", "development")].UPLOAD_FOLDER)
        if sub_folder is not None:
            upload_path = os.path.join(settings[os.environ.get("FLASK_ENV", "development")].UPLOAD_FOLDER, sub_folder)
        result = self.acutal_folder_existed(upload_path)
        self.logger.info('checking system folder existed (%s)' % result)
        return result

    def create_folder(self, src, sub_path=None, force_create=False):
        src = os.path.join(settings[os.environ.get("FLASK_ENV", "development")].UPLOAD_FOLDER, src)
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

    def create_user_folder(self, entity_id, code, sub_path=None):
        upload_path = os.path.join(settings[os.environ.get("FLASK_ENV", "development")].UPLOAD_FOLDER,
                                   settings[os.environ.get("FLASK_ENV", "development")].UPLOAD_USERS_FOLDER,
                                   entity_id)
        self.logger.info('create user folder %s (entity id: %s ,code: %s )' % (upload_path, entity_id, code))
        self.create_folder(upload_path, sub_path)

    def create_store_folder(self, entity_id, code, sub_path=None):
        upload_path = os.path.join(settings[os.environ.get("FLASK_ENV", "development")].UPLOAD_FOLDER,
                                   settings[os.environ.get("FLASK_ENV", "development")].UPLOAD_STORES_FOLDER,
                                   entity_id, code)
        self.logger.info('create store folder %s (entity id: %s ,code: %s )' % (upload_path, entity_id, code))
        self.create_folder(upload_path, sub_path)
