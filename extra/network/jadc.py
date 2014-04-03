from socket import *
import threading

serverName = "127.0.0.1"
serverPort = 12000

clientSocket = socket(AF_INET, SOCK_DGRAM)

message = "MEH"

def recvMsg():
	while 1:
		msg, serverAddress = clientSocket.recvfrom(2048)
		print "SERVER: " + msg
		if message == "":
			break

recvMsgThread = threading.Thread(target=recvMsg, args=())
recvMsgThread.start()

while 1:
	message = raw_input("Input: ")
	if message == "":
		break



clientSocket.close()
