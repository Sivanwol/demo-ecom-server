import logging
import os
from flask import Flask
from flask_jwt_extended import JWTManager

from app import main
from app.main.api import api
from app.main.database import db, migration
from app.main.logging import LOGGING_CONFIG
from flask.logging import default_handler


# Flask App Initialization
from app.services.firebase import FirebaseService

app = Flask(__name__)
app.config.from_object(main.settings[os.environ.get("FLASK_ENV", "development")])

# Logs Initialization
console = logging.getLogger('console')
print("System Config", main.settings[os.environ.get("FLASK_ENV", "development")])
# firebase loading
firebase = FirebaseService()
firebase.load_firebase()
jwt = JWTManager(app)
# Database ORM Initialization
from app import models
db.init_app(app)

# Database Migrations Initialization
migration.init_app(app, db)

# Flask API Initialization
api.init_app(app)
