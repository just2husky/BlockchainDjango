#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import logging
from .transaction_service import TransactionService
from .block_service import BlockService
from ..util import couchdb_util
from ..util.const import Const
from ..entity.doctor import Doctor

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DoctorService(object):

    @staticmethod
    def save(doctor):
        """
        保存doctor 信息，返回链尾区块的ID
        :param doctor:
        :return:
        """
        tx_list = [TransactionService.gen_tx(doctor)]
        last_block_id = BlockService.add_block(tx_list)
        logger.info("最后一个区块的ID为： " + last_block_id)
        return last_block_id

    @staticmethod
    def find_by_id(identifier):
        """
        根据 identifier 去查找病人，查找成功则返回病人信息的dict，否则返回None
        :param identifier:
        :return:
        """
        db = couchdb_util.get_db(Const.DB_NAME)
        doc = db[Const.LAST_BLOCK_ID]
        last_block = doc['last_block_id']
        doc = db[last_block]

        while True:
            # 若当前区块的 pre_id 为0，则表示便利整个区块链后，均未找到 id 为 所查询 id 的病人返回 none
            # 创世区块不存储transaction， 跳过
            if '0000000000000000000000000000000000000000000000000000000000000000' == doc['pre_id']:
                return None

            tx_list = doc['tx_list']
            # tx 保存了 一个Transaction 的 ID
            for tx in tx_list:
                tx_doc = db[tx]
                transaction_dict = tx_doc['Transaction']

                if 'doctor' == transaction_dict['tx_type']:
                    content_dict = transaction_dict['content']
                    if identifier == content_dict['identifier']:
                        content_dict['transaction_id'] = transaction_dict['id']
                        content_dict['block_id'] = doc['_id']
                        logger.info('Find doctor ' + identifier + ', in transaction ' +
                                    transaction_dict['id'] + ', in block ' + doc['_id'])
                        return content_dict
                logger.info(str(transaction_dict))

            doc = db[doc['pre_id']]

    @staticmethod
    def gen_instance_by_dict(doctor_dict):
        """
        将 doctor_dict转换为对应的doctor实例
        :param doctor_dict:
        :return:
        """
        identifier = doctor_dict['identifier']
        name = doctor_dict['name']
        gender = doctor_dict['gender']
        age = doctor_dict['age']
        nation = doctor_dict['nation']
        hospital = doctor_dict['hospital']
        department = doctor_dict['department']
        grade = doctor_dict['grade']
        return Doctor(identifier, name, gender, age, nation, hospital, department, grade)
