__all__ = (
    'SupportedConfigType',
    'ConfigSchemaItem',
)

from typing import NamedTuple, Optional, Type, Union

# 配置项所支持的目标类型
SupportedConfigType = Union[str, bool, int]


# 用于设置项。
class ConfigSchemaItem(NamedTuple):
    description: str
    for_short: str

    # 为了支持 3.6，此处无法使用泛型
    default: Optional[SupportedConfigType]

    # 目前支持 str、bool、int
    type: Type[SupportedConfigType]
