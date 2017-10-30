#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import logging

from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response, render

from ..service.medical_record_service import MedicalRecordService
from ..service.transaction_service import TransactionService
from ..service.doctor_service import DoctorService

from ..util.const import OperatorType, FindRecordType
from ..util.time_util import get_format_time

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
            find_record_type = FindRecordType.NORMAL.value
            tx_id_list = MedicalRecordService.find_by_patient_id(patient_id, find_record_type)
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
    @csrf_exempt
    def get_patient_del_records(request):
        rtn_msg = {}
        if request.POST:
            patient_id = request.POST['patient_id']
            find_record_type = FindRecordType.DELETED.value
            # tx_id_list 用于保存 MedicalRecord 类型 transaction 的 id
            # deleted_record_tx_id_list用于保存MedicalRecordDel 类型 transaction 的 id
            tx_id_list, deleted_record_tx_id_list = \
                MedicalRecordService.find_by_patient_id(patient_id, find_record_type)
            record_info_list = TransactionService.find_contents_by_ids(deleted_record_tx_id_list)
            for record in record_info_list:
                record['timestamp'] = get_format_time(record['timestamp'])
                # 根据就诊记录里的tx_id来获取已被删除的 就诊记录的信息
                tx_id = record['tx_id']
                logger.info('tx_id: ' + tx_id)
                record['record_del_info'] = TransactionService.find_contents_by_id(tx_id)

                # 根据就诊记录里的doctor_id来获取对应医生的具体信息，并追加到就诊记录dict当中返回
                doctor_id = record['doctor_id']
                doctor_dict = DoctorService.find_by_id(doctor_id)
                record['doctor'] = doctor_dict

            logger.info('tx_id_list: ' + str(tx_id_list))
            logger.info('record_info_list' + str(record_info_list))

            rtn_msg['record_info_list'] = record_info_list.copy()

        # 判断record_info_list是为None或是否为空
        if rtn_msg['record_info_list'] is not None and len(rtn_msg['record_info_list']):
            logger.info('rtn_msg: ' + str(rtn_msg))
            return render(request, 'show_patient_del_records.html', rtn_msg)

        else:
            return render(request, 'patient-manager.html', {'msg': '该病人没有任何删除的就诊记录'})

    @staticmethod
    def get_records_with_doc_info():
        pass

    @staticmethod
    def del_medical_record(request):
        if request.GET:
            tx_id = request.GET['record_tx_id']
            operator_id = request.GET['patient_id']
            logger.info('tx_id: ' + tx_id)
            logger.info('patient_id: ' + operator_id)
            operator_type = OperatorType.PATIENT.value
            MedicalRecordService.del_by_tx_id(tx_id, operator_type, operator_id)
            return render(request, 'patient-manager.html', {'msg': '删除' + tx_id + "成功"})

        return render_to_response('error.html')

    @staticmethod
    def to_update_medical_record(request):
        if request.GET:
            record_tx_id = request.GET['record_tx_id']
            logger.info('tx_id: ' + record_tx_id)
            record_dict = TransactionService.find_contents_by_id(record_tx_id)

            doctor_id = record_dict['doctor_id']
            doctor_dict = DoctorService.find_by_id(doctor_id)

            return render(request, 'update_medical_record.html', {'record': record_dict, 'doctor': doctor_dict})

        return render_to_response('error.html')

    @staticmethod
    @csrf_exempt
    def update_medical_record(request):
        if request.POST:
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
            # 更新 record_dict，下面函数会直接更改 record_dict，而不需要返回值
            MedicalRecordService.modify_record_fields(record_dict, rtn_fields_dict)

            doctor_id = record_dict['doctor_id']
            doctor_dict = DoctorService.find_by_id(doctor_id)

            return render(request, 'show_patient_record.html', {'record': record_dict, 'doctor': doctor_dict})

        return render_to_response('error.html')

