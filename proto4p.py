"""
Prototype for 4 players
Will merge all of these later on
OR not.
"""

import pygame, sys, time, random
from pygame.locals import *
import elements as e

# set up pygame 
pygame.init()

# set up the window
WINDOWWIDTH = 900
WINDOWHEIGHT = 500
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)
pygame.display.set_caption('ProtoPong 4')

#set up timer
clock = pygame.time.Clock()  
FPS = 200 #Frames Per Second

# set up arena's "dimensions"
arenaTOP = WINDOWHEIGHT/10
arenaLEFT = WINDOWWIDTH/10
arenaWIDTH = WINDOWWIDTH - arenaLEFT*2
arenaHEIGHT = WINDOWHEIGHT - arenaTOP*2


"""
For the paddle, consider this orientation:
 __
|  |
|  |
|  |
|__|

paddleWIDTH : horizontal
paddleHEIGHT : vertical

"""

#set up players
NUM_PLAYERS = 4

paddleWIDTH, paddleHEIGHT = 14, 100
pcolors = [e.MEDIUMSPRINGGREEN, e.HOTPINK, e.GOLD, e.DODGERBLUE]
pcoords = [
		[(WINDOWWIDTH)/2 - paddleHEIGHT/2, arenaTOP], #player 0 top
		[(WINDOWWIDTH)/2 - paddleHEIGHT/2, (arenaTOP+arenaHEIGHT)], #player 1 bottom
		[arenaLEFT - 5, WINDOWHEIGHT/2 - paddleHEIGHT/2], #player 2 left
		[(arenaLEFT + arenaWIDTH) - paddleWIDTH/2, WINDOWHEIGHT/2 - paddleHEIGHT/2], #player 3 right
	] #[[x,y],[x,y],[x,y],[x,y]]

players = [e.Player(i, pcolors[i], pcoords[i]) for i in range(NUM_PLAYERS)]
for p in players:
	p.set_direction(e.NONE)

#set up the ball
ballWIDTH, ballHEIGHT = 14, 14
ball = e.Ball( e.AQUA, [250, 250])
		# [ random.randint(arenaLEFT+150, arenaLEFT+arenaWIDTH-150), #random x position of ball
		# random.randint(arenaTOP+150,arenaTOP+arenaHEIGHT-150)]) #random y position of ball
ball.set_direction(e.NE)
ball.set_direction(random.choice(e.DIAGDIR))

# border coordinates and border lengths
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

# handles collisions for both the paddle and the borders
def handle_ballCollisions(ball_rect, rects, isPaddle=True):
	ball_rect.x += ball.direction[0]
	ball_rect.y += ball.direction[1]

	rect_i = ball_rect.collidelist(rects)
	
	if rect_i != -1:
		if isPaddle:
			ball.set_color(players[rect_i].color)
			if rect_i < 2: 
				ball.bounce('horizontal')
				# print 'horizontal'
			else:
				ball.bounce('vertical')
				# print 'vertical'
		else:
			# checks if the ball had just hit a horizontal border
			if borders.keys()[rect_i][-1:] == 'h':
				# print str(True)
				ball.bounce('horizontal')
			else:
				ball.bounce('vertical')
		# print "rect_i = " + str(rect_i)


def handle_borderPaddleCollisions(border_rects, paddle_rects):
	for p in paddle_rects:
		# print paddle_rects.index(p)
		p.x += players[paddle_rects.index(p)].direction[0]
		p.y += players[paddle_rects.index(p)].direction[1]

	for b in border_rects:
		paddle_i = b.collidelist(paddle_rects)
		if paddle_i != -1:
			players[paddle_i].set_direction(e.NONE)



#ball speed
BSPEED = 2

#paddle speed
PSPEED = 2
 
# main application loop
while True:
	
	# paint background
	windowSurface.fill(e.DIMMESTGRAY)
	
	# draw stage borders
	pygame.draw.rect(windowSurface, e.DIMGRAY, [arenaLEFT, arenaTOP, arenaWIDTH, arenaHEIGHT], 1)
	border_rects = []
	# print borders.keys()
	# print borders
	for b in borders.values():
		border_rects.append( pygame.draw.line(windowSurface, e.DIMMERGRAY, b[0], b[1], paddleWIDTH/2) )
		# pygame.draw.line(windowSurface, (100, 100, 100), b[0], b[1], paddleWIDTH/2)
	
	# draw the ball
	ball_rect = pygame.draw.circle(windowSurface, ball.color, (ball.x, ball.y), ballWIDTH/2)
	# ball_rect = pygame.draw.rect(windowSurface, ball.color, [ball.x, ball.y, ballWIDTH, ballHEIGHT])

	# draw the paddles
	paddle_rects = []
	for i in range(2):
		paddle_rects.append(pygame.draw.line(windowSurface, players[i].color, (players[i].x, players[i].y), (players[i].x + paddleHEIGHT, players[i].y), paddleWIDTH))
		# paddle_rects.append(pygame.draw.rect(windowSurface, players[i].color, [players[i].x, players[i].y, paddleHEIGHT, paddleWIDTH]))
	for i in range(2,4):
		paddle_rects.append(pygame.draw.line(windowSurface, players[i].color, (players[i].x, players[i].y), (players[i].x + paddleWIDTH, players[i].y), paddleHEIGHT))
		# paddle_rects.append(pygame.draw.rect(windowSurface, players[i].color, [players[i].x, players[i].y, paddleWIDTH, paddleHEIGHT])) #proper setting

	# handle user events
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()
		# elif event.type == MOUSEMOTION:
		# 	ball.set_pos(event.pos)

		elif event.type == KEYDOWN:
			if event.key == K_ESCAPE:
				pygame.event.post(pygame.event.Event(QUIT))
			
			if event.key == K_LEFT: #top
				players[0].set_direction(e.W)
			elif event.key == K_RIGHT: #top
				players[0].set_direction(e.E)
			elif event.key == K_a: #bottom
				players[1].set_direction(e.W)
			elif event.key == K_d: #bottom
				players[1].set_direction(e.E)
			elif event.key == K_w: #left
				players[2].set_direction(e.N)
			elif event.key == K_s: #left
				players[2].set_direction(e.S)
			elif event.key == K_UP: #right
				players[3].set_direction(e.N)
			elif event.key == K_DOWN: #right
				players[3].set_direction(e.S)

		elif event.type == KEYUP:
			if event.key == K_LEFT or event.key == K_RIGHT:  #player 0 top
				players[0].set_direction(e.NONE)
			elif event.key == K_a or event.key == K_d: #player 1 bottom
				players[1].set_direction(e.NONE)
			elif event.key == K_w or event.key == K_s: #player 2 left
				players[2].set_direction(e.NONE)
			elif event.key == K_UP or event.key == K_DOWN: #player 3  right
				players[3].set_direction(e.NONE)
	

	#handle collisions
	handle_ballCollisions(ball_rect, paddle_rects)
	handle_ballCollisions(ball_rect, border_rects, False)
	handle_borderPaddleCollisions(border_rects, paddle_rects)

	#update ball position
	ball.update_pos(BSPEED)
	
	#update paddle positions
	for p in players:
		p.update_pos(PSPEED)

	# restarts the ball if it ever gets out of the windor
	if ball.x < -10 or ball.x > WINDOWWIDTH+10 or ball.y < -10 or ball.y > WINDOWHEIGHT+10:
		ball = e.Ball( e.AQUA, [250, 250])
		ball.set_direction(e.NE)
	
	# window not drawn onto the actual screen unless this is called
	pygame.display.update()


	# parang time.sleep pero frames per second
	clock.tick(FPS)
