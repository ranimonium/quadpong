import pygame, sys, time, random, thread
import elements as e
from pygame.locals import *
from socket import *

# from netconfig import *

####################  PYGAME CONFIGURATION  ####################

# set up pygame 
pygame.init()

WINDOWWIDTH = 800	
WINDOWHEIGHT = 500

windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT+50), 0, 32)
pygame.display.set_caption('QuadPong')

clock = pygame.time.Clock()


# set up the window


#####################  GAME CONFIGURATION  #####################

########## set up timer ##########
frame_rate = 600 #Frames Per Second

########## set up arena's "dimensions" ##########
arenaTOP = WINDOWHEIGHT/10
arenaLEFT = WINDOWWIDTH/10
arenaWIDTH = WINDOWWIDTH - arenaLEFT*2
arenaHEIGHT = WINDOWHEIGHT - arenaTOP*2

########## set up players ##########

NUM_PLAYERS = 4

paddleWIDTH, paddleHEIGHT = 14, 100

pcolors = ['RED', 'GREEN', 'BLUE', 'YELLOW']
pcoords = [
		[(WINDOWWIDTH)/2 - paddleHEIGHT/2, arenaTOP - paddleWIDTH/2],					#player 0 top
		[(WINDOWWIDTH)/2 - paddleHEIGHT/2, (arenaTOP+arenaHEIGHT) - paddleWIDTH/2 ], 	#player 1 bottom
		[arenaLEFT - 5, WINDOWHEIGHT/2 - paddleHEIGHT/2], 								#player 2 left
		[(arenaLEFT + arenaWIDTH) - paddleWIDTH/2, WINDOWHEIGHT/2 - paddleHEIGHT/2],	#player 3 right
	]

# instantiate Player class from elements module
players = [e.Player(i, pcolors[i], pcoords[i]) for i in range(4)]

# set Player direction to be NONE (meaning they're not moving yet)
for p in players:
	if players.index(p) < 2:
		p.set_allowableDirection( ('W', 'E') )
	else:
		p.set_allowableDirection( ('N', 'S') )
	p.set_direction('NONE')

PSPEED = 2	#paddle speed

### INDICES OF PLAYERS ON AI ###
players_AI = []
# print "DAMI " + str(len(players))
for ai in players_AI:
	players[ai].on_AI()


########## set up the ball ##########
ballWIDTH, ballHEIGHT = 16, 16
ball = e.Ball( 'RED', [250, 250])
ball.set_direction('NE')
ball.set_heldBy(0) #default, player 0 holds ball

BSPEED = 2	#ball speed

########## border coordinates and border lengths ##########
borderdiv_h = 6
borderdiv_v = 20

borders = {
	'topleft_h': [(arenaLEFT, arenaTOP),(arenaLEFT + arenaWIDTH/borderdiv_h, arenaTOP)],
	'topright_h': [(arenaLEFT + arenaWIDTH - arenaWIDTH/borderdiv_h, arenaTOP),(arenaLEFT + arenaWIDTH, arenaTOP)],
	'bottomleft_h':  [(arenaLEFT, arenaTOP+arenaHEIGHT),(arenaLEFT + arenaWIDTH/borderdiv_h, arenaTOP + arenaHEIGHT)],
	'bottomright_h':  [(arenaLEFT + arenaWIDTH - arenaWIDTH/borderdiv_h, arenaTOP+arenaHEIGHT),(arenaLEFT + arenaWIDTH, arenaTOP + arenaHEIGHT)],
	'topleft_v': [(arenaLEFT, arenaTOP),(arenaLEFT, arenaTOP + arenaHEIGHT/borderdiv_v)],
	'topright_v':  [(arenaLEFT+arenaWIDTH, arenaTOP),(arenaLEFT+arenaWIDTH, arenaTOP + arenaHEIGHT/borderdiv_v)],
	'bottomleft_v':  [(arenaLEFT, arenaTOP+arenaHEIGHT - arenaHEIGHT/borderdiv_v),(arenaLEFT, arenaTOP + arenaHEIGHT)],
	'bottomright_v':  [(arenaLEFT+arenaWIDTH, arenaTOP+arenaHEIGHT - arenaHEIGHT/borderdiv_v),(arenaLEFT+arenaWIDTH, arenaTOP + arenaHEIGHT)]
}

########## BLAH BLAH BLAH ##########

curScene = 'home'
# curScene = 'setPlayer'
MY_ID = None
myUsername = ""
ball.set_heldBy(0)



################################################################


##################  NETWORKING CONFIGURATION  ##################

serverName = "127.0.0.1"
serverPort = 12000

