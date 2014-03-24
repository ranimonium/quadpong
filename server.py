"""
	SERVER for PingPong implemented on pygame
	+ connects with clients
	+ in charge of connecting client with game logic
	+ takes action from client, puts it in the game as a function, and returns to all the clients the new coordinates per object
	
"""
NUMBER_OF_PLAYERS=4
DEFAULT_PORT=1234
BUFFER_SIZE=1024

import socket
import connection

DEFAULT_CONNECTION_PORT=1234

clients=[]

#wait for clients to join
"""
	Wait for players to join by
		initiating UDP socket where client connection requests come in
		initiating 4 sockets with consecutive port numbers
		Until we have 4 clients:
			[Listen with the UDP socket
			Send next specific port number to next request] thread?
			Wait for request from client to specific port
			Accept request
			Make a connection with the socket
			Add the connection to the clients list
	
"""
def getClients():
	sockets=[]
	
	#initiate UDP socket where connection requests from clients come in
	udpsocket = socket.socket(socket.AF_NET, socket.SOCK_DGRAM)
	udpsocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	udpsocket.bind(('', DEFAULT_CONNECTION_PORT))
	
	#initiate client-specific sockets/connections
	for s in xrange(0,4):
		sockets[s]=socket.socket()
		sockets[s].setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		sockets[s].bind(('', portnum))
		portnum++
	
	#wait for connecion requests, send specific port number to each UDP-accepted request
	#turn into threads eventually
	s=0
	portnum=1001
	while len(clients)<NUMBER_OF_PLAYERS:
		udpsocket.listen(5)
		data, addr = udpsocket.recvfrom(BUFFER_SIZE)
		if data=="join game":
			udpsocket.sendto(str(portnum+s), addr)
		
			sockets[s].listen()
			remote_socket, addr = sockets[s].accept()
			clients[s]=connection.connection(remote_socket)
			clients[s].sendMessage("You have successfully joined the game")
			s++


#initialize game




#wait for actions an output each one
while True:
	for c in clients:
		message = c.getMessage()
		if message=="LEFT" or message=="UP":
			#tell game to move his paddle up/left
		else if message=="RIGHT" or message=="DOWN":
			#tell game to move paddle right/down
			
