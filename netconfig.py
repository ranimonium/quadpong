from socket import *
from gameconfig import *

##################  NETWORKING CONFIGURATION  ##################

serverName = "127.0.0.1"
serverPort = 12000

clientSocket = socket(AF_INET, SOCK_DGRAM)

BUFFER_SIZE=2048

### SHIZ TO SEND ###
ball_s = [] # ball_s = [ str(ball.heldBy), str(ball.x), str(ball.y), ball.color, ball.direction]
plyr_s = [] # plyr_s = [str(players[MY_ID].uid), str(players[MY_ID].x), str(players[MY_ID].y), str(players[MY_ID].score), players[MY_ID].color, players[MY_ID].direction, players[MY_ID].username]

def send_shiz(clientMessage, args=None):
	
	if clientMessage == "JOIN":
		clientSocket.sendto(clientMessage, (serverName, serverPort))
	elif clientMessage == "DONE":
		clientSocket.sendto(clientMessage, (serverName, serverPort))
	elif clientMessage == "STAT":
		shizSendMsg = clientMessage + str(MY_ID) + '$SHIZ$'.join( [ '$BALL$'.join(ball_s), '$PLYR$'.join(plyr_s) ] ) + "~ENDDATA~"
		clientSocket.sendto(shizSendMsg, (serverName, serverPort))
	elif clientMessage == "POUT":
		print "SEND: " + str(MY_ID)
		clientSocket.sendto(clientMessage + str(args), (serverName, serverPort))
		# myConnection.sendMessage( clientMessage + str(MY_ID) + shizSendMsg + "~ENDDATA~")

def recv_shiz():

	while True:

		msg, serverAddress = clientSocket.recvfrom(BUFFER_SIZE)
		serverMessage = msg[:4]

		# print msg

		if serverMessage == "JOIN":
			return int(msg[4:])
		elif serverMessage == "DONE":
			return int(msg[4:])
		elif serverMessage == "TIME":
			pass
		elif serverMessage == "POUT":
			print msg
			if msg[5:] == "KBYE":
				clientSocket.close()
				sys.exit()
		elif serverMessage == "STAT":

			global players

			msg = msg.split("~ENDDATA~")

			try:
				for m in msg:
					# m has ball status and player status in it
					# print m
					ID = int(m[4])

					m = m[5:] # trim from m the serverMessage and ID
					m = m.split("$SHIZ$") #separate ball status from player status

					ball_r = m[0].split("$BALL$") #separate ball fields
					plyr_r = m[1].split("$PLYR$") #separate player fields

					#update the ball if my own copy of ball 
					if ball_r[3] != players[MY_ID].color:
						ball.set_heldBy( int(ball_r[0]) )
						ball.set_pos( (int(ball_r[1]), int(ball_r[2]) ) )
						ball.set_color( ball_r[3] )
						ball.set_direction( ball_r[4] )
						
					#update the player
					if ID != MY_ID:
						players[ID].uid = int(plyr_r[0])
						players[ID].x = int(plyr_r[1])
						players[ID].y = int(plyr_r[2])
						players[ID].score = int(plyr_r[3])
						players[ID].color = plyr_r[4]
						players[ID].direction = plyr_r[5]
						players[ID].username = plyr_r[6]

			except Exception as exc:
				pass
				# print e



################################################################