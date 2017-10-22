#!/usr/bin/python3
# -*- coding: UTF-8 -*-
"""
    本文件用来保存一些对 transaction 操作的函数
"""
import os
import time
import logging

from BlockchainDjango.src.signature import Signature
from ecdsa import SigningKey
from ecdsa import VerifyingKey

from BlockchainDjango.src.transaction_pkg.transaction import Transaction
from BlockchainDjango.src.util import couchdb_util
from BlockchainDjango.src.util.const import Const
from BlockchainDjango.src.transaction_pkg.patient import Patient
from BlockchainDjango.src.transaction_pkg.doctor import Doctor
from BlockchainDjango.src.transaction_pkg.medical_record import MedicalRecord
from BlockchainDjango.src.transaction_pkg.patient_record import PatientRecord
from BlockchainDjango.src.transaction_pkg.patient_last_record import PatientLastRecord
from BlockchainDjango.src.transaction_pkg.doctor_record import DoctorRecord
from BlockchainDjango.src.transaction_pkg.doctor_last_record import DoctorLastRecord

db = couchdb_util.get_db(Const.DB_NAME)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def gen_tx(content):
    """
    测试生成一条transaction
    :return: 生成的transaction
    """
    if content is None:
        raise Exception("The content is None!")

    if os.path.exists(Const.PVT_KEY_LOC) and os.path.exists(Const.PUB_KEY_LOC):
        pvt_key = SigningKey.from_pem(open(Const.PVT_KEY_LOC).read())
        pub_key = VerifyingKey.from_pem(open(Const.PUB_KEY_LOC).read())
    else:
        pvt_key, pub_key = Signature.gen_key_pair()

    timestamp = time.time()
    # 若content是对象类型，则将其转化为json格式字符串存储
    if isinstance(content, str):
        temp_tx = Transaction(pub_key.to_pem().decode(), content, timestamp)
        signature = Signature.sign(pvt_key, content)
    else:
        temp_tx = Transaction(pub_key.to_pem().decode(), content.__dict__.__str__(), timestamp)
        signature = Signature.sign(pvt_key, content.__dict__.__str__())

    temp_tx.set_signature(signature)
    temp_tx.set_id()
    temp_tx.tx_type = get_tx_type(content)
    return temp_tx


def get_tx_type(content):
    """
    判断 content 类型并返回
    :param content: Transaction 对象所存储的内容
    :return: content 类型
    """
    if isinstance(content, Patient):
        logger.info("此 Transaction 存储的类型为 patient")
        return 'patient'

    elif isinstance(content, Doctor):
        logger.info("此 Transaction 存储的类型为 doctor")
        return 'doctor'

    elif isinstance(content, MedicalRecord):
        logger.info("此 Transaction 存储的类型为 medical_record")
        return 'medical_record'

    elif isinstance(content, PatientRecord):
        logger.info("此 Transaction 存储的类型为 patient_record")
        return 'patient_record'

    elif isinstance(content, PatientLastRecord):
        logger.info("此 Transaction 存储的类型为 patient_last_record")
        return 'patient_last_record'

    elif isinstance(content, DoctorRecord):
        logger.info("此 Transaction 存储的类型为 doctor_record")
        return 'doctor_record'

    elif isinstance(content, DoctorLastRecord):
        logger.info("此 Transaction 存储的类型为 doctor_last_record")
        return 'doctor_last_record'

    elif isinstance(content, str):
        logger.info("此 Transaction 存储的类型为 string")
        return 'string'

    elif content is None:
        logger.info("此 Transaction 存储的类型为 none")
        return 'none'

    else:
        raise Exception('未知 Transaction 类型！')


def save_tx(transaction):
    """ 将一条 transaction 信息存储 couchdb数据库里"""
    if not isinstance(transaction, Transaction):
        raise Exception("形参transaction类型错误，必须为Transaction类的实例！")
    else:
        couchdb_util.save(db, {'_id': transaction.get_id(), 'Transaction': transaction.__dict__.__str__()})


def save_tx_list(transaction_list):
    """ 循环调用 save_tx, 将transaction list 存入到数据库中"""
    for each_tx in transaction_list:
        save_tx(each_tx)


