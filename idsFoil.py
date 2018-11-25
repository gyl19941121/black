from scapy.all import *

def ddosTest(src,dst,count):
    pkt = IP(src=src,dst=dst)/ICMP(type=8,id=678)/Raw(load='1234')
    send(pkt,count=count)
    pkt = IP(src=src,dst=dst)/ICMP(type=0)/Raw(load='AAAAAAAA')
    send(pkt,count=count)
    pkt = IP(src=src,dst=dst)/UDP(dport=31335)/Raw(load='PONG')
    send(pkt,count=count)
    pkt = IP(src=src,dst=dst)/ICMP(type=0,id=456)
    send(pkt,count=count)

def scanTest(src,dst,count):
    pkt = IP(src=src,dst=dst)/UDP(dport=7)/Raw(load='cybercop')
    send(pkt)
    pkt = IP(src=src,dst=dst)/UDP(dport=10080)/Raw(load='Amanda')
    send(pkt,count=count)

src= '1.3.3.7'
dst = '192.168.1.111'
#iface = 'eth0'
count = 1
ddosTest(src,dst,count)
scanTest(src,dst,count)