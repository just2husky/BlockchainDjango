from twisted.internet import protocol, reactor
import multiprocessing

from BlockchainDjango.util.logging_util import Logger


class Echo(protocol.Protocol):

    def dataReceived(self, data):
        # As soon as any data is received, write it back
        print(data.decode())
        self.transport.write(("接收到你的数据" + data.decode()).encode())


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