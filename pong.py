import sys, time, random, thread
import elements as e
from socket import *
from gameconfig import *
from netconfig import *
import pygame
from pygame.locals import *


##################  NETWORKING CONFIGURATION  ##################

serverName = "127.0.0.1"
# serverName = "192.168.60.148"
serverPort = 12000

clientSocket = socket(AF_INET, SOCK_DGRAM)

BUFFER_SIZE=2048

### SHIZ TO SEND ###
ball_s = [] # ball_s = [ str(ball.heldBy), str(ball.x), str(ball.y), ball.color, ball.direction]
plyr_s = [] # plyr_s = [str(players[MY_ID].uid), str(players[MY_ID].x), str(players[MY_ID].y), str(players[MY_ID].score), players[MY_ID].color, players[MY_ID].direction, players[MY_ID].username]

def send_shiz(clientMessage, ID=None):
	
	if clientMessage == "JOIN":
		clientSocket.sendto(clientMessage, (serverName, serverPort))
	elif clientMessage == "DONE":
		clientSocket.sendto(clientMessage, (serverName, serverPort))
	elif clientMessage == "STAT":
		shizSendMsg = clientMessage + str(ID) + '$SHIZ$'.join( [ '$BALL$'.join(ball_s), '$PLYR$'.join(plyr_s) ] ) + "~ENDDATA~"
		clientSocket.sendto(shizSendMsg, (serverName, serverPort))
	elif clientMessage == "POUT":
		clientSocket.sendto(clientMessage + str(ID) + "".join([str(ai) for ai in players_AI]), (serverName, serverPort))

def recv_shiz():

	while True:

		msg, serverAddress = clientSocket.recvfrom(BUFFER_SIZE)
		serverMessage = msg[:4]


		if serverMessage == "JOIN":
			return int(msg[4:])
		elif serverMessage == "DONE":
			return int(msg[4:])
		elif serverMessage == "TIME":
			global seconds
			seconds = int(msg[4:])
		elif serverMessage == "POUT":
			if msg[5:] == "KBYE":
				clientSocket.close()
				sys.exit()
		elif serverMessage == "SOUT":
			print players[int(msg[4])].username + " has disconnected!"
		elif serverMessage == "DOAI":
			quittersIDs = msg[5:]
			print quittersIDs
			for q in quittersIDs:
				print "quitter " + q
				ID = int(q)
				players_AI.append(ID)
		elif serverMessage == "STAT":

			msg = msg.split("~ENDDATA~")
			
			try:
				for m in msg:

					ID = int(m[4])

					m = m[5:] # trim from m the serverMessage and ID
					m = m.split("$SHIZ$") #separate ball status from player status

					ball_r = m[0].split("$BALL$") #separate ball fields
					plyr_r = m[1].split("$PLYR$") #separate player fields

					if ball_r[0] != MY_ID:
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



	def wait_events():
		while curScene == 'wait':
			for event in pygame.event.get():
				if event.type == QUIT:
					send_shiz("POUT", MY_ID)
					clientSocket.close()
					pygame.quit()
					sys.exit()
			
				elif event.type == KEYDOWN and event.key == K_ESCAPE:
					pygame.event.post(pygame.event.Event(QUIT))	


	thread.start_new_thread(wait_events, ())

	# connect to server
	while MY_ID == None:
		print "Connecting to server..."
		send_shiz("JOIN")
		MY_ID = recv_shiz()

		if MY_ID == -1:
			print "Sorry, slots full for now.  Try again later."
			global curScene
			curScene = 'home'
			return None
	
	print "Connected! Your ID: " + str(MY_ID)

	players[MY_ID].set_username(myUsername)
	write_text( "HI, " + players[MY_ID].username + "!", players[MY_ID].color, (50, 50 + 70*0) )
	write_text( "THIS WILL BE THE COLOR OF YOUR PADDLE.",  players[MY_ID].color, (50, 50 + 70*1) )

	print "Waiting for other players to connect..."
	write_text( "WAITING FOR OTHER PLAYERS TO CONNECT...",  "WHITE", (50, 50 + 70*2) )

	while True:
		send_shiz("DONE")
		num_connectedPlayers = recv_shiz()
		if num_connectedPlayers == NUM_PLAYERS:
			print "num_connectedPlayers: " + str(num_connectedPlayers)
			curScene = 'game'
			thread.start_new_thread(recv_shiz, ())
			global frame_rate
			frame_rate = 600
			write_text( "READY!",  "WHITE", (50, 50 + 70*3) )
			time.sleep(2)
			break


