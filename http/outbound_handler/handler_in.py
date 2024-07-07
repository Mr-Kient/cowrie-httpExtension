import os
from netfilterqueue import NetfilterQueue
from scapy.all import IP, TCP
import logging

def process_packet(packet):
    scapy_packet = IP(packet.get_payload())  # Convert the raw packet to a Scapy IP packet
    if scapy_packet.haslayer(TCP):
        tcp_layer = scapy_packet[TCP]
        source_ip = scapy_packet.src  # Get source IP
        destination_port = tcp_layer.dport  # Get destination port
        payload = bytes(tcp_layer.payload)
        # Ignore packets to ports 22 (SSH) and 80 (HTTP)
        # if destination_port == 22:
        if destination_port != 22 and destination_port != 80:
            # Print packet details for other ports
            print(f"Source IP: {source_ip}, Destination Port: {destination_port}, TCP Payload: {payload}")
            logging.info(f"Source IP: {source_ip}, Destination Port: {destination_port}, TCP Payload: {payload}")

    packet.accept()  # Accept the packet after processing

nfqueue = NetfilterQueue()
nfqueue.bind(2, process_packet)  # Bind to queue number 1

logging.basicConfig(filename="InboundRecord.log", 
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
