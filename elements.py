# elements.py
#
# 	This module contains all the classes needed for the 
# 	game Multiplayer Pong.  

#set up colors
GOLD = (255, 215, 0)
RED = (255, 0, 0)
LIGHTCORAL = (240, 128, 128)
HOTPINK = (255, 105, 180)
GREEN = (0, 255, 0)
SEAGREEN = (46, 139, 87)
MEDIUMSPRINGGREEN = (0, 250, 154)
AQUA = (0, 255, 255)
MEDIUMBLUE = (0, 0, 205)
CORNFLOWERBLUE = (100, 149, 237)
DODGERBLUE = (30, 144, 255)
DIMGRAY = (105, 105, 105)
DIMMERGRAY = (80, 80, 80)
DIMMESTGRAY = (25, 25, 25)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

#set up directions = (dx, dy)
NONE = (0, 0)
N = (0, -1)
E = (1, 0)
W = (-1, 0)
S = (0, 1)
NE = (1, -1)
SE = (1, 1)
NW = (-1, -1)
SW = (-1, 1)
STRTDIR = [N,E,W,S]
DIAGDIR = [NE,NW,SE,SW]

#returns the supposed direction of the ball when it bounces
def get_bounceDirection(direction, to):
	new_dir = []
	if to == 'vertical':
		if direction == NE:
			new_dir = NW
		elif direction == NW:
			new_dir = NE
		elif direction == SE:
			new_dir = SW
		elif direction == SW:
			new_dir = SE
	else:
		if direction == NE:
			new_dir = SE
		elif direction == NW:
			new_dir = SW
		elif direction == SE:
			new_dir = NE
		elif direction == SW:
			new_dir = NW
	return new_dir

# class Stage:
# 	"""docstring for Stage"""
# 	MEH = 2
# 	TRIANGLE = 3
# 	SQUARE = 4

# 	def __init__(self, edges):
# 		self.edges = edges

#sorry I'm not a fan of getters
		
#i don't want to use pygame's Sprite 
class Sprite:
	"""
	Mother of Ball and Player

	"""

	def __init__(self, color, pos):
		self.set_color(color)
		self.set_pos(pos)

	def set_color(self, color):
		self.color = color

	#pos is simply [x,y]
	def set_pos(self, pos):
		self.x, self.y = pos[0], pos[1]

	def get_pos(self):
		return (self.x, self.y)
		
	def set_direction(self, direction):
		self.direction = direction

	def update_pos(self, speed):
		self.set_pos( (self.x + speed*self.direction[0], self.y + speed*self.direction[1]) )

class Ball(Sprite):
	
	def bounce(self, to):
		# print "BOUNCE!"
		# print self.direction
		self.set_direction(get_bounceDirection(self.direction, to))
		# print self.direction
		
class Player(Sprite):
	
	def __init__(self, uid, color, pos):
		# super(Player, self).__init__(color, pos)
		Sprite.__init__(self, color, pos)
		self.uid = uid
		self.score = 0

	def add_score(self):
		self.score += 1 

# players = [Player(i) for i in range(4)]