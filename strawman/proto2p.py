"""
So this is sort of a prototype of the multiplayer pong.
2 players only (but we'd extend up to 6 players soon).

Controls:

p1:  player 1 == player blue == player on the left
	W - up
	S - down

p2:  player 2 == player red == player on the right
	UP 
	DOWN

No scoring system yet.

So much brute force pa.  To fix this soon.
"""

import pygame, sys, time
from pygame.locals import *


# set up pygame
pygame.init()

# set up the window
WINDOWWIDTH = 800
WINDOWHEIGHT = 400
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)
pygame.display.set_caption('Pong pong')

UPRIGHT = 1 
UPLEFT = 2
DOWNRIGHT = 3
DOWNLEFT =  4
NONE = 0

AQUA = pygame.Color(0, 255, 255)
RED = pygame.Color(255, 0, 0)
CBLUE = pygame.Color(100, 149, 237)
BLACK = pygame.Color(0, 0, 0)

PSPEED = 1

BSPEED = 1

#set up game elements/characters
p1 = {'rect':pygame.Rect(10, WINDOWHEIGHT/2-100/2, 20, 100), 'color':CBLUE, 'dir':NONE}  #(left, top, width, height)
p2 = {'rect':pygame.Rect(WINDOWWIDTH-10-20, WINDOWHEIGHT/2-100/2, 20, 100), 'color':RED, 'dir':NONE}
players = [p1, p2]
ball = {'rect':pygame.Rect(WINDOWWIDTH/2, WINDOWHEIGHT/2, 20, 20), 'color':AQUA, 'dir':UPRIGHT}

while True:
	
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()

		elif event.type == KEYDOWN:
			if event.key == K_w:
				p1['dir'] = -PSPEED
			if event.key == K_s:
				p1['dir'] = PSPEED
			if event.key == K_UP:
				p2['dir'] = -PSPEED
			if event.key == K_DOWN:
				p2['dir'] = PSPEED

		elif event.type == KEYUP:
			if event.key == K_w:
				p1['dir'] = 0.
			elif event.key == K_s:
				p1['dir'] = 0.
			if event.key == K_UP:
				p2['dir'] = 0.
			elif event.key == K_DOWN:
				p2['dir'] = 0.

		# check if the paddle has moved out of the window
		if p1['rect'].top < 0:
			# paddle has moved past the top
			if p1['dir'] == UPLEFT:
				p1['dir'] = DOWNLEFT
			if p1['dir'] == UPRIGHT:
				p1['dir'] = DOWNRIGHT
		if p1['rect'].bottom > WINDOWHEIGHT:
			# paddle has moved past the bottom
			if p1['dir'] == DOWNLEFT:
				p1['dir'] = UPLEFT
			if p1['dir'] == DOWNRIGHT:
				p1['dir'] = UPRIGHT

	# move the paddle data structure
	if ball['dir'] == DOWNLEFT:
		ball['rect'].left -= BSPEED - 0.25
		ball['rect'].top += BSPEED + 0.25
	if ball['dir'] == DOWNRIGHT:
		ball['rect'].left += BSPEED
		ball['rect'].top += BSPEED
	if ball['dir'] == UPLEFT:
		ball['rect'].left -= BSPEED
		ball['rect'].top -= BSPEED
	if ball['dir'] == UPRIGHT:
		ball['rect'].left += BSPEED
		ball['rect'].top -= BSPEED


	if ball['rect'].colliderect(p1['rect']):
		ball['color'] = p1['color']
		# block has moved past the left side
		if ball['dir'] == DOWNLEFT:
			ball['dir'] = DOWNRIGHT
		if ball['dir'] == UPLEFT:
			ball['dir'] = UPRIGHT
	
	if ball['rect'].colliderect(p2['rect']):
		ball['color'] = p2['color']
		# block has moved past the right side
		if ball['dir'] == DOWNRIGHT:
			ball['dir'] = DOWNLEFT
		if ball['dir'] == UPRIGHT:
			ball['dir'] = UPLEFT
		
	if ball['rect'].top < 0:
		# block has moved past the top
		if ball['dir'] == UPLEFT:
			ball['dir'] = DOWNLEFT
		if ball['dir'] == UPRIGHT:
			ball['dir'] = DOWNRIGHT
	if ball['rect'].bottom > WINDOWHEIGHT:
		# block has moved past the bottom
		if ball['dir'] == DOWNLEFT:
			ball['dir'] = UPLEFT
		if ball['dir'] == DOWNRIGHT:
			ball['dir'] = UPRIGHT
	
	p1['rect'].top = (p1['rect'].top + p1['dir'])
	p2['rect'].top = (p2['rect'].top + p2['dir'])
	
	if p1['rect'].top < 0:
		p1['rect'].top -= p1['rect'].top
	if p2['rect'].top < 0:
		p2['rect'].top -= p2['rect'].top
	if p1['rect'].bottom > WINDOWHEIGHT:
		p1['rect'].bottom -= (p1['rect'].bottom % WINDOWHEIGHT)
	if p2['rect'].bottom > WINDOWHEIGHT:
		p2['rect'].bottom -= (p2['rect'].bottom % WINDOWHEIGHT)

	# draw the black background onto the surface
	windowSurface.fill(BLACK)

	pygame.draw.rect(windowSurface, p1['color'], p1['rect'])
	pygame.draw.rect(windowSurface, p2['color'], p2['rect'])
	pygame.draw.rect(windowSurface, ball['color'], ball['rect'])

	if ball['rect'].left < -10 or ball['rect'].right > WINDOWWIDTH+10:
		ball = {'rect':pygame.Rect(WINDOWWIDTH/2, WINDOWHEIGHT/2, 20, 20), 'color':AQUA, 'dir':UPRIGHT}
	pygame.display.update()