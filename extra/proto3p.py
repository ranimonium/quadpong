"""
Prototype for 3 players
Will merge all of these later on

"""

import pygame, sys, time
from pygame.locals import *


# set up pygame
pygame.init()

# set up the window
WINDOWWIDTH = 700
WINDOWHEIGHT = 700
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)
pygame.display.set_caption('ProtoPong 3')

#set up directions = (dx, dy)
N = (0, -1)
E = (1, 0)
W = (-1, 0)
S = (0, 1)
NE = (1, -1)
NW = (-1, 1)
SE = (1, 1)
SW = (-1, 1)

#set up colors
AQUA = pygame.Color(0, 255, 255)
RED = pygame.Color(255, 0, 0)
GREEN = pygame.Color(0, 255, 0)
BLUE = pygame.Color(0, 0, 255)
CBLUE = pygame.Color(100, 149, 237)
BLACK = pygame.Color(0, 0, 0)

#set up paddle and ball speeds
PSPEED = 1
BSPEED = 1

stage_points = {'topleft':[100, 100], 'topright':[600, 100], 'bottommiddle':[350, 450]}

#set up game elements/characters (t, r, b, l)
p1 = {'rect':pygame.draw.polygon(windowSurface, (255, 255, 255), [(350-10, 100-5),(350+10, 100-5),(350+10, 100+5),(350-10, 100+5)], 1), 'color':CBLUE, 'dir':E}
p2 = {'rect':pygame.draw.polygon(windowSurface, (255, 255, 255), [(225-4, 225-6),(175+2, 225-8),(175+2, 225+8),(175-4, 225+6)], 1), 'color':CBLUE, 'dir':E}
# players = [p1, p2]
# ball = {'rect':pygame.Rect(WINDOWWIDTH/2, WINDOWHEIGHT/2, 20, 20), 'color':AQUA, 'dir':UPRIGHT}

#main application loop
while True:
	
	#line(Surface, color, start_pos, end_pos, width=1)
	# pygame.draw.line(windowSurface, (255, 255, 255), (100, 100), (600, 100), 1)
	# pygame.draw.line(windowSurface, (255, 255, 255), (100, 100), (350, 450), 1)
	# pygame.draw.line(windowSurface, (255, 255, 255), (600, 100), (350, 450), 1)
	pygame.draw.polygon(windowSurface, (255, 255, 255), stage_points.values(), 1)
	pygame.draw.rect(windowSurface, p1['color'], p1['rect'])
	# pygame.draw.rect(windowSurface, p2['color'], p2['rect'])
	# pygame.draw.rect(windowSurface, p1['color'], p1['rect'])

	pygame.display.update()
	
