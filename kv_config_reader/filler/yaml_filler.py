__all__ = ('YamlFiller',)

from typing import Optional

from .base import BaseFiller


class YamlFiller(BaseFiller):
    def __init__(self, file_name: Optional[str], read_from_config: Optional[str]):
        if file_name is None and read_from_config is None:
            raise ValueError('file_name 与 read_from_config 必须填写一个')

        self.file_name = file_name
        self.read_from_config = read_from_config
