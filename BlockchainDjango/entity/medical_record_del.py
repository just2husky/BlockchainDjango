#!/usr/bin/python3
# -*- coding: UTF-8 -*-


class MedicalRecordDel(object):
    """
    记录被删除的就诊记录的id，删除者的id
    """

    def __init__(self, tx_id, operator_id, patient_id, doctor_id):
        self.tx_id = tx_id
        self.operator_id = operator_id
        # 存储一条就诊记录的病人与医生的信息，方便病人或医生检索自己就诊记录时，排除这些被删除的医疗记录
        self.patient_id = patient_id
        self.doctor_id = doctor_id
