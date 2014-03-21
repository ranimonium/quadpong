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
WINDOWWIDTH = 800
WINDOWHEIGHT = 400
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)
pygame.display.set_caption('ProtoPong 4')

# set up arena's "dimensions"
arenaTOP = WINDOWHEIGHT/12
arenaLEFT = WINDOWWIDTH/12
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
pcolors = [e.CBLUE, e.RED, e.GREEN, e.BLUE]
pcoords = [
		[(WINDOWWIDTH)/2 - paddleHEIGHT/2, arenaTOP - 5], #player 0 top
		[(WINDOWWIDTH)/2 - paddleHEIGHT/2, (arenaTOP+arenaHEIGHT) - 5], #player 1 bottom
		[arenaLEFT - 5, WINDOWHEIGHT/2 - paddleHEIGHT/2], #player 2 left
		[(arenaLEFT + arenaWIDTH) - paddleWIDTH/2, WINDOWHEIGHT/2 - paddleHEIGHT/2], #player 3 right
	] #[[x,y],[x,y],[x,y],[x,y]]

players = [e.Player(i, pcolors[i], pcoords[i]) for i in range(NUM_PLAYERS)]
for p in players:
	p.set_direction(e.NONE)

#set up the ball
ballWIDTH, ballHEIGHT = 14, 14
ball = e.Ball( e.AQUA, [350, 250])
		# [ random.randint(arenaLEFT+150, arenaLEFT+arenaWIDTH-150), #random x position of ball
		# random.randint(arenaTOP+150,arenaTOP+arenaHEIGHT-150)]) #random y position of ball
ball.set_direction(e.SW)
# ball.set_direction(random.choice(e.DIAGDIR))


def handle_collisions(brect, prects):
	p_indHit = brect.collidelist(prects)
	
	if p_indHit != -1:
		if p_indHit < 2: #horizontal paddles hit
			ball.bounce('horizontal')
		else:
			ball.bounce('vertical')
		ball.set_color(players[p_indHit].color)

BSPEED = 1

PSPEED = 2

while True:

	# background
	windowSurface.fill(e.BLACK)

	# pygame.draw.polygon(windowSurface, (255, 255, 255), [(100, 100), (WINDOWWIDTH-100, 100), (100, WINDOWHEIGHT-100), (WINDOWWIDTH-100, WINDOWHEIGHT-100)], 1)
	#draw borders
	pygame.draw.rect(windowSurface, (255, 255, 255), [arenaLEFT, arenaTOP, arenaWIDTH, arenaHEIGHT], 1)
	
	# draw the ball
	brect = pygame.draw.rect(windowSurface, ball.color, [ball.x, ball.y, ballWIDTH, ballHEIGHT])

	prects = []
	# draw the paddles
	for i in range(2):
		prects.append(pygame.draw.rect(windowSurface, players[i].color, [players[i].x, players[i].y, paddleHEIGHT, paddleWIDTH]))
	for i in range(2,4):
		prects.append(pygame.draw.rect(windowSurface, players[i].color, [players[i].x, players[i].y, paddleWIDTH, paddleHEIGHT])) #proper setting

	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()
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
	handle_collisions(brect, prects)
	
	#update ball position
	ball.update_pos(BSPEED)
	
	#update paddle positions
	for p in players:
		p.update_pos(PSPEED)

	if ball.x < -10 or ball.x > WINDOWWIDTH+10 or ball.y < -10 or ball.y > WINDOWHEIGHT+10:
		ball = e.Ball( e.AQUA, [350, 250])
		ball.set_direction(e.SW)
	pygame.display.update()
	time.sleep(0.0009)
