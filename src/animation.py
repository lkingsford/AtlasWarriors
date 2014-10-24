import pygcurse
import pygame
import sys
import random
import math

class Animation:
	def __init__(self):
		self.frame = -1
		self.frames = 0
		
	def update(self, window):
		self.frame += 1
		
class HealAnimation(Animation):
	def __init__(self, position):
		super().__init__()
		self.frames = 5
		self.position = position
		
	def update(self, window):
		super().update(window)
		fore = pygame.Color(self.frame * 24,self.frame * 24,self.frame * 32)		
		back = pygame.Color(self.frame * 16, self.frame * 16, self.frame * 32)
		window.putchar("*", x = self.position[0], y = self.position[1], fgcolor = fore, bgcolor = back)
		
class LevelUpAnimation(Animation):
	def __init__(self, position):
		super().__init__()
		self.frames = 5
		self.position = position

	def update(self, window):
		super().update(window)
		fore = 'silver'		
		back = pygame.Color(self.frame * 32, self.frame * 32, 0)
		window.putchar("@", x = self.position[0], y = self.position[1], fgcolor = fore, bgcolor = back)
		window.putchar(" ", x = self.position[0] - 1, y = self.position[1], fgcolor = fore, bgcolor = back)
		window.putchar(" ", x = self.position[0] + 1, y = self.position[1], fgcolor = fore, bgcolor = back)
		window.putchar(" ", x = self.position[0] , y = self.position[1] - 1, fgcolor = fore, bgcolor = back)
		window.putchar(" ", x = self.position[0] , y = self.position[1] + 1, fgcolor = fore, bgcolor = back)		

class BigPunchAnimation(Animation):
	def __init__(self, route, character):
		super().__init__()
		self.frames = len(route) + 1
		self.route = route
		self.character = character
		self.lastData = ((route[0][0], route[0][1]), '.', 'gray', 'black')
		
	def update(self, window):
		super().update(window)		
		curFrame = min(self.frame, len(self.route) - 1)
		fore = self.character.color	
		back = 'black'
		start = self.route[0]
		end = self.route[-1]
		dx = start[0] - end[0]
		dy = start[1] - end[1]		
		# Draw previous character
		if self.lastData != None:
			window.putchar(self.lastData[1], x=self.lastData[0][0], y = self.lastData[0][1], fgcolor = self.lastData[2], bgcolor = self.lastData[3])
		# Store this character
		self.lastData = (self.route[curFrame],\
			window._screenchar[self.route[curFrame][0]][self.route[curFrame][1]],\
			window._screenfgcolor[self.route[curFrame][0]][self.route[curFrame][1]],\
			window._screenbgcolor[self.route[curFrame][0]][self.route[curFrame][1]])
		# Draw dude
		window.putchar(self.character.character, x = self.route[curFrame][0], y = self.route[curFrame][1], fgcolor = fore, bgcolor = back)

