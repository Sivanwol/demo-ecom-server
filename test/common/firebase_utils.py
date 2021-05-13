import json
import os

from firebase import firebase
from firebase_admin import auth
from pyrebase import pyrebase

from config import settings


def setup_firebase_client():
    with open(settings[os.environ.get("FLASK_ENV", "development")].FIREBASE_CONFIG) as f:
        firebase_config = json.load(f)
        return pyrebase.initialize_app(firebase_config)


def check_user(email):
    try:
        user = auth.get_user_by_email(email)
        return user
    except Exception as e:
        print(e)
        return None


def create_test_user(email, password):
    user = check_user(email)
    if user is None:
        try:
            user = auth.create_user(email=email, password=password, email_verified=True, display_name="test user")
        except Exception as e:
            print(e)
            return None
    return user


def login_user(firebase_object, email, password):
    auth = firebase_object.auth()
    return auth.sign_in_with_email_and_password(email, password)
