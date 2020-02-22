import unittest

from bupt_ncov_report.program_utils import *
from bupt_ncov_report.pure_utils import *

POST_DATA_NORMAL = {
    'address': 'abc',
    'area': '',
    'bztcyy': '1',
    'city': '',
    'created': '1141141919',
    'created_uid': '0',
    'date': '20770101',
    'fjsj': '0',
    'fxyy': '',
    'geo_api_info': 'ghi',
    'glksrq': '',
    'gllx': '',
    'gwszdd': '',
    'id': '114514',
    'jcbhlx': '',
    'jcbhrq': '',
    'jchbryfs': '',
    'jcjg': '',
    'jcjgqr': '0',
    'jcqzrq': '',
    'jcwhryfs': '',
    'jhfjhbcc': '',
    'jhfjjtgj': '',
    'jhfjrq': '',
    'jhfjsftjhb': '0',
    'jhfjsftjwh': '0',
    'jrdqjcqk': [],
    'jrdqtlqk': [],
    'jrsfqzfy': '',
    'jrsfqzys': '',
    'province': 'def',
    'qksm': '',
    'remark': '',
    'sfcxtz': '0',
    'sfcxzysx': '0',
    'sfcyglq': '0',
    'sfjcbh': '0',
    'sfjchbry': '0',
    'sfjcqz': '',
    'sfjcwhry': '0',
    'sfsfbh': '0',
    'sftjhb': '0',
    'sftjwh': '0',
    'sfyqjzgc': '',
    'sfyyjc': '0',
    'sfzx': '0',
    'szgj': '',
    'tw': '3',
    'uid': '1919',
    'xjzd': '北京',
}

POST_DATA_SICK_ITEMS = {
    'jcjgqr': 1,
    'remark': '不出门，我浑身难受',
    'sfcxtz': 1,
    'sfcxzysx': 1,
    'sfcyglq': 1,
    'sfjcbh': 1,
    'sfjchbry': 1,
    'sfjcwhry': 1,
    'sftjhb': 1,
    'sftjwh': 1,
    'sfyyjc': 1,
    'tw': 6,
}


class Test_ProgramUtils_SimpleFunc(unittest.TestCase):
    """测试 ProgramUtils 中的简单函数。"""

    def setUp(self) -> None:
        self.u = ProgramUtils(PureUtils())

    def test_extractPostData_normal(self):
        """测试其能匹配出 post data，且能把新数据覆盖到旧数据上。"""
        html = '''
            var def = {"fuck": 0, "shit": 114514, "damn": "NV4NDt6ZXhJfCq5gBM2PYkz48GMkZmvraq5bqW7dP2VMNMYx"};
            var app = new Vue({
                data: {
                    oldInfo: {"fuck": "s53PuPRbqxQwYCrDy8BW3TGG6mzPYTzQF8DM95eZ9EKhVxku", "shit": "1"},
                }
            })
        '''
        post_data = self.u.extract_post_data(html)
        self.assertEqual(post_data, {
            'fuck': 0,
            'shit': 114514,
            'damn': 'NV4NDt6ZXhJfCq5gBM2PYkz48GMkZmvraq5bqW7dP2VMNMYx',
        })

    def test_extractPostData_too_short(self):
        """太短时要抛出异常。"""
        html = '''
            var def = {"a": 0};
            var app = new Vue({
                data: {
                    oldInfo: {"b": "1"},
                }
            })
        '''

        with self.assertRaises(Exception) as _asRa:
            self.u.extract_post_data(html)

    def test_propertyToPinyin(self):
        self.assertEqual(
            self.u.property_to_pinyin('注意患病人员途经湖北出事接触医院检查人员是否是人'),
            'zyhbrytjhbcsjcyyjcrysfsr'
        )


class Test_ProgramUtils_StopWhenSick(unittest.TestCase):
    """测试与「生病时停止有关」的函数。"""

    def setUp(self) -> None:
        self.u = ProgramUtils(PureUtils())

    def test_isDataBroken_normal(self):
        """普通情况"""
        self.assertFalse(self.u.is_data_broken(POST_DATA_NORMAL))

    def test_isDataBroken_1Lack(self):
        """缺一个属性"""
        data = POST_DATA_NORMAL.copy()

        for key in POST_DATA_SICK_ITEMS.keys():
            del data[key]
            self.assertTrue(self.u.is_data_broken(data))
            data[key] = POST_DATA_NORMAL[key]
            self.assertFalse(self.u.is_data_broken(data))

    def test_isDataBroken_2Lack(self):
        """缺两个属性"""
        data = POST_DATA_NORMAL.copy()

        for i, key in enumerate(POST_DATA_SICK_ITEMS.keys()):
            if i == 0:
                # 删掉第一个属性，之后不补充
                del data[key]
                continue

            # 从第二个属性开始删掉之后要补充
            del data[key]
            self.assertTrue(self.u.is_data_broken(data))
            data[key] = POST_DATA_NORMAL[key]
            self.assertTrue(self.u.is_data_broken(data))

    def test_dataSickReport_checkDataSick_normal(self):
        self.assertEqual(
            self.u.data_sick_report(POST_DATA_NORMAL),
            [],
        )
        self.u.check_data_sick(POST_DATA_NORMAL)

    def test_dataSickReport_checkDataSick_1Anomaly(self):
        """一个属性异常"""
        data = POST_DATA_NORMAL.copy()

        for i, key in enumerate(POST_DATA_SICK_ITEMS.keys()):
            data[key] = POST_DATA_SICK_ITEMS[key]
            self.assertEqual(len(self.u.data_sick_report(data)), 1)
            with self.assertRaises(Exception) as _asRa:
                self.u.check_data_sick(data)

            data[key] = POST_DATA_NORMAL[key]
            self.assertEqual(self.u.data_sick_report(data), [])
            self.u.check_data_sick(data)

    def test_dataSickReport_checkDataSick_2Anomaly(self):
        """两个属性异常"""
        data = POST_DATA_NORMAL.copy()

        for i, key in enumerate(POST_DATA_SICK_ITEMS.keys()):
            if i == 0:
                data[key] = POST_DATA_SICK_ITEMS[key]
                continue

            data[key] = POST_DATA_SICK_ITEMS[key]
            self.assertEqual(len(self.u.data_sick_report(data)), 2)
            with self.assertRaises(Exception) as _asRa:
                self.u.check_data_sick(data)

            data[key] = POST_DATA_NORMAL[key]
            self.assertEqual(len(self.u.data_sick_report(data)), 1)
            with self.assertRaises(Exception) as _asRa:
                self.u.check_data_sick(data)

    def test_dataSickReport_correct(self):
        """检测改变 sfjcbh 属性时，报告中是否有「是否接触病患」"""
        data = POST_DATA_NORMAL.copy()
        data['sfjcbh'] = 1

        sick_report = self.u.data_sick_report(data)
        self.assertEqual(len(sick_report), 1)

        shjcbh_report = sick_report[0]
        self.assertIn('是否接触病患', shjcbh_report)


if __name__ == '__main__':
    unittest.main()
