#-*- coding=utf-8 -*-
#-----author:GYl-----
#-----date:2018/12/13-----

import socket

target_host= "192.168.1.105"
target_port = 8888

client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

client.connect((target_host,target_port))
cmd = "GET /HTTP/1.1\r\nHOST:baidu.com\r\n\r\n"

client.send(bytes(cmd,encoding='utf-8'))

response=client.recv(4096)

print (response)
