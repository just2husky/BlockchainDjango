#!/usr/bin/python3
# -*- coding: UTF-8 -*-


class DoctorRecord(object):
    """
    记录医生及就诊记录对照的信息，存储在一个Transaction对象的 content field 中。
    """

    def __init__(self, doctor_id, record_id):
        """
        记录医生与其就诊记录的关系
        :param doctor_id:
        :param record_id:
        :param pre_doctor_record_id: 前一条记录的id
        """
        self.doctor_id = doctor_id
        self.record_id = record_id
        # self.pre_doctor_record_id = pre_doctor_record_id
