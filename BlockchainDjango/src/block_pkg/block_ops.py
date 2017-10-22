#!/usr/bin/python3
# -*- coding: UTF-8 -*-
"""
    本文件用来保存一些对 block 操作的函数
"""
import time
import logging

from BlockchainDjango.src.merkle_tree import gen_merkle_tree
from BlockchainDjango.src.block_pkg.block import Block
from BlockchainDjango.src.util.const import Const
from BlockchainDjango.src.util import couchdb_util
from BlockchainDjango.src.transaction_pkg.transaction_ops import get_tx_ids, save_tx_list, gen_tx
from BlockchainDjango.src.transaction_pkg.patient import Patient
from BlockchainDjango.src.transaction_pkg.doctor import Doctor
from BlockchainDjango.src.transaction_pkg.transaction_ops import class_medical_record_test
from BlockchainDjango.src.transaction_pkg.transaction_ops import class_patient_record_test
from BlockchainDjango.src.transaction_pkg.transaction_ops import class_doctor_record_test

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init_block(init_content=['This is genesis block']):
    """
    生成创世区块
    :param init_content: 存入区块链里的内容
    :return:
    """
    # 创世区块前一个区块ID为0
    pre_id = '0000000000000000000000000000000000000000000000000000000000000000'
    tree_hash = gen_merkle_tree(init_content)
    timestamp = time.time()
    tx_count = len(init_content)
    block = Block(pre_id, tree_hash, timestamp, tx_count, init_content)
    logger.info("创世区块的内容为： " + str(block))
    db = couchdb_util.init_db(Const.DB_NAME)
    couchdb_util.save(db, block.__dict__)
    couchdb_util.save(db, {'_id': Const.LAST_BLOCK_ID, 'last_block_id': block.get_id()})
    return block.get_id()


def add_block(param_tx_list):
    """
    用于使用init_block(param_tx_list)函数初始化区块链生成创世区块后，
    向区块链添加新的区块
    :param param_tx_list: 交易单Transaction类实例的列表
    :return: 返回最后一个区块的ID
    """
    db = couchdb_util.get_db(Const.DB_NAME)
    doc = db[Const.LAST_BLOCK_ID]

    pre_id = doc['last_block_id']

    # 将 Transaction 实例列表转化为 实例转为json字符串后的列表
    tx_strs = []
    for each_tx in param_tx_list:
        tx_strs.append(each_tx.__dict__.__str__())
    tree_hash = gen_merkle_tree(tx_strs)

    timestamp = time.time()
    tx_count = len(param_tx_list)
    tx_ids = get_tx_ids(param_tx_list)

    block = Block(pre_id, tree_hash, timestamp, tx_count, tx_ids)
    # 保存区块到数据库中
    couchdb_util.save(db, block.__dict__)
    # 保存交易单 Transaction 到数据库中
    save_tx_list(param_tx_list)

    # 更新最后一个区块的ID
    doc['last_block_id'] = block.get_id()
    db[Const.LAST_BLOCK_ID] = doc
    return doc['last_block_id']


def show_block_chain():
    db = couchdb_util.get_db(Const.DB_NAME)
    doc = db[Const.LAST_BLOCK_ID]
    last_block = doc['last_block_id']
    doc = db[last_block]
    block_count = 1
    print('区块：' + doc['_id'] + ' 的前一个区块ID为：' + doc['pre_id'])

    while True:
        doc = db[doc['pre_id']]
        print('区块：' + doc['_id'] + ' 的前一个区块ID为：' + doc['pre_id'])
        block_count += 1

        if '0000000000000000000000000000000000000000000000000000000000000000' == doc['pre_id']:
            break

    print("当前区块链长度为：", block_count)


if __name__ == "__main__":

    while True:
        opt_str = ('1：初始化. 2: 添加 str 区块. 3. 添加 patient. \n'
                   '4. 添加 doctor 5.添加 medical record. 6. 添加 patient record\n'
                   's: 显示区块链. q：退出 \n请输入：\n')
        opt = input(opt_str)

        if '1' == opt:
            init_block()

        elif '2' == opt:
            # 生成4个Transaction，存储的内容分别为 aaa, bbb, ccc, ddd
            tx_content_list = ["aaa", "bbb", "ccc", "ddd"]
            tx_list = []
            for tx_content in tx_content_list:
                tx_list.append(gen_tx(tx_content))

            last_block_id = add_block(tx_list)
            logger.info("最后一个区块的ID为： " + last_block_id)

        elif '3' == opt:
            patient1 = Patient('1001', '张超', '男', '18', '汉', '山东', '四川大学望江校区')
            patient2 = Patient('1002', '陈泽堃', '男', '28', '汉', '福建', '四川大学望江校区')
            patient3 = Patient('1003', '叶雄峰', '男', '28', '汉', '浙江', '四川大学望江校区')
            tx_content_list = [patient1, patient2, patient3]
            tx_list = []
            for tx_content in tx_content_list:
                tx_list.append(gen_tx(tx_content))

            last_block_id = add_block(tx_list)
            logger.info("最后一个区块的ID为： " + last_block_id)

        elif '4' == opt:
            # 生成3个Transaction，存储的内容分别为3个医生的信息
            doctor1 = Doctor('10', '邹越', '男', '28', '汉', '望江医院', '呼吸科', '主治医师')
            doctor2 = Doctor('11', '许刚', '男', '28', '汉', '华西保健医院', '口腔科', '副主任医师')
            doctor3 = Doctor('12', '郑腾霄', '男', '28', '汉', '华西医院', '消化科', '主任医师')
            tx_content_list = [doctor1, doctor2, doctor3]
            tx_list = []
            for tx_content in tx_content_list:
                tx_list.append(gen_tx(tx_content))

            last_block_id = add_block(tx_list)
            logger.info("最后一个区块的ID为： " + last_block_id)

        elif '5' == opt:
            tx_list = class_medical_record_test()
            last_block_id = add_block(tx_list)
            logger.info("最后一个区块的ID为： " + last_block_id)

        elif '6' == opt:
            tx_list1, tx_list2 = class_patient_record_test()
            add_block(tx_list1)
            last_block_id = add_block(tx_list2)
            logger.info("最后一个区块的ID为： " + last_block_id)

        elif '7' == opt:
            tx_list1, tx_list2 = class_doctor_record_test()
            add_block(tx_list1)
            last_block_id = add_block(tx_list2)
            logger.info("最后一个区块的ID为： " + last_block_id)

        elif 's' == opt:
            show_block_chain()

        elif 'q' == opt:
            logger.info("输入结束")
            break
