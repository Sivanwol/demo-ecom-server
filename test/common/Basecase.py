import json
import os
import shutil
from random import randint
from tempfile import mkstemp

from faker import Faker
from firebase_admin import auth
from flask_testing import TestCase
from config import settings
from config.app import app, containers
from config.database import db
from src.services import FileSystemService, FirebaseService, MediaService, RoleService, StoreService, UserService, SettingsService
from src.utils.enums import RolesTypes
from src.utils.firebase_utils import create_firebase_user as create_fb_user, setup_firebase_client, login_user
from src.utils.general import is_json_key_present, Struct
from test.utils import UserTestUtills, MediaTestUtills


class BaseTestCase(TestCase):
    """A base test case."""

    fake = Faker()
    TESTING = True
    platform_owner_user = "test+owner@user.com"
    platform_support_user = "test+support@user.com"
    platform_account_user = "test+account@user.com"
    platform_owner_object = None
    platform_support_object = None
    platform_accounts_object = None
    global_password = "password!0101"
    firebase_client_object = None
    firebaseService = FirebaseService()
    userService = containers[UserService]
    roleService = containers[RoleService]
    storeService = containers[StoreService]
    fileSystemService = containers[FileSystemService]
    mediaService = containers[MediaService]
    settingsService = containers[SettingsService]

    config = settings[os.environ.get("FLASK_ENV", "development")]

    def create_app(self):
        # app.config.from_object('config.TestConfig')
        print(os.environ.get("FLASK_ENV", "development"))
        print(settings[os.environ.get("FLASK_ENV", "development")].SQLALCHEMY_DATABASE_URI)
        self.firebase_client_object = setup_firebase_client()
        app.flask_app.app_context().push()

        return app.flask_app

    def setUp(self):
        self.fd, temp_path = mkstemp()
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        self.userUtils = UserTestUtills(self)
        self.mediaUtils = MediaTestUtills(self)
        db.create_all()
        db.session.commit()
        self.roleService.insert_roles()
        print(self.roleService.get_all_roles())
        self.init_unit_data()
        self.settingsService.init_system_settings()
        Faker.seed(randint(0, 100))

    def clear_uploads_folders(self):
        # let clear system folders
        upload_system_path = os.path.join(settings[os.environ.get("FLASK_ENV", "development")].UPLOAD_FOLDER,
                                          settings[os.environ.get("FLASK_ENV", "development")].UPLOAD_SYSTEM_FOLDER)
        folders = self.fileSystemService.get_folder_list(upload_system_path)
        for folder in folders:
            self.fileSystemService.remove_folder(folder)

        # let clear users folders
        upload_system_path = os.path.join(settings[os.environ.get("FLASK_ENV", "development")].UPLOAD_FOLDER,
                                          settings[os.environ.get("FLASK_ENV", "development")].UPLOAD_USERS_FOLDER)
        folders = self.fileSystemService.get_folder_list(upload_system_path)
        for folder in folders:
            self.fileSystemService.remove_folder(folder)

        # let clear stores folders
        upload_system_path = os.path.join(settings[os.environ.get("FLASK_ENV", "development")].UPLOAD_FOLDER,
                                          settings[os.environ.get("FLASK_ENV", "development")].UPLOAD_STORES_FOLDER)
        folders = self.fileSystemService.get_folder_list(upload_system_path)
        for folder in folders:
            self.fileSystemService.remove_folder(folder)

        # let clear temp folder
        upload_temp_path = os.path.join(settings[os.environ.get("FLASK_ENV", "development")].UPLOAD_FOLDER,
                                        settings[os.environ.get("FLASK_ENV", "development")].UPLOAD_TEMP_FOLDER)
        for filename in os.listdir(upload_temp_path):
            file_path = os.path.join(upload_temp_path, filename)
            if file_path != os.path.join(upload_temp_path, '.gitkeep'):
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                    print('Failed to delete %s. Reason: %s' % (file_path, e))

    def ws_renew_connection(self, namespace=None):
        self.ws_client.connect(namespace=namespace)

    def tearDown(self):
        self.fd, temp_path = mkstemp()
        db.session.remove()
        db.drop_all()
        if settings[os.environ.get("FLASK_ENV", "development")].CLEAR_FOLDER_UPLOAD:
            self.clear_uploads_folders()
        os.close(self.fd)

    def login_user(self, email):
        user = login_user(email, self.global_password)
        self.assertFalse(is_json_key_present(user, 'error'))
        token = user['idToken']
        self.assertIsNotNone(token)
        self.assertNotEqual(token, '')
        return {
            'idToken': token,
            'uid': user['localId'],
            'display_name': user['displayName']
        }

    def login_failed_user(self, email):
        user = login_user(email, self.global_password)
        self.assertTrue(is_json_key_present(user, 'error'))
        self.assertFalse(is_json_key_present(user, 'idToken'))

    def init_unit_data(self):
        self.setup_owner_user()
        self.setup_account_user()
        self.setup_support_user()

    def setup_owner_user(self):
        self.platform_owner_object = create_fb_user(self.platform_owner_user, self.global_password)
        self.assertIsNotNone(self.platform_owner_object)
        if self.platform_owner_object is not None:
            self.assertNotEqual(self.platform_owner_object.uid, '')
        roles = self.roleService.get_roles([RolesTypes.Owner.value])
        self.userService.sync_firebase_user(self.platform_owner_object.uid, roles, self.platform_owner_user, 'platform owner', True)

    def setup_support_user(self):
        self.platform_support_object = create_fb_user(self.platform_support_user, self.global_password)
        self.assertIsNotNone(self.platform_support_object)
        if self.platform_support_object is not None:
            self.assertNotEqual(self.platform_support_object.uid, '')
        roles = self.roleService.get_roles([RolesTypes.Support.value])
        self.userService.sync_firebase_user(self.platform_support_object.uid, roles, self.platform_support_user, 'platform support',
                                            True)

    def setup_account_user(self):
        self.platform_accounts_object = create_fb_user(self.platform_account_user, self.global_password)
        self.assertIsNotNone(self.platform_accounts_object)
        if self.platform_accounts_object is not None:
            self.assertNotEqual(self.platform_accounts_object.uid, '')
        roles = self.roleService.get_roles([RolesTypes.Accounts.value])
        self.userService.sync_firebase_user(self.platform_accounts_object.uid, roles, self.platform_account_user, 'platform account',
                                            True)

    def create_user(self, email, name, roles, initial_state=False, store_code=None, user_data=None, is_active=True):
        user = create_fb_user(email, self.global_password)
        self.assertIsNotNone(user)
        if user is not None:
            auth.delete_user(user.uid)  # we need make sure this user will be delete no point keep at as there a lot of tests
            user = create_fb_user(email, self.global_password)
        roles = self.roleService.get_roles(roles)
        self.userService.sync_firebase_user(user.uid, roles, email, name, initial_state, store_code)
        if user_data is not None:
            self.userService.update_user_info(user.uid, user_data)
        if not is_active:
            self.userService.toggle_freeze_user(user.uid)

    def create_firebase_store_user(self, email):
        user = create_fb_user(email, self.global_password)
        if user is not None:
            auth.delete_user(user.uid)  # we need make sure this user will be delete no point keep at as there a lot of tests
            user = create_fb_user(email, self.global_password)

        self.assertIsNotNone(user)
        return user

    def create_store(self, email, name):
        self.create_user(email, name, [RolesTypes.StoreOwner.value], True)
        user_object = self.login_user(email)
        uid = user_object['uid']
        user_object = self.login_user(self.platform_owner_user)
        owner_token = user_object['idToken']

        user = self.userService.get_user(uid, True)
        self.assertIsNone(user.store_code)
        store_name = self.fake.company()
        currency_code = 'USD'
        post_data = {
            'name': store_name,
            'description': 'store description',
            'currency_code': currency_code
        }
        response = self.request_post('/api/store/%s/create' % uid, owner_token, None, None, post_data)
        self.assert200(response, 'create store request failed')
        user = self.userService.get_user(uid, True)
        response_data = Struct(response.json)
        self.assertIsNotNone(response_data)
        self.assertTrue(response_data.status)
        self.assertIsNotNone(response_data.data)
        self.assertIsNotNone(response_data.data.info)
        self.assertIsNotNone(response_data.data.info)
        self.assertNotEqual(response_data.data.info.store_code, '')
        self.assertEqual(response_data.data.info.store_code, user.store_code)
        return response_data

    def request_get(self, url, token, query_string=None, extra_headers=None):
        if extra_headers is None:
            extra_headers = {}
        if query_string is None:
            query_string = {}
        headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer %s' % token} | extra_headers
        print('request get -> %s' % url)
        print('request query string -> %s' % json.dumps(query_string))
        print('request headers -> %s' % json.dumps(headers))
        return self.client.get(
            url,
            query_string=query_string,
            headers=headers
        )

    def request_put(self, url, token, query_string=None, extra_headers=None, data=None):
        if data is None:
            data = {}
        if extra_headers is None:
            extra_headers = {}
        if query_string is None:
            query_string = {}
        headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer %s' % token} | extra_headers
        print('request put -> %s' % url)
        print('request query string -> %s' % json.dumps(query_string))
        print('request headers -> %s' % json.dumps(headers))
        print('request put data-> %s' % json.dumps(data))
        return self.client.put(
            url,
            query_string=query_string,
            data=json.dumps(data),
            headers=headers
        )

    def request_post(self, url, token, query_string=None, extra_headers=None, data=None):
        if extra_headers is None:
            extra_headers = {}
        if data is None:
            data = {}
        if query_string is None:
            query_string = {}
        headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer %s' % token} | extra_headers
        print('request post -> %s' % url)
        print('request query string -> %s' % json.dumps(query_string))
        print('request headers -> %s' % json.dumps(headers))
        print('request post data-> %s' % json.dumps(data))
        return self.client.post(
            url,
            data=json.dumps(data),
            query_string=query_string,
            headers=headers
        )

    def request_delete(self, url, token, query_string=None, extra_headers=None):
        if extra_headers is None:
            extra_headers = {}
        if query_string is None:
            query_string = {}
        headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer %s' % token} | extra_headers
        print('request delete -> %s' % url)
        print('request query string -> %s' % json.dumps(query_string))
        print('request headers -> %s' % json.dumps(headers))
        return self.client.delete(
            url,
            query_string=query_string,
            headers=headers
        )

    def request_files_upload(self, url, token, query_string=None, extra_headers=None, data=None):
        if extra_headers is None:
            extra_headers = {}
        if data is None:
            data = {}
        if query_string is None:
            query_string = {}
        headers = {'Content-Type': 'multipart/form-data', 'Authorization': 'Bearer %s' % token} | extra_headers
        print('request post -> %s' % url)
        print('request query string -> %s' % json.dumps(query_string))
        print('request headers -> %s' % json.dumps(headers))
        return self.client.post(
            url,
            data=data,
            query_string=query_string,
            headers=headers
        )

    def get_file_content(self, file_name, allow_open=True):
        file = os.path.join(self.config.TESTING_ASSETS_FOLDER, file_name)
        return {
            'raw': (open(file, 'rb'), file) if allow_open else None,
            'path': os.path.join(self.config.TESTING_ASSETS_FOLDER, file_name)
        }

    def assertRequestPassed(self, response, message):
        print('response data -> %s' % response.data)
        self.assert200(response, message)
