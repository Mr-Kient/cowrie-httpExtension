from netfilterqueue import NetfilterQueue
from scapy.all import IP, send

def cmdRecording(payload):
    pass

def modify_and_send(packet):
    
    print(packet)
    # Convert the raw packet to a scapy IP packet
    ip_packet = IP(packet.get_payload())
    
    # Modify the source IP address
    ip_packet.src = 'new-source-ip'
    
    # CMD Recording
    cmdRecording(packet.get_payload())
    
    # Send the modified packet out
    send(ip_packet)
    
    # Drop the original packet
    packet.drop()

nfqueue = NetfilterQueue()
# Bind to the same queue number specified in the iptables rule
nfqueue.bind(1, modify_and_send)

try:
    print("Starting packet modification...")
    nfqueue.run()
except KeyboardInterrupt:
    print("Stopping...")

nfqueue.unbind()