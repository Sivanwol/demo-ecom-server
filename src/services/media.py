import os
from logging import Logger
from uuid import uuid4

from config import settings
from config.database import db
from src.exceptions import UnableCreateFolder
from src.models import MediaFolder
from src.schemas import MediaFolderSchema
from src.schemas.requests import RequestMediaCreateFolderSchema
from src.services import FileSystemService


class MediaService:
    def __init__(self, logger: Logger, fileSystemService: FileSystemService):
        self.logger = logger
        self.fileSystemService = fileSystemService

    '''
        will get upto parent_folder_id is null the sub folder path
    '''

    def get_parent_path_folder(self, ref_media: MediaFolder, ref_sub_path='') -> str:
        media = MediaFolder.query.filter_by(code=ref_media.parent_folder_code).first()
        if ref_sub_path != '':
            ref_sub_path = os.path.join(ref_sub_path, media.code)
        if media.parent_folder_id is not None:
            ref_sub_path = self.get_parent_path_folder(media, ref_sub_path)
        return ref_sub_path

    def get_virtual_folder(self, code, entity_id=None, return_model=True):
        media = MediaFolder.query.filter_by(code=code).first()
        if media is None:
            return None
        type = media.type
        if not self.virtual_folder_exists(type, code, entity_id):
            return None
        if not return_model:
            schema = MediaFolderSchema()
            return schema.dumps(media)
        return media

    def virtual_folder_exists(self, type, code, entity_id=None) -> bool:
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

    def create_virtual_folder(self, data,is_system_folder, is_store_folder, return_model=False):
        code = "%s" % uuid4()
        result = MediaFolder.query.filter_by(name=data['name']).first()
        sub_path = None
        if result is not None:
            raise UnableCreateFolder(result.code, sub_path)
        if data['parent_level'] == 1:
            data['parent_folder_code'] = None
        media = MediaFolder(code, data['name'], data['alias'], data['description'], is_system_folder, is_store_folder, data['parent_level'],
                            data['parent_folder_code'])
        self.logger.info("register folder (%s) on database" % media.__str__())
        db.session.add(media)
        db.session.commit()
        sub_path = None

        if media.parent_folder_code is not None:
            sub_path = self.get_parent_path_folder(media)
        if is_system_folder:
            self.fileSystemService.create_folder(code, sub_path)
        if is_store_folder:
            self.fileSystemService.create_store_folder(data.entity_id, sub_path)
        if not is_system_folder and not is_store_folder:
            self.fileSystemService.create_user_folder(data.entity_id, sub_path)
        if not return_model:
            schema = MediaFolderSchema()
            return schema.dump(media, many=False)
        return media

    def delele_virtual_folder(self, folder_code, type, entity_id=None):
        if self.virtual_folder_exists(folder_code, type, entity_id):
            media = MediaFolder.query.filter_by(code=folder_code).first()
            list_folders = media.get_all_child_folders()
            list_folder_codes = []
            for folder in list_folders:
                list_folder_codes.append(folder.code)
                path = self.fileSystemService.get_folder_path(type, entity_id)
                self.fileSystemService.remove_folder(path)
            delete = MediaFolder.delete().where(MediaFolder.code.in_(list_folders))
            delete.execute()
            return True
        return False
