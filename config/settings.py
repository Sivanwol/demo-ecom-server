# -*- coding: utf-8 -*-
import os

# load dotenv in the base root
from flask.cli import load_dotenv

APP_ROOT = os.path.join(os.path.dirname(__file__), '../src', '..')  # refers to application_top
dotenv_path = os.path.join(APP_ROOT, '.env.' + os.environ.get("FLASK_ENV", "development"))
load_dotenv(dotenv_path)


class Config:
    API_ROUTE = "/api{route}"
    # project root directory
    BASE_DIR = os.path.join(os.pardir, os.path.dirname(__file__))
    SECRET_KEY = os.getenv("SECRET_KEY")

    # Flask Configuration
    # --------------------------------------------------------------------
    DEBUG = True
    TESTING = False
    PORT = 8000

    # firebase config
    GOOGLE_APPLICATION_CREDENTIALS = os.getenv('FIREBASE_SERVICE_CONFIG_FILE')
    FIREBASE_CONFIG = os.getenv('FIREBASE_CONFIG_FILE')
    FIREBASE_APIKEY = os.getenv('FIREBASE_APIKEY')
    FIREBASE_OWNER_ACCOUNT_UID = os.getenv('FIREBASE_OWNER_ACCOUNT_UID')
    # log file path
    # --------------------------------------------------------------------
    enable_access_log = True
    log_socket_host = "127.0.0.1"
    log_socket_port = 514

    # redis config
    # --------------------------------------------------------------------
    REDIS_URL = os.getenv('REDIS_URL')  # docker network
    REDIS_PASSWD = os.getenv('REDIS_PASSWD')
    CACHE_KEY_PREFIX = os.getenv('CACHE_KEY_PREFIX')

    # elasticsearch config
    # --------------------------------------------------------------------
    ELASTICSEARCH_URL= os.getenv('ELASTICSEARCH_URL')

    # sqlalchemy database config
    # --------------------------------------------------------------------
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    # SQLALCHEMY_ENGINE_OPTIONS = {
    #     'executemany_mode': 'batch',
    #     'client_encoding': 'utf8',
    #     'case_sensitive': False,
    #     'echo': True,
    #     'echo_pool': True
    # }

    # SMTP server config
    # --------------------------------------------------------------------
    # SERVER_EMAIL = 'Sivan Wolberg <sivan.wolberg@wolberg.pro>'
    # DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', SERVER_EMAIL)
    # EMAIL_HOST = os.environ.get('EMAIL_HOST')
    # EMAIL_PORT = os.environ.get('EMAIL_PORT')
    # EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
    # EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')


class DevelopmentConfig(Config):
    ENV = os.environ.get("FLASK_ENV", "development")
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://localhost:5432/postgres')
    DEBUG = True
    ASSETS_DEBUG = True


class TestingConfig(Config):
    ENV = os.environ.get("FLASK_ENV", "testing")
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    DEBUG = True
    TESTING = True


class ProductionConfig(Config):
    ENV = os.environ.get("FLASK_ENV", "production")
    DEBUG = False
    USE_RELOADER = False


settings = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig,
}
