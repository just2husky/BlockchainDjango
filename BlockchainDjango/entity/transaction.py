#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import hashlib


class Transaction(object):

    def __init__(self, pub_key, content,  timestamp):
        self.id = ''
        # 客户端给该交易单的签名
        self.signature = ''
        # tx_type 用以标志当前 Transaction 对象所存储的数据的类型，如 Patient、Doctor、Record等
        self.tx_type = ''
        # 客户端该交易单签名的客户端的私钥所对应的公钥
        self.pub_key = pub_key
        # 该交易单实际存储的内容
        self.content = content
        # 交易单生成时的时间
        self.timestamp = timestamp

    # @property
    # def tx_type(self):
    #     return self.tx_type
    #
    # @tx_type.setter
    # def tx_type(self, value):
    #     self.tx_type = value

    def set_signature(self, signature):
        self.signature = signature

    def set_id(self):
        self.id = hashlib.sha256(self.signature).hexdigest()

    def get_all_attr(self):
        return self.id, self.pub_key, self.signature, self.content, self.timestamp

    def get_id(self):
        return self.id

    def get_pub_key(self):
        return self.pub_key

    def get_signature(self):
        return self.signature

    def get_content(self):
        return self.content

    def get_timestamp(self):
        return self.timestamp

    def __str__(self):
        return 'id: ' + self.id + '\npub_key: \n' + self.pub_key +\
               '\ncontent: ' + self.content + '\ntimestamp: ' + str(self.timestamp)
