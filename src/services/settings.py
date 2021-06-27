import json
import os

from flask import Flask

from config.setup import redis_connection
from config.database import db
from src.exceptions import SettingsNotSync
from src.models import Settings
from src.utils.general import Struct


class SettingsService:
    def __init__(self, app: Flask):
        self.logger = app.logger

    def getItem(self, key):
        value = None
        if not redis_connection.exists('sync_in_progress'):
            raise SettingsNotSync()
        key = f'{os.environ.get("FLASK_ENV", "development")}_{key}'
        if not bool(int(redis_connection.get('sync_in_progress'))):
            key_is_json = "%s_is_json" % key
            if not redis_connection.exists(key):
                return None
            value = redis_connection.get(key)
            is_json = int(redis_connection.get(key_is_json))
            if is_json:
                value = Struct(json.loads(value))
        else:
            key_temp = "%s_temp" % key
            key_temp_is_json = "%s_is_json" % key_temp
            if not redis_connection.exists(key_temp):
                return None
            value = redis_connection.get(key_temp)
            is_json = (redis_connection.get(key_temp_is_json))
            if is_json:
                value = Struct(json.loads(value))
        return value

    def forceSync(self):
        if not redis_connection.exists('sync_in_progress'):
            self.syncSettings()
        else:
            if not bool(int(redis_connection.get('sync_in_progress'))):
                self.syncSettings()

    def update_value(self, key, env, value, is_json=False):
        result = Settings.query.filter_by(environment=env, key=key).first()
        if result is None:
            return False
        result.value = value
        result.is_json = is_json
        db.session.merge(result)
        db.session.commit()
        return True

    def syncSettings(self):
        if not redis_connection.exists('sync_in_progress'):
            redis_connection.set('sync_in_progress', 0)
        if not bool(int(redis_connection.get('sync_in_progress'))):
            redis_connection.set('sync_in_progress', 1)
            env = os.environ.get("FLASK_ENV", "development")
            settings = Settings.query.filter_by(environment=env).all()
            for item in settings:
                key = "%s_%s" % (env, item.key)
                value = item.value
                is_json = 0
                if item.is_json:
                    is_json = 1
                self.updateSettingItem(key, is_json, str(value))
            redis_connection.set('sync_in_progress', 0)

    def updateSettingItem(self, key, is_json, value):
        key_is_json = "%s_is_json" % key
        key_temp = "%s_temp" % key
        key_temp_is_json = "%s_is_json" % key_temp
        if not redis_connection.exists(key):
            redis_connection.set(key, value)
            redis_connection.set(key_is_json, is_json)
        else:
            temp_value = redis_connection.get(key)
            temp_value_is_json = redis_connection.get(key_is_json)
            redis_connection.set(key_temp, temp_value)
            redis_connection.set(key_temp_is_json, temp_value_is_json)
            redis_connection.set(key, value)
            redis_connection.set(key_is_json, is_json)

    def init_system_settings(self):
        Settings.setupSystem()