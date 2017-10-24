#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import logging
import os
import time
from ecdsa import SigningKey
from ecdsa import VerifyingKey

from ..util import couchdb_util
from ..util.const import Const
from ..util.signature import Signature
from ..entity.transaction import Transaction
from ..entity.patient import Patient
from ..entity.doctor import Doctor
from ..entity.medical_record import MedicalRecord
from ..entity.patient_record import PatientRecord
from ..entity.patient_last_record import PatientLastRecord
from ..entity.doctor_record import DoctorRecord
from ..entity.doctor_last_record import DoctorLastRecord

db = couchdb_util.get_db(Const.DB_NAME)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TransactionService(object):

    @staticmethod
    def gen_tx(content):
        """
        测试生成一条transaction
        :return: 生成的transaction
        """
        if content is None:
            raise Exception("The content is None!")

        if os.path.exists(Const.PVT_KEY_LOC) and os.path.exists(Const.PUB_KEY_LOC):
            pvt_key = SigningKey.from_pem(open(Const.PVT_KEY_LOC).read())
            pub_key = VerifyingKey.from_pem(open(Const.PUB_KEY_LOC).read())
        else:
            pvt_key, pub_key = Signature.gen_key_pair()

        timestamp = time.time()
        # 若content是对象类型，则将其转化为json格式字符串存储
        if isinstance(content, str):
            temp_tx = Transaction(pub_key.to_pem().decode(), content, timestamp)
            signature = Signature.sign(pvt_key, content)
        else:
            temp_tx = Transaction(pub_key.to_pem().decode(), content.__dict__.__str__(), timestamp)
            signature = Signature.sign(pvt_key, content.__dict__.__str__())

        temp_tx.set_signature(signature)
        temp_tx.set_id()
        temp_tx.tx_type = TransactionService.get_tx_type(content)
        return temp_tx

    @staticmethod
    def get_tx_type(content):
        """
        判断 content 类型并返回
        :param content: Transaction 对象所存储的内容
        :return: content 类型
        """
        if isinstance(content, Patient):
            logger.info("此 Transaction 存储的类型为 patient")
            return 'patient'

        elif isinstance(content, Doctor):
            logger.info("此 Transaction 存储的类型为 doctor")
            return 'doctor'

        elif isinstance(content, MedicalRecord):
            logger.info("此 Transaction 存储的类型为 medical_record")
            return 'medical_record'

        elif isinstance(content, PatientRecord):
            logger.info("此 Transaction 存储的类型为 patient_record")
            return 'patient_record'

        elif isinstance(content, PatientLastRecord):
            logger.info("此 Transaction 存储的类型为 patient_last_record")
            return 'patient_last_record'

        elif isinstance(content, DoctorRecord):
            logger.info("此 Transaction 存储的类型为 doctor_record")
            return 'doctor_record'

        elif isinstance(content, DoctorLastRecord):
            logger.info("此 Transaction 存储的类型为 doctor_last_record")
            return 'doctor_last_record'

        elif isinstance(content, str):
            logger.info("此 Transaction 存储的类型为 string")
            return 'string'

        elif content is None:
            logger.info("此 Transaction 存储的类型为 none")
            return 'none'

        else:
            raise Exception('未知 Transaction 类型！')

    @staticmethod
    def save_tx(transaction):
        """ 将一条 transaction 信息存储 couchdb数据库里"""
        if not isinstance(transaction, Transaction):
            raise Exception("形参transaction类型错误，必须为Transaction类的实例！")
        else:
            couchdb_util.save(db, {'_id': transaction.get_id(), 'Transaction': transaction.__dict__.__str__()})

    @staticmethod
    def save_tx_list(transaction_list):
        """ 循环调用 save_tx, 将transaction list 存入到数据库中"""
        for each_tx in transaction_list:
            TransactionService.save_tx(each_tx)

    @staticmethod
    def get_tx_ids(transaction_list):
        """根据传入的 transaction_list，得到各个 transaction 的 id，以tuple的形式返回"""
        id_list = []
        for each_transaction in transaction_list:
            id_list.append(each_transaction.get_id())
        return tuple(id_list)