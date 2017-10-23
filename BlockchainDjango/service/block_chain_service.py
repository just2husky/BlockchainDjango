#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import logging

from ..src.block_pkg.block_ops import init_block

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BlockChainService(object):

    @staticmethod
    def init():
        # 初始化区块链并得到区块链尾端区块的ID
        last_block_id = init_block()
        logger.info("链尾区块ID为： " + last_block_id)

        return last_block_id
