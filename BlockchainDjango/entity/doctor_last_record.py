#!/usr/bin/python3
# -*- coding: UTF-8 -*-


class DoctorLastRecord(object):
    """
    记录医生及就诊记录对照的信息，存储在一个Transaction对象的 content field 中。
    """

    def __init__(self, doctor_id, last_record_id,):
        """
        用于记录医生最后一个区块的ID
        :param doctor_id: 病人的id
        :param last_record_id: 病人最后一条就诊记录的ID
        """
        self.doctor_id = doctor_id
        self.last_record_id = last_record_id
