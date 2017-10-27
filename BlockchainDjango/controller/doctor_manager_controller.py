#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response


class DoctorManagerController(object):
    """
    用来处理和doctor-manager相关的请求
    """

    @staticmethod
    @csrf_exempt
    def to_doctor_manager(request):
        return render_to_response('doctor-manager.html')