############ GAME SCENE ############ 
def game():

	#################### GAME TIMER SHIZ ####################	

	if seconds==0:
		global curScene
		curScene = 'over'

	#######################################################


	##################### SEND SHIZ #####################
	def send_updates(ID):

		global ball_s
		global plyr_s


		ball_s = [ str(ball.heldBy), str(ball.x), str(ball.y), ball.color, ball.direction]
		plyr_s = [str(players[ID].uid), str(players[ID].x), str(players[ID].y), str(players[ID].score), players[ID].color, players[ID].direction, players[ID].username]
		#prepare own paddle status for sending + ball.heldBy shit
		
		# print ball_s
		send_shiz("STAT", ID)


	#######################################################


	################### DRAW COMPONENTS ###################
	
	def draw_components():
		
		# draw stage borders
		pygame.draw.rect(windowSurface, e.COLOR['DIMGRAY'], [arenaLEFT, arenaTOP, arenaWIDTH, arenaHEIGHT], 1)
		border_rects = []

		# print borders
		for b in borders.values():
			border_rects.append( pygame.draw.line(windowSurface, e.COLOR['DIMMERGRAY'], b[0], b[1], paddleWIDTH/2) )
		
		#draw timer
		global seconds
		output_string = str(seconds)
		font = pygame.font.Font('assets/fonts/5x5_pixel.ttf', 200)
		text = font.render(output_string, True, (35,35,35))
		textRectobj = text.get_rect()
		textRectobj.center = (WINDOWWIDTH/2, WINDOWHEIGHT/2)
		windowSurface.blit(text, textRectobj)

		# draw the paddles
		paddle_rects = []
		for i in range(4):
			paddle_rect = None
			if i in range(2): #top bottom
				paddle_rect = pygame.Rect(players[i].x, players[i].y, paddleHEIGHT, paddleWIDTH)
			elif i in range(2,4): #left right
				paddle_rect = pygame.Rect(players[i].x, players[i].y, paddleWIDTH ,paddleHEIGHT)
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


	##################### GAME EVENTS #####################
	
	def game_events():
	

		for ai in players_AI:
			if players[ai].ball_onTerr(ball, WINDOWHEIGHT, WINDOWWIDTH):
				players[ai].move_AI(ball)

		if ball.heldBy in players_AI:
			if ball.heldBy == 0:
				ball.set_direction('SE')
			elif ball.heldBy == 1:
				ball.set_direction('NE')
			elif ball.heldBy == 2:
				ball.set_direction('NE')
			elif ball.heldBy == 3:
				ball.set_direction('SW')
			ball.set_heldBy(-1)


		for event in pygame.event.get():
			
			if event.type == QUIT:
				send_shiz("POUT", MY_ID)
				clientSocket.close()
				pygame.quit()
				sys.exit()
			
			elif event.type == KEYDOWN:
							
				if event.key == K_ESCAPE:
					clientSocket.close()
					pygame.event.post(pygame.event.Event(QUIT))				
				
				elif event.key == K_SPACE and ball.heldBy == MY_ID:
					if ball.heldBy == 0:
						ball.set_direction('SE')
					elif ball.heldBy == 1:
						ball.set_direction('NE')
					elif ball.heldBy == 2:
						ball.set_direction('NE')
					elif ball.heldBy == 3:
						ball.set_direction('SW')

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


	################## COLLISION FUCTIONS ##################


	# handles collisions for both the paddle and the borders
	def handle_ballCollisions(ball_rect, rects, isPaddle=True):
		
		ballDir = ball.get_directionValue()

		ball_rect.x += ballDir[0]
		ball_rect.y += ballDir[1]

		rect_i = ball_rect.collidelist(rects)
		
		if rect_i != -1:
			if isPaddle:
				# hitSoundObj.play()
				ball.set_color(players[rect_i].color)
				if rect_i < 2: 
					ball.bounce('horizontal')
				else:
					ball.bounce('vertical')
			else:
				# checks if the ball had just hit a horizontal border
				bounceSoundObj.play()
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
	 
	#######################################################

	#################### GAME UPDATES #####################

	def game_updates():

		#update ball position
		for ai in players_AI:
			if players[ai].color == ball.color:
				ball.update_pos(BSPEED)
		
		if ball.color == players[MY_ID].color:
			ball.update_pos(BSPEED)


		#update paddle positions
		players[MY_ID].update_pos(PSPEED)

		
		
		# if this client handles AI, it handles its own 
		for ai in players_AI:
			players[ai].update_pos(PSPEED)
			plyr_s = [str(players[ai].uid), str(players[ai].x), str(players[ai].y), str(players[ai].score), players[ai].color, players[ai].direction, players[ai].username]
			send_shiz("STAT", ai)


	#################### SCORING SYSTEM ####################

	def manage_scoring():

		# index of the player whose side had the ball come out:  0 - top; 1 - bottom; 2 - left; 3 - right
		player_side = -1 

		TOP = 0
		BOTTOM = 1
		LEFT = 2
		RIGHT = 3

		if ball.x < 0:
			player_side = LEFT
		elif ball.x > WINDOWWIDTH:
			player_side = RIGHT
		elif ball.y < 0:
			player_side = TOP
		elif ball.y > WINDOWHEIGHT:
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
			send_updates(player_side)


	###################### GAME FLOW ######################

	rects = draw_components()
	ball_rect, paddle_rects, border_rects = rects[0], rects[1], rects[2]
	
	game_events()

	handle_ballCollisions(ball_rect, paddle_rects)
	handle_ballCollisions(ball_rect, border_rects, False)
	handle_borderPaddleCollisions(border_rects, paddle_rects)
	
	game_updates()
	
	manage_scoring()

	send_updates(MY_ID)

	#######################################################




