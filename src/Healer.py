from enemy import *
import random
import Message

class Healer(Enemy):
	def __init__(self, messageLog, currentMap = None):
		super().__init__(messageLog, currentMap)
		self.levelMod = random.choice([-2,-1,0,0,0,0,0,1,1,2])
		self.level = currentMap.level + self.levelMod
		self.character = "h"
		self.name = "Healer"
		self.speed = 12
		self.hp = self.maxhp = round(13 * (max(1,self.level - 2) ** 0.4))
		self.mp = self.maxmp = round(10 * (max(1,self.level - 2) ** 0.4))
		self.mpChargeRate = round(3 * (max(1,self.level - 2) ** 0.4))
		self.baseDamage =  round(4 * (max(1,self.level - 2) ** 0.3))
		self.baseToHit =  round(2 * (max(1,self.level - 2) ** 0.2))
		self.baseToDefend = round(4 * (max(1,self.level - 2) ** 0.2)) 
		self.chartype = "Healer"
		
	def danger(self):
		return 3 + (self.levelMod / 2)
	
	def update(self):		
		# Healer tries to stay more then 4 away from PC
		
		# Find room currently in
		room = [i for i in self.currentMap.Rooms if (self.x >= i.x and self.x <= i.x + i.w and self.y >= i.y and self.y <= i.y + i.h)][0]
		# Get other characters in room
		charactersInRoom = [i for i in self.currentMap.characters if (i.x >= room.x and i.x <= room.x + room.w and i.y >= room.y and i.y <= room.y + room.h)]		
		# If got MP, heal the character on the same team with the lowest HP
		healCasted = False
		if self.mp > 2:
			try:
				lowestHealthFriend = min([i for i in charactersInRoom if i.team == self.team and i.hp < i.maxhp],
					key = lambda i: i.hp)
			except ValueError:
				lowestHealthFriend = None
			if (lowestHealthFriend != None):
				self.CastHeal(lowestHealthFriend)
				healCasted = True
		if not healCasted:
			# Run from PC of non team if nobody to heal
			try:
				nearestEnemy = min([i for i in self.currentMap.characters if i != self and i.team != self.team],
					key = lambda i: abs(self.x - i.x) + abs(self.y - i.y))
				dx = 0 if nearestEnemy.x == self.x else (1 if nearestEnemy.x < self.x else 1)
				dy = 0 if nearestEnemy.y == self.y else (1 if nearestEnemy.y < self.y else 1)
				self.tryMove(self.x + dx, self.y + dy)
				
			except ValueError:
				self.Wait()
				
