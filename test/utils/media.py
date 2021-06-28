import os
from uuid import uuid4

from config import settings
from config.database import db
from src.models import MediaFolder
from src.utils.general import Struct


class MediaTestUtills:
    def __init__(self, test_object):
        self.test_object = test_object

    def create_media_folder_parents(self, uid, limit_only_level=0):
        list_of_folders = []
        root_code = str(uuid4())
        entity_code = str(None)
        db.session.add(MediaFolder(root_code, entity_code, uid, "root-1", 'root-1', None, True, False, 1, None))
        for i in range(3):
            chile_lvl1_code = str(uuid4())
            db.session.add(MediaFolder(chile_lvl1_code, entity_code, uid, "root-1-child-1-lvl-1", 'root-1-child-1-lvl-1', None, True, False, 2, root_code))
            for r in range(3):
                chile_lvl2_code = str(uuid4())
                db.session.add(
                    MediaFolder(chile_lvl2_code, entity_code, uid, "root-1-child-1-lvl-2", 'root-1-child-1-lvl-2', None, True, False, 3, chile_lvl1_code))
        root_code = str(uuid4())
        list_of_folders.append(root_code)
        db.session.add(MediaFolder(root_code, entity_code, uid, "root-2", 'root-2', None, True, False, 1, None))
        for i in range(3):
            level = 2
            chile_lvl1_code = str(uuid4())
            if limit_only_level == level or limit_only_level == 0:
                list_of_folders.append(chile_lvl1_code)
            db.session.add(MediaFolder(chile_lvl1_code, entity_code, uid, "root-2-child-2-lvl-1", 'root-2-child-2-lvl-1', None, True, False, 2, root_code))
            for r in range(3):
                level = 3
                chile_lvl2_code = str(uuid4())
                if limit_only_level == level or limit_only_level == 0:
                    list_of_folders.append(chile_lvl2_code)
                db.session.add(
                    MediaFolder(chile_lvl2_code, entity_code, uid, "root-2-child-2-lvl-2", 'root-2-child-2-lvl-2', None, True, False, 3, chile_lvl1_code))

        db.session.commit()
        return list_of_folders

    def create_system_folder(self):
        user_object = self.test_object.login_user(self.test_object.platform_owner_user)
        uid = user_object['uid']
        token = user_object['idToken']
        post_data = {
            'name': self.test_object.fake.domain_word(),
            'alias': self.test_object.fake.domain_word(),
            'description': self.test_object.fake.sentence(nb_words=10),
            'is_system_folder': True,
            'is_store_folder': False,
            'entity_code': str(None),
            'parent_level': 1
        }
        response = self.test_object.request_post('api/media/folder/create', token, None, None, post_data)
        self.test_object.assertRequestPassed(response, 'failed request create folder')
        response_data = Struct(response.json)
        self.test_object.assertIsNotNone(response_data)
        self.test_object.assertTrue(response_data.status)
        self.test_object.assertIsNotNone(response_data.data)
        folder_code = response_data.data.media.code
        result = MediaFolder.query.filter_by(code=folder_code).first()
        self.test_object.assertTrue(self.test_object.mediaService.virtual_folder_exists(folder_code))
        self.test_object.assertIsNotNone(result)
        self.test_object.assertEqual(result.name, response_data.data.media.name)
        self.test_object.assertEqual(result.alias, response_data.data.media.alias)
        self.test_object.assertEqual(result.description, response_data.data.media.description)
        self.test_object.assertEqual(result.is_system_folder, response_data.data.media.is_system_folder)
        self.test_object.assertEqual(result.is_store_folder, response_data.data.media.is_store_folder)
        self.test_object.assertEqual(result.parent_folder_code, 'None')
        self.test_object.assertEqual(result.parent_level, 1)
        self.test_object.assertEqual(result.parent_level, response_data.data.media.parent_level)
        return response_data.data.media
