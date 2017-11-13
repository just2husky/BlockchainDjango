from twisted.internet import protocol, reactor
import multiprocessing
import json

from BlockchainDjango.util.logging_util import Logger
from BlockchainDjango.util.const import MsgType
from BlockchainDjango.entity.transaction import Transaction
from BlockchainDjango.entity.message import Message
from BlockchainDjango.service.transaction_service import TransactionService
from BlockchainDjango.service.message_service import MessageService


class Echo(protocol.Protocol):
    def dataReceived(self, data):
        # As soon as any data is received, write it back
        msg = data.decode()
        Logger.info('接收到客户端数据: ' + msg)

        msg_dict = json.loads(msg)
        msg_type = msg_dict['msg_type']
        if msg_type == MsgType.CLI.value:
            Logger.info("msg类型为: " + msg_type)
            self.process_cli_msg(msg_dict)

        else:
            raise Exception("未知的msg类型")

        self.transport.write("接收到你的数据".encode())

    def process_cli_msg(self, msg_dict):
        """
        用于处理客户端发送的请求消息
        :param msg_dict:
        :return:
        """
        # 1. 验证 Message 本身是否正确
        verify_rlt = MessageService.verify_msg(Message(**msg_dict))
        if verify_rlt:
            Logger.info("MessageService的内容为正确")
            self.transport.write("MessageService内容正确\n".encode())
        else:
            Logger.info("MessageService的内容为错误")
            self.transport.write("MessageService内容错误\n".encode())

        # 2. 验证 Message 中所存储的 Transaction 是否正确
        tx_obj = Transaction()
        tx_dict = msg_dict['transaction']
        tx_obj.init_tx_by_dict(tx_dict)
        Logger.info("Transaction的内容为: " + str(tx_dict))
        verify_rlt = TransactionService.verify_tx(tx_obj)
        if verify_rlt:
            Logger.info("Transaction的内容为正确")
            self.transport.write("Transaction内容正确\n".encode())
        else:
            Logger.info("Transaction的内容为错误")
            self.transport.write("Transaction内容错误\n".encode())


class EchoFactory(protocol.Factory):
    def buildProtocol(self, addr):
        return Echo()


def start_server(port):
    """
    根据port启动相应对的reactor
    :param port:
    :return:
    """
    port = int(port)
    Logger.info('服务起开始监听端口：' + str(port))
    reactor.listenTCP(port, EchoFactory())
    reactor.run()


if __name__ == '__main__':
    pool = multiprocessing.Pool(processes=4)
    for index in range(4):
        pool.apply_async(start_server, (9000+index, ))
    pool.close()
    pool.join()
    Logger.info("Sub-process(es) done.")