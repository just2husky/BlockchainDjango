#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import hashlib
import logging

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

    def __str__(self):
        return "id: " + str(self._id) + ", pre_id: " + str(self.pre_id) \
               + ", tree_hash: " + str(self.tree_hash)

    def get_id(self):
        return self._id