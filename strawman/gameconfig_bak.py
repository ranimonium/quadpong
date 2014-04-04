import elements as e
import random


# set up the window
WINDOWWIDTH = 800	
WINDOWHEIGHT = 500


#####################  GAME CONFIGURATION  #####################

########## set up timer ##########
frame_rate = 600 #Frames Per Second

########## set up arena's "dimensions" ##########
arenaTOP = WINDOWHEIGHT/10
arenaLEFT = WINDOWWIDTH/10
arenaWIDTH = WINDOWWIDTH - arenaLEFT*2
arenaHEIGHT = WINDOWHEIGHT - arenaTOP*2

########## set up players ##########

NUM_PLAYERS = 2

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
