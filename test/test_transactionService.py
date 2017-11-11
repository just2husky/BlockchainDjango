from unittest import TestCase
from BlockchainDjango.service.transaction_service import TransactionService


class TestTransactionService(TestCase):
    def test_find_txs_by_ids(self):
        print(TransactionService.find_txs_by_ids(['c934d45bd8da26cbc0d13caeebc3f5f2507b8c1868dd5689ba545f943d8a7857']))

    def test_gen_tx(self):
        transaction = TransactionService.gen_tx("signature")
        sig_str = transaction.signature
        self.assertNotEqual(sig_str,
        '2728add92e953edd25190d957357640fdc0d15949fbd827ea9b411fbbe1e7dc44f5ae3ecc5d8bbdb4e4832bc03650cf7',
                            '数字签名出错！')
        self.assertNotEqual(type(sig_str), 'str', '数字签名类型不为str！')
