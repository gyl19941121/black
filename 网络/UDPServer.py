from socket import *

serverPort = 1234
serverSocket = socket(AF_INET,SOCK_DGRAM)
serverSocket.bind(("",serverPort))
print("the server is ready to receive ")

while True:
    message,clientAdress=serverSocket.recvfrom(2048)
    modifideMessage = message.upper()
    serverSocket.sendto(modifideMessage,clientAdress)
