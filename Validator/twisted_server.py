from twisted.internet import protocol, reactor


class Echo(protocol.Protocol):

    def dataReceived(self, data):
        # As soon as any data is received, write it back
        print(data.decode())
        self.transport.write(data)


class EchoFactory(protocol.Factory):
    def buildProtocol(self, addr):
        return Echo()


print("等待连接")
reactor.listenTCP(9000, EchoFactory())
reactor.run()
