import unittest

from kv_config_reader.filler import *


class TestBaseFiller(unittest.TestCase):

    def setUp(self) -> None:
        self.f = BaseFiller()

    def test_fill(self):
        with self.assertRaises(NotImplementedError) as _asRa:
            self.f.fill({}, {})


if __name__ == '__main__':
    unittest.main()
