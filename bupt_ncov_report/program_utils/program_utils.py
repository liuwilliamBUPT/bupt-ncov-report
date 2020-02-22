__all__ = (
    'ProgramUtils',
)

import json
import logging
from typing import Any, Dict, List

from ..constant import *
from ..pure_utils import *

logger = logging.getLogger(__name__)


class ProgramUtils:
    """关系到疫情上报网站的具体逻辑的工具函数。"""

    def __init__(
            self,
            pure_utils: PureUtils,
    ):
        self.pure_util = pure_utils

    def extract_post_data(self, html: str) -> Dict[str, str]:
        """
        从上报页面的 HTML 中，提取出上报 API 所需要填写的参数。
        :return: 最终 POST 的参数（使用 dict 表示）
        """
        new_data = self.pure_util.match_re_group1(r'var def = (\{.+\});', html)
        old_data = self.pure_util.match_re_group1(r'oldInfo: (\{.+\}),', html)

        # 检查数据是否足够长
        if len(old_data) < REASONABLE_LENGTH or len(new_data) < REASONABLE_LENGTH:
            raise ValueError('获取到的数据过短。请阅读脚本文档的「使用前提」部分。')

        # 用原页面的「def」变量的值，覆盖掉「oldInfo」变量的值
        old_dict, new_dict = json.loads(old_data), json.loads(new_data)
        old_dict.update(new_dict)
        return old_dict

    def is_data_broken(self, data: Dict[str, Any]) -> bool:
        """
        检查最终上报数据内容是否破损（指出现不可能出现的值）
        （如果破损，可能是上报页面改版。）
        :param data: 最终上报的数据
        :return: True/False 表示是/否破损
        """
        # self.pure_util 太长了
        util = self.pure_util

        # 「其他信息」一栏存在
        if 'remark' not in data:
            return True

        # `tw` 数据必须在 1 到 9 之间
        if not util.is_number_data_in_range(data.get('tw'), (1, 10)):
            return True

        # `jcjgqr` 必须在 0 到 3 之间
        if not util.is_number_data_in_range(data.get('jcjgqr'), (0, 4)):
            return True

        # 值为 0 或 1 的属性
        BINARY_PROPERTIES = (
            'sftjwh', 'sftjhb', 'sfcxtz', 'sfyyjc',
            'sfjcwhry', 'sfjchbry', 'sfjcbh', 'sfcyglq', 'sfcxzysx',
        )

        for prop in BINARY_PROPERTIES:
            if not util.is_number_data_in_range(data.get(prop), (0, 2)):
                return True

        return False

    def property_to_pinyin(self, prop: str) -> str:
        """
        将属性转换为其对应的汉语拼音缩写（仅支持有限字符，且不检查字符是否在范围内）
        本函数是为了适应开发者的英文水平而产生的。详见：https://github.com/Liadrinz/waibao-script

        :param prop: 中文属性（如：是否途径武汉）
        :return: 汉语拼音缩写（如：sftjwh）
        """
        mapper = {x: y for x, y in zip(
            '事于人体出北医否员处征患意接是期查检武汉注湖现病离经触途院隔项',
            'syrtcbyfyczhyjsqcjwhzhxbljctygx',
        )}
        return ''.join(mapper[x] for x in prop)

    def data_sick_report(self, data: Dict[str, Any]) -> List[str]:
        """
        检测当前数据中表示生病的项，生成「生病项报告」。
        如：体温 38.5°C，「其他信息」不为空，接触过疑似确诊人群等。

        本函数假设 data 为经过检测的，未破损的数据。
        :param data: 最终上报的数据
        :return: str 数组，其中每一条为一个异常项。无异常则为空 list
        """

        abnormal_items = []

        # 体温：>= 37°C 则为异常
        body_temp = int(data['tw'])
        if body_temp > 3:
            abnormal_items.append('您上一次填报了高于 37 度的体温')

        current_situation = int(data['jcjgqr'])
        if current_situation != 0:
            abnormal_items.append('您当前状态为疑似感染/确诊感染/其他')

        if isinstance(data['remark'], str) and data['remark'].strip() != '':
            abnormal_items.append('您的「其他信息」一栏不为空')

        BINARY_PROPERTIES = (
            '是否途经武汉',
            '是否途经湖北',
            '是否出现体征',
            '是否医院检查',
            '是否接触武汉人员',
            '是否接触湖北人员',
            '是否接触病患',
            '是否处于隔离期',
            '是否出现注意事项',
        )

        for prop in BINARY_PROPERTIES:
            pinyin_prop = self.property_to_pinyin(prop)
            if int(data[pinyin_prop]) == 1:
                abnormal_items.append(f'「{prop}」，您填了「是」')

        return abnormal_items

    def check_data_sick(self, data: Dict[str, Any]) -> None:
        """
        如果提交的数据表明用户生病，则抛出异常。
        :param data: 最终提交数据
        :return: None
        """
        # 获取生病列表
        sick_list = self.data_sick_report(data)
        if len(sick_list) == 0:
            return

        # 格式化生病列表
        err_msg: List[str] = ['\n您上一次填报的数据中，以下数据异常：\n']
        for i in sick_list:
            err_msg.append('· ' + i)
        err_msg.append('\n由于您开启了 STOP_WHEN_SICK 配置，且检测到您数据为生病数据，自动上报失败；您需要手动上报。')

        raise RuntimeError('\n'.join(err_msg))
