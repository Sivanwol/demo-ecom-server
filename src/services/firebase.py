import os

import firebase_admin
from firebase_admin import credentials,auth
from src.utils.singleton import  singleton
import config

loaded_firebase = False

@singleton
class FirebaseService:
    def load_firebase(self):
        global loaded_firebase
        if not loaded_firebase: # prevent reload and reask init app of firebase
            cred = credentials.Certificate(
                config.settings[os.environ.get("FLASK_ENV", "development")].GOOGLE_APPLICATION_CREDENTIALS)
            firebase_admin.initialize_app(cred)
            loaded_firebase = True
