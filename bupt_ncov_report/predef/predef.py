__all__ = (
    'ConfigValue',
)

from typing import TypeVar, Union

ConfigValue = Union[str, bool, int]

TConfigValue = TypeVar(
    'TConfigValue',
    bound=ConfigValue,
)
