import pygame, sys, time, random, thread, connection, socket
from pygame.locals import *
import elements as e

####################  PYGAME CONFIGURATION  ####################

# set up pygame 
pygame.init()

# set up the window
WINDOWWIDTH = 800
WINDOWHEIGHT = 600
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT + 100), 0, 32)
pygame.display.set_caption('QuadPong')


#####################  GAME CONFIGURATION  #####################

########## set up timer ##########
clock = pygame.time.Clock()
# start_time = 
frame_fate = 600 #Frames Per Second

########## set up arena's "dimensions" ##########
arenaTOP = WINDOWHEIGHT/10
arenaLEFT = WINDOWWIDTH/10
arenaWIDTH = WINDOWWIDTH - arenaLEFT*2
arenaHEIGHT = WINDOWHEIGHT - arenaTOP*2

########## set up players ##########

NUM_PLAYERS = 4

paddleWIDTH, paddleHEIGHT = 14, 100

pcolors = ['MEDIUMSPRINGGREEN', 'HOTPINK', 'GOLD', 'DODGERBLUE']
pcoords = [
		[(WINDOWWIDTH)/2 - paddleHEIGHT/2, arenaTOP],					#player 0 top
		[(WINDOWWIDTH)/2 - paddleHEIGHT/2, (arenaTOP+arenaHEIGHT)], 	#player 1 bottom
		[arenaLEFT - 5, WINDOWHEIGHT/2], 								#player 2 left
		[(arenaLEFT + arenaWIDTH) - paddleWIDTH/2, WINDOWHEIGHT/2],		#player 3 right
	]

# instantiate Player class from elements module
players = [e.Player(i, pcolors[i], pcoords[i]) for i in range(NUM_PLAYERS)]

# set Player direction to be NONE (meaning they're not moving yet)
for p in players:
	if players.index(p) < 2:
		p.set_allowableDirection( ('W', 'E') )
	else:
		p.set_allowableDirection( ('N', 'S') )
	p.set_direction('NONE')

PSPEED = 2	#paddle speed


########## set up the ball ##########
ballWIDTH, ballHEIGHT = 16, 16
ball = e.Ball( 'HOTPINK', [250, 250])
ball.set_direction('NE')
ball.set_heldBy(0) #default, player 0 holds ball

BSPEED = 2	#ball speed

########## border coordinates and border lengths ##########
borderdiv = 4
borders = {
	'topleft_h': [(arenaLEFT, arenaTOP),(arenaLEFT + arenaWIDTH/borderdiv, arenaTOP)],
	'topright_h': [(arenaLEFT + arenaWIDTH - arenaWIDTH/borderdiv, arenaTOP),(arenaLEFT + arenaWIDTH, arenaTOP)],
	'bottomleft_h':  [(arenaLEFT, arenaTOP+arenaHEIGHT),(arenaLEFT + arenaWIDTH/borderdiv, arenaTOP + arenaHEIGHT)],
	'bottomright_h':  [(arenaLEFT + arenaWIDTH - arenaWIDTH/borderdiv, arenaTOP+arenaHEIGHT),(arenaLEFT + arenaWIDTH, arenaTOP + arenaHEIGHT)],
	'topleft_v': [(arenaLEFT, arenaTOP),(arenaLEFT, arenaTOP + arenaHEIGHT/borderdiv)],
	'topright_v':  [(arenaLEFT+arenaWIDTH, arenaTOP),(arenaLEFT+arenaWIDTH, arenaTOP + arenaHEIGHT/borderdiv)],
	'bottomleft_v':  [(arenaLEFT, arenaTOP+arenaHEIGHT - arenaHEIGHT/borderdiv),(arenaLEFT, arenaTOP + arenaHEIGHT)],
	'bottomright_v':  [(arenaLEFT+arenaWIDTH, arenaTOP+arenaHEIGHT - arenaHEIGHT/borderdiv),(arenaLEFT+arenaWIDTH, arenaTOP + arenaHEIGHT)]
}

################################################################

##################  NETWORKING CONFIGURATION  ##################

DEFAULT_SERVER_IP="127.0.0.1"
DEFAULT_SERVER_PORT=1234
CONNECTION_REQUEST_MESSAGE="join game"
BUFFER_SIZE=1024

myServerPort=DEFAULT_SERVER_PORT
myConnection=None

