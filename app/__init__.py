import logging
import os
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_rebar import Rebar

from app import main
from app.main.api import api
from app.main.database import db, migration
from app.main.logging import LOGGING_CONFIG


# Flask App Initialization
from app.services.firebase import FirebaseService

app = Flask(__name__)
app.config.from_object(main.settings[os.environ.get("FLASK_ENV", "development")])

cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
# Logs Initialization
console = logging.getLogger('console')
print("System Config", main.settings[os.environ.get("FLASK_ENV", "development")])
# firebase loading
firebase = FirebaseService()
firebase.load_firebase()
jwt = JWTManager(app)


rebar = Rebar()
# All handler URL rules will be prefixed by '/v1'
registry = rebar.create_handler_registry(prefix=main.settings[os.environ.get("FLASK_ENV", "development")].API_PERFIX)
# Database ORM Initialization
from app import models
db.init_app(app)

# Database Migrations Initialization
migration.init_app(app, db)

# Flask API Initialization
api.init_app(app)
