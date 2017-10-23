#!/usr/bin/python3
# -*- coding: UTF-8 -*-


def doctor_login(doctor_id, password):
    """
    登录
    :param doctor_id:
    :param password:
    :return:
    """
    if '10' == doctor_id.strip() and '123' == password.strip():
        return True
    else:
        return False
