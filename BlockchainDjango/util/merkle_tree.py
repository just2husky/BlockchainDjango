#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import logging
from merkletools import MerkleTools

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def gen_merkle_tree(tx_list):
    mt = MerkleTools(hash_type="sha256")
    mt.add_leaf(tx_list, True)
    mt.make_tree()
    for index in range(0, mt.leaves.__len__()):
        logger.info("Transaction" + str(index) + ": " + mt.get_leaf(index))

    while not mt.is_ready:
        logger.error("mt is not ready!")

    return mt.get_merkle_root()


if __name__ == "__main__":
    a_list = ["tx_a", "tx_b", "tx_c", "tx_d"]
    merkle_root = gen_merkle_tree(a_list)
    print(merkle_root)

