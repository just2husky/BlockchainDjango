from unittest import TestCase
from BlockchainDjango.service.medical_record_service import MedicalRecordService


class TestMedicalRecordService(TestCase):

    def test_find_by_id(self):
        record_id = '10120171026170032'
        medical_record = MedicalRecordService.find_by_id(record_id)
        print(medical_record)

    def test_find_by_patient_id(self):
        patient_id = '101'
        tx_list = MedicalRecordService.find_by_patient_id(patient_id)
        print(tx_list)

    def test_find_by_doctor_id(self):
        doctor_id = '001'
        tx_list = MedicalRecordService.find_by_doctor_id(doctor_id)
        print(tx_list)

