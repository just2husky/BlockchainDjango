#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import logging
from BlockchainDjango.src.block import Block
from BlockchainDjango.src.util.const import Const

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BlockTree(object):

    @staticmethod
    def init_block_tree():
        genesis_block_id = Block.init_block(["{'type': 'genesis_block'}"])
        logger.info("区块ID为： " + genesis_block_id)


if __name__ == "__main__":
    BlockTree.init_block_tree()
