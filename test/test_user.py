# tests/test_basic.py
import json
import unittest

from test.common.Basecase import BaseTestCase, Struct


class FlaskTestCase(BaseTestCase):
    # todo: need add the store create and delete checks
    def test_get_user_object(self):
        with self.client:
            user_object = self.login_user(self.firebase_owner_user, self.firebase_global_password)
            uid = user_object['uid']
            token = user_object['idToken']
            response = self.client.get(
                '/api/user/%s' % uid,
                data=dict(),
                headers=dict(
                    Authorization='Bearer ' + token
                ),
                content_type='application/json'
            )
            self.assertEqual(response.status_code, 200)
            response_data = Struct(response.json)
            user = Struct(self.userService.get_user(uid, True))
            self.assertIsNotNone(user)
            self.assertIsNotNone(response_data)
            self.assertEqual(response_data.data.user_meta.display_name, user_object['display_name'])
            self.assertEqual(response_data.data.user_data.uid, user.uid)
            self.assertEqual(response_data.data.user_data.is_pass_tutorial, user.is_pass_tutorial)
            self.assertEqual(response_data.data.user_data.id, user.id)
            self.assertEqual(response_data.data.user_data.roles[0].id, user.roles[0].id)

    # todo:  Ensure that Flask was set up correctly
    def test_sync_new_user(self):
        with self.client:
            user_object = self.login_user(self.firebase_owner_user, self.firebase_global_password)
            uid = user_object['uid']
            token = user_object['idToken']
            response = self.client.post(
                '/api/user/%s' % uid,
                data=dict(),
                headers=dict(
                    Authorization='Bearer ' + token
                ),
                content_type='application/json'
            )
            self.assertEqual(response.status_code, 200)
            user = self.userService.get_user(uid, True)
            self.assertIsNotNone(user)


if __name__ == '__main__':
    unittest.main()
