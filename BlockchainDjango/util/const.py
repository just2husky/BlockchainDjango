#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from enum import Enum, unique


class Const(object):
    DB_NAME = 'block_tree'
    LAST_BLOCK_ID = 'last_block'
    GENESIS_BLOCK_ID = 'genesis_block'
    PVT_KEY_LOC = 'sk.pem'
    PUB_KEY_LOC = 'vk.pem'


@unique
class RecordType(Enum):
    """表示就诊记录的类型"""
    ADD = 'add'
