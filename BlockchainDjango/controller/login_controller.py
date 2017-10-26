#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from django.shortcuts import render_to_response
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from BlockchainDjango.service.login_service import doctor_login


def log_page(request):
    return render_to_response('log_page.html')


@csrf_exempt
def login(request):
    if request.POST:
        doctor_id = request.POST['doctor_id']
        password = request.POST['password']
        print(request.session.get('doctor_id'))
        result = doctor_login(doctor_id, password)

        if result:
            request.session['doctor_id'] = doctor_id
            return render(request, 'login_success.html',  {'session': request.session})
        else:
            return render(request, 'login_error.html')

