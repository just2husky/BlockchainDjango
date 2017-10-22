#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import hashlib
import os
import time

from BlockchainDjango.src.signature import Signature
from ecdsa import SigningKey
from ecdsa import VerifyingKey


class Transaction(object):
    id = ''
    # 客户端该交易单签名的客户端的私钥所对应的公钥
    pub_key = ''
    # 客户端给该交易单的签名
    signature = ''
    # 该交易单实际存储的内容
    content = ''
    # 交易单生成时的时间
    timestamp = ''

    def __init__(self, pub_key, content,  timestamp):
        self.pub_key = pub_key
        self.content = content
        self.timestamp = timestamp

    @staticmethod
    def gen_tx(content):
        """
        测试生成一条transaction
        :return: 生成的transaction
        """
        if content is None:
            raise Exception("The content is None!")

        if os.path.exists('./sk.pem') and os.path.exists('./vk.pem'):
            pvt_key = SigningKey.from_pem(open("sk.pem").read())
            pub_key = VerifyingKey.from_pem(open("vk.pem").read())
        else:
            pvt_key, pub_key = Signature.gen_key_pair()

        signature = Signature.sign(pvt_key, content)
        timestamp = time.time()
        temp_tx = Transaction(pub_key.to_pem().decode(), content, timestamp)
        temp_tx.set_signature(signature)
        temp_tx.set_id()
        return temp_tx

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
