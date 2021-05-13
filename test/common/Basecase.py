import os

from flask_testing import TestCase

from config.api import app
from config.database import db
import config.routes
from src.utils.common_methods import scan_routes


class BaseTestCase(TestCase):
    """A base test case."""
    TESTING = True

    def create_app(self):
        # app.config.from_object('config.TestConfig')
        print(os.environ.get("FLASK_ENV", "development"))
        scan_routes(app)
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
