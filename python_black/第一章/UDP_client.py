#-*- coding=utf-8 -*-
#-----author:GYl-----
#-----date:2018/12/13-----

import socket

target_host= "www.baidu.com"
target_port = 80
#建立一个socket对象
client = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

cmd = "GET /HTTP/1.1\r\nHOST:baidu.com\r\n\r\n"

#发送数据
client.sendto(bytes(cmd,encoding='utf-8'),(target_host,target_port))

#recvfrom接受返回的UDP数据包
data,addr = client.recvfrom(4096)


print (data+'...'+addr)
