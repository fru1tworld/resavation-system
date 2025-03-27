import unittest
from app.utils.bcrypt_util import hash_password, verify_password

class TestPasswordUtil(unittest.TestCase):
    def test_hash_and_verify_password(self):
        plain_password = "mysecretpassword"
        hashed = hash_password(plain_password)
        self.assertTrue(verify_password(plain_password, hashed), "올바른 비밀번호 검증 실패")

    def test_verify_wrong_password(self):
        plain_password = "mysecretpassword"
        wrong_password = "wrongpassword"
        hashed = hash_password(plain_password)
        self.assertFalse(verify_password(wrong_password, hashed), "잘못된 비밀번호가 검증됨")

    def test_hash_produces_different_hashes(self):
        plain_password = "mysecretpassword"
        hashed1 = hash_password(plain_password)
        hashed2 = hash_password(plain_password)
        self.assertNotEqual(hashed1, hashed2, "같은 비밀번호에 대해 동일한 해시가 생성됨")

if __name__ == "__main__":
    unittest.main()