class DragonsBreathAnimation(Animation):
	def __init__(self,  position, flameSpreadFrames):
		super().__init__()
		
		self.flameSpreadFrames = []
		for i in flameSpreadFrames:
			for j in range(2):
				self.flameSpreadFrames.append(i)
		self.flameSpreadFrames.append(flameSpreadFrames[len(flameSpreadFrames) - 1])		
		
		currentFrame = self.flameSpreadFrames[len(self.flameSpreadFrames)-1]
		while True:	
			lastFrame = currentFrame
			currentFrame = [[0]*len(lastFrame[0]) for i in range(len(lastFrame))]
			for i in range(len(lastFrame)):
				#print ("")
				for j in range(len(lastFrame[i])):
					currentFrame[i][j] = lastFrame[i][j] - 0.15
					#print (currentFrame[i][j], " ", end="")
					
			self.flameSpreadFrames.append(currentFrame)
					
			if max(map(max,currentFrame)) <= 0:
				break
		
		self.position = position
		self.frames = len(self.flameSpreadFrames ) - 1
	
	def update(self, window):
		super().update(window)
		
		# TODO: Insert part to copy screen if frame == 0, and paint that
		# character if flameSpreadFrames		
		
		width  = len(self.flameSpreadFrames[self.frame])				
		baseX = self.position[0]
		for i in range( (width//2) * -1, width // 2):
			height = len(self.flameSpreadFrames[self.frame][i])
			baseY = self.position[1]
			for j in range ( (height//2) * -1, height // 2):
				if (baseX + i > 0) and (baseX + i < window._width) and (baseY + j > 0) and (baseY + j < window._height):
					#improve this
					if (self.flameSpreadFrames[self.frame][i][j] > 3):
						window.putchar("O", x=baseX+i, y=baseY+j, fgcolor = pygame.Color(255,0,0), bgcolor = pygame.Color(255,255,0))
					elif (self.flameSpreadFrames[self.frame][i][j] > 2):
						window.putchar("*", x=baseX+i, y=baseY+j, fgcolor = pygame.Color(255,0,0), bgcolor = pygame.Color(255,255,0))
					elif (self.flameSpreadFrames[self.frame][i][j] > 1):
						window.putchar(random.choice(['*','+',';','\"']), x=baseX+i, y=baseY+j, fgcolor = pygame.Color(255,0,0), bgcolor = pygame.Color(255,128,0))
					elif (self.flameSpreadFrames[self.frame][i][j] > 0.75):
						window.putchar(random.choice(['"','o']), x=baseX+i, y=baseY+j, fgcolor = pygame.Color(255,128,0), bgcolor = pygame.Color(128,0,0))
					elif (self.flameSpreadFrames[self.frame][i][j] > 0.5):
						window.putchar(random.choice(['.',',']), x=baseX+i, y=baseY+j, fgcolor = pygame.Color(255,128,0), bgcolor = pygame.Color(96,0,0))
					elif (self.flameSpreadFrames[self.frame][i][j] > 0.25):
						window.putchar(random.choice(['.',',']), x=baseX+i, y=baseY+j, fgcolor = pygame.Color(255,64,0), bgcolor = pygame.Color(64,0,0))
					elif (self.flameSpreadFrames[self.frame][i][j] > 0.15):
						window.putchar(random.choice(['.',',']), x=baseX+i, y=baseY+j, fgcolor = pygame.Color(128,32,0), bgcolor = pygame.Color(32,0,0))
					elif (self.flameSpreadFrames[self.frame][i][j] > 0):
						window.putchar(random.choice(['.',',']), x=baseX+i, y=baseY+j, fgcolor = pygame.Color(128,0,0), bgcolor = pygame.Color(32,0,0))

class DrawArrowAnimation(Animation):
	def __init__(self, route):
		super().__init__()
		self.frames = len(route) + 1
		self.route = route
		# This gets the previous character so it can be put back.
		# It is ( (x, y), char, fgcolor, bgcolor )
		self.lastData = None
		
	def update(self, window):
		super().update(window)		
		curFrame = min(self.frame, len(self.route) - 1)
		fore = pygame.Color(165,42,42)		
		back = 'black'
		start = self.route[0]
		end = self.route[-1]
		dx = start[0] - end[0]
		dy = start[1] - end[1]
		if dx == 0:
			char = "|"
		elif dy == 0:
			char = "-"
		elif (dx > 0 and dy > 0) or (dx < 0 and dy < 0):
			char = "\\"
		else:
			char = "/"
		
		# Draw previous character
		if self.lastData != None:
			window.putchar(self.lastData[1], x=self.lastData[0][0], y = self.lastData[0][1], fgcolor = self.lastData[2], bgcolor = self.lastData[3])
		# Store this character
		self.lastData = (self.route[curFrame],\
			window._screenchar[self.route[curFrame][0]][self.route[curFrame][1]],\
			window._screenfgcolor[self.route[curFrame][0]][self.route[curFrame][1]],\
			window._screenbgcolor[self.route[curFrame][0]][self.route[curFrame][1]])
		# Draw arrow
		window.putchar(char, x = self.route[curFrame][0], y = self.route[curFrame][1], fgcolor = fore, bgcolor = back)

class DrawNecromancerSpell(Animation):		
	def __init__(self, target, dest, color):
		super().__init__()
		self.route = self.get_line(target.x, target.y, dest.x, dest.y)
		self.frames = len(self.route) + 1
		# This gets the previous character so it can be put back.
		# It is ( (x, y), char, fgcolor, bgcolor )
		self.lastData = None
		self.color = color
		
	def update(self, window):
		super().update(window)		
		curFrame = min(self.frame, len(self.route) - 1)
		fore = pygame.Color(165,42,42)		
		back = 'black'
		start = self.route[0]
		end = self.route[-1]
		dx = start[0] - end[0]
		dy = start[1] - end[1]		
		# Draw previous character
		if self.lastData != None:
			window.putchar(self.lastData[1], x=self.lastData[0][0], y = self.lastData[0][1], fgcolor = self.lastData[2], bgcolor = self.lastData[3])
		# Store this character
		self.lastData = (self.route[curFrame],\
			window._screenchar[self.route[curFrame][0]][self.route[curFrame][1]],\
			window._screenfgcolor[self.route[curFrame][0]][self.route[curFrame][1]],\
			window._screenbgcolor[self.route[curFrame][0]][self.route[curFrame][1]])
		# Draw arrow
		window.putchar("*", x = self.route[curFrame][0], y = self.route[curFrame][1], fgcolor = self.color, bgcolor = back)
	
	# I said in orc.py if this was needed elsewhere then I'd move it out of orc.py
	# It's needed elsewhere, and I've just copied it here too
	# Evidently, I lied.
	
	def get_line(self, x1, y1, x2, y2):
		points = []
		issteep = abs(y2-y1) > abs(x2-x1)
		if issteep:
			x1, y1 = y1, x1
			x2, y2 = y2, x2
		rev = False
		if x1 > x2:
			x1, x2 = x2, x1
			y1, y2 = y2, y1
			rev = True
		deltax = x2 - x1
		deltay = abs(y2-y1)
		error = int(deltax / 2)
		y = y1
		ystep = None
		if y1 < y2:
			ystep = 1
		else:
			ystep = -1
		for x in range(x1, x2 + 1):
			if issteep:
				points.append((y, x))
			else:
				points.append((x, y))
			error -= deltay
			if error < 0:
				y += ystep
				error += deltax
		# Reverse the list if the coordinates were reversed
		if rev:
			points.reverse()
		return points	

class DrawNecromancerDeath(Animation):
	def __init__(self, start):
		super().__init__()
		self.start = start
		# Store the screen
		self.beforeScreen = None

		self.frames = 30

	def update(self, window):
		super().update(window)	
		if self.beforeScreen == None:
			self.beforeScreen = [[0 for y in range(20)] for x in range(40)]
			for x in range(40):
				for y in range(20):
					self.beforeScreen[x][y] = (window._screenchar[x][y],\
						window._screenfgcolor[x][y],\
						window._screenbgcolor[x][y])
					
		self.values = [[0 for y in range(20)] for x in range(40)]
		for ix in range(40):
			for iy in range (20):
				dx = ix - self.start[0]
				dy = iy - self.start[1]
				value = max(0, -1 * abs(math.hypot(dx,dy)-(self.frame*1.5))+3)
				if value <= 0:
					window.putchar(self.beforeScreen[ix][iy][0], x = ix, y = iy,\
						fgcolor = self.beforeScreen[ix][iy][1],\
						bgcolor = self.beforeScreen[ix][iy][2])
				elif value <= 0.6:
					window.putchar(".", x = ix, y = iy,\
						fgcolor = 'silver',\
						bgcolor = 'black')
				elif value <= 1.2:
					window.putchar("o", x = ix, y = iy,\
						fgcolor = 'silver',\
						bgcolor = 'gray')
				elif value <= 1.8:
					window.putchar("O", x = ix, y = iy,\
						fgcolor = 'silver',\
						bgcolor = 'silver')
				elif value  <= 2.4:
					window.putchar("O", x = ix, y = iy,\
						fgcolor = 'silver',\
						bgcolor = 'white')
				else:
					window.putchar("O", x = ix, y = iy,\
						fgcolor = 'white',\
						bgcolor = 'white')
					

class DrawWarlordDeath(Animation):
	# Needs more work
	def __init__(self, start):
		super().__init__()
		self.start = start
		# Store the screen
		self.beforeScreen = None

		self.frames = 157

	def update(self, window):		
		super().update(window)
		#print (self.frame)		
		iteration = self.frame // 40
		if self.beforeScreen == None:
			self.beforeScreen = [[0 for y in range(20)] for x in range(40)]
			for x in range(40):
				for y in range(20):
					self.beforeScreen[x][y] = (window._screenchar[x][y],\
						window._screenfgcolor[x][y],\
						window._screenbgcolor[x][y])
					
		self.values = [[0 for y in range(20)] for x in range(40)]
		for ix in range(40):
			for iy in range (20):
				dx = ix - self.start[0]
				dy = iy - self.start[1]
				value = max(0,
					-1 * abs(math.hypot(dx,dy)-((self.frame % 40)*1))+1+(4*(iteration)),
					-1 * abs(math.hypot(dx,dy)-((self.frame % 40)*1.5))+1+(4*(iteration/4)),
					-1 * abs(math.hypot(dx,dy)-((self.frame % 20)*2))+1+(4*(iteration/3)))
				if value <= 0:
					window.putchar(self.beforeScreen[ix][iy][0], x = ix, y = iy,\
						fgcolor = self.beforeScreen[ix][iy][1],\
						bgcolor = self.beforeScreen[ix][iy][2])
				elif value <= 1:
					window.putchar(".", x = ix, y = iy,\
						fgcolor = 'red',\
						bgcolor = 'black')
				elif value <= 1.5:
					window.putchar("o", x = ix, y = iy,\
						fgcolor = 'silver',\
						bgcolor = 'gray')					
				elif value <= 2.5:
					window.putchar("o", x = ix, y = iy,\
						fgcolor = 'red',\
						bgcolor = 'gray')
				elif value <= 3:
					window.putchar("O", x = ix, y = iy,\
						fgcolor = 'red',\
						bgcolor = 'silver')
				elif value  <= 4:
					window.putchar("0", x = ix, y = iy,\
						fgcolor = 'black',\
						bgcolor = 'red')
				elif value  <= 4.5:
					window.putchar("O", x = ix, y = iy,\
						fgcolor = 'red',\
						bgcolor = 'black')
				else:
					window.putchar("O", x = ix, y = iy,\
						fgcolor = 'black',\
						bgcolor = 'black')


# Useful for debugging
class DrawRouteAnimation(Animation):
	def __init__(self, route):
		super().__init__()
		self.frames = len(route) + 5
		self.route = route
		
	def update(self, window):
		super().update(window)		
		curFrame = min(self.frame, len(self.route))
		fore = pygame.Color(128,196,255)		
		back = 'black'
		for i in range(curFrame):			
			window.putchar("*", x = self.route[i][0], y = self.route[i][1], fgcolor = fore, bgcolor = back)
		
class DrawAttackAnimation(Animation):
	def __init__(self, route):
		super().__init__()
		self.frames = 2
		self.route = route
	
	def update(self, window):
		super().update(window)
		fore = pygame.Color(128,196,255)		
		back = 'black'
		for i in self.route:			
			window.putchar("*", x = i[0], y = i[1], fgcolor = fore, bgcolor = back)


