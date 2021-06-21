import json
import os
from distutils.util import strtobool
from logging import Logger

from config.api import redis_connection
from src.exceptions import SettingsNotSync
from src.models import Settings
from src.utils.general import Struct


class SettingsService:
    def __init__(self, logger: Logger):
        self.logger = logger

    def getItem(self, key):
        value = None
        if not redis_connection.exists('sync_in_progress'):
            raise SettingsNotSync()

        if not strtobool(redis_connection.get('sync_in_progress')):
            key_is_json = "%s_is_json" % key
            if not redis_connection.exists(key):
                return None
            value = redis_connection.get(key)
            is_json = strtobool(redis_connection.get(key_is_json))
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
        if not redis_connection.exists('sync_in_progress') or not strtobool(redis_connection.get('sync_in_progress')):
            self.syncSettings()

    def syncSettings(self):
        if not redis_connection.exists('sync_in_progress'):
            redis_connection.set('sync_in_progress', False)
        if not strtobool(redis_connection.get('sync_in_progress')):
            redis_connection.set('sync_in_progress', True)
            env = os.environ.get("FLASK_ENV", "development")
            settings = Settings.query.filter_by(environment=env).all()
            for item in settings:
                key = "%s_%s" % (env, item.key)
                value = item.value
                is_json = item.is_json
                self.updateSettingItem(key, is_json, value)
            redis_connection.set('sync_in_progress', False)

    def updateSettingItem(self, key, is_json, value):
        key_is_json = "%s_is_json" % key
        key_temp = "%s_temp" % key
        key_temp_is_json = "%s_is_json" % key_temp
        if not redis_connection.exists('key'):
            redis_connection.set(key, value)
            redis_connection.set(key_is_json, is_json)
        else:
            temp_value = redis_connection.get(key)
            temp_value_is_json = redis_connection.get(key_is_json)
            redis_connection.set(key_temp, temp_value)
            redis_connection.set(key_temp_is_json, temp_value_is_json)
            redis_connection.set(key, value)
            redis_connection.set(key_is_json, is_json)
