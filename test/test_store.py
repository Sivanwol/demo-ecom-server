# tests/test_basic.py
import json
import unittest

from test.common.Basecase import BaseTestCase, Struct


class FlaskTestCase(BaseTestCase):
    store_owner_user = "store+owner@store.com"

    # todo: need add the store create and delete checks
    def test_get_user_object(self):
        with self.client:
            user_object = self.login_user(self.firebase_owner_user, self.firebase_global_password)
            uid = user_object['uid']
            token = user_object['idToken']
            store_name = self.fake.company()
            currency_code = self.fake.currency_code()
            post_data = {
                'name': store_name,
                'description': 'store description',
                'currency_code': currency_code
            }
            response = self.request_post('/api/store/%s/create' % uid,token,post_data)
            self.assertEqual(response.status_code, 200)
            response_data = Struct(response.json)
            user = Struct(self.storeService.store(uid, True))
            self.assertIsNotNone(user)
            self.assertIsNotNone(response_data)


if __name__ == '__main__':
    unittest.main()
