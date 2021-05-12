from flask import request
from validator import validate
import logging
import os
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_rebar import Rebar

from config import settings
# from config.api import api
from src.services.firebase import FirebaseService
from src.utils.responses import response_error
from config.database import db, migration


def verify_uid(uid):
    rules = {"uid": "require|min:10"}
    result = validate({uid: uid}, rules)
    if result:
        return True
    else:
        return False


def verify_response():
    if not request.is_json:
        return response_error({"msg": "Missing JSON in request"}, None, 400)


def scan_routes(app):
    # links = []
    for rule in app.url_map.iter_rules():
        print("{url} - {method}".format(url=rule.rule, method=rule.methods))


def create_app(name):
    app = Flask(name)
    app.config.from_object(settings[os.environ.get("FLASK_ENV", "development")])

    rebar = Rebar()
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
    # Logs Initialization
    console = logging.getLogger('console')
    print("System Config", settings[os.environ.get("FLASK_ENV", "development")])
    # firebase loading
    firebase = FirebaseService()
    firebase.load_firebase()
    jwt = JWTManager(app)

    # Database ORM Initialization

    db.init_app(app)

    # Database Migrations Initialization
    migration.init_app(app, db)

    # Flask API Initialization
    rebar.init_app(app)
    # api.init_app(app)
    return app
