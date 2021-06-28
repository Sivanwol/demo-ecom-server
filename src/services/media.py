import os
from uuid import uuid4

from flask import Flask, send_file

from config.database import db
from config.setup import app
from src.exceptions import UnableCreateFolder
from src.models import MediaFolder, MediaFile
from src.schemas import MediaFolderSchema, MediaFileSchema
from src.services import FileSystemService


class MediaService:
    def __init__(self, app: Flask, fileSystemService: FileSystemService):
        self.logger = app.logger
        self.fileSystemService = fileSystemService

    '''
        will get upto parent_folder_code is null the sub folder path
    '''

    def get_parent_path_folder(self, ref_media: MediaFolder, ref_sub_path='') -> str:
        media = MediaFolder.query.filter_by(code=ref_media.code).first()
        if media.parent_level != 1:
            ref_sub_path = os.path.join(ref_sub_path, media.code)
        if media.parent_folder_code is not None and media.parent_folder_code != 'None':
            ref_sub_path = self.get_parent_path_folder(MediaFolder.query.filter_by(code=media.parent_folder_code).first(), ref_sub_path)
        return ref_sub_path

    ''' getting the root media folder the code here stupid and not optimize as well basically bad note to my self refactor this shit'''

    def get_root_virtual_folder(self, code):
        media = MediaFolder.query.filter_by(code=code).first()
        if media is None:
            return None

        if media.parent_level == 1:
            return media

        if media.parent_level == 2:
            media = MediaFolder.query.filter_by(code=media.parent_folder_code).first()

        if media.parent_level == 3:
            media = MediaFolder.query.filter_by(code=media.parent_folder_code).first()
            media = MediaFolder.query.filter_by(code=media.parent_folder_code).first()

        return media

    def get_virtual_folder(self, code, entity_id=None, return_model=True):
        media = MediaFolder.query.filter_by(code=code).first()
        if media is None:
            return None
        if not self.virtual_folder_exists(code, entity_id):
            return None
        if not return_model:
            schema = MediaFolderSchema()
            return schema.dumps(media)
        return media

    def get_file(self, code, return_model=False):
        media = MediaFile.query.filter_by(code=str(code)).first()
        if media is None:
            return False
        if not return_model:
            schema = MediaFileSchema()
            return schema.dump(media, many=False)
        return media

    def toggle_file_publish(self, code, return_model=True):
        media = MediaFile.query.filter_by(code=str(code)).first()
        if media is None:
            return False
        media.is_publish = not media.is_publish
        db.session.merge(media)
        db.session.commit()
        if not return_model:
            schema = MediaFileSchema()
            return schema.dump(media, many=False)
        return media

    def virtual_file_exists(self, code) -> bool:
        media = MediaFile.query.filter_by(code=str(code)).first()
        if media is not None:
            if self.fileSystemService.acutal_file_existed(media.file_location):
                return True
        return False

    def virtual_folder_exists(self, code, entity_code=None) -> bool:
        media = MediaFolder.query.filter_by(code=str(code)).first()
        root_media = media
        if media.parent_level != 1:
            root_media = self.get_root_virtual_folder(str(code))
        sub_path = None
        verify_folder = False
        if media is not None:
            if media.parent_folder_code != 'None':
                verify_folder = False
                sub_path = self.get_parent_path_folder(media)
            is_system_folder = root_media.is_system_folder
            is_store_folder = root_media.is_store_folder
            is_user_folder = False
            if not is_system_folder and not is_store_folder:
                is_user_folder = True
            if is_store_folder or is_user_folder:
                store_dir = app.config['UPLOAD_STORES_FOLDER']
                type = app.config['UPLOAD_USERS_FOLDER'] if is_user_folder else store_dir
                if self.fileSystemService.folder_exists(type, entity_code, sub_path):
                    verify_folder = True

            if is_system_folder:
                path = os.path.join(app.config['UPLOAD_FOLDER'],
                                    app.config['UPLOAD_SYSTEM_FOLDER'],
                                    root_media.code)
                if sub_path != '' and sub_path is not None:
                    path = os.path.join(app.config['UPLOAD_FOLDER'],
                                        app.config['UPLOAD_SYSTEM_FOLDER'],
                                        root_media.code, path)
                if self.fileSystemService.acutal_folder_existed(path):
                    verify_folder = True
        return verify_folder

    def create_user_folder(self, uid):
        name = 'main user folder %s' % uid
        code = "%s" % uuid4()
        media = MediaFolder(code, uid, uid, name, uid, '', False, False, 1, str('None'))
        db.session.add(media)
        db.session.commit()
        self.fileSystemService.create_user_folder(uid, code)
        self.logger.info(f'create media record user folder: {code}')
        return media

    def create_store_folder(self, uid, store_code):
        name = 'main store folder %s' % store_code
        code = "%s" % uuid4()
        media = MediaFolder(code, store_code, uid, name, '', '', False, True, 1, str('None'))
        db.session.add(media)
        db.session.commit()
        self.fileSystemService.create_store_folder(store_code, code)
        self.logger.info(f'create media record store folder: {code}')
        return media

    def create_virtual_folder(self, uid, data, is_system_folder, is_store_folder, return_model=False):
        code = "%s" % uuid4()
        result = MediaFolder.query.filter_by(name=data['name']).first()
        sub_path = None
        if result is not None:
            raise UnableCreateFolder(result.code, sub_path)
        if data['parent_level'] == 1:
            data['parent_folder_code'] = None
        media = MediaFolder(code, data['entity_code'], uid, data['name'], data['alias'], data['description'], is_system_folder, is_store_folder,
                            data['parent_level'], str(data['parent_folder_code']))
        self.logger.info("register folder (%s) on database" % media.__str__())
        db.session.add(media)
        db.session.commit()
        sub_path = None
        root_media = media
        if media.parent_folder_code != 'None':
            sub_path = self.get_parent_path_folder(media)
            root_media = self.get_root_virtual_folder(code)
        if is_system_folder:
            self.fileSystemService.create_folder(os.path.join(app.config['UPLOAD_SYSTEM_FOLDER'], root_media.code),
                                                 sub_path)
        if is_store_folder:
            self.fileSystemService.create_store_folder(data['entity_code'], root_media.code, sub_path)
        if not is_system_folder and not is_store_folder:
            self.fileSystemService.create_user_folder(data['entity_code'], root_media.code, sub_path)
        if not return_model:
            schema = MediaFolderSchema()
            return {
                "root_media": schema.dump(root_media, many=False) if media.parent_folder_code != 'None' else None,
                "media": schema.dump(media, many=False)
            }
        return {
            "root_media": root_media if media.parent_folder_code != 'None' else None,
            "media": media
        }

    def delete_file(self, file_code):
        media = self.get_file(file_code, True)
        self.fileSystemService.remove_file(media.file_location)
        delete = MediaFolder.delete().where(MediaFolder.code.in_(media.code))
        delete.execute()

    def delele_virtual_folder(self, folder_code, type, entity_code=None):
        if self.virtual_folder_exists(folder_code, type, entity_code):
            media = MediaFolder.query.filter_by(code=folder_code).first()
            list_folders = media.get_all_child_folders()
            list_folder_codes = []
            for folder in list_folders:
                list_folder_codes.append(folder.code)
                path = self.fileSystemService.get_folder_path(type, entity_code)
                self.fileSystemService.remove_folder(path)
            delete = MediaFolder.delete().where(MediaFolder.code.in_(list_folders))
            delete.execute()
            return True
        return False

    def register_uploaded_files(self, uid, files, metadata, is_system_file, is_store_file, is_user_file):
        system_path = os.path.join(app.config['UPLOAD_FOLDER'],
                                   app.config['UPLOAD_SYSTEM_FOLDER'])

        user_path = os.path.join(app.config['UPLOAD_FOLDER'],
                                 app.config['UPLOAD_USERS_FOLDER'])

        store_path = os.path.join(app.config['UPLOAD_FOLDER'],
                                  app.config['UPLOAD_STORES_FOLDER'])

        root_media = MediaFolder.query.filter_by(code=str(metadata['folder_code'])).first()
        sub_path = ''
        if root_media.parent_folder_code != 'None':
            sub_path = self.get_parent_path_folder(root_media)
            root_media = self.get_root_virtual_folder(str(metadata['folder_code']))
        media_files = []
        for file in files:

            temp_file_location = file['file_location']
            file_name = file['file_name']
            file_size = file['file_size']
            file_type = file['file_type']
            file_ext = file['file_ext']
            file_location = ''
            if is_system_file:
                file_location = os.path.join(system_path, root_media.code, sub_path) if sub_path != '' else os.path.join(system_path, root_media.code)
            if is_store_file:
                file_location = os.path.join(store_path, metadata['entity_code'], root_media.code)
                if sub_path != '':
                    file_location = os.path.join(store_path, metadata['entity_code'], root_media.code, sub_path)
            if is_user_file:
                file_location = os.path.join(user_path, metadata['entity_code'], root_media.code)
                if sub_path != '':
                    file_location = os.path.join(user_path, metadata['entity_code'], root_media.code, sub_path)
            file = MediaFile(str(uuid4()), uid, metadata['entity_code'], root_media.code, os.path.join(file_location, file_name), file_type.value, file_size, file_name,
                             file_ext, False, is_system_file, is_store_file)
            db.session.add(file)
            self.fileSystemService.temp_move_file(temp_file_location, os.path.join(file_location, file_name))
            media_files.append(file)
        db.session.commit()
        return media_files

    def get_list(self, owner_user_uid, entity_code, is_system, is_store, from_folder_code=None, parent_level=1, only_folder=False, return_model=False):
        items = []
        folderSchema = MediaFolderSchema()
        fileSchema = MediaFileSchema()
        if parent_level == 1:
            result_folders = MediaFolder.query.filter_by(owner_user_uid=owner_user_uid, entity_code=entity_code, is_system_folder=is_system,
                                                         is_store_folder=is_store, parent_level=1).all()
        else:
            folder = self.get_root_virtual_folder(from_folder_code)
            result_folders = folder.get_all_child_folders(True)

        for folder in result_folders:
            if not only_folder:
                files = MediaFile.query.filter_by(owner_user_uid=owner_user_uid, entity_code=entity_code, folder_code=folder.code, is_system_file=is_system, is_store_file=is_store)
                item = {folder, files}
                if not return_model:
                    item = {
                        'folder': folderSchema.dump(folder, many=False),
                        'files': fileSchema.dump(files, many=True)
                    }
                items.append(item)
            else:
                item = {folder}
                if not return_model:
                    item = {
                        'folder': folderSchema.dump(folder, many=False)
                    }
                items.append(item)
        return items

    def post_process_files_uploads(self, files):
        pass
