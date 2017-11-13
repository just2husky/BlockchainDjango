#!/usr/bin/python3
# -*- coding: UTF-8 -*-


class Message(object):
    """
    发送给Validator的信息
    """
    def __init__(self, msg_id, msg_type, transaction, timestamp, pub_key, signature):
        self.msg_id = msg_id
        self.msg_type = msg_type
        self.transaction = transaction
        self.timestamp = timestamp
        self.pub_key = pub_key
        self.signature = signature
