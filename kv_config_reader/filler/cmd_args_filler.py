__all__ = (
    'CmdArgsFiller',
)

import sys
from argparse import ArgumentParser
from typing import Any, Dict, Mapping, MutableMapping, Optional, Sequence, Union

from .base import *
from .._util import *
from ..predef import *


class CmdArgsFiller(BaseFiller):
    """
    从命令行参数中读取配置。
    参数为空且类型不为 bool 视作未填写；参数类型错误视作未填写。
    """

    def __init__(
            self,
            description: Optional[str] = None,
            args: Optional[Sequence[str]] = None,
    ):
        """
        初始化 filler。
        :param description: 程序的简介。会显示在 --help 输出的内容中。
        :param args: 纯的命令行参数（不含程序路径）。
        """
        if args is None:
            args = sys.argv[1:]

        self.description = description
        self.args = args

    def fill(
            self,
            config: MutableMapping[str, Optional[SupportedConfigType]],
            config_schema: Mapping[str, ConfigSchemaItem],
    ) -> None:
        parser = ArgumentParser(
            description=self.description,
        )

        for name, schema_item in config_schema.items():
            # 当类型为 bool 时，不能传入 type 参数
            parser_args: Dict[str, Any] = {
                'help': schema_item.description,
                'metavar': f'<{schema_item.for_short}>',
                'dest': name,
                'default': None,
                'action': 'store',
                'type': str,
            }
            if schema_item.type == bool:
                del parser_args['type']
                del parser_args['metavar']
                parser_args['action'] = 'store_true'

            # 将形如 FOO_BAR 的名字转换为 --foo-bar，添加为命令行参数
            parser.add_argument('--' + name.lower().replace('_', '-'), **parser_args)

        # 解析命令行参数，将被指定的项填写到 _conf 变量中
        args: Dict[str, Union[str, bool, None]]
        args = vars(parser.parse_args(args=self.args))

        for k, v in args.items():
            if isinstance(v, bool):
                config[k] = v
                continue

            # 空字符串视作 None
            if v is None or v == '':
                continue

            parse_result = parse_env_as_type(v, config_schema[k].type)
            if parse_result is None:
                continue

            config[k] = parse_result
