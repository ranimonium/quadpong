from socket import *
import threading

serverPort = 12000
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))

print "The server is ready to receive"

BUFFERSIZE = 2048
NUMBER_OF_PLAYERS = 4

client_addresses = []

def recvMsg():
	
	while True:

		msg, clientAddress = serverSocket.recvfrom(BUFFERSIZE)
		
		header = msg[:4]

		if header == "JOIN": #sends ID too
			if len(client_addresses) < NUMBER_OF_PLAYERS:
				client_addresses.append(clientAddress)
				serverSocket.sendto(header + str(client_addresses.index(clientAddress)), clientAddress)
			else:
				serverSocket.sendto(header + str(-1), clientAddress)
		elif header == "DONE":
			pass
			# client.sendMessage( header + players_Complete )
		elif header == "STAT":
			# print msg
			for c in client_addresses:
				serverSocket.sendto( msg, c )


getClientThread = threading.Thread(target=getClient, args=())
getClientThread.start()