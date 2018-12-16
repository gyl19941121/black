#-*- coding:utf-8 -*-
#----author:gyl----
#----date:2018/12/15----

import sys
import socket
import getopt
import threading
import  subprocess


#定义全局变量
listen = False
command = False
upload = False
execute = ""
target = ""
upload_destination  = ""
port  = 0

def usage():
    print("BHP Net Tool")
    print("")
    print("usage:netcat.py -t target_host -p port")
    print ("-l --listen   --listen on [host]:[port] for incoming connections")
    print("-e --execute = file_to_run  -execute the given file uopn receiveing a connection")
    print("-c --command  --initialize a command shell ")
    print("-u --upload = denstination -upon receiving connection  upload a file and write to [destinations]")
    print('')
    print("")
    print("examples:")
    print("netcat.py -t 12.168.1.10 -p 555 -l -c")
    print("netcat.py -t 12.168.1.10 -p 555 -l -u=c:\\target.exe")
    print("netcat.py -t 12.168.1.10 -p 555 -l -e=\\cat /etc/passwd")
    print("echo 'acnc' |netcat.py -t 12.168.1.10 -p 555")
    sys.exit(0)

def client_sender(buffer):
    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    try:
        #链接到目标主机
        client.connect((target,port))
        if len(buffer):
            client.send(buffer)

        while True:
            #现在等待数据回传
            recv_len=1
            response = ""

            while recv_len:
                data = client.recv(4096)
                recv_len=len(data)
                response += data

                if recv_len<4096:
                    break
            print(response)

            # 等待更多输入
            buffer = input("")
            buffer += "\n"

            #发送出去
            client.send(buffer)
    except:
        print("[*] Exception Exiting ")

        #关闭链接
        client.close()

def server_loop():

    global target


    #如果没有定义目标，我们要监听所有接口
    if not len(str(target)):
        target = "0.0.0.0"
    print(type(target))

    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    server.bind((target,port))

    server.listen(5)

    while True:
        client_socket,addr = server.accept()

        #拆分一个线程处理新的客户端
        client_thread = threading.Thread(target=client_handler,args=(client_socket,))
        client_thread.start()


def run_command(command):
    command = command.rstrip()
    #运行命令并输出返回
    try:
        output = subprocess.check_output(command,stderr=subprocess.STDOUT,shell=True)

    except:
        output = "Falied to execute commadn.\r\n"

    return  output

def client_handler(client_socket):
    global upload
    global execute
    global command

    #检测上传文件
    if len(upload_destination):
        #读取所有的字符并写下目标
        file_buffer = ""

        #持续读取数据，直到没有符合的数据
        while True:
            data = client_socket.recv(1024)

            if not data:
                break
            else:
                file_buffer += data
        #将接受的数据写出来

        try:
            file_descriptor = open(upload_destination,'wb')
            file_descriptor.write(file_buffer)
            file_descriptor.close()

            #确认文件已经写了下来
            client_socket.send("successfully saved file to %s\r\n"%upload_destination)
        except:
            client_socket.send("Failed to save file to %s\r\n"%upload_destination)

    #检查命令执行
    if len(execute):
        output = run_command(execute)
        #运行命令
        client_socket.send(output)

    #如果需要一个命令行的shell，我们进入另外一个循环
    if command:
        while True:
        #跳出一个窗口
            client_socket.send("<BHP:#> ")
            #现在我们接受文件直至发现换行符
            cmd_buffer = ""

            while "\n" not in cmd_buffer:
                cmd_buffer += client_socket.recv(1024)

                #返还命令输出
                response = run_command(cmd_buffer)

                #返回相应数据
                client_socket.send(response)


def main():
    global listen
    global command
    global upload
    global execute
    global target
    global upload_destination
    global port

    if not len(sys.argv[1:]):
        usage()

    try :
        opts,args = getopt.getopt(sys.argv[1:],"hle:t:p:cu:",["help","listen","execute","target","port","command","upload"])
    except getopt.GetoptError as err:
        print(str(err))
        usage()

    for  o,a in opts:
        if o in ("-h","--help"):
            usage()
        elif o in ("-l","--listen"):
            listen = True
        elif o in ("-e","--execute"):
            execute = a
        elif o in ("-c","--command"):
            command = True
        elif o in ("-u","--upload"):
            upload_destination=a
        elif o in ("-t","--target"):
            target=a
        elif o in ("-p","--port"):
            target =int(a)

        else:
            assert False,"unhandled Options"

    # 我们是进行舰艇还是仅从标准输入发送数据
    if not listen and len(target) and  port >0:
        #从命令行读取内存数据
        #这里将阻塞，所以不再向标准输入发送数据时发送CTRL-D
        buffer = sys.stdin.read()

        #发送数据
        client_sender(buffer)

    # 我们开始监听病准备上传文件、执行命令
    #防止一个反弹shell
    #取决于上面命令行选项
    if listen:
        server_loop()

if __name__ == '__main__':
    main()