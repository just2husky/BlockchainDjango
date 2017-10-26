from unittest import TestCase
from BlockchainDjango.service.medical_record_service import MedicalRecordService


class TestMedicalRecordService(TestCase):

    def test_find_by_id(self):
        record_id = '10120171026170032'
        medical_record = MedicalRecordService.find_by_id(record_id)
        print(medical_record)

