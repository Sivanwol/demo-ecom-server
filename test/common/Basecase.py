import os

from flask_testing import TestCase

from config.api import app
from config.database import db
from src.services.firebase import FirebaseService
from src.services.user import UserService
from src.utils.enums import RolesTypes
from src.utils.firebase_utils import create_firebase_user, setup_firebase_client


class BaseTestCase(TestCase):
    """A base test case."""
    userService = UserService()
    TESTING = True
    firebase_owner_user = "test+owner@user.com"
    firebase_support_user = "test+support@user.com"
    firebase_account_user = "test+account@user.com"
    firebase_global_password = "password!0101"
    firebase_owner_object = None
    firebase_support_object = None
    firebase_accounts_object = None
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
        self.init_unit_data()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def init_unit_data(self):
        self.setup_owner_user()
        self.setup_account_user()
        self.setup_support_user()

    def setup_owner_user(self):
        self.firebase_owner_object = create_firebase_user(self.firebase_owner_user, self.firebase_global_password)
        self.assertIsNotNone(self.firebase_owner_object)
        if self.firebase_owner_object is not None:
            self.assertNotEqual(self.firebase_owner_object.uid, '')
        self.userService.sync_firebase_user(self.firebase_owner_object.uid, [RolesTypes.Owner])

    def setup_support_user(self):
        self.firebase_support_object = create_firebase_user(self.firebase_support_user, self.firebase_global_password)
        self.assertIsNotNone(self.firebase_support_object)
        if self.firebase_support_object is not None:
            self.assertNotEqual(self.firebase_support_object.uid, '')
        self.userService.sync_firebase_user(self.firebase_support_object.uid, [RolesTypes.Support])

    def setup_account_user(self):
        self.firebase_accounts_object = create_firebase_user(self.firebase_account_user, self.firebase_global_password)
        self.assertIsNotNone(self.firebase_accounts_object)
        if self.firebase_accounts_object is not None:
            self.assertNotEqual(self.firebase_accounts_object.uid, '')
        self.userService.sync_firebase_user(self.firebase_accounts_object.uid, [RolesTypes.Accounts])
