# test/test_ws_ping.py
import unittest
from test.common.Basecase import BaseTestCase


class FlaskTestCase(BaseTestCase):
    def test_ws_ping_noauth(self):
        namespace = "/ping"
        self.ws_renew_connection(namespace)
        global request_event_data
        request_event_data = None
        self.ws_client.get_received(namespace)
        data = {'nickname': 'foo', 'password': 'bar'}
        self.ws_client.emit('pong', data, namespace=namespace)
        recvd = self.ws_client.get_received(namespace)
        print(recvd)
        self.assertEqual(len(recvd), 1)
        self.assertEqual(recvd[0]['args'][0]['data']['nickname'], data['nickname'])
        self.assertEqual(recvd[0]['args'][0]['data']['password'], data['password'])
        self.assertTrue(recvd[0]['args'][0]['status'])
