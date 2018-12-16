from socket import *

serverName = "192.168.1.108"
serverPort = 1234
clientSocket = socket(AF_INET,SOCK_DGRAM)
message = input("intput the message: ")
clientSocket.sendto(message,(serverName,serverPort))
modifiedMessage,serverAdress=clientSocket.recvfrom(2048)
print (modifiedMessage)
clientSocket.close()