#!/usr/bin/python3
from ecdsa import SigningKey
import ecdsa

from .const import Const


class Signature(object):

    @staticmethod
    def gen_key_pair():
        """
        生成一对秘钥对，分别存储在sk.pem（私钥），vk.pem（公钥）文件中
        :return: 返回秘钥对
        """
        pvt_key = SigningKey.generate()
        open(Const.PVT_KEY_LOC, "wb").write(pvt_key.to_pem())
        pub_key = pvt_key.get_verifying_key()
        open(Const.PUB_KEY_LOC, "wb").write(pub_key.to_pem())
        return pvt_key, pub_key

    @staticmethod
    def sign(pvt_key, content):
        """
        根据私钥对content进行数字签名
        :param pvt_key:
        :param content:
        :return:
        """
        return pvt_key.sign(bytes(content, encoding="utf8"),  sigencode=ecdsa.util.sigencode_string)

    @staticmethod
    def verify(pub_key, content, signature):
        """
        根据公钥，数字签名对content进行验证
        :param pub_key:
        :param content:
        :param signature:
        :return:
        """
        return pub_key.verify(signature, bytes(content, encoding="utf8"))


if __name__ == "__main__":
    sk, vk = Signature.gen_key_pair()
    print(sk)
    print(vk)
