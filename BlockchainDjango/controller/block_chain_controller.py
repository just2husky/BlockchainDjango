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
        return render_to_response('blockchain_manager.html')

    @staticmethod
    def to_add_patient(request):
        return render_to_response('add-patient.html')

    @staticmethod
    def to_add_doctor(request):
        return render_to_response('add-doctor.html')

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
