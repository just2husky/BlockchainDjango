#!/usr/bin/python3
# -*- coding: UTF-8 -*-


class MedicalRecordUpdate(object):
    """
    记录被删除的就诊记录的id，删除者的id
    """

    def __init__(self, old_tx_id, new_tx_id, operator_type, operator_id, old_patient_id, old_doctor_id):
        """

        :param old_tx_id: 更新前的就诊记录所在的交易单id
        :param new_tx_id: 更新后的诊记录所在的交易单id
        :param operator_type: 操作人的类型，如病人、医生、管理员等
        :param operator_id: 操作人的id
        :param old_patient_id: 更新前的就诊记录中的病人id
        :param old_doctor_id: 更新前的就诊记录中的病人id
        """
        self.old_tx_id = old_tx_id
        self.new_tx_id = new_tx_id
        self.operator_type = operator_type
        self.operator_id = operator_id
        # 存储一条就诊记录的病人与医生的信息，方便病人或医生检索自己就诊记录时，排除这些被删除的医疗记录
        self.old_patient_id = old_patient_id
        self.old_doctor_id = old_doctor_id
