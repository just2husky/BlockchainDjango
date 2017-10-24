from unittest import TestCase
from BlockchainDjango.service.patient_service import PatientService


class TestPatientService(TestCase):
    def test_save(self):
        self.fail()

    def test_find_by_id(self):
        patient_dict = PatientService.find_by_id('101')
        if patient_dict is not None:
            print(patient_dict)

        else:
            print('未查找到病人')
