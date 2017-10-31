#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import logging

from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response, render

from ..util.const import OperatorType
from ..service.medical_record_service import MedicalRecordService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MedicalRecordController(object):
    """
    处理与 medical record 相关的请求
    """
    @staticmethod
    def del_medical_record(request):
        if request.GET:
            tx_id = request.GET['record_tx_id']
            operator_type = request.GET['operator_type']
            operator_id = request.GET['operator_id']

            logger.info('tx_id: ' + tx_id)
            logger.info('operator_type: ' + operator_type)
            logger.info('operator_id: ' + operator_id)

            MedicalRecordService.del_by_tx_id(tx_id, operator_type, operator_id)

            return render(request, 'blockchain_manager.html', {'msg': '删除' + tx_id + "成功"})

        return render_to_response('error.html')
