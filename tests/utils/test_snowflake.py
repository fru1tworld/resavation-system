import time
import unittest
from app.utils import snowflake

class TestSnowflake(unittest.TestCase):
    def setUp(self):
        snowflake.last_timestamp = -1
        snowflake.sequence = 0

    def test_generate_id_type(self):
        id_val = snowflake.generate_snowflake_id()
        self.assertIsInstance(id_val, int)

    def test_generate_id_uniqueness(self):
        ids = set()
        for _ in range(1000):
            id_val = snowflake.generate_snowflake_id()
            self.assertNotIn(id_val, ids)
            ids.add(id_val)

    def test_id_structure(self):
        id_val = snowflake.generate_snowflake_id()

        timestamp_part = id_val >> 22
        machine_id_part = (id_val >> 12) & 0x3FF  
        sequence_part = id_val & snowflake.SEQUENCE_MASK

        current_timestamp = int(time.time() * 1000)
        self.assertTrue(snowflake.EPOCH + timestamp_part <= current_timestamp)
        self.assertEqual(machine_id_part, snowflake.MACHINE_ID)
        self.assertTrue(0 <= sequence_part <= snowflake.SEQUENCE_MASK)

if __name__ == '__main__':
    unittest.main()
