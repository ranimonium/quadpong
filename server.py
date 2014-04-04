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
players_AI = []

# DONE = True


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
			# if len(client_addresses) == NUM_PLAYERS:
				# global notDONE
				# notDONE = False
			serverSocket.sendto( header + str(len(client_addresses)), clientAddress )
		elif header == "STAT":
			for c in client_addresses:
				serverSocket.sendto( msg, c )
		elif header == "POUT": #player quits
			
			print msg
			ID_quitter = int(msg[4])

			#player quits upon wait
			if len(client_addresses) < NUM_PLAYERS:
				available_IDs.append( ID_quitter )
				serverSocket.sendto(header + "KBYE", clientAddress)
				client_addresses.remove(clientAddress)
			#already in game
			else:
				print str(players_AI)
				players_AI.append( ID_quitter )
				print str(players_AI)
				serverSocket.sendto(header + "KBYE", clientAddress)
				# client_addresses.remove(clientAddress)
				
				if len(players_AI) != NUM_PLAYERS:
					
					#handle the AI handled by quitter (if there's any)
					quittersIDs = msg[4:]

					ID_handle = None #ID of player that would handle AI
					for i in range(NUM_PLAYERS):
						if i not in players_AI:
							ID_handle = i

					print quittersIDs
					print "player to handle AI: " + str(ID_handle)
					serverSocket.sendto("DOAI" + str(ID_handle) + quittersIDs, client_addresses[ID_handle])
					print "DOAI sent"


try:
	recvMsgThread = threading.Thread(target=recvMsg, args=())
	recvMsgThread.start()
	print "Now waiting for players to connect..."
except KeyboardInterrupt:
	sys.exit()
except Exception as e:
	print e
	sys.exit()