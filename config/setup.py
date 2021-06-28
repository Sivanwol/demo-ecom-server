import os

import sentry_sdk
from celery import Celery
from fakeredis import FakeStrictRedis
from flask import Flask
from flask_caching import Cache
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from redis import Redis
from sentry_sdk.integrations.flask import FlaskIntegration
from config import settings
from config.database import db, migration
from config.logs import logging
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

redis_url = "redis://{password}@{host}:{port}/{db}".format(
    password=app.config['REDIS_PASSWORD'],
    host=app.config['REDIS_HOST'],
    port=app.config['REDIS_PORT'],
    db=app.config['REDIS_DB']
)
# on level of testing we dont need redis also need disable the caching system
if os.environ.get("FLASK_ENV", "development") == 'testing':
    cache = Cache(app, config={
        'CACHE_TYPE': 'NullCache'
    })
    celery = Celery(__name__)
    redis_connection = FakeStrictRedis()
else:
    redis_connection = Redis(
        password=app.config['REDIS_PASSWORD'],
        host=app.config['REDIS_HOST'],
        port=app.config['REDIS_PORT'],
        db=app.config['REDIS_DB']
    )
    cache = Cache(app, config={
        'CACHE_TYPE': 'RedisCache',
        'CACHE_KEY_PREFIX': app.config['CACHE_KEY_PREFIX'],
        'CACHE_REDIS_HOST': app.config['REDIS_HOST'],
        'CACHE_REDIS_PORT': app.config['REDIS_PORT'],
        'CACHE_REDIS_DB': app.config['REDIS_CACHE_DB'],
        'CACHE_REDIS_PASSWORD': app.config['REDIS_PASSWORD']
    })
    celery = Celery(__name__, backend=redis_url, broker=redis_url)
cache.init_app(app)