def get_tx_ids(transaction_list):
    """根据传入的 transaction_list，得到各个 transaction 的 id，以tuple的形式返回"""
    id_list = []
    for each_transaction in transaction_list:
        id_list.append(each_transaction.get_id())
    return tuple(id_list)


def class_medical_record_test():
    # 测试 MedicalRecord 类
    # 生成3个Transaction，存储的内容分别为3个医生的信息
    patient1_id = '1001'
    patient2_id = '1002'
    patient3_id = '1003'

    record1_time = time.strftime("%Y%m%d%H%M%S", time.localtime())
    record2_time = time.strftime("%Y%m%d%H%M%S", time.localtime())
    record3_time = time.strftime("%Y%m%d%H%M%S", time.localtime())

    doctor1_id = '10'
    doctor2_id = '11'
    doctor3_id = '12'

    record1_id = patient1_id + record1_time
    record2_id = patient2_id + record2_time
    record3_id = patient3_id + record3_time

    record1_loc = '望江医院呼吸科'
    record2_loc = '华西保健医院口腔科'
    record3_loc = '华西医院消化科'

    chief_complaint1 = '咳嗽'
    chief_complaint2 = '牙疼'
    chief_complaint3 = '肚子疼'

    present_illness_history1 = '支气管炎'
    present_illness_history2 = '龋齿'
    present_illness_history3 = '肠胃炎'

    past_history1 = '鼻窦炎'
    past_history2 = '牙髓炎'
    past_history3 = '胃溃疡'

    record_type1 = 'add'
    record_type2 = 'add'
    record_type3 = 'add'

    medical_record1 = MedicalRecord(record1_id, doctor1_id, patient1_id, record1_time, record1_loc,
                                    chief_complaint1, present_illness_history1, past_history1, record_type1)
    medical_record2 = MedicalRecord(record2_id, doctor2_id, patient2_id, record2_time, record2_loc,
                                    chief_complaint2, present_illness_history2, past_history2, record_type2)
    medical_record3 = MedicalRecord(record3_id, doctor3_id, patient3_id, record3_time, record3_loc,
                                    chief_complaint3, present_illness_history3, past_history3, record_type3)
    content_list = [medical_record1, medical_record2, medical_record3]
    transaction_list = []
    for content in content_list:
        transaction_list.append(gen_tx(content))

    # save_tx_list(transaction_list)
    return transaction_list.copy()


def class_patient_record_test():
    """

    :return: 返回 新生成的 PatientRecord Transaction list 与 PatientLastRecord Transaction list
    """
    patient1_id = '1001'
    patient2_id = '1002'
    patient3_id = '1003'

    record1_id = 'e6a0a03baa28085f3c088814f674d5e2bf8f8faf48b96709c51c0ad69e3db04c'
    record2_id = 'e6d455b76121f63ea9516fb5bce0e881c126491ecaa4302a99b930d42810e640'
    record3_id = 'b74fd24a4fa6078f81cdcb7f327ff999a84c2b4e732fac2efced046f3b1b186f'

    # 病人第一条就诊记录的 pre_patient_record_id 值为0
    pre_patient_record_id = '0000000000000000000000000000000000000000000000000000000000000000'

    pr1 = PatientRecord(patient1_id, record1_id, pre_patient_record_id)
    pr2 = PatientRecord(patient2_id, record2_id, pre_patient_record_id)
    pr3 = PatientRecord(patient3_id, record3_id, pre_patient_record_id)

    pr_content_list = [pr1, pr2, pr3]
    pr_list = []
    for content in pr_content_list:
        pr_list.append(gen_tx(content))

    plr1 = PatientLastRecord(patient1_id, record1_id)
    plr2 = PatientLastRecord(patient2_id, record2_id)
    plr3 = PatientLastRecord(patient3_id, record3_id)

    plr_content_list = [plr1, plr2, plr3]
    plr_list = []
    for content in plr_content_list:
        plr_list.append(gen_tx(content))

    return pr_list.copy(), plr_list.copy()


