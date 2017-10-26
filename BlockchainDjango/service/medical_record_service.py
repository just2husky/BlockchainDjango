#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import logging
import time

from ..entity.medical_record import MedicalRecord
from ..entity.patient_record import PatientRecord
from ..entity.doctor_record import DoctorRecord

from ..util.const import RecordType
from ..util import couchdb_util
from ..util.const import Const
from .transaction_service import TransactionService
from .block_service import BlockService
from .block_chain_service import BlockChainService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MedicalRecordService(object):
    
    @staticmethod
    def add(patient_id, doctor_id, record_loc, chief_complaint, present_illness_history, past_history):
        """
        根据传入的参数构建一个就诊记录对象，存入区块链中，并返回该区块
        :param patient_id:
        :param doctor_id:
        :param record_loc:
        :param chief_complaint:
        :param present_illness_history:
        :param past_history:
        :return:
        """
        record_time = time.strftime("%Y%m%d%H%M%S", time.localtime())
        record_id = patient_id + record_time
        record_type = RecordType.ADD.value
        medical_record = MedicalRecord(record_id, doctor_id, patient_id, record_time, record_loc,
                                       chief_complaint, present_illness_history, past_history, record_type)

        # 添加一条就诊记录信息时，同时添加病人与该就诊记录对照关系的Transaction和添加医生与该就诊记录对照关系的Transaction
        record_tx = TransactionService.gen_tx(medical_record)
        patient_record_tx = MedicalRecordService.gen_medical_patient_tx(patient_id, record_tx.id)
        doctor_record_tx = MedicalRecordService.gen_medical_doctor_tx(doctor_id, record_tx.id)

        last_block_id = BlockService.add_block([record_tx, patient_record_tx, doctor_record_tx])
        return last_block_id

    @staticmethod
    def find_by_id(record_id):
        """
        根据就诊记录的ID返回就诊记录的内容，以dict的形式。
        若不存在，则返回None
        :param record_id:
        :return:
        """
        tx_type = 'medical_record'
        return BlockChainService.find_content(record_id, tx_type)

    @staticmethod
    def gen_medical_patient_tx(patient_id, record_tx_id):
        """
        用于生成 就诊记录与病人对照关系的函数
        :param patient_id:
        :param record_tx_id:
        :return:
        """
        patient_record = PatientRecord(patient_id, record_tx_id)
        patient_record_tx = TransactionService.gen_tx(patient_record)
        return patient_record_tx

    @staticmethod
    def gen_medical_doctor_tx(doctor_id, record_tx_id):
        """
        用于生成 就诊记录与医生对照关系的函数
        :param doctor_id:
        :param record_tx_id:
        :return:
        """
        doctor_record = DoctorRecord(doctor_id, record_tx_id)
        doctor_record_tx = TransactionService.gen_tx(doctor_record)
        return doctor_record_tx

    @staticmethod
    def find_by_patient_id(patient_id):
        """
        根据病人的ID查找其所有的就诊记录
        :param patient_id:
        :return:
        """
        tx_type = 'patient_record'
        record_list = []

        db = couchdb_util.get_db(Const.DB_NAME)
        doc = db[Const.LAST_BLOCK_ID]
        last_block = doc['last_block_id']
        doc = db[last_block]

        while True:
            # 若当前区块的 pre_id 为0，则表示便利整个区块链后，均未找到 id 为 所查询 id 的病人返回 none
            # 创世区块不存储transaction， 跳过
            if '0000000000000000000000000000000000000000000000000000000000000000' == doc['pre_id']:
                break

            tx_list = doc['tx_list']
            # tx 保存了 一个Transaction 的 ID
            for tx in tx_list:
                tx_doc = db[tx]
                transaction_str = tx_doc['Transaction']
                transaction_dict = eval(transaction_str)

                if tx_type == transaction_dict['tx_type']:
                    content_str = transaction_dict['content']
                    content_dict = eval(content_str)
                    if patient_id == content_dict['patient_id']:
                        logger.info('Find ' + patient_id + ', in transaction ' +
                                    transaction_dict['id'] + ', in block ' + doc['_id'])
                        record_list.append(content_dict['record_tx_id'])
                logger.info(transaction_str)

            doc = db[doc['pre_id']]

        return record_list
