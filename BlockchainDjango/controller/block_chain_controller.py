#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import logging

from django.shortcuts import render_to_response, render
from django.views.decorators.csrf import csrf_exempt

from ..service.block_chain_service import BlockChainService
from ..entity.patient import Patient
from ..entity.doctor import Doctor
from ..service.patient_service import PatientService
from ..service.doctor_service import DoctorService
from ..service.medical_record_service import MedicalRecordService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BlockChainController(object):

    @staticmethod
    def init(request):
        last_block_id = BlockChainService.init()
        rtn_msg = {'msg': '初始化区块链成功，初始区块ID为：' + last_block_id}
        # ctx['msg'] = '初始化区块链成功，初始区块ID为：' + last_block_id
        return render(request, 'blockchain_manager.html', rtn_msg)

    @staticmethod
    def manager(request):
        return render(request, 'blockchain_manager.html', {'session': request.session})

    @staticmethod
    def to_add_patient(request):
        return render_to_response('add-patient.html')

    @staticmethod
    def to_add_doctor(request):
        return render_to_response('add-doctor.html')

    @staticmethod
    @csrf_exempt
    def to_add_medical_record(request):
        """
        若医生已登录，则跳转到 add-medical-record.html 页面
        否则跳转到登录页面
        :param request:
        :return:
        """

        doctor_id = request.session.get('doctor_id')
        if '' != doctor_id and doctor_id is not None:
            logger.info(doctor_id + " 已登录")
            patient = PatientService.find_by_id(request.POST['patient_id'])
            if patient is not None:
                rtn_msg = {'session': request.session, 'patient': patient}
                return render(request, 'add-medical-record.html', rtn_msg)
            else:
                return render(request, 'blockchain_manager.html',
                              {'msg': '病人' + request.POST['patient_id'] + '不存在！'})

        else:
            logger.info("未登录，跳转到登录页面")
            return render_to_response('log_page.html')

    @staticmethod
    @csrf_exempt
    def add_medical_record(request):

        rtn_msg = {}
        if request.POST:
            patient_id = request.POST['patient_id']
            doctor_id = request.session.get('doctor_id')
            chief_complaint = request.POST['chief_complaint']
            present_illness_history = request.POST['present_illness_history']
            past_history = request.POST['past_history']
            record_loc = request.POST['record_loc']
            last_block_id = MedicalRecordService.add(patient_id, doctor_id, record_loc,
                                                     chief_complaint, present_illness_history, past_history)
            rtn_msg['msg'] = '就诊记录信息存储成功，所在区块为：' + last_block_id

        return render(request, 'blockchain_manager.html', rtn_msg)

    @staticmethod
    @csrf_exempt
    def add_patient(request):
        rtn_msg = {}
        if request.POST:
            identifier = request.POST['identifier']
            name = request.POST['name']
            gender = request.POST['gender']
            age = request.POST['age']
            nation = request.POST['nation']
            born_loc = request.POST['born_loc']
            address = request.POST['address']
            patient = Patient(identifier, name, gender, age, nation, born_loc, address)
            last_block_id = PatientService.save(patient)
            rtn_msg['msg'] = '病人信息存储成功，所在区块为：' + last_block_id

        return render(request, 'add-patient.html', rtn_msg)

    @staticmethod
    @csrf_exempt
    def add_doctor(request):
        rtn_msg = {}
        if request.POST:
            identifier = request.POST['identifier']
            name = request.POST['name']
            gender = request.POST['gender']
            age = request.POST['age']
            nation = request.POST['nation']
            hospital = request.POST['hospital']
            department = request.POST['department']
            grade = request.POST['grade']
            doctor = Doctor(identifier, name, gender, age, nation, hospital, department, grade)
            last_block_id = DoctorService.save(doctor)
            rtn_msg['msg'] = '医生信息存储成功，所在区块为：' + last_block_id

        return render(request, 'add-doctor.html', rtn_msg)

    @staticmethod
    @csrf_exempt
    def find_patient(request):
        # status 0:获取失败 1:获取成功
        rtn_msg = {}
        if request.POST:
            identifier = request.POST['identifier']
            patient_dict = PatientService.find_by_id(identifier)
            if patient_dict is not None:
                patient_dict['status'] = '1'
                rtn_msg['patient'] = patient_dict
            else:
                rtn_msg['patient'] = {'status': '0'}

        return render(request, 'blockchain_manager.html', rtn_msg)

    @staticmethod
    @csrf_exempt
    def find_doctor(request):
        # status 0:获取失败 1:获取成功
        rtn_msg = {}
        if request.POST:
            identifier = request.POST['identifier']
            doctor_dict = DoctorService.find_by_id(identifier)
            if doctor_dict is not None:
                doctor_dict['status'] = '1'
                rtn_msg['doctor'] = doctor_dict
            else:
                rtn_msg['doctor'] = {'status': '0'}

        return render(request, 'blockchain_manager.html', rtn_msg)

