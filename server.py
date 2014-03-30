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
import threading
import sys
# import thread


TCP_IP = '0.0.0.0'

clients=[]
threads = []

# player_stats=[]
ball_stats = []

players_Complete = "False"

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
	global players_Complete
	# global player_stats

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

	print "Waiting..."

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
			
			# threading shiz
			thread = threading.Thread(target=recv_shiz,args=(clients[s],))
			thread.start()
			threads.append(thread)

			clients[s].sendMessage("You have successfully joined the game")

			# thread.start_new_thread(recv_shiz, (clients[s],))
			# thread.start_new_thread(send_shiz, (clients[s],))
			
			print portnum
			s+=1
			portnum+=1

	#getting clients complete
	players_Complete = "True"

	#joining the threads
	for thread in threads:
		thread.join()

def send_shiz(client):
	pass
	# global players_Complete

	# if players_Complete == "True":
	# 	for c in clients:
	# 		c.sendMessage(players_Complete)
	# 	players_Complete = "done now, stop sending players_Complete"


### SHIZ TO RECV ###
others_status = [] # contains others' points too

def recv_shiz(client):
	while True:
		msg = client.getMessage()
		# print "I RECEIVED THE SHIT " + msg
		
		clientMessage = msg[:4]

		if clientMessage == "NOTH":
			pass
		elif clientMessage == "MYID":
			client.sendMessage( clientMessage + str(clients.index(client)) )
		elif clientMessage == "BALL":
			pass
		elif clientMessage == "PLYR":
			print msg
			for c in clients:
				c.sendMessage( msg + "~ENDDATA~")
		elif clientMessage == "DONE":
			# print clientMessage
			client.sendMessage( clientMessage + players_Complete )





def clientThread(client):
	while True:
		msg = client.getMessage()
		print msg
		for c in clients:
			c.sendMessage(msg)
		
	


#initialize game
def beAGameServer():
	getClients()
	# for c in clients:
	# 	thread.start_new_thread(clientThread, (c,))
	while True:
		# print "here"
		j=1
		
try:
	beAGameServer()
except Exception as e:
	print e
finally:
	sys.exit()


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
			