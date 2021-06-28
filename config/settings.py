# -*- coding: utf-8 -*-
import os

# load dotenv in the base root
from flask.cli import load_dotenv

APP_ROOT = os.path.join(os.path.dirname(__file__), '../src', '..')  # refers to application_top
dotenv_path = os.path.join(APP_ROOT, '.env.' + os.environ.get("FLASK_ENV", "development"))
print("Dot Env File %s" % dotenv_path)
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
    SENTRY_ENABLE = os.getenv('SENTRY_ENABLE')
    SENTRY_URI = os.getenv('SENTRY_URI')
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
    REDIS_HOST = os.getenv('REDIS_HOST')  # docker network
    REDIS_PORT = os.getenv('REDIS_PORT')
    REDIS_DB = os.getenv('REDIS_DB')
    REDIS_CACHE_DB = os.getenv('REDIS_CACHE_DB')
    REDIS_PASSWORD = os.getenv('REDIS_PASSWORD')
    CACHE_KEY_PREFIX = os.getenv('CACHE_KEY_PREFIX')

    # elasticsearch config
    # --------------------------------------------------------------------
    ELASTICSEARCH_URL = os.getenv('ELASTICSEARCH_URL')

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

    # Upload System Settings

    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER')
    UPLOAD_TEMP_FOLDER = os.getenv('UPLOAD_TEMP_FOLDER')
    UPLOAD_SYSTEM_FOLDER = os.getenv('UPLOAD_SYSTEM_FOLDER')
    UPLOAD_USERS_FOLDER = os.getenv('UPLOAD_USERS_FOLDER')
    UPLOAD_STORES_FOLDER = os.getenv('UPLOAD_STORES_FOLDER')
    UPLOAD_TYPE_OPTIONS = [UPLOAD_SYSTEM_FOLDER, UPLOAD_USERS_FOLDER, UPLOAD_STORES_FOLDER]
    MAX_CONTENT_LENGTH = 8 * 1024 * 1024
    # SMTP server config
    # --------------------------------------------------------------------
    # SERVER_EMAIL = 'Sivan Wolberg <sivan.wolberg@wolberg.pro>'
    # DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', SERVER_EMAIL)
    # EMAIL_HOST = os.environ.get('EMAIL_HOST')
    # EMAIL_PORT = os.environ.get('EMAIL_PORT')
    # EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
    # EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
    # Testing settings
    CLEAR_FOLDER_UPLOAD = False
    TESTING_ASSETS_FOLDER = ''
    # General Settings
    MAX_PARENT_LEVEL = os.getenv('MAX_PARENT_LEVEL')


class DevelopmentConfig(Config):
    ENV = os.environ.get("FLASK_ENV", "development")
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://localhost:5432/postgres')
    DEBUG = True
    ASSETS_DEBUG = True


class TestingConfig(Config):
    ENV = os.environ.get("FLASK_ENV", "testing")
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    TESTING_ASSETS_FOLDER = os.getenv('TESTING_ASSETS_FOLDER') if os.getenv('TESTING_ASSETS_FOLDER') is not None else os.path.join('test', 'assets')
    DEBUG = True
    SENTRY_ENABLE = False
    TESTING = True
    CLEAR_FOLDER_UPLOAD = os.getenv('CLEAR_FOLDER_UPLOAD')


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
