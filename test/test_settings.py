# test/test_settings.py
import os
import unittest
from src.exceptions import SettingsNotSync
from src.models import Settings
from test.common.Basecase import BaseTestCase


class FlaskTestCase(BaseTestCase):
    def test_raise_when_no_sync(self):
        with self.assertRaises(SettingsNotSync):
            self.settingsService.getItem('XX')

    def test_none_exists_key(self):
        env = os.environ.get("FLASK_ENV", "development")
        key = env + '_XX'
        self.settingsService.forceSync()
        value = self.settingsService.getItem(key)
        self.assertIsNone(value)

    def test_sync_settings(self):
        env = os.environ.get("FLASK_ENV", "development")
        self.settingsService.forceSync()
        value = self.settingsService.getItem(env + '_UPLOAD_MAX_SIZE')
        result = Settings.query.filter_by(environment=env, key='UPLOAD_MAX_SIZE').first()
        self.assertIsNotNone(result)
        self.assertIsNotNone(value)
        self.assertEqual(int(value), int(result.value))

    def test_update_value_no_update_redis(self):
        env = os.environ.get("FLASK_ENV", "development")
        key = env + '_UPLOAD_MAX_SIZE'
        db_key = 'UPLOAD_MAX_SIZE'
        self.settingsService.forceSync()
        value = self.settingsService.getItem(key)
        result = Settings.query.filter_by(environment=env, key=db_key).first()
        self.assertIsNotNone(result)
        self.assertIsNotNone(value)
        self.assertEqual(int(value), int(result.value))
        self.settingsService.update_value(db_key, env, 550)
        value = self.settingsService.getItem(key)
        result = Settings.query.filter_by(environment=env, key=db_key).first()
        self.assertIsNotNone(result)
        self.assertIsNotNone(value)
        self.assertNotEqual(int(value), int(result.value))

    def test_force_settings(self):
        env = os.environ.get("FLASK_ENV", "development")
        key = env + '_UPLOAD_MAX_SIZE'
        db_key = 'UPLOAD_MAX_SIZE'
        self.settingsService.forceSync()
        value = self.settingsService.getItem(key)
        result = Settings.query.filter_by(environment=env, key=db_key).first()
        self.assertIsNotNone(result)
        self.assertIsNotNone(value)
        self.assertEqual(int(value), int(result.value))
        self.settingsService.update_value(db_key, env, 550)
        self.settingsService.forceSync()
        value = self.settingsService.getItem(key)
        result = Settings.query.filter_by(environment=env, key=db_key).first()
        self.assertIsNotNone(result)
        self.assertIsNotNone(value)
        self.assertEqual(int(value), int(result.value))
