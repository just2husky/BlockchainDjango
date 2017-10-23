#!/usr/bin/python3
# -*- coding: UTF-8 -*-

"""生成init函数里的成员变量"""

attr_str = ('patient_id, record_id, pre_patient_record_id')

attr_list = attr_str.split(', ')

for attr in attr_list:
    print('self.' + attr + ' = ' + attr)
