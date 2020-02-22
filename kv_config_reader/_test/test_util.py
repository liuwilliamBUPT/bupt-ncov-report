import unittest

from kv_config_reader._util import *


class TestUtil(unittest.TestCase):

    def test_parseEnvAsType_EmptyStr_int(self):
        self.assertEqual(parse_env_as_type('', int), None)

    def test_parseEnvAsType_233_int(self):
        self.assertEqual(parse_env_as_type('233', int), 233)

    def test_parseEnvAsType_Text_int(self):
        self.assertEqual(parse_env_as_type('text', int), None)

    def test_parseEnvAsType_Text_str(self):
        self.assertEqual(parse_env_as_type('text', str), 'text')

    def test_parseEnvAsType_EmptyStr_bool(self):
        self.assertEqual(parse_env_as_type('', bool), False)

    def test_parseEnvAsType_0_bool(self):
        self.assertEqual(parse_env_as_type('0', bool), True)

    def test_parseEnvAsType_abc_bool(self):
        self.assertEqual(parse_env_as_type('abc', bool), True)


if __name__ == '__main__':
    unittest.main()
