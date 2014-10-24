from enemy import *
import Message
import animation
# The necromancer is a special and unique enemy, hence these values are hardcoded 
#
# The necromancer uses nearby Zombies like mana
# He can drain zombies to:
#   - heal (and increase maximum health if healed enough);
#   - increase speed temporarily; (?)
#   - increase level; (?)
#   - increase unarmed skill for next hit
#
# Upon death, all zombies on the level will die.

class Necromancer(Enemy):
	def __init__(self, messageLog, currentMap = None):
		super().__init__(messageLog, currentMap)
		self.name = "Necromancer"
		self.level = 10
		self.character = "N"		
		self.speed = 14
		self.hp = self.maxhp = 15
		self.mp = self.maxmp = 16
		self.mpChargeRate = 2
		self.baseDamage =  6
		self.baseToHit =  7
		self.baseToDefend = 5
		self.color = "gray"	
		self.chartype = "Necromancer"
		self.curDanger = 25
		self.team = 3
	
	def danger(self):
		return self.curDanger
	
	def update(self):		
		# What are our priorities?
		# If health is low, we wanna heal. We'd kinda like enough maxhealth to reduce
		#   the expected damage of the PC to under 1/3 damage
		# If the chance of hitting the PC is less then half, we want to boost it
		# If the damage done to the PC is less then 1/3rd, we want to boost it
		# If there are no zombies nearby, we want to find our zombie friends
		# If there are enemies nearby, we want to kill them
		# If there are no enemies nearby, health is sufficient and boost is sufficient, nick some speed
		# Randomly choose to nick speed, health or boost if health is sufficient and enemy more then two away
	
		
		# Nearest enemy is naive and is simply approximate - I don't use pathfinding
		# It should always be the PC. Unless the PC lures him downstairs :D
		
					
		super().update()

		
		enemies = [i for i in self.currentMap.characters if i != self and i.team != self.team]
		if len(enemies)>0:
			nearestEnemy = min(enemies,
					key = lambda i: abs(self.x - i.x) + abs(self.y - i.y))
		else:
			self.Wait()
			return
		
		
		EnemyAverageDamage = nearestEnemy.GetAverageDamage(self.ToDefend(), self.level)
		MyAverageDamage = self.GetAverageDamage(nearestEnemy.ToDefend(), nearestEnemy.level)
		
		ChanceToHit = self.ChanceToHit(self.ToHit()[0][0], self.ToDefend())
		
		ZombiesInRoom =  [i for i in self.currentMap.characters\
			if (i.team == self.team) and\
			len(self.currentMap.Map[self.x][self.y].rooms & self.currentMap.Map[i.x][i.y].rooms) > 0]
			
		# Priority list is tuplets of (priority, number)
		HealPriority = -1 * (self.hp/3 - EnemyAverageDamage)
		BoostPriority = 0.2 * (nearestEnemy.hp/3 - MyAverageDamage) - 0.3 * (ChanceToHit - 0.5)
		ZombieFriendPriority = -1 * 0.5 * len(ZombiesInRoom) + 2
		RandomPriority = 0 if HealPriority < 0 and ZombieFriendPriority < 0 and (abs(nearestEnemy.x - self.x) + abs(nearestEnemy.y - self.y)) > 2 else random.random() 
		Priorities = [
			(0, HealPriority), # Priority to Heal
			(1, BoostPriority), #Priority To Boost
			(2, ZombieFriendPriority), # Priority to finding zombie friendsies
			(4, 1), # Priority to attack
			(random.choice([0,1,3]), RandomPriority)] # Priority to randomly zapping a zombie for stuff nearby 
			
		AllZombies = [i for i in self.currentMap.characters\
			if (i.team == self.team)]			

		# Sort priorities in decreasing order
		Priorities.sort(key=lambda i: i[1], reverse=True)
		
		print (Priorities)
		
		if Priorities[0][0] == 0:
			# We wanna heal
			
			# If nobody to leach health off, go friend looking
			if len(ZombiesInRoom) == 0:				
				Priorities[0] = 2, 0
			else:
				# Leach health from the a random zombie
				Target = random.choice(ZombiesInRoom)
				self.drainToHeal(Target)
							
		if Priorities[0][0] == 1:
			# We wanna boost
			
			# If nobody to leach health off, go friend looking
			if len(ZombiesInRoom) == 0:				
				Priorities[0] = 2, 0
			
			else:
				# Leach boost from the a random zombie
				Target = random.choice(ZombiesInRoom)
				self.drainToBoost(Target)
				
		if Priorities[0][0] == 2:
			# We wanna find friends
			
			# If nobody left, just plain attack
			if len(AllZombies) == 0:
				Priorities[0] = 4, 0
			else:
				# Find nearest zombie
				moveTo = self.GetNearest(lambda i: len([j for j in self.currentMap.characters if j.team == self.team and j.x == i[0] and j.y == i[1]]) > 0)
				
				# If no route, try to attack
				if moveTo == []:
					Priorities[0] = 4, 0
					
				else:
					moveTo = moveTo[1]
					self.tryMove(moveTo[0], moveTo[1])
			
			
		if Priorities[0][0] == 3:
			# We wanna steal some speed
			# This can only come up randomly, so
			# don't try to go back to looking for friends
			# It should only come up when they're already there
			if len(ZombiesInRoom) > 0:
				Target = random.choice(ZombiesInRoom)
				self.drainToSpeed(Target)
			else:
				Priorities[0] = 4, 0
		
		if Priorities[0][0] == 4:
			# Attack
			moveTo = self.GetRoute((nearestEnemy.x, nearestEnemy.y))
			if moveTo == []:
				moveTo = None
			if moveTo != None:
				moveTo = moveTo[1]
		
			if moveTo == None:
				self.Wait()
			else:
				self.tryMove(moveTo[0], moveTo[1])
		
	def drainToHeal(self, target):
		self.hp += target.hp
		self.maxhp = max(self.maxhp, self.hp)
		target.hp = 0
		self.messageLog.append(Message.Message("The necromancer drains the lifeforce from the zombie"))
		self.messageLog.append(Message.Message("The zombie collapses!"))
		self.animations.append(animation.DrawNecromancerSpell(target, self, 'red'))
		self.ticksUntilTurn += round(100/self.speed)
	
	def drainToSpeed(self, target):
		speedIncrease = min(3, target.speed - 1)
		target.speed -= speedIncrease
		self.speed += speedIncrease
		self.messageLog.append(Message.Message("The necromancer drains speed from the zombie"))
		self.messageLog.append(Message.Message("The zombie stiffens"))
		self.animations.append(animation.DrawNecromancerSpell(target, self, 'green'))
		self.ticksUntilTurn += round(100/self.speed)
	
	def drainToBoost(self, target):
		# Increases damage and ToHit by just increasing the skill of the unarmed weapon
		self.skills[0] = 0, self.skills[0][1] + 2
		self.messageLog.append(Message.Message("The necromancer draws the tormented soul of the zombie into his bony fist"))
		self.messageLog.append(Message.Message("The zombie collapses!"))
		self.animations.append(animation.DrawNecromancerSpell(target, self, 'blue'))
		self.ticksUntilTurn += round(100/self.speed)

	# Special version needed because of the pumping up damage. This is not really what it was intended for, but it saves
	# a lot of programming. This returns the unarmed skill to 0 every hit.
	def RegisterSkillHit(self, skill):
		self.skills[skill] = 0,0

	def Attacked(self, damage, attacker):
		dead = super().Attacked(damage, attacker)
		
		# Kill all zombies!
		if dead:
			self.animations.append(animation.DrawNecromancerDeath(self.x,self.y))
			Zombies = [i for i in self.currentMap.characters if i.chartype == "Zombie"]
			if len(Zombies) > 0:
				for i in Zombies:
					i.hp = 0
				self.messageLog.append(Message.Message("The necromancer explodes into a shower of light"))
				self.messageLog.append(Message.Message("You feel the peace of a thousand lost souls being freed"))
				self.curDanger += i.danger()
			else:
				self.messageLog.append(Message.Message("The necromancer explodes into a shower of light"))
				self.messageLog.append(Message.Message("You feel nothing"))
				
