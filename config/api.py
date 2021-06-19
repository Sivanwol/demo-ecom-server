import logging
import os

import sentry_sdk
from celery import Celery
from flask import Flask
from flask_caching import Cache
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_socketio import SocketIO
from sentry_sdk.integrations.flask import FlaskIntegration
from config import settings
from config.database import db, migration
from src.services.firebase import FirebaseService


def load_application():
    if settings[os.environ.get("FLASK_ENV", "development")].SENTRY_ENABLE:
        sentry_sdk.init(
            dsn=settings[os.environ.get("FLASK_ENV", "development")].SENTRY_URI,
            integrations=[FlaskIntegration()],

            # Set traces_sample_rate to 1.0 to capture 100%
            # of transactions for performance monitoring.
            # We recommend adjusting this value in production.
            traces_sample_rate=1.0
        )
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

redis_url = "redis://{password}@{hostname}:{port}/{db}".format(
    password=settings[os.environ.get("FLASK_ENV", "development")].REDIS_PASSWORD,
    hostname=settings[os.environ.get("FLASK_ENV", "development")].REDIS_HOST,
    port=settings[os.environ.get("FLASK_ENV", "development")].REDIS_PORT,
    db=settings[os.environ.get("FLASK_ENV", "development")].REDIS_DB,
)
APP_DEBUG_MODE = False
if os.environ.get("FLASK_ENV", "development") == 'development' or os.environ.get("FLASK_ENV", "development") == 'testing':
    APP_DEBUG_MODE = True
# on level of testing we dont need redis also need disable the caching system
if os.environ.get("FLASK_ENV", "development") == 'testing':
    cache = Cache(app, config={
        'CACHE_TYPE': 'NullCache'
    })
    celery = Celery(__name__)
else:
    cache = Cache(app, config={
        'CACHE_TYPE': 'RedisCache',
        'CACHE_KEY_PREFIX': settings[os.environ.get("FLASK_ENV", "development")].CACHE_KEY_PREFIX,
        'CACHE_REDIS_HOST': settings[os.environ.get("FLASK_ENV", "development")].REDIS_HOST,
        'CACHE_REDIS_PORT': settings[os.environ.get("FLASK_ENV", "development")].REDIS_PORT,
        'CACHE_REDIS_DB': settings[os.environ.get("FLASK_ENV", "development")].REDIS_DB,
        'CACHE_REDIS_PASSWORD': settings[os.environ.get("FLASK_ENV", "development")].REDIS_PASSWORD
    })
    celery = Celery(__name__, backend=redis_url, broker=redis_url)
cache.init_app(app)
socketio = SocketIO(app, logger=True, debug=APP_DEBUG_MODE, host="0.0.0.0", engineio_logger=APP_DEBUG_MODE)
