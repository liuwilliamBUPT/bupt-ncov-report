__all__ = (
    'PureUtils',
)

import re
from typing import Any, Tuple


class PureUtils:
    """与疫情上报网站无关的工具函数。"""

    def is_number_data_in_range(self, data: Any, range: Tuple[int, int]) -> bool:
        """
        检查 data 所表示的十进制数字是否在 range 所表示的前闭后开区间内。
        :param data: 数字，或可转换为数字的类型
        :param range: 前闭后开区间
        :return: True/False 表示是/否在区间内
        """
        if not isinstance(data, int):
            try:
                data = int(data)
            except:
                return False

        return range[0] <= data < range[1]

    def match_re_group1(self, re_str: str, text: str) -> str:
        """
        在 text 中匹配正则表达式 re_str，返回第 1 个捕获组（即首个用括号包住的捕获组）
        :param re_str: 正则表达式（字符串）
        :param text: 要被匹配的文本
        :return: 第 1 个捕获组
        """
        match = re.search(re_str, text)
        if match is None:
            raise ValueError(f'在文本中匹配 {re_str} 失败，没找到任何东西。\n请阅读脚本文档中的「使用前提」部分。')

        return match.group(1)