def class_doctor_record_test():
    """

    :return: 返回 新生成的 DoctorRecord Transaction list 与 DoctorLastRecord Transaction list
    """
    doctor1_id = '10'
    doctor2_id = '11'
    doctor3_id = '12'

    record1_id = 'e6a0a03baa28085f3c088814f674d5e2bf8f8faf48b96709c51c0ad69e3db04c'
    record2_id = 'e6d455b76121f63ea9516fb5bce0e881c126491ecaa4302a99b930d42810e640'
    record3_id = 'b74fd24a4fa6078f81cdcb7f327ff999a84c2b4e732fac2efced046f3b1b186f'

    # 病人第一条就诊记录的 pre_doctor_record_id 值为0
    pre_doctor_record_id = '0000000000000000000000000000000000000000000000000000000000000000'

    dr1 = DoctorRecord(doctor1_id, record1_id, pre_doctor_record_id)
    dr2 = DoctorRecord(doctor2_id, record2_id, pre_doctor_record_id)
    dr3 = DoctorRecord(doctor3_id, record3_id, pre_doctor_record_id)

    dr_content_list = [dr1, dr2, dr3]
    dr_list = []
    for content in dr_content_list:
        dr_list.append(gen_tx(content))

    plr1 = DoctorLastRecord(doctor1_id, record1_id)
    plr2 = DoctorLastRecord(doctor2_id, record2_id)
    plr3 = DoctorLastRecord(doctor3_id, record3_id)

    plr_content_list = [plr1, plr2, plr3]
    plr_list = []
    for content in plr_content_list:
        plr_list.append(gen_tx(content))

    return dr_list.copy(), plr_list.copy()


if __name__ == "__main__":
    """测试"""
    opt = '8'

    if '1' == opt:
        aTransaction = gen_tx("save_tx(transaction) 测试")
        save_tx(aTransaction)

    elif '2' == opt:
        # 生成4个Transaction，存储的内容分别为 aaa, bbb, ccc, ddd
        tx_content_list = ["aaa", "bbb", "ccc", "ddd"]
        tx_list = []
        for tx_content in tx_content_list:
            tx_list.append(gen_tx(tx_content))

        save_tx_list(tx_list)

    elif'3' == opt:
        # 生成4个Transaction，存储的内容分别为 aaa, bbb, ccc, ddd
        tx_content_list = ["aaa", "bbb", "ccc", "ddd"]
        tx_list = []
        for tx_content in tx_content_list:
            tx_list.append(gen_tx(tx_content))

        tx_ids = get_tx_ids(tx_list)
        print(type(tx_ids))
        print(tx_ids)

    elif '4' == opt:
        # 生成3个Transaction，存储的内容分别为3个病人的信息

        patient1 = Patient('1001', '张超', '男', '18', '汉', '山东', '四川大学望江校区')
        patient2 = Patient('1002', '陈泽堃', '男', '28', '汉', '福建', '四川大学望江校区')
        patient3 = Patient('1003', '叶雄峰', '男', '28', '汉', '浙江', '四川大学望江校区')
        tx_content_list = [patient1, patient2, patient3]
        tx_list = []
        for tx_content in tx_content_list:
            tx_list.append(gen_tx(tx_content))

        save_tx_list(tx_list)

    elif '5' == opt:
        # 测试 Doctor 类
        # 生成3个Transaction，存储的内容分别为3个医生的信息
        doctor1 = Doctor('10', '邹越', '男', '28', '汉', '望江医院', '呼吸科', '主治医师')
        doctor2 = Doctor('11', '许刚', '男', '28', '汉', '华西保健医院', '口腔科', '副主任医师')
        doctor3 = Doctor('12', '郑腾霄', '男', '28', '汉', '华西医院', '消化科', '主任医师')
        tx_content_list = [doctor1, doctor2, doctor3]
        tx_list = []
        for tx_content in tx_content_list:
            tx_list.append(gen_tx(tx_content))

        save_tx_list(tx_list)

    elif '6' == opt:
        tx_list = class_medical_record_test()
        save_tx_list(tx_list)

    elif '7' == opt:
        tx_list1, tx_list2 = class_patient_record_test()
        save_tx_list(tx_list1)
        save_tx_list(tx_list2)

    elif '8' == opt:
        tx_list1, tx_list2 = class_doctor_record_test()
        save_tx_list(tx_list1)
        save_tx_list(tx_list2)
