import unittest

from kv_config_reader.filler import *
from kv_config_reader.predef import *

CONFIG_SCHEMA = {
    'FUCK_STR': ConfigSchemaItem(description='fuck you', for_short='fy', default='fuck', type=str),
    'SUCK_STR': ConfigSchemaItem(description='it sucks', for_short='is', default='suck', type=str),
    'DAMN_STR': ConfigSchemaItem(description='damn it', for_short='di', default='damn', type=str),
    'SHIT_STR': ConfigSchemaItem(description='oh shit', for_short='os', default=None, type=str),

    'FUCK_INT': ConfigSchemaItem(description='fuck you', for_short='fy', default=1, type=int),
    'SUCK_INT': ConfigSchemaItem(description='it sucks', for_short='is', default=2, type=int),
    'DAMN_INT': ConfigSchemaItem(description='damn it', for_short='di', default=3, type=int),
    'SHIT_INT': ConfigSchemaItem(description='oh shit', for_short='os', default=4, type=int),

    'FUCK_BOOL': ConfigSchemaItem(description='fuck you', for_short='fy', default=False, type=bool),
    'SUCK_BOOL': ConfigSchemaItem(description='it sucks', for_short='is', default=False, type=bool),
    'DAMN_BOOL': ConfigSchemaItem(description='damn it', for_short='di', default=False, type=bool),
    'SHIT_BOOL': ConfigSchemaItem(description='oh shit', for_short='os', default=False, type=bool),
}

DEFAULT_CONFIG = {
    'FUCK_STR': 'fuck',
    'SUCK_STR': 'suck',
    'DAMN_STR': 'damn',
    'SHIT_STR': None,

    'FUCK_INT': 1,
    'SUCK_INT': 2,
    'DAMN_INT': 3,
    'SHIT_INT': 4,

    'FUCK_BOOL': False,
    'SUCK_BOOL': False,
    'DAMN_BOOL': False,
    'SHIT_BOOL': False,
}

PERFECT_ENV = {
    'FUCK_STR': 'a',
    'SUCK_STR': 'b',
    'DAMN_STR': 'c',
    'SHIT_STR': 'd',

    'FUCK_INT': '11',
    'SUCK_INT': '22',
    'DAMN_INT': '33',
    'SHIT_INT': '44',

    'FUCK_BOOL': '+',
    'SUCK_BOOL': '-',
    'DAMN_BOOL': '*',
    'SHIT_BOOL': '/',
}


class TestEnvFilter(unittest.TestCase):

    def test_normal(self):
        """正常情况"""

        filler = EnvFiller(env=PERFECT_ENV)
        config = DEFAULT_CONFIG.copy()
        filler.fill(config, CONFIG_SCHEMA)

        self.assertEqual(config, {
            'FUCK_STR': 'a',
            'SUCK_STR': 'b',
            'DAMN_STR': 'c',
            'SHIT_STR': 'd',

            'FUCK_INT': 11,
            'SUCK_INT': 22,
            'DAMN_INT': 33,
            'SHIT_INT': 44,

            'FUCK_BOOL': True,
            'SUCK_BOOL': True,
            'DAMN_BOOL': True,
            'SHIT_BOOL': True,
        })

    def test_invalid_values(self):
        """
        - 空字符串（不含空白符）不覆盖原值
        - 类型错误不覆盖原值
        - 未填写不覆盖原值
        """
        filler = EnvFiller(env={
            'FUCK_STR': 'a',
            'SUCK_STR': '',

            'FUCK_INT': '233',
            'SUCK_INT': 'abc',
            'DAMN_INT': '',

            'FUCK_BOOL': '123',
            'SUCK_BOOL': '*',
            'DAMN_BOOL': '',
        })
        config = DEFAULT_CONFIG.copy()
        filler.fill(config, CONFIG_SCHEMA)

        self.assertEqual(config, {
            'FUCK_STR': 'a',
            'SUCK_STR': 'suck',
            'DAMN_STR': 'damn',
            'SHIT_STR': None,

            'FUCK_INT': 233,
            'SUCK_INT': 2,
            'DAMN_INT': 3,
            'SHIT_INT': 4,

            'FUCK_BOOL': True,
            'SUCK_BOOL': True,
            'DAMN_BOOL': False,
            'SHIT_BOOL': False,
        })

    def test_strange_schema(self):
        """
        空 schema 不改变 config
        schema 与 config 完全不一致，不改变 config
        """

        filler = EnvFiller(env=PERFECT_ENV)
        config = DEFAULT_CONFIG.copy()

        filler.fill(config, {})
        self.assertEqual(config, DEFAULT_CONFIG)

        filler.fill(config, {
            'STRANGE_SCHEMA': ConfigSchemaItem(
                description='strange schema',
                for_short='ss',
                default=None,
                type=int,
            ),
        })
        self.assertEqual(config, DEFAULT_CONFIG)
