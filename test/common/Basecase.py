import json
import os
from random import randint

from faker import Faker
from firebase_admin import auth
from flask_testing import TestCase

from config.api import app
from config.database import db
from src.services.firebase import FirebaseService
from src.services.roles import RolesService
from src.services.store import StoreService
from src.services.user import UserService
from src.utils.enums import RolesTypes
from src.utils.firebase_utils import create_firebase_user as create_fb_user, setup_firebase_client, login_user
from src.utils.general import is_json_key_present, Struct


class BaseTestCase(TestCase):
    """A base test case."""

    fake = Faker()
    userService = UserService()
    roleService = RolesService()
    storeService = StoreService()
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

    def create_app(self):
        # app.config.from_object('config.TestConfig')
        print(os.environ.get("FLASK_ENV", "development"))
        self.firebase_client_object = setup_firebase_client()
        app.app_context().push()
        return app

    def testSetUp(self):
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        db.create_all()
        db.session.commit()
        self.roleService.insert_roles()
        print(self.roleService.get_all_roles())
        self.init_unit_data()
        Faker.seed(randint(0, 100))

    def testTearDown(self):
        db.session.remove()
        db.drop_all()

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
        self.userService.sync_firebase_user(self.platform_support_object.uid, roles, self.platform_support_user, 'platform support', True)

    def setup_account_user(self):
        self.platform_accounts_object = create_fb_user(self.platform_account_user, self.global_password)
        self.assertIsNotNone(self.platform_accounts_object)
        if self.platform_accounts_object is not None:
            self.assertNotEqual(self.platform_accounts_object.uid, '')
        roles = self.roleService.get_roles([RolesTypes.Accounts.value])
        self.userService.sync_firebase_user(self.platform_accounts_object.uid, roles, self.platform_account_user, 'platform account', True)

    def create_user(self, email, roles, initial_state=False, store_code=None):
        user = create_fb_user(email, self.global_password)
        self.assertIsNotNone(user)
        if user is not None:
            auth.delete_user(user.uid)  # we need make sure this user will be delete no point keep at as there a lot of tests
            user = create_fb_user(email, self.global_password)
        roles = self.roleService.get_roles(roles)
        self.userService.sync_firebase_user(user.uid, roles, email, self.fake.name(), initial_state, store_code)

    def create_firebase_store_user(self, email):
        user = create_fb_user(email, self.global_password)
        if user is not None:
            auth.delete_user(user.uid)  # we need make sure this user will be delete no point keep at as there a lot of tests
            user = create_fb_user(email, self.global_password)

        self.assertIsNotNone(user)
        return user

    def create_store(self, email):
        self.create_user(email, [RolesTypes.StoreOwner.value], True)
        user_object = self.login_user(email)
        uid = user_object['uid']
        user_object = self.login_user(self.platform_owner_user)
        owner_token = user_object['idToken']

        user = self.userService.get_user(uid, True)
        self.assertIsNone(user.store_code)
        store_name = self.fake.company()
        currency_code = self.fake.currency_code()
        post_data = {
            'name': store_name,
            'description': 'store description',
            'currency_code': currency_code
        }
        response = self.request_post('/api/store/%s/create' % uid, owner_token, None, post_data)
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

    def request_get(self, url, token, extra_headers=None):
        if extra_headers is None:
            extra_headers = {}
        headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer %s' % token} | extra_headers
        print('request get -> %s' % url)
        print('request headers -> %s' % json.dumps(headers))
        return self.client.get(
            url,
            headers=headers
        )

    def request_put(self, url, token, extra_headers=None, data=None):
        if data is None:
            data = {}
        if extra_headers is None:
            extra_headers = {}
        headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer %s' % token} | extra_headers
        print('request put -> %s' % url)
        print('request headers -> %s' % json.dumps(headers))
        print('request put data-> %s' % json.dumps(data))
        return self.client.put(
            url,
            data=json.dumps(data),
            headers=headers
        )

    def request_post(self, url, token, extra_headers=None, data=None):
        if extra_headers is None:
            extra_headers = {}
        if data is None:
            data = {}
        headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer %s' % token} | extra_headers
        print('request post -> %s' % url)
        print('request headers -> %s' % json.dumps(headers))
        print('request post data-> %s' % json.dumps(data))
        return self.client.post(
            url,
            data=json.dumps(data),
            headers=headers
        )

    def request_delete(self, url, token, extra_headers=None):
        if extra_headers is None:
            extra_headers = {}
        headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer %s' % token} | extra_headers
        print('request delete -> %s' % url)
        print('request headers -> %s' % json.dumps(headers))
        return self.client.delete(
            url,
            headers=headers
        )

    def assertRequestPassed(self, response, message):
        print('response headers -> %s' % response.data)
        self.assert200(response, message)
