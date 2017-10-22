#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import hashlib
import time
import logging

from BlockchainDjango.src.util.const import Const
from BlockchainDjango.src.util import couchdb_util
from BlockchainDjango.src.merkle_tree import gen_merkle_tree

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Block(object):
    # 为了以区块的id作为couchdb中的_id
    _id = ''
    pre_id = ''
    tree_hash = ''
    time_stamp = 0.0
    tx_count = 0
    tx_list = []

    def __init__(self, pre_id, tree_hash, time_stamp, tx_count, tx_list):
        self.pre_id = pre_id
        self.tree_hash = tree_hash
        self.time_stamp = time_stamp
        self.tx_count = tx_count
        self.tx_list = tx_list
        hash_content = pre_id + tree_hash + str(time_stamp)
        # 利用sha256算法计算一个区块的ID
        self._id = hashlib.sha256(bytes(hash_content, encoding='utf-8')).hexdigest()

    @staticmethod
    def init_block(init_content=['This is genesis block']):
        """
        生成创世区块
        :param init_content: 存入区块链里的内容
        :return:
        """
        # 创世区块前一个区块ID为0
        pre_id = '0000000000000000000000000000000000000000000000000000000000000000'
        tree_hash = gen_merkle_tree(init_content)
        timestamp = time.time()
        tx_count = len(init_content)
        block = Block(pre_id, tree_hash, timestamp, tx_count, init_content)
        logger.info("创世区块的内容为： " + str(block))
        # print(block.tx_list)
        # print(block.__dict__)
        db = couchdb_util.init_db(Const.DB_NAME)
        couchdb_util.save(db, block.__dict__)
        couchdb_util.save(db, {'_id': Const.LAST_BLOCK_ID, 'last_block_id': block.get_id()})
        return block.get_id()

    @staticmethod
    def gen_province_block(content_list):
        """
        在创世区块下生成区块书第二层省一级区块，并将这些区块ID记录到数据库中
        :param content_list:
        :return:
        """
        pre_id = Const.GENESIS_BLOCK_ID
        pass

    @staticmethod
    def block_tree_add(content_list, pre_id):
        """
        用于使用init_block(param_tx_list)函数初始化区块链生成创世区块后，
        向区块链添加新的区块
        :param content_list: 交易单Transaction列表
        :param pre_id: 在以pre_id作为ID的区块后添加一个区块
        :return: 返回当前新添加区块的ID
        """
        db = couchdb_util.get_db(Const.DB_NAME)
        tree_hash = gen_merkle_tree(content_list)
        timestamp = time.time()
        tx_count = len(content_list)
        block = Block(pre_id, tree_hash, timestamp, tx_count, content_list)
        couchdb_util.save(db, block.__dict__)
        return block.get_id()

    @staticmethod
    def add_block(param_tx_list):
        """
        用于使用init_block(param_tx_list)函数初始化区块链生成创世区块后，
        向区块链添加新的区块
        :param param_tx_list: 交易单Transaction列表
        :return: 返回最后一个区块的ID
        """
        db = couchdb_util.get_db(Const.DB_NAME)
        doc = db[Const.LAST_BLOCK_ID]
        pre_id = doc['last_block_id']
        tree_hash = gen_merkle_tree(param_tx_list)
        timestamp = time.time()
        tx_count = len(param_tx_list)
        block = Block(pre_id, tree_hash, timestamp, tx_count, param_tx_list)
        couchdb_util.save(db, block.__dict__)
        doc['last_block_id'] = block.get_id()
        db[Const.LAST_BLOCK_ID] = doc
        return doc['last_block_id']

    def __str__(self):
        return "id: " + str(self._id) + ", pre_id: " + str(self.pre_id) \
               + ", tree_hash: " + str(self.tree_hash)

    def get_id(self):
        return self._id
