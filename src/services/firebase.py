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
            cert_file = config.settings[os.environ.get("FLASK_ENV", "development")].GOOGLE_APPLICATION_CREDENTIALS
            print("loading firebase file => %s" % cert_file)
            print("debug: show config")
            with open(cert_file, 'r') as f:
                print(f.read())
            cred = credentials.Certificate(cert_file)
            firebase_admin.initialize_app(cred)
            loaded_firebase = True
