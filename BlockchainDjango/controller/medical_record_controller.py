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

    @staticmethod
    @csrf_exempt
    def update_medical_record(request):
        if request.POST:
            # 1. 根据更改的字段构建新的 MedicalRecord 对象
            record_tx_id = request.POST['record_tx_id']
            logger.info('tx_id: ' + record_tx_id)
            record_dict = TransactionService.find_contents_by_id(record_tx_id)
            # 将html里传入的字段保存在rtn_fields_dict中
            rtn_fields_dict = {
                'record_time': request.POST['record_time'].strip(),
                'record_loc': request.POST['record_loc'].strip(),
                'chief_complaint': request.POST['chief_complaint'].strip(),
                'present_illness_history': request.POST['present_illness_history'].strip(),
                'past_history': request.POST['past_history'].strip()
            }

            # 2. 保存旧的就诊记录，后，更新
            old_record_dict = record_dict.copy()
            # 更新 record_dict，下面函数会直接更改 record_dict，而不需要返回值
            MedicalRecordService.modify_record_fields(record_dict, rtn_fields_dict)

            # 3. 保存新的就诊记录，以及新旧记录的关系，到区块链中
            operator_type = request.POST['operator_type']
            operator_id = request.POST['record_tx_id']
            last_block_id = MedicalRecordService.update_record(old_record_dict, record_dict, operator_type, operator_id)
            logger.info('last_block_id: ' + last_block_id)

            if operator_type == OperatorType.PATIENT.value:
                # 4. 获取医生的信息
                doctor_id = record_dict['doctor_id']
                doctor_dict = DoctorService.find_by_id(doctor_id)
                logger.info('doctor_dict: ' + str(doctor_dict))
                return render(request, 'show_patient_record.html', {'record': record_dict, 'doctor': doctor_dict,
                                                                    'block_id': last_block_id})

            elif operator_type == OperatorType.DOCTOR.value:
                patient_id = record_dict['patient_id']
                patient_dict = PatientService.find_by_id(patient_id)
                logger.info('patient_dict: ' + str(patient_dict))
                return render(request, 'show_doctor_record.html', {'record': record_dict, 'patient': patient_dict,
                                                                   'block_id': last_block_id})

            else:
                return render(request, 'error.html', {'msg': '未知的 operator_type !'})

        return render(request, 'error.html', {'msg': '请求类型不为POST！'})
