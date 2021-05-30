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

    # todo: need add the store create and delete checks
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
            user = Struct(self.userService.get_user(uid, True))
            self.assertIsNotNone(user)
            self.assertIsNotNone(response_data)
            self.assertEqual(response_data.data.user_meta.display_name, user_object['display_name'])
            self.assertEqual(response_data.data.user_data.uid, user.uid)
            self.assertEqual(response_data.data.user_data.is_pass_tutorial, user.is_pass_tutorial)
            self.assertEqual(response_data.data.user_data.id, user.id)
            self.assertEqual(response_data.data.user_data.roles[0].id, user.roles[0].id)

    def test_check_role_not_match(self):

        with self.client:
            self.create_store_user(self.platform_owner_user, [RolesTypes.StoreOwner.value], True)
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
            response = self.request_post('/api/store/%s/create' % uid, token, post_data)
            self.assert401(response, 'role checks request not failed')
            response_data = Struct(response.json)
            self.assertFalse(response_data.status)

    # todo:  Ensure that Flask was set up correctly
    def test_sync_new_user(self):
        pass
        # with self.client:
        #     user_object = self.login_user(self.platform_owner_user)
        #     uid = user_object['uid']
        #     token = user_object['idToken']
        #     response = self.client.post(
        #         '/api/user/%s' % uid,
        #         data=dict(),
        #         headers=dict(
        #             Authorization='Bearer %s' + token
        #         ),
        #         content_type='application/json'
        #     )
        #     self.assertEqual(response.status_code, 200)
        #     user = self.userService.get_user(uid, True)
        #     self.assertIsNotNone(user)


if __name__ == '__main__':
    unittest.main()
