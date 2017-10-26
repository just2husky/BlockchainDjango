#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import logging

from ..src.block_pkg.block_ops import init_block
from ..util import couchdb_util
from ..util.const import Const


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BlockChainService(object):

    @staticmethod
    def init():
        # 初始化区块链并得到区块链尾端区块的ID
        last_block_id = init_block()
        logger.info("链尾区块ID为： " + last_block_id)

        return last_block_id

    @staticmethod
    def find_content(identifier, tx_type):
        """
        根据 Transaction 的 tx_type 和其中所存储的 content 的 id 来查找Transaction，并以dict的形式返回 content 的内容
        :param identifier:
        :param tx_type:
        :return:
        """
        db = couchdb_util.get_db(Const.DB_NAME)
        doc = db[Const.LAST_BLOCK_ID]
        last_block = doc['last_block_id']
        doc = db[last_block]

        while True:
            # 若当前区块的 pre_id 为0，则表示便利整个区块链后，均未找到 id 为 所查询 id 的病人返回 none
            # 创世区块不存储transaction， 跳过
            if '0000000000000000000000000000000000000000000000000000000000000000' == doc['pre_id']:
                return None

            tx_list = doc['tx_list']
            # tx 保存了 一个Transaction 的 ID
            for tx in tx_list:
                tx_doc = db[tx]
                transaction_str = tx_doc['Transaction']
                transaction_dict = eval(transaction_str)

                if tx_type == transaction_dict['tx_type']:
                    content_str = transaction_dict['content']
                    content_dict = eval(content_str)
                    if identifier == content_dict['identifier']:
                        content_dict['transaction_id'] = transaction_dict['id']
                        content_dict['block_id'] = doc['_id']
                        logger.info('Find ' + identifier + ', in transaction ' +
                                    transaction_dict['id'] + ', in block ' + doc['_id'])
                        return content_dict
                logger.info(transaction_str)

            doc = db[doc['pre_id']]
