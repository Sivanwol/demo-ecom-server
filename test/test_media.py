# test/test_media.py
import os
import unittest

from config import settings
from src.models import MediaFolder
from src.utils.general import Struct
from test.common.Basecase import BaseTestCase


class FlaskTestCase(BaseTestCase):
    def test_model_get_all_parent_folders(self):
        user_object = self.login_user(self.platform_owner_user)
        uid = user_object['uid']
        list_folders = self.mediaUtils.create_media_folder_parents(uid)
        root_code = list_folders[0]
        list_folders.pop(0)
        result = MediaFolder.query.filter_by(code=root_code).first()
        self.assertIsNotNone(result)
        self.assertEqual(result.code, root_code)
        folders = result.get_all_child_folders()
        test_folder_codes = []
        for folder in folders:
            test_folder_codes.append(folder.code)
        self.assertEqual(len(test_folder_codes), len(list_folders))
        for code in test_folder_codes:
            self.assertIn(code, list_folders)

    def test_model_get_next_level_parent_folders(self):
        user_object = self.login_user(self.platform_owner_user)
        uid = user_object['uid']
        list_folders = self.mediaUtils.create_media_folder_parents(uid, 2)
        root_code = list_folders[0]
        list_folders.pop(0)
        result = MediaFolder.query.filter_by(code=root_code).first()
        self.assertIsNotNone(result)
        self.assertEqual(result.code, root_code)
        folders = result.get_all_child_folders(True)
        test_folder_codes = []
        for folder in folders:
            test_folder_codes.append(folder.code)
        self.assertEqual(len(test_folder_codes), len(list_folders))
        for code in test_folder_codes:
            self.assertIn(code, list_folders)

    def test_create_folder_type_system_level_root(self):
        with self.client:
            user_object = self.login_user(self.platform_owner_user)
            uid = user_object['uid']
            token = user_object['idToken']
            post_data = {
                'name': self.fake.domain_word(),
                'alias': self.fake.domain_word(),
                'description': self.fake.sentence(nb_words=10),
                'is_system_folder': True,
                'is_store_folder': False,
                'parent_level': 1
            }
            response = self.request_post('api/media/folder/create', token, None, None, post_data)
            self.assertRequestPassed(response, 'failed request create folder')
            response_data = Struct(response.json)
            self.assertIsNotNone(response_data)
            self.assertTrue(response_data.status)
            self.assertIsNotNone(response_data.data)
            folder_code = response_data.data.code
            result = MediaFolder.query.filter_by(code=folder_code).first()
            self.assertTrue(self.mediaService.virtual_folder_exists(post_data['type'], folder_code))
            self.assertIsNotNone(result)
            self.assertEqual(result.name, response_data.data.name)
            self.assertEqual(result.alias, response_data.data.alias)
            self.assertEqual(result.description, response_data.data.description)
            self.assertEqual(result.type, response_data.data.type)
            self.assertIsNone(result.parent_folder_code)
            self.assertEqual(result.parent_level, 1)
            self.assertEqual(result.parent_level, response_data.data.parent_level)
