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
import thread


TCP_IP = '0.0.0.0'

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
	global clients
	sockets=[0 for i in xrange(0,NUMBER_OF_PLAYERS)]
	
	#initiate UDP socket where connection requests from clients come in
	udpsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	#udpsocket=socket.socket()
	udpsocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	udpsocket.bind(('', DEFAULT_PORT))
	
	"""
	portnum=2001
	#initiate client-specific sockets/connections
	for s in xrange(0,4):
		sockets[s]=(socket.socket())
		sockets[s].setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		sockets[s].bind((TCP_IP, portnum))
		portnum+=1
	"""
	
	#wait for connecion requests, send specific port number to each UDP-accepted request
	#turn into threads eventually
	s=0
	portnum=2001
	while len(clients)<NUMBER_OF_PLAYERS:
		#udpsocket.listen(5)
		data, addr = udpsocket.recvfrom(BUFFER_SIZE)
		if data=="join game":
			print addr[0], "wants to join game"
			udpsocket.sendto(str(portnum), addr)
		
			sockets[s]=(socket.socket())
			sockets[s].setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
			sockets[s].bind((TCP_IP, portnum))
			
			sockets[s].listen(1)
			remote_socket, addr = sockets[s].accept()
			clients.append(connection.connection(remote_socket))
			clients[s].sendMessage("You have successfully joined the game")
			
			print portnum
			s+=1
			portnum+=1


def clientThread(client):
	while True:
		msg = client.getMessage()
		print msg
		for c in clients:
			c.sendMessage(msg)
		
	


#initialize game
def beAGameServer():
	getClients()
	for c in clients:
		thread.start_new_thread(clientThread, (c,))
	while True:
		j=1
		

beAGameServer()



"""
#wait for actions an output each one
while True:
	for c in clients:
		message = c.getMessage()
		if message=="LEFT" or message=="UP":
			print "up"
			#tell game to move his paddle up/left
		elif message=="RIGHT" or message=="DOWN":
			print "down"
			#tell game to move paddle right/down
"""
				
