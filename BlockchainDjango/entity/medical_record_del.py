#!/usr/bin/python3
# -*- coding: UTF-8 -*-


class MedicalRecordDel(object):
    """
    记录被删除的就诊记录的id，删除者的id
    """

    def __init__(self, tx_id, operator_id):
        self.tx_id = tx_id
        self.operator_id = operator_id
