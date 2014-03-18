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
WINDOWWIDTH = 700
WINDOWHEIGHT = 700
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)
pygame.display.set_caption('ProtoPong 4')

# set up arena's "dimensions"
arenaTOP = 75
arenaLEFT = 75
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

paddleWIDTH, paddleHEIGHT = 10, 50
pcolors = [e.CBLUE, e.RED, e.GREEN, e.BLUE]
pcoords = [
		[(WINDOWWIDTH)/2 - paddleHEIGHT/2, arenaTOP - 5], #player 0 top
		[(WINDOWWIDTH)/2 - paddleHEIGHT/2, (arenaTOP+arenaHEIGHT) - 5], #player 1 bottom
		[arenaLEFT - 5, WINDOWHEIGHT/2 - paddleHEIGHT/2], #player 2 left
		[(arenaLEFT + arenaWIDTH) - paddleWIDTH/2, WINDOWHEIGHT/2 - paddleHEIGHT/2], #player 3 right
	] #[[x,y],[x,y],[x,y],[x,y]]

players = [e.Player(i, pcolors[i], pcoords[i]) for i in range(NUM_PLAYERS)]


#set up the ball
ballWIDTH, ballHEIGHT = 10, 10
ball = e.Ball( e.AQUA, 
		[ random.randint(arenaLEFT+150, arenaLEFT+arenaWIDTH-150), #random x position of ball
		random.randint(arenaTOP+150,arenaTOP+arenaHEIGHT-150)]) #random y position of ball

while True:

	# pygame.draw.polygon(windowSurface, (255, 255, 255), [(100, 100), (WINDOWWIDTH-100, 100), (100, WINDOWHEIGHT-100), (WINDOWWIDTH-100, WINDOWHEIGHT-100)], 1)
	pygame.draw.rect(windowSurface, (255, 255, 255), [arenaLEFT, arenaTOP, arenaHEIGHT, arenaWIDTH], 1)
	
	# draw the ball
	pygame.draw.rect(windowSurface, ball.color, [ball.x, ball.y, ballWIDTH, ballHEIGHT])

	# draw the paddles
	for i in range(2):
		pygame.draw.rect(windowSurface, players[i].color, [players[i].x, players[i].y, paddleHEIGHT, paddleWIDTH])
	for i in range(2,4):
		pygame.draw.rect(windowSurface, players[i].color, [players[i].x, players[i].y, paddleWIDTH, paddleHEIGHT]) #proper setting

	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()
		elif event.type == KEYDOWN:
			if event.key == K_ESCAPE:
				pygame.event.post(pygame.event.Event(QUIT))
	
	#update ball positions
	#update paddle positions

	pygame.display.update()