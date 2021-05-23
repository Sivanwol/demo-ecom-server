from urllib.parse import urlparse
from flask import request, url_for
from validator import validate
import os
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import settings
from src.exceptions.unable_create_owner_user import CommandUnableCreateOwnerUser
from src.services.firebase import FirebaseService
from src.services.roels import RolesService
from src.services.user import UserService
from src.utils.firebase_utils import check_user, create_firebase_user
from src.utils.responses import response_error
from config.database import db, migration

roleSerivce = RolesService()
userService = UserService()

def verify_uid(uid):
    rules = {"uid": "required|min:10"}
    result = validate({"uid": uid}, rules)  # True
    if result:
        return True
    else:
        return False


def verify_response():
    if not request.is_json:
        return response_error({"msg": "Missing JSON in request"}, None, 400)


def setup_owner_user(email, password):
    user = check_user(email)

    if user is None:
        print("Firebase user creation")
        user = create_firebase_user(email, password)
    if user is None:
        raise CommandUnableCreateOwnerUser(email)

    user_data = user.__dict__['_data']
    print('owner user {} => {}, {}'.format(email, password, user_data))
    uid = user_data['localId']
    roles = roleSerivce.get_roles(['owner'])
    userService.sync_user(uid, roles)
    print('owner user create {} => {}'.format(email, uid))


def scan_routes(app):
    output = []
    for rule in app.url_map.iter_rules():

        options = {}
        for arg in rule.arguments:
            options[arg] = "[{0}]".format(arg)

        methods = ','.join(rule.methods)
        url = url_for(rule.endpoint, **options)
        line = urlparse("{:50s} {:20s} {}".format(rule.endpoint, methods, url))
        output.append(line)

    for line in sorted(output):
        print(line)


def create_app(name):
    app = Flask(name)
    app.config.from_object(settings[os.environ.get("FLASK_ENV", "development")])
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
    print("System Config", settings[os.environ.get("FLASK_ENV", "development")])
    # firebase loading
    firebase = FirebaseService()
    firebase.load_firebase()
    jwt = JWTManager(app)

    # Database ORM Initialization

    db.init_app(app)

    # Database Migrations Initialization
    migration.init_app(app, db)
    return app