clientSocket = socket(AF_INET, SOCK_DGRAM)

BUFFER_SIZE=2048

### SHIZ TO SEND ###
ball_s = [] # ball_s = [ str(ball.heldBy), str(ball.x), str(ball.y), ball.color, ball.direction]
plyr_s = [] # plyr_s = [str(players[MY_ID].uid), str(players[MY_ID].x), str(players[MY_ID].y), str(players[MY_ID].score), players[MY_ID].color, players[MY_ID].direction, players[MY_ID].username]

def send_shiz(clientMessage, MY_ID=None):
	
	if clientMessage == "JOIN":
		clientSocket.sendto(clientMessage, (serverName, serverPort))
	elif clientMessage == "DONE":
		clientSocket.sendto(clientMessage, (serverName, serverPort))
	elif clientMessage == "STAT":
		shizSendMsg = clientMessage + str(MY_ID) + '$SHIZ$'.join( [ '$BALL$'.join(ball_s), '$PLYR$'.join(plyr_s) ] ) + "~ENDDATA~"
		# print shizSendMsg
		clientSocket.sendto(shizSendMsg, (serverName, serverPort))
	elif clientMessage == "POUT":
		print "SEND: " + str(MY_ID)
		clientSocket.sendto(clientMessage + str(MY_ID), (serverName, serverPort))
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

			# print "RECV STAT1"
			global players

			# print "RECV STAT1"
			msg = msg.split("~ENDDATA~")
			# print "RECV STAT2 " + str(msg)

			try:
				# print "RECV STAT3"
				for m in msg:
					# print "RECV STAT4 " + m
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







############ HOME SCREEN ############ 
def home():
	
	def home_events():
		
		for event in pygame.event.get():
			
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			
			elif event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					pygame.event.post(pygame.event.Event(QUIT))	
				elif event.key == K_SPACE:
					global curScene
					global frame_rate
					frame_rate = 600
					curScene = 'setPlayer'
					windowSurface.fill(e.COLOR['DIMMESTGRAY'])
					pygame.display.update()
					time.sleep(0.25)
	
	def draw_components():
		
		#draw title
		title_image = pygame.image.load("assets/images/title_"+ random.choice(pcolors) +".png")
		title_rect = title_image.get_rect()
		title_rect.center = (WINDOWWIDTH/2, WINDOWHEIGHT/2)
		# pygame.draw.rect(windowSurface, e.COLOR['WHITE'], title_rect)
		windowSurface.blit(title_image, title_rect)
		
		#draw press key thingy
		press_image = pygame.image.load("assets/images/press_"+ random.choice(pcolors) +".png")
		press_rect = press_image.get_rect()
		press_rect.center = (WINDOWWIDTH/2, WINDOWHEIGHT - WINDOWHEIGHT/6)
		# pygame.draw.rect(windowSurface, e.COLOR['WHITE'], title_rect)
		windowSurface.blit(press_image, press_rect)

	draw_components()
	home_events()


############ GET NAME OF PLAYER ############ 
def setPlayer():

	def isAlphaNum(key):
		
		# key numeric
		if 48 <= key and key <= 57:
			return True
		# key is letter
		elif 97 <= key and key <= 122:
			return True
		else:
			return False

	def setPlayer_events():

		global myUsername

		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()

			if event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					pygame.event.post(pygame.event.Event(QUIT))	
				elif event.key == K_BACKSPACE:
					myUsername = myUsername[0:-1]
				elif isAlphaNum(event.key) and len(myUsername) < 8:
					myUsername += chr(event.key)
					myUsername = myUsername.upper()
				elif event.key == K_RETURN:
					global curScene
					curScene = 'wait'
					#set up username later
					windowSurface.fill(e.COLOR['DIMMESTGRAY'])
					pygame.display.update()
					time.sleep(0.25)

	def draw_components():

		fontObj = pygame.font.Font("assets/fonts/pixel_maz.ttf", 72)

		label = 'USERNAME: '
		labelSurfaceObj = fontObj.render(label, False, e.COLOR['WHITE'])
		labelRectobj = labelSurfaceObj.get_rect()
		labelRectobj.midright = (WINDOWWIDTH/2, WINDOWHEIGHT/2)
		windowSurface.blit(labelSurfaceObj, labelRectobj)

		name = " " + myUsername + "".join(['_' for i in range( 8-(len(myUsername)) )])
		nameSurfaceObj = fontObj.render(name, False, e.COLOR['WHITE'])
		nameRectObj = nameSurfaceObj.get_rect()
		nameRectObj.midleft = (WINDOWWIDTH/2, WINDOWHEIGHT/2)
		# pygame.draw.rect(windowSurface, e.COLOR['WHITE'], nameRectObj, 0)
		windowSurface.blit(nameSurfaceObj, nameRectObj)


		fontObj = pygame.font.Font("assets/fonts/pixel_maz.ttf", 50)
		enter = 'PRESS ENTER TO CONTINUE'
		enterSurfaceObj = fontObj.render(enter, False, e.COLOR['WHITE'])
		enterRectObj = enterSurfaceObj.get_rect()
		enterRectObj.center = (WINDOWWIDTH/2 - 10, 3*WINDOWHEIGHT/4)

		windowSurface.blit(enterSurfaceObj, enterRectObj)

	draw_components()
	setPlayer_events()

