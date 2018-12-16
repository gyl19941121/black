import socket
import os


#监听主机

host = "192.168.1.105"

#创建原始的套接字，绑定再公开接口上
while True:
    if os.name=="nt":
        socket_protocol = socket.IPPROTO_IP
    else:
        socket_protocol = socket.IPPROTO_ICMP

    sniffer = socket.socket(socket.AF_INET,socket.SOCK_RAW,socket_protocol)

    sniffer.bind((host,0))

    #设置一下捕获的数据包的IP头

    sniffer.setsockopt(socket.IPPROTO_IP,socket.IP_HDRINCL,1)

    #在windows平台下，我们需要设置IOCTL启用混杂模式

    if os.name=="nt":
        sniffer.ioctl(socket.SIO_RCVALL,socket.RCVALL_ON)

    #读取单个数据包
    print(sniffer.recvfrom(65565))

    #再windows平台上关闭混杂模式

    if os.name=="nt":
        sniffer.ioctl(socket.SIO_RCVALL,socket.RCVALL_OFF)
