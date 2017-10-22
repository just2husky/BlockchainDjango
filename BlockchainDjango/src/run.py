#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import logging

from BlockchainDjango.src.merkle_tree import gen_merkle_tree
from BlockchainDjango.src.block import Block
from BlockchainDjango.src.transaction import Transaction

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# def verify_tx(pub_key, content, signature):
#     if not os.path.exists('./sk.pem') or not os.path.exists('./vk.pem'):
#         raise Exception("Key pair error! sk.pem or vk.pem does not existed!")


if __name__ == "__main__":

    # 生成4个Transaction，存储的内容分别为 aaa, bbb, ccc, ddd
    tx_content_list = ["aaa", "bbb", "ccc", "ddd"]
    tx_list = []
    for tx in tx_content_list:
        tx_list.append(Transaction.gen_tx(tx).__dict__.__str__())

    logger.info("========生成的Transaction如下========")
    for tx in tx_list:
        logger.info(tx)
    # 根据tx_list，生成 Merkle 树
    merkle_root = gen_merkle_tree(tx_list)
    logger.info("merkle_root: " + merkle_root)
    logger.info("========结束输出========")

    # # 1. 生成一个Transaction，其存储的内容为hello
    # tx = Transaction.gen_tx("hello")
    # arg_pub_key = VerifyingKey.from_pem(open("vk.pem").read())
    # # 2. 校验
    # try:
    #     result = Signature.verify(arg_pub_key, "hello", tx.get_signature())
    # except BadSignatureError:
    #     logger.error("校验失败！")
    # else:
    #     logger.info("校验结果：" + str(result))

    while True:
        opt = input("0：初始化. 1: 添加区块. q：退出 请输入：\n")
        if '0' == opt:
            # 初始化区块链并得到区块链尾端区块的ID
            last_block_id = Block.init_block(tx_list)
            logger.info("链尾区块ID为： " + last_block_id)
        elif '1' == opt:
            last_block_id = Block.add_block(tx_list)
            logger.info("链尾区块ID为： " + last_block_id)
        elif 'q' == opt:
            logger.info("输入结束")
            break
