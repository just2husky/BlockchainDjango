#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import logging
import time
from BlockchainDjango.util.merkle_tree import gen_merkle_tree
from BlockchainDjango.entity.block import Block
from BlockchainDjango.util import couchdb_util
from BlockchainDjango.util.const import Const
from .transaction_service import TransactionService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BlockService(object):

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
        db = couchdb_util.init_db(Const.DB_NAME)
        couchdb_util.save(db, block.__dict__)
        couchdb_util.save(db, {'_id': Const.LAST_BLOCK_ID, 'last_block_id': block.get_id()})
        return block.get_id()

    @staticmethod
    def add_block(param_tx_list):
        """
        用于使用init_block(param_tx_list)函数初始化区块链生成创世区块后，
        向区块链添加新的区块
        :param param_tx_list: 交易单Transaction类实例的列表
        :return: 返回最后一个区块的ID
        """
        db = couchdb_util.get_db(Const.DB_NAME)
        doc = db[Const.LAST_BLOCK_ID]

        pre_id = doc['last_block_id']

        # 将 Transaction 实例列表转化为 实例转为json字符串后的列表
        tx_strs = []
        for each_tx in param_tx_list:
            tx_strs.append(each_tx.__dict__.__str__())
        tree_hash = gen_merkle_tree(tx_strs)

        timestamp = time.time()
        tx_count = len(param_tx_list)
        tx_ids = TransactionService.get_tx_ids(param_tx_list)

        block = Block(pre_id, tree_hash, timestamp, tx_count, tx_ids)
        # 保存区块到数据库中
        couchdb_util.save(db, block.__dict__)
        # 保存交易单 Transaction 到数据库中
        TransactionService.save_tx_list(param_tx_list)

        # 更新最后一个区块的ID
        doc['last_block_id'] = block.get_id()
        db[Const.LAST_BLOCK_ID] = doc
        return doc['last_block_id']

    @staticmethod
    def show_block_chain():
        db = couchdb_util.get_db(Const.DB_NAME)
        doc = db[Const.LAST_BLOCK_ID]
        last_block = doc['last_block_id']
        doc = db[last_block]
        block_count = 1
        print('区块：' + doc['_id'] + ' 的前一个区块ID为：' + doc['pre_id'])

        while True:
            doc = db[doc['pre_id']]
            print('区块：' + doc['_id'] + ' 的前一个区块ID为：' + doc['pre_id'])
            block_count += 1

            if '0000000000000000000000000000000000000000000000000000000000000000' == doc['pre_id']:
                break

        print("当前区块链长度为：", block_count)