def connectToServer():
	global myConnection
	global MY_ID

	udpsocket=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	udpsocket.sendto(CONNECTION_REQUEST_MESSAGE, (DEFAULT_SERVER_IP, DEFAULT_SERVER_PORT))
	data, addr = udpsocket.recvfrom(BUFFER_SIZE)
	myServerPort = int(data)
	
	print "Will connect to ", data
	
	s = socket.socket()
	s.connect((DEFAULT_SERVER_IP, myServerPort))
	
	myConnection = connection.connection(s)

	print myConnection.getMessage()

### SHIZ TO SEND ###
ball_s = [] # ball_s = [ str(ball.heldBy), str(ball.x), str(ball.y), ball.color, ball.direction]
plyr_s = [] # plyr_s = [str(players[MY_ID].uid), str(players[MY_ID].x), str(players[MY_ID].y), str(players[MY_ID].score), players[MY_ID].color, players[MY_ID].direction]

def send_shiz(clientMessage):
	
	if clientMessage == "MYID":
		myConnection.sendMessage( clientMessage )
	elif clientMessage == "DONE":
		myConnection.sendMessage( clientMessage )
	elif clientMessage == "STAT":
		shizSendMsg = '$SHIZ$'.join( [ '$BALL$'.join(ball_s), '$PLYR$'.join(plyr_s) ] )
		myConnection.sendMessage( clientMessage + str(MY_ID) + shizSendMsg + "~ENDDATA~")

def recv_shiz():

	while True:

		msg = myConnection.getMessage()
		serverMessage = msg[:4]

		if serverMessage == "MYID":
			return int(msg[4:])
		elif serverMessage == "DONE":
			return str(msg[4:])
		elif serverMessage == "TIME":
			pass
		elif serverMessage == "STAT":

			global players

			msg = msg.split("~ENDDATA~")

			try:
				for m in msg:
					# m has ball status and player status in it
					print m
					ID = int(m[4])

					m = m[5:] # trim from m the serverMessage and ID
					m = m.split("$SHIZ$") #separate ball status from player status

					ball_r = m[0].split("$BALL$") #separate ball fields
					plyr_r = m[1].split("$PLYR$") #separate player fields

					#update the ball if my own copy of ball 
					if ball_r[3] != players[MY_ID].color:
						ball.set_heldBy( int(ball_r[0]) )
						ball.set_pos( (int(ball_r[1]), int(ball_r[2]) ) )
						ball.set_direction( ball_r[4] )
						
					#update the player
					if ID != MY_ID:
						players[ID].uid = int(plyr_r[0])
						players[ID].x = int(plyr_r[1])
						players[ID].y = int(plyr_r[2])
						players[ID].score = int(plyr_r[3])
						players[ID].color = plyr_r[4]
						players[ID].direction = plyr_r[5]
						

			except Exception as e:
				print e



################################################################

############ HOME SCREEN ############ 
def home():
	
	title = 'QuadruPong'
	fontObj = pygame.font.SysFont("None", 100)

	msgSurfaceObj = fontObj.render(title, False, (0,0,255))
	msgRectobj = msgSurfaceObj.get_rect()
	msgRectobj.center = (WINDOWHEIGHT/2, WINDOWHEIGHT/2)
	windowSurface.blit(msgSurfaceObj, msgRectobj)

############ WAITING FOR OTHER PLAYERS TO CONNECT ############ 
def wait():
	
	global curScene
	global MY_ID

	# connect to server
	if MY_ID == None:
		connectToServer()
		send_shiz("MYID")
		MY_ID = recv_shiz()
	print MY_ID

	while True:
		send_shiz("DONE")
		isDone = recv_shiz()
		if isDone == "True":
			print isDone
			curScene = 'game'
			thread.start_new_thread(recv_shiz, ())
			break


