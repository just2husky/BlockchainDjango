#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import logging

from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response, render

from ..service.medical_record_service import MedicalRecordService
from ..service.transaction_service import TransactionService
from ..service.patient_service import PatientService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DoctorManagerController(object):
    """
    用来处理和doctor-manager相关的请求
    """

    @staticmethod
    @csrf_exempt
    def to_doctor_manager(request):
        return render_to_response('doctor-manager.html')

    @staticmethod
    @csrf_exempt
    def get_doctor_records(request):
        rtn_msg = {}
        if request.POST:
            doctor_id = request.POST['doctor_id']
            tx_id_list = MedicalRecordService.find_by_doctor_id(doctor_id)
            record_info_list = TransactionService.find_contents_by_ids(tx_id_list)

            # 根据就诊记录里的patient_id来获取对应病人的具体信息，并追加到就诊记录dict当中返回
            for record in record_info_list:
                patient_id = record['patient_id']
                patient_dict = PatientService.find_by_id(patient_id)
                record['patient'] = patient_dict

            logger.info('tx_id_list: ' + str(tx_id_list))
            logger.info('record_info_list: ' + str(record_info_list))
            rtn_msg['record_info_list'] = record_info_list.copy()

        # 判断record_info_list是为None或是否为空
        if rtn_msg['record_info_list'] is not None and len(rtn_msg['record_info_list']):
            logger.info('rtn_msg: ' + str(rtn_msg))
            return render(request, 'show_doctor_records.html', rtn_msg)

        else:
            return render(request, 'doctor-manager.html', {'msg': '该医生没有任何就诊记录'})
