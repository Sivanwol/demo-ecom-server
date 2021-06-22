# test/test_media.py
import os
import unittest

from src.models import MediaFolder
from test.common.Basecase import BaseTestCase


class FlaskTestCase(BaseTestCase):
    def test_model_get_parent_folders(self):
        user_object = self.login_user(self.platform_owner_user)
        uid = user_object['uid']
        list_folders = self.mediaUtils.create_media_folder_parents(uid)
        root_code = list_folders[0]
        list_folders.pop(0)
        result = MediaFolder.query.filter_by(code=root_code).first()
        self.assertIsNotNone(result)
        self.assertEqual(result.code, root_code)
        folders = result.get_all_child_folders()
        test_folder_codes = []
        for folder in folders:
            test_folder_codes.append(folder.code)
        self.assertEqual(len(test_folder_codes), len(list_folders))
        for code in test_folder_codes:
            self.assertIn(code, list_folders)
