#!/usr/bin/python3
# -*- coding: UTF-8 -*-
from django.shortcuts import render_to_response, render
from django.views.decorators.csrf import csrf_exempt

from ..service.block_chain_service import BlockChainService
from ..entity.patient import Patient
from ..service.patient_service import PatientService


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
    def find_patient(request):
        rtn_msg = {'msg': 'find_patient'}
        if request.POST:
            identifier = request.POST['identifier']
            rtn_msg['msg'] = PatientService.find_by_id(identifier)

        return render(request, 'blockchain_manager.html', rtn_msg)