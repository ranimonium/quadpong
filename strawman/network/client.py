from socket import *

serverName = "127.0.0.1"
serverPort = 12000

clientSocket = socket(AF_INET, SOCK_DGRAM)

while 1:
	message = raw_input("Input lowercase sentence: ")
	if message == "":
		break

	clientSocket.sendto(message,(serverName, serverPort))
	modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
	print "SERVER: " + modifiedMessage


clientSocket.close()
