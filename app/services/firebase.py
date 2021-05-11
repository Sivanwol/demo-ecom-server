import os

import firebase_admin
from firebase_admin import credentials
from app.utils.singleton import  singleton
from app import main


@singleton
class FirebaseService:
    def load_firebase(self):
        cred = credentials.Certificate(main.settings[os.environ.get("FLASK_ENV", "development")].GOOGLE_APPLICATION_CREDENTIALS)
        firebase_admin.initialize_app(cred)
        pass
