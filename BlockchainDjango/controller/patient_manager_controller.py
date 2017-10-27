#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import logging

from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response, render

from ..service.medical_record_service import MedicalRecordService
from ..service.transaction_service import TransactionService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PatientManagerController(object):
    """
    用来处理和patient-manager相关的请求
    """

    @staticmethod
    def to_patient_manager(request):
        return render_to_response('patient-manager.html')

    @staticmethod
    @csrf_exempt
    def get_patient_records(request):
        rtn_msg = {}
        if request.POST:
            patient_id = request.POST['patient_id']
            tx_id_list = MedicalRecordService.find_by_patient_id(patient_id)
            tx_list = TransactionService.find_contents_by_ids(tx_id_list)
            logger.info(str(tx_id_list))
            logger.info(str(tx_list))
            rtn_msg['tx_list'] = tx_list.copy()
        logger.info(str(rtn_msg))
        return render(request, 'show_patient_records.html', rtn_msg)
