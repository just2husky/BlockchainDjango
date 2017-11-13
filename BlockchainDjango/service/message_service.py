#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import logging
import time

from ..util.signature import Signature
from ..entity.message import Message

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MessageService(object):

    @staticmethod
    def gen_msg(msg_type, transaction):
        """
        根据 msg type 和 transaction 生成一个 Message 类对象
        :param msg_type:
        :param transaction: Transaction对象
        :return:
        """
        timestamp = str(time.time())
        pvt_key, pub_key = Signature.get_key_pair()
        signature = bytes.hex(Signature.sign(pvt_key, transaction.__dict__.__str__()))
        msg_id = Signature.gen_id_by_sig(signature)
        # transaction=transaction.__dict__ 为了json 序列化
        # pub_key=bytes.hex(pub_key.to_string()) 为了json 序列化
        return Message(msg_id=msg_id, msg_type=msg_type, transaction=transaction.__dict__,
                       timestamp=timestamp, pub_key=bytes.hex(pub_key.to_string()), signature=signature)
