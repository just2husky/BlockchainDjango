#!/usr/bin/python3
# -*- coding: UTF-8 -*-


class MedicalRecord(object):
    """
        记录一条病历的信息，存储在一个Transaction对象的 content field 中。
    """

    def __init__(self, identifier, doctor_id, patient_id, record_time, record_loc, chief_complaint,
                 present_illness_history, past_history, record_type='add'):
        """

        :param identifier:
        :param doctor_id:
        :param patient_id:
        :param record_time: 记录的时间
        :param record_loc: 记录所在的医院、科室
        :param chief_complaint: 主诉
        :param present_illness_history: 现病史
        :param past_history: 既往史
        :param record_type: 此条记录的类型，如为新添加的一条记录、对前面记录修改、或删除之前的一条记录
        """
        self.identifier = identifier
        self.doctor_id = doctor_id
        self.patient_id = patient_id
        self.record_time = record_time
        self.record_loc = record_loc
        self.chief_complaint = chief_complaint
        self.present_illness_history = present_illness_history
        self.past_history = past_history
        self.record_type = record_type

