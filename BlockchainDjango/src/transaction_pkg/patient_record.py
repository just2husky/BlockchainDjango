#!/usr/bin/python3
# -*- coding: UTF-8 -*-


class PatientRecord(object):
    """
    记录病人及就诊记录对照的信息，存储在一个Transaction对象的 content field 中。
    """

    def __init__(self, patient_id, record_id, pre_patient_record_id):
        """
        记录病人与其就诊记录的关系
        :param patient_id:
        :param record_id:
        :param pre_patient_record_id: 前一条记录的id
        """
        self.patient_id = patient_id
        self.record_id = record_id
        self.pre_patient_record_id = pre_patient_record_id
