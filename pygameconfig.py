import pygame
from pygame.locals import *

####################  PYGAME CONFIGURATION  ####################

# set up pygame 
pygame.init()

# set up the window
WINDOWWIDTH = 800	
WINDOWHEIGHT = 500

windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT+50), 0, 32)
pygame.display.set_caption('QuadPong')

clock = pygame.time.Clock()

####################  PYGAME-DEPENDENT GAME CONFIG  ####################

############ set up sounds ##########
bgmusicfile = 'assets/sounds/bgmusic.mp3'
hitSoundObj = pygame.mixer.Sound('assets/sounds/Hit.wav')
bounceSoundObj = pygame.mixer.Sound('assets/sounds/Bounce.wav')
scoreSoundObj = pygame.mixer.Sound('assets/sounds/Score.wav')


########### PLAY BACKGROUND MUSIC ##############
def playmusic():
	pygame.mixer.music.load(bgmusicfile)
	pygame.mixer.music.play(-1)