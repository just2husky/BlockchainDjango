from unittest import TestCase
from BlockchainDjango.service.transaction_service import TransactionService


class TestTransactionService(TestCase):

    def test_find_txs_by_ids(self):
        print(TransactionService.find_txs_by_ids(['c934d45bd8da26cbc0d13caeebc3f5f2507b8c1868dd5689ba545f943d8a7857']))
