# tests/test_basic.py
import json
import unittest

from src.utils.enums import RolesTypes
from test.common.Basecase import BaseTestCase, Struct
from elasticmock import elasticmock


class FlaskTestCase(BaseTestCase):

    @elasticmock
    def test_create_store(self):
        with self.client:
            self.create_store_user(self.store_owner_user, [RolesTypes.StoreOwner.value], True)
            user_object = self.login_user(self.platform_owner_user)
            uid = user_object['uid']
            token = user_object['idToken']
            user = self.userService.get_user(uid, True)
            has_store_code = False
            if 'store_code' in user:
                has_store_code = True
            self.assertFalse(has_store_code)
            store_name = self.fake.company()
            currency_code = self.fake.currency_code()
            post_data = {
                'name': store_name,
                'description': 'store description',
                'currency_code': currency_code
            }
            response = self.request_post('/api/store/%s/create' % uid, token, post_data)
            self.assert200(response, 'create store request failed')
            response_data = Struct(response.json)
            self.assertIsNotNone(response_data)
            self.assertTrue(response_data.status)
            self.assertNotEqual(response_data.data.store_code, '')
            store = self.storeService.get_store(uid, response_data.data.store_code, True)
            user = self.userService.get_user(uid, True)
            self.assertIsNotNone(user)
            self.assertIsNotNone(store)
            self.assertIsNotNone(response_data.data)
            self.assertEqual(response_data.data.store_code, store.store_code)
            self.assertEqual(user.store_code, store.store_code)
            self.assertEqual(response_data.data.name, post_data['name'])
            self.assertEqual(response_data.data.default_currency_code, post_data['currency_code'])


if __name__ == '__main__':
    unittest.main()