############ GAME END SCENE ############ 
def over():
	

	def over_events():
		for event in pygame.event.get():
			
			if event.type == QUIT:
				clientSocket.close()
				pygame.quit()
				sys.exit()
			
			elif event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					pygame.event.post(pygame.event.Event(QUIT))	


	def draw_components():
		# ---- draw GAME OVER here ----
		fontObj = pygame.font.Font("assets/fonts/pixel_maz.ttf", 120)

		overSurfaceObj = fontObj.render("GAME OVER", False, e.COLOR[random.choice(pcolors)])
		overRectobj = overSurfaceObj.get_rect()
		overRectobj.center = (WINDOWWIDTH/2, WINDOWHEIGHT/5)
		windowSurface.blit(overSurfaceObj, overRectobj)

		# ---- draw scores ----
		fontObj = pygame.font.Font("assets/fonts/pixel_maz.ttf", 60)
		
		pname_coord = [
				(arenaLEFT + 50, arenaTOP + 150 + 60*0),
				(arenaLEFT + 50, arenaTOP + 150 + 60*1),
				(arenaLEFT + 50, arenaTOP + 150 + 60*2),
				(arenaLEFT + 50, arenaTOP + 150 + 60*3)
			]

		pscore_coord = [
				(arenaLEFT + arenaWIDTH - 130, arenaTOP + 150 + 60*0),
				(arenaLEFT + arenaWIDTH - 130, arenaTOP + 150 + 60*1),
				(arenaLEFT + arenaWIDTH - 130, arenaTOP + 150 + 60*2),
				(arenaLEFT + arenaWIDTH - 130, arenaTOP + 150 + 60*3)
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

	over_events()
	draw_components()



try:

	playmusic()
	
	#main application loop tralalalala
	while True:
		

		# paint background
		windowSurface.fill(e.COLOR['DIMMESTGRAY'])

		if curScene == 'home':
			frame_rate = 10
			home()
		elif curScene == 'setPlayer':
			setPlayer()
		elif curScene == 'wait':
			wait()
		elif curScene == 'game':
			frame_rate = 500
			game()
		elif curScene == 'over':
			frame_rate = 5
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