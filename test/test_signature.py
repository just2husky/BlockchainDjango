from unittest import TestCase
from BlockchainDjango.service.transaction_service import TransactionService


class TestSignature(TestCase):

    def test_verify(self):
        transaction = TransactionService.gen_tx("signature")
        self.assertNotEqual(TransactionService.verify_tx(transaction), 'True')

