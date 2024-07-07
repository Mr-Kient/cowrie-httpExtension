import os
from netfilterqueue import NetfilterQueue
from scapy.all import IP, TCP
import logging

def process_packet(packet):
    scapy_packet = IP(packet.get_payload())  # Convert the raw packet to a Scapy IP packet
    if scapy_packet.haslayer(TCP):
        tcp_layer = scapy_packet[TCP]
        source_port = tcp_layer.sport  # Get source port
        destination_ip = scapy_packet.dst  # Get destination IP
        payload = bytes(tcp_layer.payload)  # Access the payload from the TCP layer

        # Print packet details
        print(f"Source Port: {source_port}, Destination IP: {destination_ip}, TCP Payload: {payload}")
        logging.info(f"Source Port: {source_port}, Destination IP: {destination_ip}, TCP Payload: {payload}")
    packet.accept()  # Accept the packet after processing

nfqueue = NetfilterQueue()
nfqueue.bind(1, process_packet)  # Bind to queue number 1

logging.basicConfig(filename="OutboundRecord.log", 
                    filemode="w", 
                    format="%(asctime)s %(name)s:%(levelname)s:%(message)s", 
                    datefmt="%d-%m-%Y %H:%M:%S", 
                    level=logging.DEBUG)

try:
    print("Starting packet processing...")
    nfqueue.run()
except KeyboardInterrupt:
    print("Stopping packet processing...")
    nfqueue.unbind()
