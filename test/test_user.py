# tests/test_basic.py

import unittest

from test.common.Basecase import BaseTestCase


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
            data = response.json()
            user = self.userService.get_user(uid, True)
            self.assertIsNotNone(user)
            self.assertEqual(data.uid , user.uid)
            self.assertEqual(data.is_pass_tutorial , user.is_pass_tutorial)
            self.assertEqual(data.id , user.id)
            self.assertEqual(data.roles[0].id , user.roles[0].id)


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
