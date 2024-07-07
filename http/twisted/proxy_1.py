from twisted.internet import reactor, protocol
from twisted.web import proxy, http
from twisted.python import log
from twisted.python.logfile import DailyLogFile
from sys import stdout

# Configure logging to a file
log_file = DailyLogFile.fromFullPath('/root/twisted/proxy.log')  # Set the file path to '/root/twisted/proxy.log'
log.startLogging(log_file)

# Define the ProxyClientProtocol class to handle communication with the real server
class ProxyClientProtocol(protocol.Protocol):
    def __init__(self, proxy_request):
        self.proxy_request = proxy_request

    def connectionMade(self):
        self.proxy_request.client_connection_made(self)

    def dataReceived(self, data):
        self.proxy_request.client_data_received(data)

    def connectionLost(self, reason):
        self.proxy_request.client_connection_lost(reason)

# Define the ProxyRequest class to process requests from clients
class ProxyRequest(proxy.ProxyRequest):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.real_server_protocol = None

    def process(self):
        log.msg(f"Received request from client {self.getClientIP()}: {self.method} {self.uri}")
        self.content.seek(0, 0)
        data = self.content.read()
        self.content = None
        real_server_ip = '163.114.104.81'  # Replace 'REAL_SERVER_IP' with the actual IP address of the real server
        real_server_port = 80  # Replace REAL_SERVER_PORT with the actual port of the real server
        client_protocol = ProxyClientProtocol(self)
        reactor.connectTCP(real_server_ip, real_server_port, ProxyClientFactory(client_protocol))

    def getClientIP(self):
        peer = self.transport.getPeer()
        return peer.host

    def client_connection_made(self, client_protocol):
        self.real_server_protocol = client_protocol
        self.real_server_protocol.transport.write(self.content.getvalue())

    def client_data_received(self, data):
        self.transport.write(data)

    def client_connection_lost(self, reason):
        self.real_server_protocol = None

# Define the Proxy class to handle HTTP requests from clients
class Proxy(proxy.Proxy):
    requestFactory = ProxyRequest

# Define the ProxyClientFactory class to create instances of the ProxyClientProtocol class
class ProxyClientFactory(protocol.ClientFactory):
    def __init__(self, client_protocol):
        self.client_protocol = client_protocol

    def buildProtocol(self, addr):
        return self.client_protocol

# Define the ProxyFactory class to create instances of the Proxy class
class ProxyFactory(http.HTTPFactory):
    protocol = Proxy

# Start the proxy server
reactor.listenTCP(80, ProxyFactory())
log.msg("Proxy server started!")
reactor.run()