############ WAITING FOR OTHER PLAYERS TO CONNECT ############ 
def wait():
	
	global curScene
	global MY_ID

	def write_text(text, color, position):
		fontObj = pygame.font.Font("assets/fonts/pixel_maz.ttf", 60)

		textSurfaceObj = fontObj.render(text, False, e.COLOR[color])
		textRectobj = textSurfaceObj.get_rect()
		textRectobj.topleft = position
		windowSurface.blit(textSurfaceObj, textRectobj)
		
		pygame.display.update()


	write_text("Connecting to server...", "WHITE", (50, 50))

	def wait_events():
		while curScene == 'wait':
			for event in pygame.event.get():
				if event.type == QUIT:
					print "send pout mwah"
					pygame.quit()
					send_shiz("POUT", MY_ID)

			
				elif event.type == KEYDOWN and event.key == K_ESCAPE:
					pygame.event.post(pygame.event.Event(QUIT))	


	thread.start_new_thread(wait_events, ())


	# connect to server
	while MY_ID == None:
		print "Connecting to server..."
		send_shiz("JOIN")
		MY_ID = recv_shiz()

		# players_AI.remove(MY_ID)

		if MY_ID == -1:
			print "Sorry, slots full for now.  Try again later."
			global curScene
			curScene = 'home'
			return None
	
	print "Connected! Your ID: " + str(MY_ID)
	write_text( "CONNECTED!", "WHITE", (50, 50 + 70*1) )

	players[MY_ID].set_username(myUsername)
	write_text( "HI, " + players[MY_ID].username + "!", players[MY_ID].color, (50, 50 + 70*2) )
	write_text( "THIS WILL BE THE COLOR OF YOUR PADDLE.",  players[MY_ID].color, (50, 50 + 70*3) )

	print "Waiting for other players to connect..."
	write_text( "WAITING FOR OTHER PLAYERS TO CONNECT...",  "WHITE", (50, 50 + 70*4) )

	# print "rawr"
	while True:
		send_shiz("DONE")
		num_connectedPlayers = recv_shiz()
		if num_connectedPlayers == NUM_PLAYERS:
			print "num_connectedPlayers: " + str(num_connectedPlayers)
			curScene = 'game'
			thread.start_new_thread(recv_shiz, ())
			global frame_rate
			frame_rate = 600
			write_text( "READY!",  "WHITE", (50, 50 + 70*5) )
			time.sleep(2)
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
	

		for ai in players_AI:
			if players[ai].ball_onTerr(ball, WINDOWHEIGHT, WINDOWWIDTH):
				players[ai].move_AI(ball)

		if ball.heldBy in players_AI:
			ball.set_heldBy(-1)



		for event in pygame.event.get():
			
			if event.type == QUIT:
				clientSocket.close()
				pygame.quit()
				sys.exit()
			
			elif event.type == KEYDOWN:
							
				if event.key == K_ESCAPE:
					clientSocket.close()
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
		
		# draw stage borders
		pygame.draw.rect(windowSurface, e.COLOR['DIMGRAY'], [arenaLEFT, arenaTOP, arenaWIDTH, arenaHEIGHT], 1)
		border_rects = []

		# print borders
		for b in borders.values():
			border_rects.append( pygame.draw.line(windowSurface, e.COLOR['DIMMERGRAY'], b[0], b[1], paddleWIDTH/2) )
		

		# draw the paddles
		paddle_rects = []
		for i in range(4):
			paddle_rect = None
			if i in range(2): #top bottom
				paddle_rect = pygame.Rect(players[i].x, players[i].y, paddleHEIGHT, paddleWIDTH)
				# paddle_rect = pygame.draw.line(windowSurface, players[i].get_colorValue(), (players[i].x, players[i].y), (players[i].x + paddleHEIGHT, players[i].y), paddleWIDTH)
			elif i in range(2,4): #left right
				paddle_rect = pygame.Rect(players[i].x, players[i].y, paddleWIDTH ,paddleHEIGHT)
				# paddle_rect = pygame.draw.line(windowSurface, players[i].get_colorValue(), (players[i].x, players[i].y), (players[i].x + paddleWIDTH, players[i].y), paddleHEIGHT)
			windowSurface.blit(pygame.image.load("assets/images/paddle_"+players[i].allowDir[0]+players[i].allowDir[1]+"_"+players[i].color+".png"), paddle_rect)
			paddle_rects.append(paddle_rect)


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
		# ball_rect = pygame.draw.circle(windowSurface, ball.get_colorValue(), (ball.x, ball.y), ballWIDTH/2)
		ball_rect = pygame.Rect((ball.x, ball.y), (ballWIDTH, ballHEIGHT))
		ball_rect.center = (ball.x, ball.y)
		windowSurface.blit(pygame.image.load("assets/images/ball_"+ball.color+".png"), ball_rect)
		rects = [ball_rect, paddle_rects, border_rects] 

		#draw scoreboard
		fontObj = pygame.font.Font("assets/fonts/pixel_maz.ttf", 60)

		pscore_coord = [
			((arenaLEFT+arenaWIDTH)/4 -50, WINDOWHEIGHT-20),
			(2*(arenaLEFT+arenaWIDTH)/4 -50, WINDOWHEIGHT-20),
			(3*(arenaLEFT+arenaWIDTH)/4 -50, WINDOWHEIGHT-20),
			(4*(arenaLEFT+arenaWIDTH)/4 -50, WINDOWHEIGHT-20)
		]

		for p in players:
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
		# if ball.color == players[MY_ID].color:
		ball.update_pos(BSPEED)

		ball_s = [ str(ball.heldBy), str(ball.x), str(ball.y), ball.color, ball.direction]


		#update paddle positions
		# for p in players:
		# 	p.update_pos(PSPEED)
		players[MY_ID].update_pos(PSPEED)
		
		for ai in players_AI:
			players[ai].update_pos(PSPEED)
		#prepare own paddle status for sending + ball.heldBy shit
		plyr_s = [str(players[MY_ID].uid), str(players[MY_ID].x), str(players[MY_ID].y), str(players[MY_ID].score), players[MY_ID].color, players[MY_ID].direction, players[MY_ID].username]
		# print "stat " + str(MY_ID)
		send_shiz("STAT", MY_ID)

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
	
	def draw_components():
		# ---- draw GAME OVER here ----



		# ---- draw scores ----
		fontObj = pygame.font.Font("assets/fonts/pixel_maz.ttf", 60)
		
		pname_coord = [
				(arenaLEFT + 50, arenaTOP + 100 + 60*0),
				(arenaLEFT + 50, arenaTOP + 100 + 60*1),
				(arenaLEFT + 50, arenaTOP + 100 + 60*2),
				(arenaLEFT + 50, arenaTOP + 100 + 60*3)
			]

		pscore_coord = [
				(arenaLEFT + arenaWIDTH - 130, arenaTOP + 100 + 60*0),
				(arenaLEFT + arenaWIDTH - 130, arenaTOP + 100 + 60*1),
				(arenaLEFT + arenaWIDTH - 130, arenaTOP + 100 + 60*2),
				(arenaLEFT + arenaWIDTH - 130, arenaTOP + 100 + 60*3)
			]

		for p in players:
			msgSurfaceObj = fontObj.render(str(p.username), False, p.get_colorValue())
			msgRectobj = msgSurfaceObj.get_rect()
			msgRectobj.topleft = pname_coord[players.index(p)]
			windowSurface.blit(msgSurfaceObj, msgRectobj)

			msgSurfaceObj = fontObj.render(str(p.score), False, p.get_colorValue())
			msgRectobj = msgSurfaceObj.get_rect()
			msgRectobj.topleft = pscore_coord[players.index(p)]
			windowSurface.blit(msgSurfaceObj, msgRectobj)




try:
	#main application loop tralalalala
	while True:
		
		# paint background
		windowSurface.fill(e.COLOR['DIMMESTGRAY'])

		if curScene == 'home':
			home()
		elif curScene == 'setPlayer':
			setPlayer()
		elif curScene == 'wait':
			wait()
		elif curScene == 'game':
			game()
		elif curScene == 'over':
			over()

		pygame.display.update()
		clock.tick(frame_rate)

except error, msg:
	print msg
	sys.exit()
except KeyboardInterrupt:
	sys.exit()
except Exception as exc:
	print exc