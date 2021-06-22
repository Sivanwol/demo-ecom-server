# test/test_store.py
import unittest

from src.utils.general import Struct
from test.common.Basecase import BaseTestCase
from src.utils.enums import RolesTypes


class FlaskTestCase(BaseTestCase):
    user_owner = 'store2.owner@store.user'
    store_owner_user = 'store.owner@store.user'

    def test_create_store(self):
        with self.client:
            self.create_user(self.store_owner_user, self.fake.name(), [RolesTypes.StoreOwner.value], True)
            user_object = self.login_user(self.platform_owner_user)
            uid = user_object['uid']
            token = user_object['idToken']
            user = self.userService.get_user(uid, True)
            self.assertIsNone(user.store_code)
            store_name = self.fake.company()
            currency_code = 'USD'
            post_data = {
                'name': store_name,
                'description': 'store description',
                'currency_code': currency_code
            }
            response = self.request_post('/api/store/%s/create' % uid, token, None, None, post_data)
            self.assert200(response, 'create store request failed')
            response_data = Struct(response.json)
            self.assertIsNotNone(response_data)
            self.assertTrue(response_data.status)
            self.assertNotEqual(response_data.data.info.store_code, '')
            store = self.storeService.get_store(uid, response_data.data.info.store_code, True)
            user = self.userService.get_user(uid, True)
            self.assertIsNotNone(user)
            self.assertIsNotNone(store)
            self.assertTrue(response_data.status)
            self.assertIsNotNone(response_data.data)
            self.assertIsNotNone(response_data.data.info)
            self.assertIsNotNone(response_data.data.locations)
            self.assertEqual(response_data.data.info.store_code, store.store_code)
            self.assertEqual(user.store_code, store.store_code)
            self.assertEqual(response_data.data.info.name, store.name)
            self.assertEqual(response_data.data.info.default_currency_code, store.default_currency_code)
            self.assertEqual(len(response_data.data.locations), 0)
            self.assertEqual(len(response_data.data.hours), 0)
            path = self.fileSystemService.get_folder_path('stores', store.store_code)
            self.assertIsNotNone(path)
            self.assertTrue(self.fileSystemService.acutal_folder_existed(path))

    def test_freeze_store(self):
        with self.client:
            self.create_user(self.user_owner, self.fake.name(), [RolesTypes.StoreOwner.value], True)
            user_object = self.login_user(self.platform_owner_user)
            store_user_object = self.login_user(self.user_owner)
            uid = store_user_object['uid']
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
            self.assert200(response, 'create store request failed')
            response_data = Struct(response.json)
            self.assertIsNotNone(response_data)
            self.assertTrue(response_data.status)
            self.assertIsNotNone(response_data.data)
            self.assertIsNotNone(response_data.data.info)
            self.assertIsNotNone(response_data.data.info)
            self.assertNotEqual(response_data.data.info.store_code, '')
            store_code = response_data.data.info.store_code
            self.assertNotEqual(store_code, '')
            store = self.storeService.get_store(uid, store_code, True)
            self.assertIsNotNone(store)
            self.assertIsNotNone(response_data.data)
            self.assertEqual(user.store_code, store.store_code)
            response = self.request_delete('/api/store/{}/{}'.format(uid, user.store_code), token)
            self.assert200(response, 'create store request failed')
            store = self.storeService.get_store(uid, store_code, True)
            user = self.userService.get_user(uid, True)
            self.assertTrue(store.is_maintenance)
            self.assertFalse(user.is_active)

    def test_toggle_store_maintenance(self):
        with self.client:
            self.create_user(self.user_owner, self.fake.name(), [RolesTypes.StoreOwner.value], True)
            user_object = self.login_user(self.platform_owner_user)
            store_user_object = self.login_user(self.user_owner)
            uid = store_user_object['uid']
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
            self.assert200(response, 'create store request failed')
            response_data = Struct(response.json)
            self.assertIsNotNone(response_data)
            self.assertTrue(response_data.status)
            self.assertIsNotNone(response_data.data)
            self.assertIsNotNone(response_data.data.info)
            self.assertIsNotNone(response_data.data.info)
            self.assertNotEqual(response_data.data.info.store_code, '')
            store_code = response_data.data.info.store_code
            store = self.storeService.get_store(uid, store_code, True)
            self.assertIsNotNone(store)
            self.assertIsNotNone(response_data.data)
            self.assertFalse(store.is_maintenance)
            self.assertEqual(user.store_code, store.store_code)
            response = self.request_put('/api/store/{}/{}/toggle/maintenance'.format(uid, user.store_code), token)
            self.assert200(response, 'toggle maintenance store request failed')
            store = self.storeService.get_store(uid, store_code, True)
            self.assertTrue(store.is_maintenance)

    def test_get_store_info(self):
        with self.client:
            self.create_user(self.user_owner, self.fake.name(), [RolesTypes.StoreOwner.value], True)
            user_object = self.login_user(self.platform_owner_user)
            store_user_object = self.login_user(self.user_owner)
            uid = store_user_object['uid']
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
            self.assert200(response, 'create store request failed')
            response_data = Struct(response.json)
            self.assertIsNotNone(response_data)
            self.assertTrue(response_data.status)
            self.assertIsNotNone(response_data.data)
            self.assertIsNotNone(response_data.data.info)
            self.assertIsNotNone(response_data.data.info)
            self.assertNotEqual(response_data.data.info.store_code, '')
            store_code = response_data.data.info.store_code
            self.assertNotEqual(store_code, '')

            store_code = response_data.data.info.store_code
            user_object = self.login_user(self.platform_support_user)
            token = user_object['idToken']
            locations = [
                {'lat': 0, 'lng': 0, 'address': 'hagat', 'city': 'ramat fam', 'country_code': 'IL', 'is_close': False},
                {'address': 'hagat', 'city': 'ramat fam', 'country_code': 'IL', 'is_close': True},
            ]
            response = self.request_post('/api/store/{}/{}/locations'.format(uid, store_code), token, None, None, locations)
            self.assert200(response, 'update store loocation request failed')
            hours = [
                {'day': 1, 'location_id': None, 'from_time': 8, 'to_time': 21, 'is_open_24': False, 'is_close': False},
                {'day': 2, 'location_id': None, 'from_time': 8, 'to_time': 20, 'is_open_24': False, 'is_close': False},
                {'day': 3, 'location_id': None, 'from_time': 8, 'to_time': 18, 'is_open_24': False, 'is_close': False},
                {'day': 4, 'location_id': None, 'from_time': None, 'to_time': None, 'is_open_24': True, 'is_close': False},
                {'day': 5, 'location_id': None, 'from_time': 8, 'to_time': 17, 'is_open_24': False, 'is_close': False},
                {'day': 6, 'location_id': None, 'from_time': None, 'to_time': None, 'is_open_24': False, 'is_close': False},
                {'day': 7, 'location_id': None, 'from_time': None, 'to_time': None, 'is_open_24': False, 'is_close': True},
            ]
            response = self.request_post('/api/store/{}/{}/hours'.format(uid, store_code), token, None, None, hours)
            self.assert200(response, 'update store hours request failed')
            response_data = Struct(response.json)
            self.assertIsNotNone(response_data)
            self.assertTrue(response_data.status)
            response = self.request_get('/api/store/{}/info'.format(store_code), token)
            self.assert200(response, 'get store info request failed')
            response_data = Struct(response.json)
            store = self.storeService.get_store_by_status_code(store_code)
            self.assertIsNotNone(response_data)
            self.assertTrue(response_data.status)
            self.assertIsNotNone(response_data.data)
            self.assertIsNotNone(response_data.data.info)
            self.assertIsNotNone(response_data.data.locations)
            self.assertEqual(response_data.data.info.store_code, store_code)
            self.assertEqual(user.store_code, store_code)
            self.assertEqual(response_data.data.info.name, store['info']['name'])
            self.assertEqual(response_data.data.info.default_currency_code, store['info']['default_currency_code'])
            self.assertEqual(len(response_data.data.locations), 2)
            self.assertEqual(len(response_data.data.hours), 7)
            self.assertListEqual(response.json['data']['locations'], store['locations'])
            self.assertListEqual(response.json['data']['hours'], store['hours'])

    def test_update_hours(self):
        self.create_user(self.user_owner, self.fake.name(), [RolesTypes.StoreOwner.value], True)
        user_object = self.login_user(self.platform_owner_user)
        store_user_object = self.login_user(self.user_owner)
        uid = store_user_object['uid']
        token = user_object['idToken']
        user = self.userService.get_user(uid, True)
        self.assertIsNone(user.store_code)
        store_name = self.fake.company()
        currency_code = 'USD'
        post_data = {
            'name': store_name,
            'description': 'store description',
            'currency_code': currency_code
        }
        response = self.request_post('/api/store/%s/create' % uid, token, None, None, post_data)
        self.assert200(response, 'create store request failed')
        response_data = Struct(response.json)
        self.assertIsNotNone(response_data)
        self.assertTrue(response_data.status)
        self.assertIsNotNone(response_data.data)
        self.assertIsNotNone(response_data.data.info)
        self.assertIsNotNone(response_data.data.info)
        self.assertNotEqual(response_data.data.info.store_code, '')
        store_code = response_data.data.info.store_code
        self.assertNotEqual(store_code, '')

        store_code = response_data.data.info.store_code
        user_object = self.login_user(self.platform_support_user)
        token = user_object['idToken']
        hours = [
            {'day': 1, 'location_id': None, 'from_time': 8, 'to_time': 21, 'is_open_24': False, 'is_close': False},
            {'day': 2, 'location_id': None, 'from_time': 8, 'to_time': 20, 'is_open_24': False, 'is_close': False},
            {'day': 3, 'location_id': None, 'from_time': 8, 'to_time': 18, 'is_open_24': False, 'is_close': False},
            {'day': 4, 'location_id': None, 'from_time': None, 'to_time': None, 'is_open_24': True, 'is_close': False},
            {'day': 5, 'location_id': None, 'from_time': 8, 'to_time': 17, 'is_open_24': False, 'is_close': False},
            {'day': 6, 'location_id': None, 'from_time': None, 'to_time': None, 'is_open_24': False, 'is_close': False},
            {'day': 7, 'location_id': None, 'from_time': None, 'to_time': None, 'is_open_24': False, 'is_close': True},
        ]
        response = self.request_post('/api/store/{}/{}/hours'.format(uid, store_code), token, None, None, hours)
        self.assert200(response, 'update store hours request failed')
        response_data = Struct(response.json)

        store = self.storeService.get_store_by_status_code(store_code)
        self.assertIsNotNone(response_data)
        self.assertTrue(response_data.status)
        self.assertIsNotNone(response_data.data)
        self.assertIsNotNone(response_data.data.info)
        self.assertIsNotNone(response_data.data.locations)
        self.assertEqual(response_data.data.info.store_code, store_code)
        self.assertEqual(user.store_code, store_code)
        self.assertEqual(response_data.data.info.name, store['info']['name'])
        self.assertEqual(response_data.data.info.default_currency_code, store['info']['default_currency_code'])
        self.assertEqual(len(response_data.data.locations), 0)
        self.assertEqual(len(response_data.data.hours), 7)
        self.assertListEqual(response.json['data']['hours'], store['hours'])

    def test_get_stores(self):
        with self.client:
            user_owner_secand = 'user_owner_2@store.us'
            self.create_user(self.user_owner, self.fake.name(), [RolesTypes.StoreOwner.value], True)
            self.create_user(user_owner_secand, self.fake.name(), [RolesTypes.StoreOwner.value], True)
            user_object = self.login_user(self.platform_owner_user)
            store_user_object = self.login_user(self.user_owner)
            uid = store_user_object['uid']
            token = user_object['idToken']
            user = self.userService.get_user(uid, True)
            self.assertIsNone(user.store_code)
            store_name = self.fake.company()
            currency_code = self.fake.currency_code()
            post_data = {
                'name': store_name + '_1',
                'description': 'store description',
                'currency_code': currency_code
            }
            response = self.request_post('/api/store/%s/create' % uid, token, None, None, post_data)
            self.assert200(response, 'create store #1 request failed')
            response_data = Struct(response.json)
            self.assertIsNotNone(response_data)
            self.assertTrue(response_data.status)
            self.assertIsNotNone(response_data.data)
            self.assertIsNotNone(response_data.data.info)
            self.assertIsNotNone(response_data.data.info)
            self.assertNotEqual(response_data.data.info.store_code, '')

            store_user_object = self.login_user(user_owner_secand)
            uid = store_user_object['uid']
            post_data = {
                'name': store_name + '_2',
                'description': 'store description',
                'currency_code': currency_code
            }
            response = self.request_post('/api/store/%s/create' % uid, token, None, None, post_data)
            self.assert200(response, 'create store #2 request failed')
            self.assertIsNotNone(response_data)
            self.assertTrue(response_data.status)
            self.assertIsNotNone(response_data.data)
            self.assertIsNotNone(response_data.data.info)
            self.assertIsNotNone(response_data.data.info)
            self.assertNotEqual(response_data.data.info.store_code, '')

            response = self.request_get('/api/store/list', token)

            self.assert200(response, 'get stores list request failed')
            response_data = Struct(response.json)
            stores = self.storeService.get_stores()
            self.assertIsNotNone(response_data)
            self.assertTrue(response_data.status)
            self.assertIsNotNone(response_data.data)
            self.assertEqual(len(stores), len(response_data.data))
            self.assertListEqual(response.json['data'], stores)

    def test_update_zero_locations(self):
        with self.client:
            self.create_user(self.user_owner, self.fake.name(), [RolesTypes.StoreOwner.value], True)
            user_object = self.login_user(self.platform_owner_user)
            store_user_object = self.login_user(self.user_owner)
            uid = store_user_object['uid']
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
            self.assert200(response, 'create store request failed')
            response_data = Struct(response.json)
            self.assertIsNotNone(response_data)
            self.assertTrue(response_data.status)
            self.assertIsNotNone(response_data.data)
            self.assertIsNotNone(response_data.data.info)
            self.assertIsNotNone(response_data.data.info)
            self.assertNotEqual(response_data.data.info.store_code, '')
            store_code = response_data.data.info.store_code
            user_object = self.login_user(self.platform_support_user)
            token = user_object['idToken']
            locations = [
                {'lat': 0, 'lng': 0, 'address': 'hagat', 'city': 'ramat fam', 'country_code': 'IL', 'is_close': False},
                {'address': 'hagat', 'city': 'ramat fam', 'country_code': 'IL', 'is_close': True},
            ]

            response = self.request_post('/api/store/{}/{}/locations'.format(uid, store_code), token, None, None, locations)
            self.assert200(response, 'update store loocation request failed')
            response_data = Struct(response.json)
            store = self.storeService.get_store_by_status_code(store_code, True)
            self.assertIsNotNone(response_data)
            self.assertTrue(response_data.status)
            self.assertIsNotNone(response_data.data)
            self.assertEqual(response_data.data.info.store_code, store.store_code)
            self.assertEqual(user.store_code, store.store_code)
            self.assertEqual(response_data.data.info.name, store.name)
            self.assertEqual(response_data.data.info.default_currency_code, store.default_currency_code)
            self.assertEqual(len(response_data.data.locations), 2)
            locations = []
            response = self.request_post('/api/store/{}/{}/locations'.format(uid, store_code), token, None, None, locations)
            self.assert200(response, 'update store loocation request failed')
            response_data = Struct(response.json)
            store = self.storeService.get_store_by_status_code(store_code, True)
            user = self.userService.get_user(uid, True)
            self.assertIsNotNone(response_data)
            self.assertTrue(response_data.status)
            self.assertIsNotNone(response_data.data)
            self.assertEqual(response_data.data.info.store_code, store.store_code)
            self.assertEqual(user.store_code, store.store_code)
            self.assertEqual(response_data.data.info.name, store.name)
            self.assertEqual(response_data.data.info.default_currency_code, store.default_currency_code)
            self.assertEqual(len(response_data.data.locations), 0)

    def test_update_locations(self):
        with self.client:
            self.create_user(self.user_owner, self.fake.name(), [RolesTypes.StoreOwner.value], True)
            user_object = self.login_user(self.platform_owner_user)
            store_user_object = self.login_user(self.user_owner)
            uid = store_user_object['uid']
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
            self.assert200(response, 'create store request failed')
            response_data = Struct(response.json)
            self.assertIsNotNone(response_data)
            self.assertTrue(response_data.status)
            self.assertIsNotNone(response_data.data)
            self.assertIsNotNone(response_data.data.info)
            self.assertIsNotNone(response_data.data.info)
            self.assertNotEqual(response_data.data.info.store_code, '')
            store_code = response_data.data.info.store_code
            user_object = self.login_user(self.platform_support_user)
            token = user_object['idToken']
            locations = [
                {'lat': 0, 'lng': 0, 'address': 'hagat', 'city': 'ramat fam', 'country_code': 'IL', 'is_close': False},
                {'address': 'hagat', 'city': 'ramat fam', 'country_code': 'IL', 'is_close': True},
            ]

            response = self.request_post('/api/store/{}/{}/locations'.format(uid, store_code), token, None, None, locations)
            self.assert200(response, 'update store loocation request failed')
            response_data = Struct(response.json)
            store = self.storeService.get_store_by_status_code(store_code)
            user = self.userService.get_user(uid, True)
            self.assertIsNotNone(response_data)
            self.assertTrue(response_data.status)
            self.assertIsNotNone(response_data.data)
            self.assertEqual(response_data.data.info.store_code, store_code)
            self.assertEqual(user.store_code, store_code)
            self.assertEqual(response_data.data.info.name, store['info']['name'])
            self.assertEqual(response_data.data.info.default_currency_code, store['info']['default_currency_code'])
            self.assertEqual(len(response_data.data.locations), 2)
            self.assertListEqual(response.json['data']['locations'], store['locations'])

    def test_update_store_info(self):
        self.create_user(self.user_owner, self.fake.name(), [RolesTypes.StoreOwner.value], True)
        user_object = self.login_user(self.platform_owner_user)
        store_user_object = self.login_user(self.user_owner)
        uid = store_user_object['uid']
        token = user_object['idToken']
        user = self.userService.get_user(uid, True)
        self.assertIsNone(user.store_code)
        store_name = self.fake.company()
        currency_code = 'USD'
        post_data = {
            'name': store_name,
            'description': 'store description',
            'currency_code': currency_code
        }
        response = self.request_post('/api/store/%s/create' % uid, token, None, None, post_data)
        self.assert200(response, 'create store request failed')
        response_data = Struct(response.json)
        self.assertIsNotNone(response_data)
        self.assertTrue(response_data.status)
        self.assertIsNotNone(response_data.data)
        self.assertIsNotNone(response_data.data.info)
        self.assertIsNotNone(response_data.data.info)
        self.assertNotEqual(response_data.data.info.store_code, '')
        user_object = self.login_user(self.platform_support_user)
        token = user_object['idToken']
        store_code = response_data.data.info.store_code
        store_name = self.fake.company()
        currency_code = 'USD'
        post_data = {
            'name': store_name,
            'description': 'store description updated',
            'currency_code': currency_code
        }
        response = self.request_put('/api/store/{}/{}/update'.format(uid, store_code), token, None, None, post_data)

        self.assert200(response, 'update store info request failed')
        response_data = Struct(response.json)
        store = self.storeService.get_store_by_status_code(store_code)
        self.assertIsNotNone(response_data)
        self.assertTrue(response_data.status)
        self.assertIsNotNone(response_data.data)
        self.assertEqual(response_data.data.info.store_code, store_code)
        self.assertEqual(user.store_code, store_code)
        self.assertEqual(response_data.data.info.name, store['info']['name'])
        self.assertEqual(response_data.data.info.default_currency_code, store['info']['default_currency_code'])


if __name__ == '__main__':
    unittest.main()
