import unittest

from bupt_ncov_report.pure_utils import *


class Test_PureUtils(unittest.TestCase):

    def setUp(self) -> None:
        self.u = PureUtils()

    def test_isNumberDataInRange_None(self):
        self.assertFalse(self.u.is_number_data_in_range(None, (-1, 1)))

    def test_isNumberDataInRange_EmptyStr(self):
        self.assertFalse(self.u.is_number_data_in_range('', (-1, 1)))

    def test_isNumberDataInRange_Hex_1(self):
        self.assertFalse(self.u.is_number_data_in_range('0X1A', (0, 32)))

    def test_isNumberDataInRange_Hex_2(self):
        self.assertFalse(self.u.is_number_data_in_range('1A', (0, 32)))

    def test_isNumberDataInRange_Text(self):
        self.assertFalse(self.u.is_number_data_in_range('abc', (0, 32)))

    def test_isNumberDataInRange_UpperBound(self):
        self.assertFalse(self.u.is_number_data_in_range(100, (-82, 100)))

    def test_isNumberDataInRange_NumInStr(self):
        self.assertTrue(self.u.is_number_data_in_range('233', (0, 1000)))

    def test_isNumberDataInRange_LowerBound(self):
        self.assertTrue(self.u.is_number_data_in_range('-82', (-82, 100)))

    def test_matchReGroup1_1Group(self):
        with self.assertRaises(BaseException) as _ctxt:
            self.u.match_re_group1(r'abc(\d+)def', 'abcdef')

        self.assertEqual(self.u.match_re_group1(r'abc(\d+)def', 'abc1234def'), '1234')

    def test_matchReGroup1_2Group(self):
        self.assertEqual(self.u.match_re_group1(r'abc(\d+)(def)', 'abc1234def'), '1234')


if __name__ == '__main__':
    unittest.main()
