# test/test_media.py
import unittest
from io import BytesIO

from src.models import MediaFolder, MediaFile
from src.utils.general import Struct
from test.common.Basecase import BaseTestCase


class FlaskTestCase(BaseTestCase):
    store_owner_user = 'store.owner@store.user'

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
                'entity_code': str(None),
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
            folder_code = response_data.data.media.code
            result = MediaFolder.query.filter_by(code=folder_code).first()
            self.assertTrue(self.mediaService.virtual_folder_exists(folder_code))
            self.assertIsNotNone(result)
            self.assertEqual(result.name, response_data.data.media.name)
            self.assertEqual(result.alias, response_data.data.media.alias)
            self.assertEqual(result.description, response_data.data.media.description)
            self.assertEqual(result.is_system_folder, response_data.data.media.is_system_folder)
            self.assertEqual(result.is_store_folder, response_data.data.media.is_store_folder)
            self.assertEqual(result.parent_folder_code, 'None')
            self.assertEqual(result.parent_level, 1)
            self.assertEqual(result.parent_level, response_data.data.media.parent_level)

    def test_create_folder_type_system_level_1(self):
        with self.client:
            user_object = self.login_user(self.platform_owner_user)
            uid = user_object['uid']
            token = user_object['idToken']
            post_data = {
                'name': self.fake.domain_word(),
                'alias': self.fake.domain_word(),
                'description': self.fake.sentence(nb_words=10),
                'entity_code': str(None),
                'is_system_folder': True,
                'is_store_folder': False,
                'parent_level': 1
            }
            response = self.request_post('api/media/folder/create', token, None, None, post_data)
            self.assertRequestPassed(response, 'failed request create folder root level')
            response_data = Struct(response.json)
            self.assertIsNotNone(response_data)
            self.assertTrue(response_data.status)
            self.assertIsNotNone(response_data.data)
            root_folder_code = response_data.data.media.code
            root_media = MediaFolder.query.filter_by(code=root_folder_code).first()
            self.assertTrue(self.mediaService.virtual_folder_exists(root_folder_code))
            self.assertIsNotNone(root_media)
            self.assertEqual(root_media.code, response_data.data.media.code)
            self.assertEqual(root_media.name, response_data.data.media.name)
            self.assertEqual(root_media.alias, response_data.data.media.alias)
            self.assertEqual(root_media.description, response_data.data.media.description)
            self.assertEqual(root_media.is_system_folder, response_data.data.media.is_system_folder)
            self.assertEqual(root_media.is_store_folder, response_data.data.media.is_store_folder)
            self.assertEqual(root_media.parent_folder_code, 'None')
            self.assertEqual(root_media.parent_level, 1)
            self.assertEqual(root_media.parent_level, response_data.data.media.parent_level)

            post_data = {
                'name': self.fake.domain_word(),
                'alias': self.fake.domain_word(),
                'description': self.fake.sentence(nb_words=10),
                'entity_code': str(None),
                'is_system_folder': True,
                'is_store_folder': False,
                'parent_level': 2,
                'parent_folder_code': root_folder_code
            }
            response = self.request_post('api/media/folder/create', token, None, None, post_data)
            self.assertRequestPassed(response, 'failed request create folder level 1')
            response_data = Struct(response.json)
            self.assertIsNotNone(response_data)
            self.assertTrue(response_data.status)
            self.assertIsNotNone(response_data.data)
            lvl1_folder_code = response_data.data.media.code
            result = MediaFolder.query.filter_by(code=lvl1_folder_code).first()
            self.assertTrue(self.mediaService.virtual_folder_exists(lvl1_folder_code))
            self.assertIsNotNone(result)
            self.assertEqual(result.name, response_data.data.media.name)
            self.assertEqual(result.alias, response_data.data.media.alias)
            self.assertEqual(result.description, response_data.data.media.description)
            self.assertEqual(result.is_system_folder, response_data.data.media.is_system_folder)
            self.assertEqual(result.is_store_folder, response_data.data.media.is_store_folder)
            self.assertIsNotNone(result.parent_folder_code)
            self.assertEqual(result.parent_level, 2)
            self.assertEqual(result.parent_level, response_data.data.media.parent_level)
            self.assertEqual(result.code, lvl1_folder_code)
            self.assertEqual(result.parent_folder_code, root_media.code)
            self.assertEqual(root_media.code, response_data.data.root_media.code)

    def test_create_folder_type_user_level_root(self):
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
                'entity_code': uid,
                'parent_level': 1
            }
            response = self.request_post('api/media/folder/create', token, None, None, post_data)
            self.assertRequestPassed(response, 'failed request create folder')
            response_data = Struct(response.json)
            self.assertIsNotNone(response_data)
            self.assertTrue(response_data.status)
            self.assertIsNotNone(response_data.data)
            folder_code = response_data.data.media.code
            result = MediaFolder.query.filter_by(code=folder_code).first()
            self.assertTrue(self.mediaService.virtual_folder_exists(folder_code))
            self.assertIsNotNone(result)
            self.assertEqual(result.name, response_data.data.media.name)
            self.assertEqual(result.alias, response_data.data.media.alias)
            self.assertEqual(result.description, response_data.data.media.description)
            self.assertEqual(result.is_system_folder, response_data.data.media.is_system_folder)
            self.assertEqual(result.is_store_folder, response_data.data.media.is_store_folder)
            self.assertEqual(result.parent_folder_code, 'None')
            self.assertEqual(result.parent_level, 1)
            self.assertEqual(result.parent_level, response_data.data.media.parent_level)

    def test_create_folder_type_user_level_1(self):
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
                'entity_code': uid,
                'parent_level': 1
            }
            response = self.request_post('api/media/folder/create', token, None, None, post_data)
            self.assertRequestPassed(response, 'failed request create folder root level')
            response_data = Struct(response.json)
            self.assertIsNotNone(response_data)
            self.assertTrue(response_data.status)
            self.assertIsNotNone(response_data.data)
            root_folder_code = response_data.data.media.code
            root_media = MediaFolder.query.filter_by(code=root_folder_code).first()
            self.assertTrue(self.mediaService.virtual_folder_exists(root_folder_code, uid))
            self.assertIsNotNone(root_media)
            self.assertEqual(root_media.code, response_data.data.media.code)
            self.assertEqual(root_media.name, response_data.data.media.name)
            self.assertEqual(root_media.alias, response_data.data.media.alias)
            self.assertEqual(root_media.description, response_data.data.media.description)
            self.assertEqual(root_media.is_system_folder, response_data.data.media.is_system_folder)
            self.assertEqual(root_media.is_store_folder, response_data.data.media.is_store_folder)
            self.assertEqual(root_media.parent_folder_code, 'None')
            self.assertEqual(root_media.parent_level, 1)
            self.assertEqual(root_media.parent_level, response_data.data.media.parent_level)

            post_data = {
                'name': self.fake.domain_word(),
                'alias': self.fake.domain_word(),
                'description': self.fake.sentence(nb_words=10),
                'is_system_folder': True,
                'is_store_folder': False,
                'entity_code': uid,
                'parent_level': 2,
                'parent_folder_code': root_folder_code
            }
            response = self.request_post('api/media/folder/create', token, None, None, post_data)
            self.assertRequestPassed(response, 'failed request create folder level 1')
            response_data = Struct(response.json)
            self.assertIsNotNone(response_data)
            self.assertTrue(response_data.status)
            self.assertIsNotNone(response_data.data)
            lvl1_folder_code = response_data.data.media.code
            result = MediaFolder.query.filter_by(code=lvl1_folder_code).first()
            self.assertTrue(self.mediaService.virtual_folder_exists(lvl1_folder_code, uid))
            self.assertIsNotNone(result)
            self.assertEqual(result.name, response_data.data.media.name)
            self.assertEqual(result.alias, response_data.data.media.alias)
            self.assertEqual(result.description, response_data.data.media.description)
            self.assertEqual(result.is_system_folder, response_data.data.media.is_system_folder)
            self.assertEqual(result.is_store_folder, response_data.data.media.is_store_folder)
            self.assertIsNotNone(result.parent_folder_code)
            self.assertEqual(result.parent_level, 2)
            self.assertEqual(result.parent_level, response_data.data.media.parent_level)
            self.assertEqual(result.code, lvl1_folder_code)
            self.assertEqual(result.parent_folder_code, root_media.code)
            self.assertEqual(root_media.code, response_data.data.root_media.code)

    def test_create_folder_type_store_level_root(self):
        with self.client:
            store = self.create_store(self.store_owner_user, 'shop owner')
            store_code = store.data.info.store_code
            user_object = self.login_user(self.store_owner_user)
            token = user_object['idToken']
            post_data = {
                'name': self.fake.domain_word(),
                'alias': self.fake.domain_word(),
                'description': self.fake.sentence(nb_words=10),
                'is_system_folder': False,
                'is_store_folder': True,
                'entity_code': store_code,
                'parent_level': 1
            }
            response = self.request_post('api/media/folder/create', token, None, None, post_data)
            self.assertRequestPassed(response, 'failed request create folder')
            response_data = Struct(response.json)
            self.assertIsNotNone(response_data)
            self.assertTrue(response_data.status)
            self.assertIsNotNone(response_data.data)
            folder_code = response_data.data.media.code
            result = MediaFolder.query.filter_by(code=folder_code).first()
            self.assertTrue(self.mediaService.virtual_folder_exists(folder_code, store_code))
            self.assertIsNotNone(result)
            self.assertEqual(result.name, response_data.data.media.name)
            self.assertEqual(result.alias, response_data.data.media.alias)
            self.assertEqual(result.description, response_data.data.media.description)
            self.assertEqual(result.is_system_folder, response_data.data.media.is_system_folder)
            self.assertEqual(result.is_store_folder, response_data.data.media.is_store_folder)
            self.assertEqual(result.parent_folder_code, 'None')
            self.assertEqual(result.parent_level, 1)
            self.assertEqual(result.parent_level, response_data.data.media.parent_level)

    def test_create_folder_type_user_level_1(self):
        with self.client:
            store = self.create_store(self.store_owner_user, 'shop owner')
            store_code = store.data.info.store_code
            user_object = self.login_user(self.store_owner_user)
            token = user_object['idToken']
            post_data = {
                'name': self.fake.domain_word(),
                'alias': self.fake.domain_word(),
                'description': self.fake.sentence(nb_words=10),
                'is_system_folder': False,
                'is_store_folder': True,
                'entity_code': store_code,
                'parent_level': 1
            }
            response = self.request_post('api/media/folder/create', token, None, None, post_data)
            self.assertRequestPassed(response, 'failed request create folder root level')
            response_data = Struct(response.json)
            self.assertIsNotNone(response_data)
            self.assertTrue(response_data.status)
            self.assertIsNotNone(response_data.data)
            root_folder_code = response_data.data.media.code
            root_media = MediaFolder.query.filter_by(code=root_folder_code).first()
            self.assertTrue(self.mediaService.virtual_folder_exists(root_folder_code, store_code))
            self.assertIsNotNone(root_media)
            self.assertEqual(root_media.code, response_data.data.media.code)
            self.assertEqual(root_media.name, response_data.data.media.name)
            self.assertEqual(root_media.alias, response_data.data.media.alias)
            self.assertEqual(root_media.description, response_data.data.media.description)
            self.assertEqual(root_media.is_system_folder, response_data.data.media.is_system_folder)
            self.assertEqual(root_media.is_store_folder, response_data.data.media.is_store_folder)
            self.assertEqual(root_media.parent_folder_code, 'None')
            self.assertEqual(root_media.parent_level, 1)
            self.assertEqual(root_media.parent_level, response_data.data.media.parent_level)

            post_data = {
                'name': self.fake.domain_word(),
                'alias': self.fake.domain_word(),
                'description': self.fake.sentence(nb_words=10),
                'is_system_folder': False,
                'is_store_folder': True,
                'entity_code': store_code,
                'parent_level': 2,
                'parent_folder_code': root_folder_code
            }
            response = self.request_post('api/media/folder/create', token, None, None, post_data)
            self.assertRequestPassed(response, 'failed request create folder level 1')
            response_data = Struct(response.json)
            self.assertIsNotNone(response_data)
            self.assertTrue(response_data.status)
            self.assertIsNotNone(response_data.data)
            lvl1_folder_code = response_data.data.media.code
            result = MediaFolder.query.filter_by(code=lvl1_folder_code).first()
            self.assertTrue(self.mediaService.virtual_folder_exists(root_folder_code, store_code))
            self.assertIsNotNone(result)
            self.assertEqual(result.name, response_data.data.media.name)
            self.assertEqual(result.alias, response_data.data.media.alias)
            self.assertEqual(result.description, response_data.data.media.description)
            self.assertEqual(result.is_system_folder, response_data.data.media.is_system_folder)
            self.assertEqual(result.is_store_folder, response_data.data.media.is_store_folder)
            self.assertIsNotNone(result.parent_folder_code)
            self.assertEqual(result.parent_level, 2)
            self.assertEqual(result.parent_level, response_data.data.media.parent_level)
            self.assertEqual(result.code, lvl1_folder_code)
            self.assertEqual(result.parent_folder_code, root_media.code)
            self.assertEqual(root_media.code, response_data.data.root_media.code)

    def test_upload_media_system_file(self):
        with self.client:
            self.settingsService.syncSettings()
            media_folder = self.mediaUtils.create_system_folder()
            user_object = self.login_user(self.platform_owner_user)
            uid = user_object['uid']
            token = user_object['idToken']
            post_data = {
                'folder_code': media_folder.code,
                'alias': self.fake.domain_word(),
                'is_store_file': False,
                'is_system_file': True,
                'files': []
            }
            post_data['files'].append(self.get_file_content('dragon.png')['raw'])
            response = self.request_files_upload('/api/media/None/uploads', token, None, None, post_data)
            self.assertRequestPassed(response, 'failed request upload media file')
            response_data = Struct(response.json)
            self.assertIsNotNone(response_data)
            self.assertTrue(response_data.status)
            self.assertIsNotNone(response_data.data)
            self.assertEqual(len(response_data.data), 1)
            data = response_data.data[0]
            file_code = data.code
            result = MediaFile.query.filter_by(code=file_code).first()
            self.assertTrue(self.mediaService.virtual_file_exists(file_code))
            self.assertIsNotNone(result)
            self.assertEqual(result.file_type, data.file_type)
            self.assertEqual(result.code, data.code)
            self.assertEqual(result.file_size, data.file_size)
            self.assertEqual(result.is_published, data.is_published)
            self.assertEqual(result.is_system_file, data.is_system_file)
            self.assertEqual(result.is_store_file, data.is_store_file)

    def test_upload_media_system_files(self):
        with self.client:
            self.settingsService.syncSettings()
            media_folder = self.mediaUtils.create_system_folder()
            user_object = self.login_user(self.platform_owner_user)
            uid = user_object['uid']
            token = user_object['idToken']
            post_data = {
                'folder_code': media_folder.code,
                'alias': self.fake.domain_word(),
                'is_store_file': False,
                'is_system_file': True,
                'files': []
            }
            post_data['files'].append(self.get_file_content('dragon.png')['raw'])
            post_data['files'].append(self.get_file_content('dragon.jpg')['raw'])
            response = self.request_files_upload('/api/media/None/uploads', token, None, None, post_data)
            self.assertRequestPassed(response, 'failed request upload media file')
            response_data = Struct(response.json)
            self.assertIsNotNone(response_data)
            self.assertTrue(response_data.status)
            self.assertIsNotNone(response_data.data)
            self.assertEqual(len(response_data.data), 2)
            for data in response_data.data:
                file_code = data.code
                result = MediaFile.query.filter_by(code=file_code).first()
                self.assertTrue(self.mediaService.virtual_file_exists(file_code))
                self.assertIsNotNone(result)
                self.assertEqual(result.file_type, data.file_type)
                self.assertEqual(result.code, data.code)
                self.assertEqual(result.file_size, data.file_size)
                self.assertEqual(result.is_published, data.is_published)
                self.assertEqual(result.is_system_file, data.is_system_file)
                self.assertEqual(result.is_store_file, data.is_store_file)

    def test_get_list_system_files_and_folder_no_filters(self):
        with self.client:
            self.settingsService.syncSettings()
        user_object = self.login_user(self.platform_owner_user)
        uid = user_object['uid']
        token = user_object['idToken']
        post_data = {
            'name': self.fake.domain_word(),
            'alias': self.fake.domain_word(),
            'description': self.fake.sentence(nb_words=10),
            'is_system_folder': True,
            'is_store_folder': False,
            'entity_code': str(None),
            'parent_level': 1
        }
        response = self.request_post('api/media/folder/create', token, None, None, post_data)
        self.assertRequestPassed(response, 'failed request create folder root level')
        response_data = Struct(response.json)
        self.assertIsNotNone(response_data)
        self.assertTrue(response_data.status)
        self.assertIsNotNone(response_data.data)
        root_folder_code = response_data.data.media.code
        root_media = MediaFolder.query.filter_by(code=root_folder_code).first()
        self.assertTrue(self.mediaService.virtual_folder_exists(root_folder_code))
        self.assertIsNotNone(root_media)
        self.assertEqual(root_media.code, response_data.data.media.code)
        self.assertEqual(root_media.name, response_data.data.media.name)
        self.assertEqual(root_media.alias, response_data.data.media.alias)
        self.assertEqual(root_media.description, response_data.data.media.description)
        self.assertEqual(root_media.is_system_folder, response_data.data.media.is_system_folder)
        self.assertEqual(root_media.is_store_folder, response_data.data.media.is_store_folder)
        self.assertEqual(root_media.parent_folder_code, 'None')
        self.assertEqual(root_media.parent_level, 1)
        self.assertEqual(root_media.parent_level, response_data.data.media.parent_level)
        post_data = {
            'name': self.fake.domain_word(),
            'alias': self.fake.domain_word(),
            'description': self.fake.sentence(nb_words=10),
            'is_system_folder': True,
            'is_store_folder': False,
            'entity_code': str(None),
            'parent_level': 1
        }
        response = self.request_post('api/media/folder/create', token, None, None, post_data)
        self.assertRequestPassed(response, 'failed request create folder root level')
        root_code = root_media.code
        post_data = {
            'folder_code': root_code,
            'alias': self.fake.domain_word(),
            'is_store_file': False,
            'is_system_file': True,
            'files': []
        }
        post_data['files'].append(self.get_file_content('dragon.png')['raw'])
        post_data['files'].append(self.get_file_content('dragon.jpg')['raw'])
        response = self.request_files_upload('/api/media/None/uploads', token, None, None, post_data)
        self.assertRequestPassed(response, 'failed request upload media file')
        response_data = Struct(response.json)
        self.assertIsNotNone(response_data)
        self.assertTrue(response_data.status)
        self.assertIsNotNone(response_data.data)
        self.assertEqual(len(response_data.data), 2)
        for data in response_data.data:
            file_code = data.code
            result = MediaFile.query.filter_by(code=file_code).first()
            self.assertTrue(self.mediaService.virtual_file_exists(file_code))
            self.assertIsNotNone(result)
            self.assertEqual(result.file_type, data.file_type)
            self.assertEqual(result.code, data.code)
            self.assertEqual(result.file_size, data.file_size)
            self.assertEqual(result.is_published, data.is_published)
            self.assertEqual(result.is_system_file, data.is_system_file)
            self.assertEqual(result.is_store_file, data.is_store_file)
        query_string = {
            'is_system': 1,
            'is_store': 0,
            'entity_code': str(None),
        }
        response = self.request_get('/api/media/list', token, query_string)
        self.assertRequestPassed(response, 'failed request list media items')
        response_data = Struct(response.json)
        self.assertIsNotNone(response_data)
        self.assertTrue(response_data.status)
        self.assertIsNotNone(response_data.data)
        self.assertEqual(len(response_data.data), 2)
        self.assertEqual(response_data.data[0].folder.code, root_code)
        self.assertEqual(len(response_data.data[0].files), 2)

    def test_download_file(self):
        with self.client:
            self.settingsService.syncSettings()
            media_folder = self.mediaUtils.create_system_folder()
            user_object = self.login_user(self.platform_owner_user)
            uid = user_object['uid']
            token = user_object['idToken']
            post_data = {
                'folder_code': media_folder.code,
                'alias': self.fake.domain_word(),
                'is_store_file': False,
                'is_system_file': True,
                'files': []
            }
            post_data['files'].append(self.get_file_content('dragon.png')['raw'])
            response = self.request_files_upload('/api/media/None/uploads', token, None, None, post_data)
            self.assertRequestPassed(response, 'failed request upload media file')
            response_data = Struct(response.json)
            self.assertIsNotNone(response_data)
            self.assertTrue(response_data.status)
            self.assertIsNotNone(response_data.data)
            self.assertEqual(len(response_data.data), 1)
            data = response_data.data[0]
            file_code = data.code
            self.assertTrue(self.mediaService.virtual_file_exists(file_code))
            response = self.request_get(f'/api/media/file/{file_code}', token)
            self.assertRequestPassed(response, 'failed request download media file')
