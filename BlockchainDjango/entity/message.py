#!/usr/bin/python3
# -*- coding: UTF-8 -*-


class Message(object):
    """
    发送给Validator的信息
    """
    def __init__(self, msg_type, transaction, timestamp):
        self.msg_type = msg_type
        self.transaction = transaction
        self.timestamp = timestamp
