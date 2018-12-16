
import sys
import socket
import threading

def server_loop(local_host,local_port,remote_host,remote_port,receive_first):

    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    try:
        server.bind((local_host,local_port))

    except:
        print("[!!] Falied to listen on %s :%d"%(local_host,local_port))
        print ("[!!] check for other listening sockets or correct premissions")

        sys.exit(0)

    print("[**] listening on %s:%d"%(local_host,local_port))

    server.listen(5)

    while True:
        client_socket,addr=server.accept()

        #打印处本地链接信息
        print("[====>] Receivering incoming connection from %s:%d"%(addr[0],addr[1]))

        #开启一个线程与远程主机通讯
        proxy_thread=threading.Thread(target=proxy_handler,args=(client_socket,remote_host,remote_port,receive_first))

        proxy_thread.start()


def proxy_handler(client_socket,remote_host,remote_port,receive_first):

    #链接远程主机
    remote_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    remote_socket.connect((remote_host,remote_port))

    #如果有必要则从远程主机接受数据
    if receive_first:

        remote_buffer = receive_from(remote_socket)
        hexdump(remote_buffer)

        #进行响应处理
        remote_buffer = response_handler(remote_buffer)

        #有数据则发给本地客户端
        if len(remote_buffer):
            print("[<====] sending %d bytes ti localhost"%len(remote_buffer))
            client_socket.send(remote_buffer)

    #从本地循环读取数据，发送给远程主机和本地主机
    while True:

        #从本地读取数据
        local_buffer = receive_from(client_socket)

        if len(local_buffer):
            print("[===>] received %d bytes from localhost "%len(local_buffer))
            hexdump(local_buffer)
            # 发送给我们的本地请求
            local_buffer = request_handler(local_buffer)

            # 向远程主机发送数据
            remote_socket.send(local_buffer)
            print("[===>] sent to remote")

        #接受响应的数据
        remote_buffer = receive_from(remote_socket)

        if len(remote_buffer):
            print("[<===] Received %d bytes from remote  "%len(remote_buffer))
            hexdump(remote_buffer)

            #发送响应数据
            remote_buffer = response_handler(remote_buffer)

            #讲响应数据发送给本地socket
            client_socket.send(remote_buffer)

            print("[<===] sent to localhost")

        if not len(local_buffer) or not len(remote_buffer):
            client_socket.closed()
            remote_socket.close()
            print("not more data closing connection")

            break


def receive_from(connection):
    buffer = ""
    #设置2s延迟

    connection.settimeout(1)
    try:
        while True:
            data = connection.recv(4096)
            if not data:
                break

            buffer += data
    except:
        pass

    return buffer

# 对目标是远程主机的请求进行修改

def request_handler(buffer):
    return buffer


#对目标是本地主机的响应进行修改
def response_handler(buffer):
    return buffer

def hexdump():
    result = []
    digits = 4 if isinstance(src,unicode) else 2
    for i in range(0,len(src),length):
        s = src[i:i+length]
        hexa = b''.join(["%0*X"%(digits,ord(x)) for x in s])
        text = b''.join([x if 0x20 <= ord(x) < 0x7F else b'.' for x in s])
        result.append(b" %04X %-*s  %s"%(i,length*(digits+1),hexa,text))

    print(b'\n'.join(result))


def main():
    if len(sys.argv[1:]) !=5:
        print("usage :./ proxy.py [localhost] [localport] [remotehost] [remoteport] [receivefirst]")
        sys .exit(0)

    local_host = sys.argv[1]
    local_port = sys.argv[2]
    remote_host = sys.argv[3]
    remote_port= sys.argv[4]
    receive_first = sys.argv[5]

    if "True" in receive_first:
        receive_first = True
    else:
        receive_first = False
    #现在设置好我们的监听 socket

    server_loop(local_host,local_port,remote_host,remote_port,receive_first)