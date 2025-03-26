# tests/test_jwt_util.py

import os
import unittest
from datetime import timedelta
from app. utils.jwt_util import create_access_token, verify_access_token

class TestJWTUtil(unittest.TestCase):
    def setUp(self):
        if "SECRET_KEY" in os.environ:
            del os.environ["SECRET_KEY"]
        self.default_secret_key = "happycat"

    def test_create_and_verify_token(self):
        data = {"sub": "testuser"}
        token = create_access_token(data, expires_delta=timedelta(minutes=1))
        payload = verify_access_token(token)
        self.assertEqual(payload["sub"], "testuser")

if __name__ == "__main__":
    unittest.main()
