#!/usr/bin/python3
from ecdsa import SigningKey
from ecdsa import VerifyingKey
import ecdsa
import os.path
import hashlib

from .const import Const


class Signature(object):

    @staticmethod
    def gen_key_pair():
        """
        生成一对秘钥对，分别存储在sk.pem（私钥），vk.pem（公钥）文件中
        :return: 返回秘钥对
        """

        pvt_key = SigningKey.generate(curve=Const.CURVE)
        open(Const.PVT_KEY_LOC, "wb").write(pvt_key.to_pem())
        pub_key = pvt_key.get_verifying_key()
        open(Const.PUB_KEY_LOC, "wb").write(pub_key.to_pem())
        return pvt_key, pub_key

    @staticmethod
    def get_key_pair():
        """
        若保存密钥对的文件存在则从文件中读取秘钥，否则重新生成
        :return:
        """
        if os.path.exists(Const.PVT_KEY_LOC) and os.path.exists(Const.PUB_KEY_LOC):
            pvt_key = SigningKey.from_pem(open(Const.PVT_KEY_LOC).read())
            pub_key = VerifyingKey.from_pem(open(Const.PUB_KEY_LOC).read())

        else:
            pvt_key, pub_key = Signature.gen_key_pair()

        return pvt_key, pub_key

    @staticmethod
    def sign(pvt_key, content):
        """
        根据私钥对content进行数字签名
        :param pvt_key:
        :param content: 为string类型
        :return:
        """
        return pvt_key.sign(bytes(content, encoding="utf8"),  sigencode=ecdsa.util.sigencode_string)

    @staticmethod
    def verify(pub_key, content, signature):
        """
        根据公钥，数字签名对content进行验证
        :param pub_key:
        :param content:
        :param signature: 为string类型
        :return:
        """
        return pub_key.verify(bytes.fromhex(signature), bytes(content, encoding="utf8"))

    @staticmethod
    def gen_id_by_sig(signature):
        """
        根据传入的 signature，生成交易的ID
        :param signature: 为sting类型
        :return: 交易的id
        """
        return hashlib.sha256(bytes.fromhex(signature)).hexdigest()


if __name__ == "__main__":
    sk, vk = Signature.gen_key_pair()
    print(sk)
    print(vk)
