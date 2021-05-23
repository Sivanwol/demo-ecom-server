import os

from flask_testing import TestCase

from config.api import app
from config.database import db
from src.services.firebase import FirebaseService
from src.utils.firebase_utils import create_firebase_user, setup_firebase_client


class BaseTestCase(TestCase):
    """A base test case."""
    TESTING = True
    firebase_user = "test@user.com"
    firebase_password = "password!0101"
    firebase_UID = None
    firebase_client_object = None
    firebaseService = FirebaseService()

    def create_app(self):
        # app.config.from_object('config.TestConfig')
        print(os.environ.get("FLASK_ENV", "development"))
        self.firebase_UID = create_firebase_user(self.firebase_user, self.firebase_password)
        self.assertIsNotNone(self.firebase_UID)
        if self.firebase_UID is not None:
            self.assertNotEqual(self.firebase_UID.uid, '')
        self.firebase_client_object = setup_firebase_client()
        app.app_context().push()
        return app

    def setUp(self):
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        db.create_all()
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
