#!/usr/bin/python
# -*- coding: UTF-8 -*-
# 文件名：client.py

import socket
import json
import time

from BlockchainDjango.service.transaction_service import TransactionService
from BlockchainDjango.entity.message import Message
from BlockchainDjango.util.const import MsgType

if __name__ == "__main__":
    s = socket.socket()         # 创建 socket 对象
    host = socket.gethostname()  # 获取本地主机名
    port = 8000  # 设置端口好

    s.connect((host, port))
    transaction = TransactionService.gen_tx("signature")
    tx_str = json.dumps(Message(msg_type=MsgType.CLI.value,
                                transaction=transaction.__dict__,
                                timestamp=str(time.time())).__dict__)
    print(tx_str)
    s.send(bytes(tx_str + '\n', 'utf-8'))
    print(s.recv(1024).decode('utf-8'))
    s.close()
