#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import ecdsa
import os.path
from enum import Enum, unique


class Const(object):
    DB_NAME = 'block_tree'
    LAST_BLOCK_ID = 'last_block'
    GENESIS_BLOCK_ID = 'genesis_block'
    PVT_KEY_LOC = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'files', 'sk.pem')
    PUB_KEY_LOC = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'files', 'vk.pem')
    # SECP256k1 is the Bitcoin elliptic curve
    CURVE = ecdsa.SECP256k1


@unique
class RecordType(Enum):
    """表示就诊记录的类型"""
    ADD = 'add'


@unique
class OperatorType(Enum):
    """表示就诊记录的类型"""
    PATIENT = 'patient'
    DOCTOR = 'doctor'


@unique
class FindRecordType(Enum):
    """
    查找就诊记录时的类型
    """
    ALL = 'all'
    # 表示去除被删除和被更新记录
    NORMAL = 'normal'
    DELETED = 'deleted'
    # 被更新过的记录
    UPDATED = 'updated'


@unique
class MsgType(Enum):
    """表示该message的类型"""
    CLI = 'cli'  # 由客户端发往主节点
