import os
from logging import Logger
from uuid import uuid4

from config import settings
from config.database import db
from src.models import MediaFolder
from src.schemas.requests import RequestMediaCreateFolderSchema
from src.services import FileSystemService


class MediaService:
    def __init__(self, logger: Logger, fileSystemService: FileSystemService):
        self.logger = logger
        self.fileSystemService = fileSystemService

    '''
        will get upto parent_folder_id is null the sub folder path
    '''

    def get_parent_path_folder(self, ref_media: MediaFolder, ref_sub_path=''):

        media = MediaFolder.query.filter_by(code=ref_media.parent_folder_code).first()
        if ref_sub_path != '':
            ref_sub_path = os.path.join(ref_sub_path, media.code)
        if media.parent_folder_id is not None:
            ref_sub_path = self.get_parent_path_folder(media, ref_sub_path)
        return ref_sub_path

    def virtual_folder_exists(self, type, code, entity_id=None):
        media = MediaFolder.query.filter_by(code=code).first()
        sub_path = None
        verify_folder = False
        if media is not None:
            verify_folder = True
            if media.parent_folder_code is not None:
                verify_folder = False
                sub_path = self.get_parent_path_folder(media)
            if type != settings[os.environ.get("FLASK_ENV", "development")].UPLOAD_SYSTEM_FOLDER:
                if sub_path is not None and entity_id is not None:
                    if self.fileSystemService.folder_exists(type, entity_id, sub_path):
                        verify_folder = True
            else:
                if self.fileSystemService.system_folder_exists(sub_path):
                    verify_folder = True
        return verify_folder

    def create_virtual_folder(self, data: RequestMediaCreateFolderSchema):
        code = "%s" % uuid4()
        media = MediaFolder(code, data.name, data.alias, data.description, data.is_system_folder, data.parent_folder_code)
        db.session.add(media)
        db.session.commit()
        sub_path = None
        if data.type == settings[os.environ.get("FLASK_ENV", "development")].UPLOAD_USERS_FOLDER:
            if media.parent_folder_code is not None:
                sub_path = self.get_parent_path_folder(media)
            self.fileSystemService.create_user_folder(data.entity_id, sub_path)

        if data.type == settings[os.environ.get("FLASK_ENV", "development")].UPLOAD_STORES_FOLDER:
            if media.parent_folder_code is not None:
                sub_path = self.get_parent_path_folder(media)
            self.fileSystemService.create_store_folder(data.entity_id, sub_path)

        if data.type == settings[os.environ.get("FLASK_ENV", "development")].UPLOAD_SYSTEM_FOLDER:
            if media.parent_folder_code is not None:
                sub_path = self.get_parent_path_folder(media)
            self.fileSystemService.create_folder(code, sub_path)