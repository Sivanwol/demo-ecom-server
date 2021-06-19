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

    def create_folder(self, src, force_create=False):
        if not self.file_existed(src):
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
        upload_path = settings[os.environ.get("FLASK_ENV", "development")].UPLOAD_FOLDER
        upload_path += "/%s/%s" % (settings[os.environ.get("FLASK_ENV", "development")].UPLOAD_USERS_FOLDER, entity_id)
        app.logger.info('create user folder %s (entity id: %s)' % (upload_path, entity_id))
        self.create_folder(upload_path)

    def create_store_folder(self, entity_id):
        upload_path = settings[os.environ.get("FLASK_ENV", "development")].UPLOAD_FOLDER
        upload_path += "/%s/%s" % (settings[os.environ.get("FLASK_ENV", "development")].UPLOAD_USERS_FOLDER, entity_id)
        app.logger.info('create store folder %s (entity id: %s)' % (upload_path, entity_id))
        self.create_folder(upload_path)
