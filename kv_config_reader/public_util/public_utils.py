__all__ = (
    'initialize_config',
)

from typing import Dict, Mapping, Optional

from ..predef import *


def initialize_config(
        config_schema: Mapping[str, ConfigSchemaItem]
) -> Dict[str, Optional[SupportedConfigType]]:
    """
    用 schema 中的默认值初始化 _conf，返回初始化好的 _conf 对象。
    :param config_schema: schema
    :return: _conf 对象，类型为 dict，键/值为配置名/默认值
    """

    config = {}
    for k, v in config_schema.items():
        config[k] = v.default

    return config
