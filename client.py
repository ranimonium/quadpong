"""
	CLIENT for PingPong game implemented on pygame
	+ means by which a player connects to the server and other players
	+ gives instructions to the client's copy of the game
	+ sends actions to the server; server responds with new game state

"""

import socket
import connection

DEFAULT_SERVER_IP="127.0.0.1"
DEFAULT_SERVER_PORT=1234
CONNECTION_REQUEST_MESSAGE="join game"
BUFFER_SIZE=1024

myServerPort=DEFAULT_SERVER_PORT
myConnection=None

"""
	Uses a UDP connection to send initial request
	Waits on UDP connection for server acknowledgement in the form of a TCP port
	Connects to specific (TCP) port
	myConnection is the connection on the TCP port

"""
def connectToServer():
	udpsocket=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	udpsocket.sendto(CONNECTION_REQUEST_MESSAGE, (DEFAULT_SERVER_IP, DEFAULT_SERVER_PORT))
	data, addr = udpsocket.recvfrom(BUFFER_SIZE)
	myServerPort = int(data)
	print "Will connect to ", data
	
	s = socket.socket()
	s.connect((DEFAULT_SERVER_IP, myServerPort))
	myConnection = connection.connection(s)
	print myConnection.getMessage #or add this to the GUI later on
	
"""
def playerAction():
	#game sends player's move here
	
def sendAction():
	#client sends player's move to server

def updateGameScreen():
	#client receives new game state from server
	#relays information to game which will update the GUI
"""
	

connectToServer()
