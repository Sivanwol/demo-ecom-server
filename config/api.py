import logging
import os

from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from config import settings
from config.database import db, migration
from src.services.firebase import FirebaseService
# from src.utils.json_encoder import AlchemyEncoder


def load_application():
    app = Flask(__name__)
    app.config.from_object(settings[os.environ.get("FLASK_ENV", "development")])
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
    print("System Config", settings[os.environ.get("FLASK_ENV", "development")])

    firebase = FirebaseService()
    firebase.load_firebase()
    jwt = JWTManager(app)
    # Database ORM Initialization
    db.init_app(app)

    # Database Migrations Initialization
    migration.init_app(app, db)
    app.logger = logging.getLogger('console')
    return app


app = load_application()
