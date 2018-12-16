#-*- coding=utf-8 -*-
#-----author:GYl-----
#-----date:2018/12/13-----


import socket
import threading

bind_ip = "0.0.0.0"
bind_port= 8888

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

server.bind((bind_ip,bind_port))

server.listen(5)

print ("[*] listing  on %s:%d"%(bind_ip,bind_port))

def handle_client(client_socket):
    request = client_socket.recv(1024)
    print ('[*] received:%s'%request)

    #返回一个数据包
    client_socket.send(bytes("ack",encoding='utf-8'))
    client_socket.close()

while True:
    client,addr = server.accept()
    print ("[*] Accept connection form:%s:%d"%(addr[0],addr[1]))

    #挂起客户端线程，处理传入的数据
    client_handler=threading.Thread(target=handle_client,args=(client,))
    client_handler.start()