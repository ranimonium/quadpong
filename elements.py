# elements.py
#
# 	This module contains all the classes needed for the 
# 	game Multiplayer Pong.  

#set up colors
COLOR = {
	'YELLOW': (255, 255, 0),
	'RED': (255, 0, 0),
	'GREEN': (0, 255, 0),
	'BLUE': (0, 0, 255),
	'DIMGRAY': (105, 105, 105),
	'DIMMERGRAY': (80, 80, 80),
	'DIMMESTGRAY': (25, 25, 25),
	'BLACK': (0, 0, 0),
	'WHITE': (255, 255, 255),
}

#set up directions = (dx, dy)
DIR = {
	'NONE': (0, 0),
	'N': (0, -1),
	'E': (1, 0),
	'W': (-1, 0),
	'S': (0, 1),
	'NE': (1, -1),
	'SE': (1, 1),
	'NW': (-1, -1),
	'SW': (-1, 1)
	}


#returns the supposed direction of the ball when it bounces
def get_bounceDirection(direction, to):
	new_dir = []
	if to == 'vertical':
		if direction == 'NE':
			new_dir = 'NW'
		elif direction == 'NW':
			new_dir = 'NE'
		elif direction == 'SE':
			new_dir = 'SW'
		elif direction == 'SW':
			new_dir = 'SE'
	else:
		if direction == 'NE':
			new_dir = 'SE'
		elif direction == 'NW':
			new_dir = 'SW'
		elif direction == 'SE':
			new_dir = 'NE'
		elif direction == 'SW':
			new_dir = 'NW'
	return new_dir

def get_oppositeDirection(direction):

	new_dir = []

	if direction == DIR['N']:
		new_dir = DIR['S']
	elif direction == DIR['S']:
		new_dir = DIR['N']
	elif direction == DIR['E']:
		new_dir = DIR['W']
	elif direction == DIR['W']:
		new_dir = DIR['E']

	return new_dir

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
		self.color = color  #this is a string

	def get_colorValue(self):
		return COLOR[self.color]
	#pos is simply [x,y]
	def set_pos(self, pos):
		self.x, self.y = pos[0], pos[1]

	def get_pos(self):
		return (self.x, self.y)
		
	def set_direction(self, direction):
		self.direction = direction #this is a string, a key to the DIR dictionry

	def get_directionValue(self):
		return DIR[self.direction]

	def set_allowableDirection(self, directions):
		self.allowDir = directions

	def update_pos(self, speed):
		curDir = self.get_directionValue()
		self.set_pos( (self.x + speed*curDir[0], self.y + speed*curDir[1]) )

class Ball(Sprite):
	
	def bounce(self, to):
		self.set_direction(get_bounceDirection(self.direction, to))
	
	def set_heldBy(self, heldBy):
		self.heldBy = heldBy

class Player(Sprite):
	
	def __init__(self, uid, color, pos):
		Sprite.__init__(self, color, pos)
		self.uid = uid
		self.score = 0
		self.ai = False
		self.username = "PLAYER " + str(self.uid + 1)

	def add_score(self):
		self.score += 1

	def set_username(self, username):
		if username != "":
			self.username = username

	def on_AI(self):
		self.ai = True

	def move_AI(self, ball):

		if self.allowDir == ('W', 'E'):
			if ball.x > self.x:
				self.set_direction('E')
			elif ball.x < self.x:
				self.set_direction('W')
		elif self.allowDir == ('N', 'S'):
			if ball.y > self.y:
				self.set_direction('S')
			elif ball.y < self.y:
				self.set_direction('N')
	
	def ball_onTerr(self, ball, terr_HEIGHT, terr_WIDTH):

		if self.uid == 0 and ball.y < terr_HEIGHT/2: # top
			return True
		elif self.uid == 1 and ball.y > terr_HEIGHT/2: # bottom
			return True
		elif self.uid == 2 and ball.x < terr_WIDTH/3: # left
			return True
		elif self.uid == 3 and ball.x > 2*terr_WIDTH/3: # right
			return True
		else:
			return False