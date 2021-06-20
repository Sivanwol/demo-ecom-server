import os
import pathlib
import shutil

from config import settings
from config.api import app


class FileSystemService:
    def file_existed(self, src):
        file = pathlib.Path(src)
        if file.exists() and file.is_file():
            return True
        return False

    def folder_existed(self, src):
        folder = pathlib.Path(src)
        if folder.exists() and folder.is_dir():
            return True
        return False

    def remove_folders(self, src):
        try:
            app.logger.info('delete folder %s' % src)
            shutil.rmtree(src)
        except OSError as e:
            print("Error: %s : %s" % (src, e.strerror))
            app.logger.error("Error: %s : %s" % (src, e.strerror), {
                'path': src,
                'error': e.strerror
            })

    def getFolderList(self, src):
        folders = []
        for dirname, dirnames, filenames in os.walk(src):
            # print path to all subdirectories first.
            for subdirname in dirnames:
                folders.append(os.path.join(dirname, subdirname))
        return folders

    def getFolderPath(self, type, entity_id):
        user_path = settings[os.environ.get("FLASK_ENV", "development")].UPLOAD_USERS_FOLDER
        system_path = settings[os.environ.get("FLASK_ENV", "development")].UPLOAD_SYSTEM_FOLDER
        store_path = settings[os.environ.get("FLASK_ENV", "development")].UPLOAD_STORES_FOLDER
        upload_path = None
        if type == user_path or type == system_path or type == store_path:
            upload_path = os.path.join(settings[os.environ.get("FLASK_ENV", "development")].UPLOAD_FOLDER,
                                       type,
                                       entity_id)
        return upload_path

    def create_folder(self, src, force_create=False):
        if not self.folder_existed(src):
            if force_create:
                self.remove_folders(src)
            try:
                os.mkdir(src)
            except OSError as e:
                print("Error: %s : %s" % (src, e.strerror))
                app.logger.error("Error: %s : %s" % (src, e.strerror), {
                    'path': src,
                    'error': e.strerror
                })

    def create_user_folder(self, entity_id):
        upload_path = os.path.join(settings[os.environ.get("FLASK_ENV", "development")].UPLOAD_FOLDER,
                                   settings[os.environ.get("FLASK_ENV", "development")].UPLOAD_USERS_FOLDER,
                                   entity_id)
        app.logger.info('create user folder %s (entity id: %s)' % (upload_path, entity_id))
        self.create_folder(upload_path)

    def create_store_folder(self, entity_id):
        upload_path = os.path.join(settings[os.environ.get("FLASK_ENV", "development")].UPLOAD_FOLDER,
                                   settings[os.environ.get("FLASK_ENV", "development")].UPLOAD_STORES_FOLDER,
                                   entity_id)
        app.logger.info('create store folder %s (entity id: %s)' % (upload_path, entity_id))
        self.create_folder(upload_path)
