__all__ = (
    'parse_env_as_type',
)

from typing import Optional, Type

from ..predef import *


def parse_env_as_type(
        text: str,
        target_type: Type[SupportedConfigType],
) -> Optional[SupportedConfigType]:
    """
    将字符串 text 解析为目标类型。目前支持 str、int、bool。
    当无法解析为目标类型时，返回 None。

    :param text: 要解析的字符串
    :param target_type: 目标类型
    :return: 目标类型的值
    """
    if target_type is int:
        try:
            return int(text)
        except:
            return None
    elif target_type is bool:
        return True if text != '' else False
    elif target_type is str:
        return text

    assert False
