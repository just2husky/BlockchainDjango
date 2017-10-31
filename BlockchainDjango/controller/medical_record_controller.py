#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import logging

from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response, render

from ..service.medical_record_service import MedicalRecordService
from ..service.transaction_service import TransactionService
from ..service.doctor_service import DoctorService
from ..service.patient_service import PatientService

from ..util.const import OperatorType

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

            return render(request, 'blockchain_manager.html', {'msg': '删除' + tx_id + '成功'})

        return render_to_response('error.html')

    @staticmethod
    def to_update_medical_record(request):
        if request.GET:
            record_tx_id = request.GET['record_tx_id']
            operator_type = request.GET['operator_type']
            operator_id = request.GET['operator_id']

            logger.info('tx_id: ' + record_tx_id)
            logger.info('operator_type: ' + operator_type)
            logger.info('operator_id: ' + operator_id)

            record_dict = TransactionService.find_contents_by_id(record_tx_id)

            if operator_type == OperatorType.PATIENT.value:
                doctor_id = record_dict['doctor_id']
                doctor_dict = DoctorService.find_by_id(doctor_id)
                logger.info('doctor_dict: ' + str(doctor_dict))
                return render(request, 'update_medical_record.html', {'record': record_dict, 'doctor': doctor_dict})

            elif operator_type == OperatorType.DOCTOR.value:
                patient_id = record_dict['patient_id']
                patient_dict = PatientService.find_by_id(patient_id)
                logger.info('patient_dict: ' + str(patient_dict))
                return render(request, 'update_medical_record.html', {'record': record_dict, 'patient': patient_dict})

            else:
                return render(request, 'error.html', {'msg': '未知的 operator_type !'})

        return render(request, 'error.html', {'msg': '请求类型不为GET！'})
