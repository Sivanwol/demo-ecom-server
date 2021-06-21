# test/test_settings.py
import unittest

from src.exceptions import SettingsNotSync
from test.common.Basecase import BaseTestCase


class FlaskTestCase(BaseTestCase):
    def test_raise_when_no_sync(self):
        with self.assertRaises(SettingsNotSync):
            self.settingsService.getItem('XX')
