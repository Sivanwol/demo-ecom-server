# test/test_user.py
import unittest

from src.schemas.user_schema import UserSchema
from src.utils.enums import RolesTypes
from src.utils.general import Struct
from src.utils.validations import valid_user_list_params
from test.common.Basecase import BaseTestCase
from urllib.parse import urlencode


class FlaskTestCase(BaseTestCase):

    # region Test User List

    def test_get_user_list_platform_no_filters_no_order(self):
        with self.client:
            self.assertEqual.__self__.maxDiff = None
            user_object = self.login_user(self.platform_owner_user)
            token = user_object['idToken']
            uid = user_object['uid']
            self.userUtils.create_platforms_users()
            query_params = {
                'filter_names': None,
                'filter_emails': None,
                'filter_stores': None,
                'filter_countries': None,
                'filter_store_users': 0,
                'filter_inactive': 0,
                'filter_platform': 1,
                'order_by[]': [],
                'per_page': 20,
                'page': 1
            }
            query_string = urlencode(query_params)
            response = self.request_get('/api/user/list', token, query_string)
            self.assertRequestPassed(response, 'getting user list request failed')
            response_data = Struct(response.json)
            filters = {
                'names': [],
                'emails': [],
                'stores': [],
                'countries': [],
                'store_users': False,
                'platform': True
            }
            self.assertIsNotNone(response_data)
            self.assertTrue(response_data.status)
            self.assertIsNotNone(response_data.data)
            users = self.userService.get_users(filters, [], 20, 1, False)
            schema = UserSchema()
            data = schema.dump(users.items, many=True)
            self.assertListEqual(data, response.json['data']['items'])
            self.assertEqual(response_data.data.meta.pages, users.pages)
            self.assertEqual(response_data.data.meta.total_items, users.total)
            self.assertFalse(response_data.data.meta.next)
            self.assertFalse(response_data.data.meta.prev)

    def test_get_user_list_platform_email_filters_no_order(self):
        with self.client:
            self.assertEqual.__self__.maxDiff = None
            user_object = self.login_user(self.platform_owner_user)
            token = user_object['idToken']
            uid = user_object['uid']
            users = self.userUtils.create_platforms_users()
            selected_params = [
                users['accounts'][0]['email'],
                users['accounts'][1]['email'],
                users['support'][0]['email']
            ]
            query_params = {
                'filter_names': None,
                'filter_emails': ','.join(selected_params),
                'filter_stores': None,
                'filter_countries': None,
                'filter_store_users': 0,
                'filter_inactive': 0,
                'filter_platform': 1,
                'order_by[]': [],
                'per_page': 20,
                'page': 1
            }
            query_string = urlencode(query_params)
            response = self.request_get('/api/user/list', token, query_string)
            self.assertRequestPassed(response, 'getting user list request failed')
            response_data = Struct(response.json)
            filters = {
                'names': [],
                'emails': selected_params,
                'stores': [],
                'countries': [],
                'store_users': False,
                'platform': True
            }
            self.assertIsNotNone(response_data)
            self.assertTrue(response_data.status)
            self.assertIsNotNone(response_data.data)
            users = self.userService.get_users(filters, [], 20, 1, False)
            schema = UserSchema()
            data = schema.dump(users.items, many=True)
            for idx, item in enumerate(response.json['data']['items']):
                self.assertDictEqual(item, data[idx])
            self.assertEqual(response_data.data.meta.pages, users.pages)
            self.assertEqual(response_data.data.meta.total_items, users.total)
            self.assertFalse(response_data.data.meta.next)
            self.assertFalse(response_data.data.meta.prev)

    def test_get_user_list_platform_names_filters_no_order(self):
        with self.client:
            self.assertEqual.__self__.maxDiff = None
            user_object = self.login_user(self.platform_owner_user)
            token = user_object['idToken']
            uid = user_object['uid']
            users = self.userUtils.create_platforms_users()
            selected_params = [
                users['accounts'][0]['name'],
                users['accounts'][1]['name'],
                users['support'][0]['name']
            ]
            query_params = {
                'filter_names': ','.join(selected_params),
                'filter_emails': None,
                'filter_stores': None,
                'filter_countries': None,
                'filter_store_users': 0,
                'filter_inactive': 0,
                'filter_platform': 1,
                'order_by[]': [],
                'per_page': 20,
                'page': 1
            }
            query_string = urlencode(query_params)
            response = self.request_get('/api/user/list', token, query_string)
            self.assertRequestPassed(response, 'getting user list request failed')
            response_data = Struct(response.json)
            filters = {
                'names': selected_params,
                'emails': [],
                'stores': [],
                'countries': [],
                'store_users': False,
                'platform': True
            }
            self.assertIsNotNone(response_data)
            self.assertTrue(response_data.status)
            self.assertIsNotNone(response_data.data)
            users = self.userService.get_users(filters, [], 20, 1, False)
            schema = UserSchema()
            data = schema.dump(users.items, many=True)
            self.assertListEqual(data, response.json['data']['items'])
            self.assertEqual(response_data.data.meta.pages, users.pages)
            self.assertEqual(response_data.data.meta.total_items, users.total)
            self.assertFalse(response_data.data.meta.next)
            self.assertFalse(response_data.data.meta.prev)

    def test_get_user_list_platform_inactive_filters_no_order(self):
        with self.client:
            self.assertEqual.__self__.maxDiff = None
            user_object = self.login_user(self.platform_owner_user)
            token = user_object['idToken']
            uid = user_object['uid']
            self.userUtils.create_inactive_platform_users()
            query_params = {
                'filter_names': None,
                'filter_emails': None,
                'filter_stores': None,
                'filter_countries': None,
                'filter_store_users': 0,
                'filter_inactive': 1,
                'filter_platform': 1,
                'order_by[]': [],
                'per_page': 20,
                'page': 1
            }
            query_string = urlencode(query_params)
            response = self.request_get('/api/user/list', token, query_string)
            self.assertRequestPassed(response, 'getting user list request failed')
            response_data = Struct(response.json)
            filters = {
                'names': [],
                'emails': [],
                'stores': [],
                'countries': [],
                'store_users': False,
                'platform': True
            }
            self.assertIsNotNone(response_data)
            self.assertTrue(response_data.status)
            self.assertIsNotNone(response_data.data)
            users = self.userService.get_users(filters, [], 20, 1, True)
            schema = UserSchema()
            data = schema.dump(users.items, many=True)
            self.assertListEqual(data, response.json['data']['items'])
            self.assertEqual(response_data.data.meta.pages, users.pages)
            self.assertEqual(response_data.data.meta.total_items, users.total)
            self.assertFalse(response_data.data.meta.next)
            self.assertFalse(response_data.data.meta.prev)

    def test_get_user_list_platform_multi_filters_no_order(self):
        with self.client:
            self.assertEqual.__self__.maxDiff = None
            user_object = self.login_user(self.platform_owner_user)
            token = user_object['idToken']
            uid = user_object['uid']
            users = self.userUtils.create_platforms_users()
            selected_params_email = [
                users['accounts'][0]['email'],
                users['accounts'][1]['email'],
                users['support'][0]['email']
            ]
            selected_params_name = [
                users['accounts'][2]['name'].split(' ')[0],
                users['support'][1]['name'].split(' ')[0]
            ]
            query_params = {
                'filter_names': ','.join(selected_params_name),
                'filter_emails': ','.join(selected_params_email),
                'filter_stores': None,
                'filter_countries': None,
                'filter_store_users': 0,
                'filter_inactive': 0,
                'filter_platform': 1,
                'order_by[]': [],
                'per_page': 20,
                'page': 1
            }
            query_string = urlencode(query_params)
            response = self.request_get('/api/user/list', token, query_string)
            self.assertRequestPassed(response, 'getting user list request failed')
            response_data = Struct(response.json)
            filters = {
                'names': selected_params_name,
                'emails': selected_params_email,
                'stores': [],
                'countries': [],
                'store_users': False,
                'platform': True
            }
            self.assertIsNotNone(response_data)
            self.assertTrue(response_data.status)
            self.assertIsNotNone(response_data.data)
            users = self.userService.get_users(filters, [], 20, 1, False)
            schema = UserSchema()
            data = schema.dump(users.items, many=True)
            self.assertListEqual(data, response.json['data']['items'])
            self.assertEqual(response_data.data.meta.pages, users.pages)
            self.assertEqual(response_data.data.meta.total_items, users.total)
            self.assertFalse(response_data.data.meta.next)
            self.assertFalse(response_data.data.meta.prev)

    def test_get_user_list_platform_stores_filters_no_order(self):
        with self.client:
            self.assertEqual.__self__.maxDiff = None
            user_object = self.login_user(self.platform_owner_user)
            token = user_object['idToken']
            uid = user_object['uid']
            users = self.userUtils.create_random_of_stores_users()

            selected_params_stores = [
                users['stores'][2]['store_code'],
                users['stores'][1]['store_code'],
                users['stores'][0]['store_code']
            ]
            query_params = {
                'filter_names': None,
                'filter_emails': None,
                'filter_stores': ','.join(selected_params_stores),
                'filter_countries': None,
                'filter_store_users': 1,
                'filter_inactive': 0,
                'filter_platform': 1,
                'order_by[]': [],
                'per_page': 20,
                'page': 1
            }
            query_string = urlencode(query_params)
            response = self.request_get('/api/user/list', token, query_string)
            self.assertRequestPassed(response, 'getting user list request failed')
            response_data = Struct(response.json)
            filters = {
                'names': [],
                'emails': [],
                'stores': selected_params_stores,
                'countries': [],
                'store_users': True,
                'platform': True
            }
            self.assertIsNotNone(response_data)
            self.assertTrue(response_data.status)
            self.assertIsNotNone(response_data.data)
            users = self.userService.get_users(filters, [], 20, 1, False, True)
            schema = UserSchema()
            data = schema.dump(users.items, many=True)
            self.assertListEqual(data, response.json['data']['items'])
            self.assertEqual(response_data.data.meta.pages, users.pages)
            self.assertEqual(response_data.data.meta.total_items, users.total)
            self.assertFalse(response_data.data.meta.next)
            self.assertFalse(response_data.data.meta.prev)

    def test_get_user_list_platform_all_stores_filters_no_order(self):
        with self.client:
            self.assertEqual.__self__.maxDiff = None
            user_object = self.login_user(self.platform_owner_user)
            token = user_object['idToken']
            uid = user_object['uid']
            users = self.userUtils.create_random_of_stores_users()
            query_params = {
                'filter_names': None,
                'filter_emails': None,
                'filter_stores': None,
                'filter_countries': None,
                'filter_store_users': 1,
                'filter_inactive': 0,
                'filter_platform': 1,
                'order_by[]': [],
                'per_page': 20,
                'page': 1
            }
            query_string = urlencode(query_params)
            response = self.request_get('/api/user/list', token, query_string)
            self.assertRequestPassed(response, 'getting user list request failed')
            response_data = Struct(response.json)
            filters = {
                'names': [],
                'emails': [],
                'stores': [],
                'countries': [],
                'store_users': True,
                'platform': True
            }
            self.assertIsNotNone(response_data)
            self.assertTrue(response_data.status)
            self.assertIsNotNone(response_data.data)
            users = self.userService.get_users(filters, [], 20, 1, False, True)
            schema = UserSchema()
            data = schema.dump(users.items, many=True)
            self.assertListEqual(data, response.json['data']['items'])
            self.assertEqual(response_data.data.meta.pages, users.pages)
            self.assertEqual(response_data.data.meta.total_items, users.total)
            self.assertFalse(response_data.data.meta.next)
            self.assertFalse(response_data.data.meta.prev)

    def test_get_user_list_platform_no_filters_email_order_asc_sort(self):
        with self.client:
            self.assertEqual.__self__.maxDiff = None
            user_object = self.login_user(self.platform_owner_user)
            token = user_object['idToken']
            uid = user_object['uid']
            self.userUtils.create_random_of_stores_users()
            order_by = [{
                'field': 'email',
                'sort': 'asc'
            }]
            query_params = {
                'filter_names': None,
                'filter_emails': None,
                'filter_stores': None,
                'filter_countries': None,
                'filter_store_users': 0,
                'filter_inactive': 0,
                'filter_platform': 1,
                'order_by': self.userUtils.convert_order_by_list_string(order_by),
                'per_page': 20,
                'page': 1
            }
            query_string = urlencode(query_params)
            response = self.request_get('/api/user/list', token, query_string)
            self.assertRequestPassed(response, 'getting user list request failed')
            response_data = Struct(response.json)
            filters = {
                'names': [],
                'emails': [],
                'stores': [],
                'countries': [],
                'store_users': False,
                'platform': True
            }
            self.assertIsNotNone(response_data)
            self.assertTrue(response_data.status)
            self.assertIsNotNone(response_data.data)
            result = valid_user_list_params(filters, order_by)
            users = self.userService.get_users(filters, result['orders'], 20, 1, False)
            schema = UserSchema()
            data = schema.dump(users.items, many=True)
            self.assertListEqual(data, response.json['data']['items'])
            self.assertEqual(response_data.data.meta.pages, users.pages)
            self.assertEqual(response_data.data.meta.total_items, users.total)
            self.assertFalse(response_data.data.meta.next)
            self.assertFalse(response_data.data.meta.prev)

    def test_get_user_list_platform_no_filters_email_order_desc_sort(self):
        with self.client:
            self.assertEqual.__self__.maxDiff = None
            user_object = self.login_user(self.platform_owner_user)
            token = user_object['idToken']
            uid = user_object['uid']
            self.userUtils.create_random_of_stores_users()
            order_by = [{
                'field': 'email',
                'sort': 'desc'
            }]
            query_params = {
                'filter_names': None,
                'filter_emails': None,
                'filter_stores': None,
                'filter_countries': None,
                'filter_store_users': 0,
                'filter_inactive': 0,
                'filter_platform': 1,
                'order_by': self.userUtils.convert_order_by_list_string(order_by),
                'per_page': 20,
                'page': 1
            }
            query_string = urlencode(query_params)
            response = self.request_get('/api/user/list', token, query_string)
            self.assertRequestPassed(response, 'getting user list request failed')
            response_data = Struct(response.json)
            filters = {
                'names': [],
                'emails': [],
                'stores': [],
                'countries': [],
                'store_users': False,
                'platform': True
            }
            self.assertIsNotNone(response_data)
            self.assertTrue(response_data.status)
            self.assertIsNotNone(response_data.data)
            result = valid_user_list_params(filters, order_by)
            users = self.userService.get_users(filters, result['orders'], 20, 1, False)
            schema = UserSchema()
            data = schema.dump(users.items, many=True)
            self.assertListEqual(data, response.json['data']['items'])
            self.assertEqual(response_data.data.meta.pages, users.pages)
            self.assertEqual(response_data.data.meta.total_items, users.total)
            self.assertFalse(response_data.data.meta.next)
            self.assertFalse(response_data.data.meta.prev)

    def test_get_user_list_platform_no_filters_multi_order(self):
        with self.client:
            self.assertEqual.__self__.maxDiff = None
            user_object = self.login_user(self.platform_owner_user)
            token = user_object['idToken']
            uid = user_object['uid']
            self.userUtils.create_random_of_stores_users()
            order_by = [{
                'field': 'store_code',
                'sort': 'desc'
            }, {
                'field': 'fullname',
                'sort': 'desc'
            }]
            query_params = {
                'filter_names': None,
                'filter_emails': None,
                'filter_stores': None,
                'filter_countries': None,
                'filter_store_users': 1,
                'filter_inactive': 0,
                'filter_platform': 1,
                'order_by': self.userUtils.convert_order_by_list_string(order_by),
                'per_page': 20,
                'page': 1
            }
            query_string = urlencode(query_params)
            response = self.request_get('/api/user/list', token, query_string)
            self.assertRequestPassed(response, 'getting user list request failed')
            response_data = Struct(response.json)
            filters = {
                'names': [],
                'emails': [],
                'stores': [],
                'countries': [],
                'store_users': True,
                'platform': True
            }
            self.assertIsNotNone(response_data)
            self.assertTrue(response_data.status)
            self.assertIsNotNone(response_data.data)
            result = valid_user_list_params(filters, order_by)
            users = self.userService.get_users(filters, result['orders'], 20, 1, False, True)
            schema = UserSchema()
            data = schema.dump(users.items, many=True)
            self.assertListEqual(data, response.json['data']['items'])
            self.assertEqual(response_data.data.meta.pages, users.pages)
            self.assertEqual(response_data.data.meta.total_items, users.total)
            self.assertFalse(response_data.data.meta.next)
            self.assertFalse(response_data.data.meta.prev)

    def test_get_user_list_platform_no_filters_name_order_3pages(self):
        with self.client:
            self.assertEqual.__self__.maxDiff = None
            user_object = self.login_user(self.platform_owner_user)
            token = user_object['idToken']
            uid = user_object['uid']
            self.userUtils.create_3pages_platform_users()
            order_by = [{
                'field': 'fullname',
                'sort': 'desc'
            }]
            query_params = {
                'filter_names': None,
                'filter_emails': None,
                'filter_stores': None,
                'filter_countries': None,
                'filter_store_users': 0,
                'filter_inactive': 0,
                'filter_platform': 1,
                'order_by': self.userUtils.convert_order_by_list_string(order_by),
                'per_page': 20,
                'page': 1
            }
            query_string = urlencode(query_params)
            response = self.request_get('/api/user/list', token, query_string)
            self.assertRequestPassed(response, 'getting user list page->1 request failed')
            response_data = Struct(response.json)
            filters = {
                'names': [],
                'emails': [],
                'stores': [],
                'countries': [],
                'store_users': False,
                'platform': True
            }
            self.assertIsNotNone(response_data)
            self.assertTrue(response_data.status)
            self.assertIsNotNone(response_data.data)
            result = valid_user_list_params(filters, order_by)
            users = self.userService.get_users(filters, result['orders'], 20, 1, False)
            schema = UserSchema()
            data = schema.dump(users.items, many=True)
            self.assertListEqual(data, response.json['data']['items'])
            self.assertEqual(response_data.data.meta.pages, users.pages)
            self.assertEqual(response_data.data.meta.total_items, users.total)
            self.assertTrue(response_data.data.meta.next)
            self.assertFalse(response_data.data.meta.prev)
            query_params['page'] = 2
            query_string = urlencode(query_params)
            response = self.request_get('/api/user/list', token, query_string)
            self.assertRequestPassed(response, 'getting user list page->2 request failed')
            response_data = Struct(response.json)
            users = self.userService.get_users(filters, result['orders'], 20, 2, False)
            schema = UserSchema()
            data = schema.dump(users.items, many=True)
            self.assertListEqual(data, response.json['data']['items'])
            self.assertEqual(response_data.data.meta.pages, users.pages)
            self.assertEqual(response_data.data.meta.total_items, users.total)
            self.assertTrue(response_data.data.meta.next)
            self.assertTrue(response_data.data.meta.prev)

            query_params['page'] = 3
            query_string = urlencode(query_params)
            response = self.request_get('/api/user/list', token, query_string)
            self.assertRequestPassed(response, 'getting user list page->3 request failed')
            response_data = Struct(response.json)
            users = self.userService.get_users(filters, result['orders'], 20, 3, False)
            schema = UserSchema()
            data = schema.dump(users.items, many=True)
            self.assertListEqual(data, response.json['data']['items'])
            self.assertEqual(response_data.data.meta.pages, users.pages)
            self.assertEqual(response_data.data.meta.total_items, users.total)
            self.assertFalse(response_data.data.meta.next)
            self.assertTrue(response_data.data.meta.prev)

    def test_get_user_list_store_stores_filters_no_order(self):
        with self.client:
            self.assertEqual.__self__.maxDiff = None
            user_object = self.login_user(self.platform_owner_user)
            token = user_object['idToken']
            uid = user_object['uid']
            users = self.userUtils.create_store_users()
            query_params = {
                'filter_names': None,
                'filter_emails': None,
                'filter_stores': users['stores'][0]['store_code'],
                'filter_countries': None,
                'filter_store_users': 0,
                'filter_inactive': 0,
                'filter_platform': 0,
                'order_by': '',
                'per_page': 20,
                'page': 1
            }
            query_string = urlencode(query_params)
            response = self.request_get('/api/user/list', token, query_string)
            self.assertRequestPassed(response, 'getting user list request failed')
            response_data = Struct(response.json)
            filters = {
                'names': [],
                'emails': [],
                'stores': [users['stores'][0]['store_code']],
                'countries': [],
                'store_users': False,
                'platform': False
            }
            self.assertIsNotNone(response_data)
            self.assertTrue(response_data.status)
            self.assertIsNotNone(response_data.data)
            users = self.userService.get_users(filters, [], 20, 1)
            schema = UserSchema()
            data = schema.dump(users.items, many=True)
            self.assertListEqual(data, response.json['data']['items'])
            self.assertEqual(response_data.data.meta.pages, users.pages)
            self.assertEqual(response_data.data.meta.total_items, users.total)
            self.assertFalse(response_data.data.meta.next)
            self.assertFalse(response_data.data.meta.prev)

    # region Test User Actions

    def test_check_user_not_active(self):
        with self.client:
            user_not_active = "noactive@user.com"
            self.create_user(user_not_active, self.fake.name(), [RolesTypes.Support.value], True)
            user_object = self.login_user(self.platform_owner_user)
            owner_uid = user_object['uid']
            owner_token = user_object['idToken']
            user = self.userService.get_user(owner_uid, True)
            self.assertIsNone(user.store_code)
            store_name = self.fake.company()
            post_data = {
                'name': store_name,
                'description': 'store description',
                'currency_code': 'USD'
            }
            response = self.request_post('/api/store/%s/create' % owner_uid, owner_token, None, None, post_data)
            self.assertRequestPassed(response, 'create store request failed')
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
            self.assertRequestPassed(response, 'toggle active state of user request failed')
            response_data = Struct(response.json)
            self.assertIsNotNone(response_data)
            self.assertTrue(response_data.status)
            self.assertIsNotNone(response_data.data)
            user = self.userService.get_user(uid, True)
            self.assertIsNotNone(user)
            self.assertFalse(user.is_active)

            self.login_failed_user(user_not_active)

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
            response = self.request_post('/api/store/%s/create' % uid, token, None, None, post_data)
            self.assert401(response, 'role checks request not failed')
            response_data = Struct(response.json)
            self.assertFalse(response_data.status)

    def test_sync_new_user(self):
        with self.client:
            store_owner_user = "user@gmail.com"
            store_customer_user = "customer@gmail.com"
            store_info = self.create_store(store_owner_user, self.fake.name())
            self.create_firebase_store_user(store_customer_user)
            user_object = self.login_user(store_customer_user)
            uid = user_object['uid']
            token = user_object['idToken']
            response = self.request_post('/api/user/{}/bind/{}'.format(uid, store_info.data.info.store_code), token)
            self.assertRequestPassed(response, 'bind user to store request failed')
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
            path = self.fileSystemService.get_folder_path('users', uid)
            self.assertIsNotNone(path)
            self.assertTrue(self.fileSystemService.acutal_folder_existed(path))

    def test_service_user_part_of_store_valid(self):
        with self.client:
            new_user = "user@gmail.com"
            store_info = self.create_store(new_user, self.fake.name())
            user_object = self.login_user(new_user)
            uid = user_object['uid']
            self.assertTrue(self.userService.check_user_part_store(uid, store_info.data.info.store_code))
            path = self.fileSystemService.get_folder_path('users', uid)
            self.assertIsNotNone(path)
            self.assertTrue(self.fileSystemService.acutal_folder_existed(path))

    def test_service_user_part_of_store_staff_valid(self):
        with self.client:
            user_staff = "staff@gmail.com"
            new_user = "user@gmail.com"
            store_info = self.create_store(new_user, self.fake.name())
            self.create_user(user_staff, self.fake.name(), [RolesTypes.StoreAccount.value], False, store_info.data.info.store_code)
            user_object = self.login_user(user_staff)
            uid = user_object['uid']
            self.assertTrue(self.userService.check_user_part_store(uid, store_info.data.info.store_code))

    def test_service_user_part_of_store_invalid(self):
        with self.client:
            user_not_active = "noactive@user.com"
            self.create_user(user_not_active, self.fake.name(), [RolesTypes.Support.value], True)
            new_user = "user@gmail.com"
            store_info = self.create_store(new_user, self.fake.name())
            user_object = self.login_user(user_not_active)
            uid = user_object['uid']
            self.assertFalse(self.userService.check_user_part_store(uid, store_info.data.info.store_code))

    def test_mark_user_finish_tutrial(self):
        with self.client:
            store_owner_user = "user@gmail.com"
            store_customer_user = "customer@gmail.com"
            store_info = self.create_store(store_owner_user, self.fake.name())
            self.create_firebase_store_user(store_customer_user)
            user_object = self.login_user(store_customer_user)
            uid = user_object['uid']
            token = user_object['idToken']
            response = self.request_post('/api/user/{}/bind/{}'.format(uid, store_info.data.info.store_code), token)
            self.assertRequestPassed(response, 'bind user to store request failed')
            user = self.userService.get_user(uid, True)
            self.assertFalse(user.is_pass_tutorial)
            response = self.request_put('/api/user/passed_tutorial', token)
            self.assertRequestPassed(response, 'mark user pass tutrial as passed request failed')
            user = self.userService.get_user(uid, True)
            self.assertTrue(user.is_pass_tutorial)

    def test_user_update_info_self(self):
        with self.client:
            user_object = self.login_user(self.platform_support_user)
            uid = user_object['uid']
            token = user_object['idToken']
            # old_user_data = self.userService.get_user(uid, True)
            country = self.fake.country_code()
            currency = self.fake.currency_code()
            fullname = self.fake.name()
            address1 = self.fake.address()
            address2 = self.fake.address()
            post_data = {
                'fullname': fullname,
                'address1': address1,
                'address2': address2,
                'currency': currency,
                'country': country
            }
            response = self.request_put('/api/user/update', token, None, None, post_data)
            self.assertRequestPassed(response, 'update user info request failed')
            response_data = Struct(response.json)
            user = self.userService.get_user(uid, True)
            self.assertIsNotNone(response_data)
            self.assertTrue(response_data.status)
            self.assertEqual(user.fullname, fullname)
            self.assertEqual(user.address1, address1)
            self.assertEqual(user.address2, address2)
            self.assertEqual(user.country, country)
            self.assertEqual(user.currency, currency)

    def test_user_update_info_as_global_support(self):
        with self.client:
            store_customer_user = "customer@gmail.com"
            store_owner_user = "user@gmail.com"
            user_object = self.login_user(self.platform_support_user)
            token = user_object['idToken']
            store_info = self.create_store(store_owner_user, self.fake.name())
            self.create_user(store_customer_user, self.fake.name(), [RolesTypes.StoreCustomer.value], False, store_info.data.info.store_code)
            user_object = self.login_user(store_customer_user)
            uid = user_object['uid']
            # old_user_data = self.userService.get_user(uid, True)
            country = "USA"
            currency = 'USD'
            fullname = self.fake.name()
            address1 = self.fake.address()
            address2 = self.fake.address()
            post_data = {
                'fullname': fullname,
                'address1': address1,
                'address2': address2,
                'currency': currency,
                'country': country
            }
            response = self.request_put('/api/user/{}/update'.format(uid), token, None, None, post_data)
            self.assertRequestPassed(response, 'update user info request failed')
            response_data = Struct(response.json)
            user = self.userService.get_user(uid, True)
            self.assertIsNotNone(response_data)
            self.assertTrue(response_data.status)
            self.assertEqual(user.fullname, fullname)
            self.assertEqual(user.address1, address1)
            self.assertEqual(user.address2, address2)
            self.assertEqual(user.country, country)
            self.assertEqual(user.currency, currency)

    def test_user_update_info_as_store_support(self):
        with self.client:
            store_customer_user = "customer@gmail.com"
            store_owner_user = "user@gmail.com"
            store_support_user = "support_store@gmail.com"
            store_info = self.create_store(store_owner_user, self.fake.name())

            self.create_user(store_customer_user, self.fake.name(), [RolesTypes.StoreCustomer.value], False, store_info.data.info.store_code)
            self.create_user(store_support_user, self.fake.name(), [RolesTypes.StoreSupport.value], False, store_info.data.info.store_code)

            user_object = self.login_user(store_support_user)
            token = user_object['idToken']
            user_object = self.login_user(store_customer_user)
            uid = user_object['uid']
            # old_user_data = self.userService.get_user(uid, True)
            country = self.fake.country_code()
            currency = self.fake.currency_code()
            fullname = self.fake.name()
            address1 = self.fake.address()
            address2 = self.fake.address()
            post_data = {
                'fullname': fullname,
                'address1': address1,
                'address2': address2,
                'currency': currency,
                'country': country
            }
            response = self.request_put('/api/user/{}/update'.format(uid), token, None, None, post_data)
            self.assertRequestPassed(response, 'update user info request failed')
            response_data = Struct(response.json)
            user = self.userService.get_user(uid, True)
            self.assertIsNotNone(response_data)
            self.assertTrue(response_data.status)
            self.assertEqual(user.fullname, fullname)
            self.assertEqual(user.address1, address1)
            self.assertEqual(user.address2, address2)
            self.assertEqual(user.country, country)
            self.assertEqual(user.currency, currency)

    def test_user_update_info_as_store_support_invalid(self):
        with self.client:
            store_customer_user = self.fake.email()
            store_owner_user = self.fake.email()
            store_diff_owner_user = self.fake.email()
            store_support_user = self.fake.email()
            store_info = self.create_store(store_owner_user, self.fake.name())
            diff_store_info = self.create_store(store_diff_owner_user, self.fake.name())

            self.create_user(store_customer_user, self.fake.name(), [RolesTypes.StoreCustomer.value], False, diff_store_info.data.info.store_code)
            self.create_user(store_support_user, self.fake.name(), [RolesTypes.StoreSupport.value], False, store_info.data.info.store_code)

            user_object = self.login_user(store_support_user)
            token = user_object['idToken']
            user_object = self.login_user(store_customer_user)
            uid = user_object['uid']
            # old_user_data = self.userService.get_user(uid, True)
            country = self.fake.country_code()
            currency = self.fake.currency_code()
            fullname = self.fake.name()
            address1 = self.fake.address()
            address2 = self.fake.address()
            post_data = {
                'fullname': fullname,
                'address1': address1,
                'address2': address2,
                'currency': currency,
                'country': country
            }
            response = self.request_put('/api/user/{}/update'.format(uid), token, None, None, post_data)
            self.assert400(response, 'update user info passed with invalid user store entered (diff store_code)')

    def test_add_store_staff_by_store_owner(self):
        with self.client:
            store_owner_user = "user@gmail.com"
            store_staff_user = self.fake.ascii_company_email()
            store_info = self.create_store(store_owner_user, self.fake.name())
            user_object = self.login_user(store_owner_user)
            token = user_object['idToken']
            uid = user_object['uid']
            post_data = {
                'email': store_staff_user,
                'password': self.global_password,
                'roles': [RolesTypes.StoreSupport.value, RolesTypes.StoreReport.value],
                'fullname': self.fake.name(),

            }
            response = self.request_post('/api/user/staff/%s' % store_info.data.info.store_code, token, None, None, post_data)
            self.assertRequestPassed(response, 'update store staff user request failed')

            user_object = self.login_user(store_staff_user)
            uid = user_object['uid']
            response_data = Struct(response.json)
            user = self.userService.get_user(uid, True)
            self.assertIsNotNone(response_data)
            self.assertTrue(response_data.status)
            self.assertEqual(user.fullname, post_data['fullname'])
            self.assertEqual(user.email, post_data['email'])

    def test_add_store_staff_by_store_support_staff(self):
        with self.client:
            store_owner_user = "user@gmail.com"
            store_support_user = "support_store@gmail.com"
            store_staff_user = self.fake.ascii_company_email()
            store_info = self.create_store(store_owner_user, self.fake.name())
            self.create_user(store_support_user, self.fake.name(), [RolesTypes.StoreSupport.value], False, store_info.data.info.store_code)
            user_object = self.login_user(store_support_user)
            token = user_object['idToken']
            uid = user_object['uid']
            post_data = {
                'email': store_staff_user,
                'password': self.global_password,
                'roles': [RolesTypes.StoreSupport.value, RolesTypes.StoreReport.value],
                'fullname': self.fake.name(),

            }
            response = self.request_post('/api/user/staff/%s' % store_info.data.info.store_code, token, None, None, post_data)
            self.assertRequestPassed(response, 'update store staff user request failed')

            user_object = self.login_user(store_staff_user)
            uid = user_object['uid']
            response_data = Struct(response.json)
            user = self.userService.get_user(uid, True)
            self.assertIsNotNone(response_data)
            self.assertTrue(response_data.status)
            self.assertEqual(user.fullname, post_data['fullname'])
            self.assertEqual(user.email, post_data['email'])

    def test_add_store_staff_by_store_platform_staff(self):
        with self.client:
            store_owner_user = "user@gmail.com"
            store_staff_user = self.fake.ascii_company_email()
            store_info = self.create_store(store_owner_user, self.fake.name())
            user_object = self.login_user(self.platform_support_user)
            token = user_object['idToken']
            uid = user_object['uid']
            post_data = {
                'email': store_staff_user,
                'password': self.global_password,
                'roles': [RolesTypes.StoreSupport.value, RolesTypes.StoreReport.value],
                'fullname': self.fake.name(),
            }
            response = self.request_post('/api/user/staff/%s' % store_info.data.info.store_code, token, None, None, post_data)
            self.assertRequestPassed(response, 'update store staff user request failed')

            user_object = self.login_user(store_staff_user)
            uid = user_object['uid']
            response_data = Struct(response.json)
            user = self.userService.get_user(uid, True)
            self.assertIsNotNone(response_data)
            self.assertTrue(response_data.status)
            self.assertEqual(user.fullname, post_data['fullname'])
            self.assertEqual(user.email, post_data['email'])

    def test_add_store_staff_by_store_support_staff_invalid_store(self):
        with self.client:
            store_owner_user = "user@gmail.com"
            store_owner_user1 = "user1@gmail.com"
            store_support_user = self.fake.ascii_company_email()
            store_staff_user = self.fake.ascii_company_email()
            store_info = self.create_store(store_owner_user, self.fake.name())
            diff_store_info = self.create_store(store_owner_user1, self.fake.name())
            self.create_user(store_support_user, self.fake.name(), [RolesTypes.StoreSupport.value], False, diff_store_info.data.info.store_code)
            user_object = self.login_user(store_support_user)
            token = user_object['idToken']
            uid = user_object['uid']
            post_data = {
                'email': store_staff_user,
                'password': self.global_password,
                'roles': [RolesTypes.StoreSupport.value, RolesTypes.StoreReport.value],
                'fullname': self.fake.name(),

            }
            response = self.request_post('/api/user/staff/%s' % store_info.data.info.store_code, token, None, None, post_data)
            self.assert400(response, 'update store staff user request passed with invalid user store entered (diff store_code)')

    # endregion

    def test_get_user_object(self):
        with self.client:
            user_object = self.login_user(self.platform_owner_user)
            uid = user_object['uid']
            token = user_object['idToken']
            display_name = user_object['display_name']
            response = self.request_get('/api/user/{}'.format(uid), token)
            self.assertRequestPassed(response, 'get user request failed')
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
            self.assertEqual(response_data.data.user_data.email, user.email)
            self.assertEqual(response_data.data.user_data.fullname, user.fullname)
            self.assertEqual(response_data.data.user_data.roles[0].name, user.roles[0].name)


if __name__ == '__main__':
    unittest.main()
