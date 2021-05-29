import json
import os
import firebase_admin
import requests

from config import settings
from test.common.firebase_emulator_url import FB_SIGNIN_EMAIL


def setup_firebase_client():
    with open(settings[os.environ.get("FLASK_ENV", "development")].FIREBASE_CONFIG) as f:
        firebase_config = json.load(f)


def check_user(email):
    try:
        user = firebase_admin.auth.get_user_by_email(email)
        return user
    except Exception as e:
        print(e)
        return None


def create_firebase_user(email, password):
    user = check_user(email)
    if user is None:
        try:
            user = firebase_admin.auth.create_user(email=email, password=password, email_verified=True,
                                                   display_name="test user %s" % email)
        except Exception as e:
            print(e)
            return None
    return user


def make_request(url, method, data=None, idToken=None):
    headers = {}
    if idToken is not None:
        headers = {'Authorization': idToken}

    res = requests.request(method, url, json=data, headers=headers)
    print('sending request -> {url} , {method}  {status}'.format(url=url, method=method, status=res.status_code))
    return res.json()


def login_user(email, password):
    print("login user %s" % email)
    data = make_request(FB_SIGNIN_EMAIL % settings[os.environ.get("FLASK_ENV", "development")].FIREBASE_APIKEY, 'post',
                        {
                            'email': email,
                            'password': password
                        })
    return data

