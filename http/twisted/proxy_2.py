from twisted.web import server, http
from twisted.internet import reactor

class ProxyRequest(http.Request):
    """
    Custom HTTP request handler that forwards requests to the real server
    and relays the response back to the client.
    """

    def __init__(self, channel, real_server_host, real_server_port):
        http.Request.__init__(self, channel)
        self.real_server_host = real_server_host
        self.real_server_port = real_server_port

    def process(self):
        """
        Overrides the default process method to handle forwarding logic.
        """
        self.headers['Host'] = self.getHeader('Host').decode()  # Ensure proper decoding
        self.path = self.path.decode()  # Decode the path component

        # Create a new client factory to connect to the real server
        factory = http.ClientFactory(reactor.callLater(0, self.handle_response))
        reactor.connectTCP(self.real_server_host, self.real_server_port, factory)
        factory.proxy_request = self  # Store a reference to the proxy request
        factory.buildProtocol(self.transport)  # Send the request to the real server

    def handle_response(self, response):
        """
        Callback function that handles the response from the real server.
        Forwards the response to the client.
        """
        self.setResponseCode(response.code, response.reason.phrase)
        for key, value in response.headers.items():
            self.setHeader(key.decode(), value.decode())  # Decode headers
        self.setContentLength(response.length)
        self.write(response.read())
        self.finish()

class Proxy(server.Site):
    """
    Proxy server class that sets up the request handler.
    """

    def __init__(self, real_server_host, real_server_port):
        # **Fix:** Pass the channel argument from the Site constructor
        handler = ProxyRequest(self.channel, real_server_host, real_server_port)
        server.Site.__init__(self, handler)

if __name__ == '__main__':
    # Replace with your desired real server host and port
    REAL_SERVER_HOST = "163.114.104.81"
    REAL_SERVER_PORT = 80

    # Create and start the proxy server
    proxy = Proxy(REAL_SERVER_HOST, REAL_SERVER_PORT)
    reactor.listenTCP(8080, proxy)  # Replace 8080 with your chosen port
    reactor.run()
