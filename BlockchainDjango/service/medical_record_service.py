#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import logging
import time

from ..entity.medical_record import MedicalRecord
from ..util.const import RecordType
from .transaction_service import TransactionService
from .block_service import BlockService

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

        last_block_id = BlockService.add_block([TransactionService.gen_tx(medical_record)])
        return last_block_id
