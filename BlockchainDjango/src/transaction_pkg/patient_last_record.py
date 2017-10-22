#!/usr/bin/python3
# -*- coding: UTF-8 -*-


class PatientLastRecord(object):
    """
    记录病人及就诊记录对照的信息，存储在一个Transaction对象的 content field 中。
    """

    def __init__(self, patient_id, last_record_id,):
        """
        用于记录病人最后一个区块的ID
        :param patient_id: 病人的id
        :param last_record_id: 病人最后一条就诊记录的ID
        """
        self.patient_id = patient_id
        self.last_record_id = last_record_id
