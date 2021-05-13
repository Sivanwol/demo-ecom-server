from urllib.parse import urlparse
from flask import request, url_for
from validator import validate
import logging
import os
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import settings
from src.services.firebase import FirebaseService
from src.utils.responses import response_error
from config.database import db, migration


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
    return app
