import unittest

from kv_config_reader.predef import *
from kv_config_reader.public_util import *

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


class TestPublicUtil(unittest.TestCase):

    def test_initializeConfig(self):
        self.assertEqual(initialize_config(CONFIG_SCHEMA), DEFAULT_CONFIG)
