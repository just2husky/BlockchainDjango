#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import logging
from .transaction_service import TransactionService
from .block_service import BlockService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PatientService(object):

    @staticmethod
    def save(patient):
        """
        保存patient 信息，返回链尾区块的ID
        :param patient:
        :return:
        """
        tx_list = [TransactionService.gen_tx(patient)]
        last_block_id = BlockService.add_block(tx_list)
        logger.info("最后一个区块的ID为： " + last_block_id)
        return last_block_id