############ GAME SCENE ############ 
def game():

	#################### GAME TIMER FCN ####################	





	#################### GAME FUCTIONS ####################


	# handles collisions for both the paddle and the borders
	def handle_ballCollisions(ball_rect, rects, isPaddle=True):
		
		ballDir = ball.get_directionValue()

		ball_rect.x += ballDir[0]
		ball_rect.y += ballDir[1]

		rect_i = ball_rect.collidelist(rects)
		
		if rect_i != -1:
			if isPaddle:
				ball.set_color(players[rect_i].color)
				if rect_i < 2: 
					ball.bounce('horizontal')
				else:
					ball.bounce('vertical')
			else:
				# checks if the ball had just hit a horizontal border
				if borders.keys()[rect_i][-1:] == 'h':
					ball.bounce('horizontal')
				else:
					ball.bounce('vertical')


	#handle paddle-border limitations
	def handle_borderPaddleCollisions(border_rects, paddle_rects):
		for p in paddle_rects:
			pDir = players[paddle_rects.index(p)].get_directionValue()
			p.x += pDir[0]
			p.y += pDir[1]

		for b in border_rects:
			paddle_i = b.collidelist(paddle_rects)
			if paddle_i != -1:
				players[paddle_i].set_direction('NONE')

	def manage_scoring():

		# index of the player whose side had the ball come out:  0 - top; 1 - bottom; 2 - left; 3 - right
		player_side = -1 

		TOP = 0
		BOTTOM = 1
		LEFT = 2
		RIGHT = 3

		if ball.x < -150:
			player_side = LEFT
		elif ball.x > WINDOWWIDTH+150:
			player_side = RIGHT
		elif ball.y < -150:
			player_side = TOP
		elif ball.y > WINDOWHEIGHT+150:
			player_side = BOTTOM

		if player_side != -1:
			player_scored_i = [p.get_colorValue() for p in players].index(ball.get_colorValue())

			if player_scored_i != player_side: # to ensure that you won't score from your own loss
				players[ player_scored_i ].add_score()
				print "Score for " + players[ player_scored_i ].username
				print "Scores:"
				for p in players:
					print str(p.username) + " " + str(p.score)
			#renew the ball
			ball.set_color(players[player_side].color)
			ball.set_heldBy(player_side)
			ball.set_direction('NE')
	 
	#######################################################


	##################### GAME EVENTS #####################
	def game_events():
	
		for event in pygame.event.get():
			
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			
			elif event.type == KEYDOWN:
			
						
				if event.key == K_ESCAPE:
					pygame.event.post(pygame.event.Event(QUIT))				
				
				elif event.key == K_SPACE and ball.heldBy == MY_ID:
					ball.set_heldBy(-1)

				elif event.key == K_LEFT or event.key == K_a: 
					players[MY_ID].set_direction(players[MY_ID].allowDir[0])
				elif event.key == K_UP or event.key == K_w: 
					players[MY_ID].set_direction(players[MY_ID].allowDir[0])
				elif event.key == K_RIGHT or event.key == K_d: 
					players[MY_ID].set_direction(players[MY_ID].allowDir[1])
				elif event.key == K_DOWN or event.key == K_s: 
					players[MY_ID].set_direction(players[MY_ID].allowDir[1])

			elif event.type == KEYUP:
				if event.key == K_LEFT or event.key == K_RIGHT:
					players[MY_ID].set_direction('NONE')
				elif event.key == K_a or event.key == K_d:
					players[MY_ID].set_direction('NONE')
				elif event.key == K_w or event.key == K_s:
					players[MY_ID].set_direction('NONE')
				elif event.key == K_UP or event.key == K_DOWN:
					players[MY_ID].set_direction('NONE')

	#######################################################


	################### DRAW COMPONENTS ###################
	
	def draw_components():
		
		# paint background
		windowSurface.fill(e.COLOR['DIMMESTGRAY'])
		
		# draw stage borders
		pygame.draw.rect(windowSurface, e.COLOR['DIMGRAY'], [arenaLEFT, arenaTOP, arenaWIDTH, arenaHEIGHT], 1)
		border_rects = []

		# print borders
		for b in borders.values():
			border_rects.append( pygame.draw.line(windowSurface, e.COLOR['DIMMERGRAY'], b[0], b[1], paddleWIDTH/2) )
		

		# draw the paddles
		paddle_rects = []
		for i in range(2): #top bottom
			paddle_rects.append(pygame.draw.line(windowSurface, players[i].get_colorValue(), (players[i].x, players[i].y), (players[i].x + paddleHEIGHT, players[i].y), paddleWIDTH))
		for i in range(2,4): #left right
			paddle_rects.append(pygame.draw.line(windowSurface, players[i].get_colorValue(), (players[i].x, players[i].y), (players[i].x + paddleWIDTH, players[i].y), paddleHEIGHT))


		# draw the ball
		if ball.heldBy == 0:
			ball.set_pos( (paddle_rects[0].left + 2*paddleHEIGHT/3, paddle_rects[0].bottom + ballWIDTH/2) )
		elif ball.heldBy == 1:
			ball.set_pos( (paddle_rects[1].right - paddleHEIGHT/3, paddle_rects[1].top - ballHEIGHT/2) )
		elif ball.heldBy == 2:
			ball.set_pos( (paddle_rects[2].right + ballWIDTH/2 - 1, paddle_rects[2].top + paddleHEIGHT/3) )
		elif ball.heldBy == 3:
			ball.set_pos( (paddle_rects[3].left - ballWIDTH/2, paddle_rects[3].top + paddleHEIGHT/3) )
		if ball.heldBy != -1:
			ball.set_color(players[ball.heldBy].color)
		ball_rect = pygame.draw.circle(windowSurface, ball.get_colorValue(), (ball.x, ball.y), ballWIDTH/2)

		rects = [ball_rect, paddle_rects, border_rects] 

		#draw scoreboard
		pygame.draw.rect(windowSurface, e.COLOR['DIMMERGRAY'], [arenaLEFT, WINDOWHEIGHT-20, arenaWIDTH, 100], 0)
		fontObj = pygame.font.SysFont("None", 42)
		pname_coord = [
				(arenaLEFT + 20, WINDOWHEIGHT-10),
				(arenaLEFT + 20, WINDOWHEIGHT+35),
				(arenaLEFT + arenaWIDTH/2 + 20, WINDOWHEIGHT-10),
				(arenaLEFT + arenaWIDTH/2 + 20, WINDOWHEIGHT+35)
			]
		pscore_coord = [
				(arenaLEFT + arenaWIDTH/2 - 60, WINDOWHEIGHT-10),
				(arenaLEFT + arenaWIDTH/2 - 60, WINDOWHEIGHT+35),
				(WINDOWWIDTH-100 - 60, WINDOWHEIGHT-10),
				(WINDOWWIDTH-100 - 60, WINDOWHEIGHT+35)
			]

		for p in players:
			msgSurfaceObj = fontObj.render(p.username, False, p.get_colorValue())
			msgRectobj = msgSurfaceObj.get_rect()
			msgRectobj.topleft = pname_coord[players.index(p)]
			windowSurface.blit(msgSurfaceObj, msgRectobj)

			msgSurfaceObj = fontObj.render(str(p.score), False, p.get_colorValue())
			msgRectobj = msgSurfaceObj.get_rect()
			msgRectobj.topleft = pscore_coord[players.index(p)]
			windowSurface.blit(msgSurfaceObj, msgRectobj)


		return rects

	#######################################################

	#################### GAME UPDATES #####################
	def game_updates():
		
		global ball_s
		global plyr_s

		#update ball position
		ball.update_pos(BSPEED)

		ball_s = [ str(ball.heldBy), str(ball.x), str(ball.y), ball.color, ball.direction]

		#update paddle positions
		for p in players:
			p.update_pos(PSPEED)

		#prepare own paddle status for sending + ball.heldBy shit
		plyr_s = [str(players[MY_ID].uid), str(players[MY_ID].x), str(players[MY_ID].y), str(players[MY_ID].score), players[MY_ID].color, players[MY_ID].direction]
		send_shiz("STAT")
		# own_status = [str(players[MY_ID].uid), players[MY_ID].color, players[MY_ID].direction, str(players[MY_ID].x), str(players[MY_ID].y)]

	#######################################################

	###################### GAME FLOW ######################
	
	rects = draw_components()
	ball_rect, paddle_rects, border_rects = rects[0], rects[1], rects[2]
	
	game_events()

	handle_ballCollisions(ball_rect, paddle_rects)
	handle_ballCollisions(ball_rect, border_rects, False)
	handle_borderPaddleCollisions(border_rects, paddle_rects)
	
	game_updates()
	
	manage_scoring()

	#######################################################
	


############ GAME END SCENE ############ 
def over():
	pass


curScene = 'wait'
MY_ID = None
ball.set_heldBy(0)

#main application loop tralalalala
while True:
	
	if curScene == 'home':
		home()
	elif curScene == 'wait':
		wait()
	elif curScene == 'setPlayer':
		setPlayer()
	elif curScene == 'game':
		game()
	elif curScene == 'over':
		over()

	pygame.display.update()
	clock.tick(frame_fate)
	# time.sleep(0.1)