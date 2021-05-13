# tests/test_basic.py

import unittest

from src.models import User
from test.common.Basecase import BaseTestCase


class FlaskTestCase(BaseTestCase):

    # Ensure that Flask was set up correctly
    def test_register_user(self):
        with self.client:
            uid = self.Firebase_UID
            response = self.client.post(
                '/api/user/%s' % uid,
                data=dict(),
                headers=dict(
                    Authorization='Bearer ' + 'abc'
                ),
                content_type='application/json'
            )
            self.assertEqual(response.status_code, 200)
            user = User.query.filter_by(uid=uid).first()
            self.assertIsNotNone(user)


if __name__ == '__main__':
    unittest.main()
