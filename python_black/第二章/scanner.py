from netaddr import *
import socket

for ip in  IPNetwork("192.168.1.0/24"):
    s = socket.socket()
    print(ip)
    s.connect((ip,25))