#!/usr/bin/python3
# -*- coding: UTF-8 -*-
from .doctor_service import DoctorService


def doctor_login(doctor_id, password):
    """
    登录
    :param doctor_id:
    :param password:
    :return:
    """

    doctor_dict = DoctorService.find_by_id(doctor_id)
    if doctor_dict is not None and '123' == password.strip():
        return True
    else:
        return False
