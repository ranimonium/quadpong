"""
	SERVER for PingPong implemented on pygame
	+ connects with clients
	+ in charge of connecting client with game logic
	+ takes action from client, puts it in the game as a function, and returns to all the clients the new coordinates per object
	
"""

NUMBER_OF_PLAYERS = 4
BUFFER_SIZE = 2048

import socket
from socket import *
import sys
import threading

serverPort = 12000
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
serverSocket.bind(('', serverPort))


client_addresses = []

### function to receive messages from client and send appropriate responses/broadcast ###
def recvMsg():
	
	while True:

		msg, clientAddress = serverSocket.recvfrom(BUFFER_SIZE)
		
		header = msg[:4]

		if header == "JOIN": #sends ID too
			if len(client_addresses) < NUMBER_OF_PLAYERS:
				client_addresses.append(clientAddress)
				serverSocket.sendto(header + str(client_addresses.index(clientAddress)), clientAddress)
				print str(clientAddress) + " has connected!"
				print str(NUMBER_OF_PLAYERS - len(client_addresses)) + " more player(s) to go."
			else:
				serverSocket.sendto(header + str(-1), clientAddress)
		elif header == "DONE":
			serverSocket.sendto( header + str(len(client_addresses)), clientAddress )
		elif header == "STAT":
			# print msg
			for i in range(len(client_addresses)):
				print str(i) + " " + str(client_addresses[i])
			for c in client_addresses:
				serverSocket.sendto( msg, c )

try:
	recvMsgThread = threading.Thread(target=recvMsg, args=())
	recvMsgThread.start()
	print "Now waiting for players to connect..."
except KeyboardInterrupt:
	sys.exit()
except Exception as e:
	print e
	sys.exit()