#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import logging

from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response, render

from ..service.medical_record_service import MedicalRecordService
from ..service.transaction_service import TransactionService
from ..service.doctor_service import DoctorService

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
            record_info_list = TransactionService.find_contents_by_ids(tx_id_list)

            # 根据就诊记录里的doctor_id来获取对应医生的具体信息，并追加到就诊记录dict当中返回
            for record in record_info_list:
                doctor_id = record['doctor_id']
                doctor_dict = DoctorService.find_by_id(doctor_id)
                record['doctor'] = doctor_dict

            logger.info(str(tx_id_list))
            logger.info(str(record_info_list))
            rtn_msg['record_info_list'] = record_info_list.copy()

        # 判断record_info_list是为None或是否为空
        if rtn_msg['record_info_list'] is not None and len(rtn_msg['record_info_list']):
            logger.info('rtn_msg: ' + str(rtn_msg))
            return render(request, 'show_patient_records.html', rtn_msg)

        else:
            return render(request, 'patient-manager.html', {'msg': '该病人没有任何就诊记录'})

    @staticmethod
    def del_medical_record(request):
        tx_id = request.GET['record_tx_id']
        operator_id = request.GET['patient_id']
        logger.info('tx_id: ' + tx_id)
        logger.info('patient_id: ' + operator_id)
        MedicalRecordService.del_by_tx_id(tx_id, operator_id)
        return render(request, 'patient-manager.html', {'msg': '删除' + tx_id + "成功"})

