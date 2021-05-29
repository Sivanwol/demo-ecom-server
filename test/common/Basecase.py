import json
import os

from faker import Faker
from flask_testing import TestCase

from config.api import app
from config.database import db
from src.services.firebase import FirebaseService
from src.services.roles import RolesService
from src.services.store import StoreService
from src.services.user import UserService
from src.utils.common_methods import is_json_key_present
from src.utils.enums import RolesTypes
from src.utils.firebase_utils import create_firebase_user as create_fb_user, setup_firebase_client, login_user


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

    def setUp(self):
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        db.create_all()
        db.session.commit()
        self.roleService.insert_roles()
        print(self.roleService.get_all_roles())
        self.init_unit_data()
        Faker.seed(0)

    def tearDown(self):
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
        self.userService.sync_firebase_user(self.platform_owner_object.uid, roles, True)

    def setup_support_user(self):
        self.platform_support_object = create_fb_user(self.platform_support_user, self.global_password)
        self.assertIsNotNone(self.platform_support_object)
        if self.platform_support_object is not None:
            self.assertNotEqual(self.platform_support_object.uid, '')
        roles = self.roleService.get_roles([RolesTypes.Support.value])
        self.userService.sync_firebase_user(self.platform_owner_object.uid, roles, True)

    def setup_account_user(self):
        self.platform_accounts_object = create_fb_user(self.platform_account_user, self.global_password)
        self.assertIsNotNone(self.platform_accounts_object)
        if self.platform_accounts_object is not None:
            self.assertNotEqual(self.platform_accounts_object.uid, '')
        roles = self.roleService.get_roles([RolesTypes.Accounts.value])
        self.userService.sync_firebase_user(self.platform_owner_object.uid, roles, True)

    def create_store_user(self,email, roles, inital_state=False, store_code=None):
        user = create_fb_user(email, self.global_password)
        self.assertIsNotNone(user)
        if user is not None:
            self.assertNotEqual(user.uid, '')
        roles = self.roleService.get_roles(roles)
        if inital_state:
            store_code = None
        self.userService.sync_firebase_user(user.uid, roles, inital_state, store_code)

    def request_get(self, url, token):
        headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer %s' % token}
        print('request get -> %s' % url)
        print('request headers -> %s' % json.dumps(headers))
        return self.client.get(
            url,
            headers=headers
        )

    def request_put(self, url, token, data={}):
        headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer %s' % token}
        print('request put -> %s' % url)
        print('request headers -> %s' % json.dumps(headers))
        print('request put data-> %s' % json.dumps(data))
        return self.client.put(
            url,
            data=json.dumps(data),
            headers=headers
        )

    def request_post(self, url, token, data={}):
        headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer %s' % token}
        print('request post -> %s' % url)
        print('request headers -> %s' % json.dumps(headers))
        print('request post data-> %s' % json.dumps(data))
        return self.client.post(
            url,
            data=json.dumps(data),
            headers=headers
        )

    def request_delete(self, url, token):
        headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer %s' % token}
        print('request delete -> %s' % url)
        print('request headers -> %s' % json.dumps(headers))
        return self.client.delete(
            url,
            headers=headers
        )