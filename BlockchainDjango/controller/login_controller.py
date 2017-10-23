#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from django.shortcuts import render_to_response


def log_page(request):
    return render_to_response('log_page.html')


def login(request):
    if request.POST:
        doctor_id = request.POST['doctor_id']
        password = request.POST['password']

