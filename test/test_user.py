# tests/test_basic.py

import unittest

from src.models import User
from test.common.Basecase import BaseTestCase
from test.common.firebase_utils import login_user


class FlaskTestCase(BaseTestCase):

    # Ensure that Flask was set up correctly
    def test_register_user(self):
        user = login_user(self.firebase_user, self.firebase_password)
        token = user['idToken']
        self.assertIsNotNone(token)
        self.assertNotEqual(token, '')
        uid = self.firebase_UID
        response = self.client.post(
            '/api/user/%s' % uid,
            data=dict(),
            headers=dict(
                Authorization='Bearer ' + token
            ),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        user = User.query.filter_by(uid=uid).first()
        self.assertIsNotNone(user)


if __name__ == '__main__':
    unittest.main()
