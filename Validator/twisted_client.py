import json
import time
from twisted.internet import reactor, protocol

from BlockchainDjango.service.transaction_service import TransactionService
from BlockchainDjango.entity.message import Message
from BlockchainDjango.util.const import MsgType
from BlockchainDjango.util.logging_util import Logger


class EchoClient(protocol.Protocol):
    def connectionMade(self):
        self.send_tx()

    def dataReceived(self, data):
        Logger.info("Server said: " + data.decode())
        self.transport.loseConnection()

    def connectionLost(self, reason):
        Logger.info("connection lost")

    def send_tx(self):
        """
        发送一个测试用的Transaction
        :return:
        """
        transaction = TransactionService.gen_tx("signature")
        tx_str = json.dumps(Message(msg_type=MsgType.CLI.value,
                                    transaction=transaction.__dict__,
                                    timestamp=str(time.time())).__dict__)
        self.transport.write(tx_str.encode())


class EchoFactory(protocol.ClientFactory):
    def buildProtocol(self, addr):
        return EchoClient()

    def clientConnectionFailed(self, connector, reason):
        Logger.info("Connection failed - goodbye!")
        reactor.stop()

    def clientConnectionLost(self, connector, reason):
        Logger.info("Connection lost - goodbye!")
        reactor.stop()


reactor.connectTCP("localhost", 9001, EchoFactory())
reactor.run()
