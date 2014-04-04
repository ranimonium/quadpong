"""
	SERVER for PingPong implemented on pygame
	+ connects with clients
	+ in charge of connecting client with game logic
	+ takes action from client, puts it in the game as a function, and returns to all the clients the new coordinates per object
	
"""

NUM_PLAYERS = 4
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

#contains available indices for client_address
available_IDs = [i for i in range(NUM_PLAYERS)]

### function to receive messages from client and send appropriate responses/broadcast ###
def recvMsg():
	
	while True:

		msg, clientAddress = serverSocket.recvfrom(BUFFER_SIZE)
		
		header = msg[:4]
		
		# print available_IDs

		if header == "JOIN": #sends ID too
			if len(client_addresses) < NUM_PLAYERS:
				ID_toGive = available_IDs.pop(0)
				client_addresses.insert(ID_toGive, clientAddress)
				serverSocket.sendto(header + str(ID_toGive), clientAddress)
				print str(clientAddress) + " has connected!"
				print str(NUM_PLAYERS - len(client_addresses)) + " more player(s) to go."
			else:
				serverSocket.sendto(header + str(-1), clientAddress)
		elif header == "DONE":
			serverSocket.sendto( header + str(len(client_addresses)), clientAddress )
		elif header == "STAT":
			# print msg
			print client_addresses
			for c in client_addresses:
				print c
				serverSocket.sendto( msg, c )
		elif header == "POUT": #player quits
			
			print msg
			ID = int(msg[4])

			#player quits upon wait
			if len(client_addresses) < NUM_PLAYERS:
				available_IDs.append( ID )
				client_addresses.remove(clientAddress)
				serverSocket.sendto(header + "KBYE", clientAddress)
			#already in game
			# else:

try:
	recvMsgThread = threading.Thread(target=recvMsg, args=())
	recvMsgThread.start()
	print "Now waiting for players to connect..."
except KeyboardInterrupt:
	sys.exit()
except Exception as e:
	print e
	sys.exit()