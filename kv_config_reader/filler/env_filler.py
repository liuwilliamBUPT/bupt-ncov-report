__all__ = (
    'EnvFiller',
)

import os
from typing import Mapping, MutableMapping, Optional

from .base import *
from .._util import *
from ..predef import *


class EnvFiller(BaseFiller):
    """从环境变量中读取配置。"""

    def __init__(self, env: Optional[Mapping[str, str]] = None):
        if env is None:
            env = os.environ

        self.env = env

    def fill(
            self,
            config: MutableMapping[str, Optional[SupportedConfigType]],
            config_schema: Mapping[str, ConfigSchemaItem],
    ) -> None:
        for name, schema_item in config_schema.items():
            # 获取同名环境变量
            value_as_text: Optional[str] = self.env.get(name)
            if value_as_text is None or value_as_text == '':
                continue

            # 如果环境变量存在，试图将其解析为相应类型；可能返回 None
            parse_result = parse_env_as_type(value_as_text, schema_item.type)
            if parse_result is None:
                continue

            config[name] = parse_result
