# tests/test_basic.py
import unittest

from src.utils.enums import RolesTypes
from src.utils.general import Struct
from test.common.Basecase import BaseTestCase


class FlaskTestCase(BaseTestCase):

    def setUp(self):
        self.testSetUp()

    def tearDown(self):
        self.testTearDown()

    # Todo: checking if try get user with correct roles when the user not active
    def test_check_user_not_active(self):
        with self.client:
            user_not_active = "noactive@user.com"
            self.create_user(user_not_active, [RolesTypes.Support.value], True)
            user_object = self.login_user(self.platform_owner_user)
            owner_uid = user_object['uid']
            owner_token = user_object['idToken']
            user = self.userService.get_user(owner_uid, True)
            self.assertIsNone(user.store_code)
            store_name = self.fake.company()
            currency_code = self.fake.currency_code()
            post_data = {
                'name': store_name,
                'description': 'store description',
                'currency_code': currency_code
            }
            response = self.request_post('/api/store/%s/create' % owner_uid, owner_token, None, post_data)
            self.assert200(response, 'create store request failed')
            response_data = Struct(response.json)
            self.assertIsNotNone(response_data)
            self.assertTrue(response_data.status)
            self.assertIsNotNone(response_data.data)
            self.assertIsNotNone(response_data.data.info)
            self.assertIsNotNone(response_data.data.info)
            self.assertNotEqual(response_data.data.info.store_code, '')
            user_object = self.login_user(user_not_active)
            uid = user_object['uid']
            token = user_object['idToken']
            response = self.request_put('/api/user/%s/toggle_active' % uid, owner_token)
            self.assert200(response, 'toggle active state of user request failed')
            response_data = Struct(response.json)
            self.assertIsNotNone(response_data)
            self.assertTrue(response_data.status)
            self.assertIsNotNone(response_data.data)
            user = self.userService.get_user(uid, True)
            self.assertIsNotNone(user)
            self.assertFalse(user.is_active)

            self.login_failed_user(user_not_active)

    def test_get_user_object(self):
        with self.client:
            user_object = self.login_user(self.platform_owner_user)
            uid = user_object['uid']
            token = user_object['idToken']
            response = self.request_get('/api/user/{}'.format(uid), token)
            self.assert200(response, 'get user request failed')
            response_data = Struct(response.json)
            self.assertTrue(response_data.status)
            self.assertIsNotNone(response_data)
            self.assertIsNotNone(response_data.data)
            user = self.userService.get_user(uid, True)
            self.assertIsNotNone(user)
            self.assertIsNotNone(response_data)
            self.assertEqual(response_data.data.user_meta.display_name, user_object['display_name'])
            self.assertEqual(response_data.data.user_data.uid, user.uid)
            self.assertEqual(response_data.data.user_data.is_pass_tutorial, user.is_pass_tutorial)
            self.assertEqual(response_data.data.user_data.id, user.id)
            self.assertEqual(response_data.data.user_data.roles[0].id, user.roles[0].id)

    def test_check_role_not_match(self):
        with self.client:
            user_object = self.login_user(self.platform_support_user)
            uid = user_object['uid']
            token = user_object['idToken']
            user = self.userService.get_user(uid, True)
            self.assertIsNone(user.store_code)
            store_name = self.fake.company()
            currency_code = self.fake.currency_code()
            post_data = {
                'name': store_name,
                'description': 'store description',
                'currency_code': currency_code
            }
            response = self.request_post('/api/store/%s/create' % uid, token, None, post_data)
            self.assert401(response, 'role checks request not failed')
            response_data = Struct(response.json)
            self.assertFalse(response_data.status)

    def test_sync_new_user(self):
        with self.client:
            store_owner_user = "user@gmail.com"
            store_customer_user = "customer@gmail.com"
            store_info = self.create_store(store_owner_user)
            self.create_firebase_store_user(store_customer_user)
            user_object = self.login_user(store_customer_user)
            uid = user_object['uid']
            token = user_object['idToken']
            response = self.request_post('/api/user/{}/bind/{}'.format(uid, store_info.data.info.store_code), token)
            self.assert200(response, 'bind user to store request failed')
            response_data = Struct(response.json)
            user = self.userService.get_user(uid, True)
            self.assertIsNotNone(response_data)
            self.assertTrue(response_data.status)
            self.assertIsNotNone(response_data.data)
            self.assertIsNotNone(response_data.data.extend_info)
            self.assertIsNotNone(response_data.data.extend_info)
            self.assertEqual(response_data.data.extend_info.store_code, store_info.data.info.store_code)
            self.assertEqual(response_data.data.extend_info.store_code, user.store_code)
            self.assertEqual(response_data.data.extend_info.uid, uid)
            self.assertFalse(user.is_pass_tutorial)

    def test_service_user_part_of_store_valid(self):
        new_user = "user@gmail.com"
        store_info = self.create_store(new_user)
        user_object = self.login_user(new_user)
        uid = user_object['uid']
        self.assertTrue(self.userService.check_user_part_store(uid, store_info.data.info.store_code))

    def test_service_user_part_of_store_staff_valid(self):
        user_staff = "staff@gmail.com"
        new_user = "user@gmail.com"
        store_info = self.create_store(new_user)
        self.create_user(user_staff, [RolesTypes.StoreAccount.value], False, store_info.data.info.store_code)
        user_object = self.login_user(user_staff)
        uid = user_object['uid']
        self.assertTrue(self.userService.check_user_part_store(uid, store_info.data.info.store_code))

    def test_service_user_part_of_store_invalid(self):
        user_not_active = "noactive@user.com"
        self.create_user(user_not_active, [RolesTypes.Support.value], True)
        new_user = "user@gmail.com"
        store_info = self.create_store(new_user)
        user_object = self.login_user(user_not_active)
        uid = user_object['uid']
        self.assertFalse(self.userService.check_user_part_store(uid, store_info.data.info.store_code))

    def test_mark_user_finish_tutrial(self):
        store_owner_user = "user@gmail.com"
        store_customer_user = "customer@gmail.com"
        store_info = self.create_store(store_owner_user)
        self.create_firebase_store_user(store_customer_user)
        user_object = self.login_user(store_customer_user)
        uid = user_object['uid']
        token = user_object['idToken']
        response = self.request_post('/api/user/{}/bind/{}'.format(uid, store_info.data.info.store_code), token)
        self.assert200(response, 'bind user to store request failed')
        user = self.userService.get_user(uid, True)
        self.assertFalse(user.is_pass_tutorial)
        response = self.request_put('/api/user/{}/passed_tutorial'.format(uid), token)
        self.assert200(response, 'mark user pass tutrial as passed request failed')
        user = self.userService.get_user(uid, True)
        self.assertTrue(user.is_pass_tutorial)


if __name__ == '__main__':
    unittest.main()
