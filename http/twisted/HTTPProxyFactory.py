from twisted.internet import reactor, protocol
from twisted.web import http

import threading
import logging

TARGET_SERVER_IP = '163.114.104.81'  # Example IP address
TARGET_SERVER_PORT = 80  # Example port number


class ProxyClient(http.HTTPClient):
    def __init__(self, method, postData, headers, originalRequest, clientAddress):
        self.method = method
        self.postData = postData
        self.headers = headers
        self.originalRequest = originalRequest
        self.clientAddress = clientAddress

    def connectionMade(self):
    #     print(f"Connected to server: {self.transport.getPeer()}")
        print('OriginalRequest:'+ str(self.originalRequest))
        self.sendRequest()
        
    def sendRequest(self):
    #    print(f"Sending request to server: {self.method}")  # Logging request sent to server
        self.sendCommand(self.method, self.originalRequest.uri)
        for header, value in self.headers.items():
            print(f"Function-sedRequest: {header} : {value}")
            self.sendHeader(header, value[0])
        self.endHeaders()
        if self.postData:
            print('********  Postdata Transport  **********',end = '\n')
            print(self.postData)
            logging.info(f'********  Postdata Transport  ********')
            logging.info(f'{self.postData}')
            logging.info(f'*******************')
            self.transport.write(self.postData)

    def handleStatus(self, version, code, message):
        print(f"Received response status: {code} {message}")  # Logging response status
        self.originalRequest.setResponseCode(int(code), message)

    def handleHeader(self, key, value):
        print(f"Received response header: {key}: {value}")  # Logging response header
        self.originalRequest.responseHeaders.addRawHeader(key, value)

    def handleResponse(self, data):
    #    print(f"Received response data: {data}")  # Logging response data
        self.originalRequest.write(data)
        self.originalRequest.finish()
        self.transport.loseConnection()

class ProxyClientFactory(protocol.ClientFactory):
    def __init__(self, method, postData, headers, originalRequest, clientAddress):
        self.protocol = ProxyClient
        self.method = method
        self.postData = postData
        self.headers = headers
        self.originalRequest = originalRequest
        self.clientAddress = clientAddress

    def buildProtocol(self, addr):
        p = self.protocol(self.method, self.postData, self.headers, self.originalRequest, self.clientAddress)
        p.factory = self
        print(f"Connected to server: {addr}")  # Logging server connection
        print('client protocol is being instantiated and connected to the server')
        return p

    def clientConnectionFailed(self, connector, reason):
        print("Failed to connect to server:", reason)
        self.originalRequest.setResponseCode(503)  # Service Unavailable
        self.originalRequest.finish()

class ProxyRequestHandler(http.Request):
    def process(self):
        self.content.seek(0, 0)
        postData = self.content.read()
        headers = dict(self.requestHeaders.getAllRawHeaders())
        print(f'OriginalRequest Headers: total pairs is {len(headers)}')
        for key ,value in headers.items():
            print('{key} : {value}, {valuetype}'.format(key = key, value = value, valuetype = type(value)))
        clientFactory = ProxyClientFactory(self.method, postData, headers, self, self.client.host)
        print(f"****** \n Request from IP: {self.client.host}\n method: {self.method} \n uri: {self.uri} \n clientproto: {self.clientproto} \n *******")  # Logging client request
        logging.info(f"***********************")
        logging.warning(f'Request from IP: {self.client.host}')
        logging.info(f'method: {self.method}')
        logging.info(f'uri: {self.uri}')
        logging.info(f'clientproto: {self.clientproto}')
        logging.info('***********************')
        print(f"Request sent to server: {self.method} {self.uri} HTTP/{self.clientproto}")# Logging request sent to server
        logging.info(f"Request forward to server: {TARGET_SERVER_IP} : {TARGET_SERVER_PORT}")
        logging.info(f'method: {self.method}')
        logging.info(f'uri: {self.uri}')
        logging.info(f'version: {self.clientproto}')
        logging.info('***********************')
        try:
            reactor.connectTCP(TARGET_SERVER_IP, TARGET_SERVER_PORT, clientFactory)
        except Exception as e:
            print("Error processing request:", e)
            logging.warning(f'Error processing request: {e}')
            self.setResponseCode(500)  # Internal Server Error
            self.finish()


class ProxyFactory(http.HTTPFactory):
    def buildProtocol(self, addr):
        protocol = http.HTTPChannel()
        protocol.requestFactory = ProxyRequestHandler
        return protocol

port = 80  # Port number for the proxy server
logging.basicConfig(filename="HttpProxy.log", 
                    filemode="w", 
                    format="%(asctime)s %(name)s:%(levelname)s:%(message)s", 
                    datefmt="%d-%m-%Y %H:%M:%S", 
                    level=logging.DEBUG)
reactor.listenTCP(port, ProxyFactory())
print(f"Proxy server running on port {port}")
logging.info(f"Proxy server running on port {port}")
reactor.run()


# def start_reactor():
#     reactor.run(installSignalHandlers=False)

# def stop_proxy():
#     print("Stopping proxy server...")
#     reactor.stop()

# if __name__ == '__main__':
#     port = 80  # Port number for the proxy server
#     logging.basicConfig(filename="HttpProxy.log", 
#                         filemode="w", 
#                         format="%(asctime)s %(name)s:%(levelname)s:%(message)s", 
#                         datefmt="%d-%m-%Y %H:%M:%S", 
#                         level=logging.DEBUG)
#     reactor.listenTCP(port, ProxyFactory())
#     print(f"Proxy server running on port {port}")
#     logging.info(f"Proxy server running on port {port}")
#     # Start reactor in a separate thread
#     reactor_thread = threading.Thread(target=start_reactor)
#     reactor_thread.start()
    
#     try:
#         while True:
#             # Keep the main thread alive
#             pass
#     except KeyboardInterrupt:
#         # If KeyboardInterrupt is received (e.g., Ctrl+C), stop the proxy server gracefully
#         stop_proxy()
