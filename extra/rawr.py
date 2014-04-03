import pygame, sys, time, random, thread, connection, socket
from pygame.locals import *
import elements as e
from socket import *

####################  PYGAME CONFIGURATION  ####################

# set up pygame 
pygame.init()

# set up the window
WINDOWWIDTH = 800	
WINDOWHEIGHT = 500
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT+20), 0, 32)
pygame.display.set_caption('QuadPong')

########## set up arena's "dimensions" ##########
arenaTOP = WINDOWHEIGHT/10
arenaLEFT = WINDOWWIDTH/10
arenaWIDTH = WINDOWWIDTH - arenaLEFT*2
arenaHEIGHT = WINDOWHEIGHT - arenaTOP*2



players = [("jadurani", 1), ("jadurani", 10), ("jadurani", 9), ("jadurani", 4)]
pcolors = [e.COLOR['RED'], e.COLOR['GREEN'], e.COLOR['BLUE'], e.COLOR['YELLOW']]

while True:

	pygame.draw.rect(windowSurface, e.COLOR['DIMGRAY'], [arenaLEFT, arenaTOP, arenaWIDTH, arenaHEIGHT], 1)

	fontObj = pygame.font.Font("assets/pixel_maz.ttf", 60)
	# pname_coord = 
	# 		(arenaLEFT + 20, WINDOWHEIGHT-20),
	# 		(arenaLEFT + 20, WINDOWHEIGHT),
	# 		(arenaLEFT + arenaWIDTH/2 + 20, WINDOWHEIGHT-10),
	# 		(arenaLEFT + arenaWIDTH/2 + 20, WINDOWHEIGHT+35)
	# 	]
	pscore_coord = [
			((arenaLEFT+arenaWIDTH)/4 -50, WINDOWHEIGHT-20),
			(2*(arenaLEFT+arenaWIDTH)/4 -50, WINDOWHEIGHT-20),
			(3*(arenaLEFT+arenaWIDTH)/4 -50, WINDOWHEIGHT-20),
			(4*(arenaLEFT+arenaWIDTH)/4 -50, WINDOWHEIGHT-20)
		]
	# pname_coord = [
	# 		(arenaLEFT + 20, WINDOWHEIGHT-20),
	# 		(arenaLEFT + 20, WINDOWHEIGHT),
	# 		(arenaLEFT + arenaWIDTH/2 + 20, WINDOWHEIGHT-10),
	# 		(arenaLEFT + arenaWIDTH/2 + 20, WINDOWHEIGHT+35)
	# 	]
	# pscore_coord = [
	# 		(arenaLEFT + arenaWIDTH/2 - 60, WINDOWHEIGHT-10),
	# 		(arenaLEFT + arenaWIDTH/2 - 60, WINDOWHEIGHT+35),
	# 		(WINDOWWIDTH-100 - 60, WINDOWHEIGHT-10),
	# 		(WINDOWWIDTH-100 - 60, WINDOWHEIGHT+35)
	# 	]


	for i in range(len(players)):
		# msgSurfaceObj = fontObj.render(players[i][0], False, pcolors[i])
		# msgRectobj = msgSurfaceObj.get_rect()
		# msgRectobj.topleft = pname_coord[i]
		# windowSurface.blit(msgSurfaceObj, msgRectobj)

		msgSurfaceObj = fontObj.render(str(players[i][1]), False, pcolors[i])
		msgRectobj = msgSurfaceObj.get_rect()
		msgRectobj.topleft = pscore_coord[i]
		windowSurface.blit(msgSurfaceObj, msgRectobj)

	pygame.display.update()

sys.ext()