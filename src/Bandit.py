from enemy import *
import random
import Message
import copy

class Bandit(Enemy):
    def __init__(self, messageLog, currentMap = None, badass = -1):
        super().__init__(messageLog, currentMap)
        self.name = "Bandit"
        self.levelMod = random.choice([-2,-1,0,0,0,0,0,1,1,2])
        self.level = currentMap.level + self.levelMod               
        self.character = "b"        
        self.speed = 15
        self.hp = self.maxhp = round(5 * (max(1,self.level) ** 0.4))
        self.baseDamage =  round(3 * (max(1,self.level) ** 0.2))
        self.baseToHit =  round(4 * (max(1,self.level) ** 0.2))
        self.baseToDefend = round(2 * (max(1,self.level) ** 0.2))
        self.color = "silver"       
                        
        # 0 is normal, 1 is badass, 2 is super-badass
        #
        # Chance of Badass = 0.02 * level
        # Chance of Superbadass = -0.1 + 0.02 * level
        # Chance of Super^2badass = -0.2 + 0.02 * level
        self.badass = badass if badass != -1 else 1 if random.random() < (0.02 * currentMap.level) else 2 if random.random() < (-.1 + 0.02 * currentMap.level) else 3 if random.random() < (-.2 + 0.02 * currentMap.level) else 0
        if (self.badass == 1):
            self.name = "Experienced Bandit"
            self.hp = self.maxhp = self.hp * 2
            self.baseDamage = self.baseDamage * 2
            self.baseToHit = self.baseToHit * 2
            self.baseToDefend = self.baseToDefend * 2
            self.character = "B"
            self.color = "yellow"
        elif (self.badass == 2):
            self.name = "Veteran Bandit"
            self.character = "B"
            self.hp = self.maxhp = self.hp * 4
            self.baseDamage = round(self.baseDamage * 4)
            self.baseToHit = self.baseToHit * 4
            self.baseToDefend = self.baseToDefend * 4
            self.color = "red"
        elif (self.badass == 3):
            self.name = "Bandit Warlord"
            self.character = "B"
            self.hp = self.maxhp = self.hp * 8
            self.baseDamage = round(self.baseDamage * 8)
            self.baseToHit = self.baseToHit * 8
            self.baseToDefend = self.baseToDefend * 8
            self.color = "fuchsia"
        
        # Choose some weapons, and maybe a shield
        # Choose weapon. 
        # weaponType = random.choice([1,2,3,4,5])
    
        if self.level < 3:
            weapon = random.choice([1,2,3,4,5])
            shieldEquipped = random.random() < .1
            if shieldEquipped:
                shield = 5
                
        elif self.level < 5:
            weapon = random.choice([1,2,3,4,5,7,11,16,17,19,24])
            shieldEquipped = random.random() < .3
            if shieldEquipped:
                shield = random.choice([5,30])
        else:
            weapon = random.choice([1,2,3,4,5,7,11,16,17,19,24, 8, 12, 21,28])
            shieldEquipped = random.random() < .5
            if shieldEquipped:
                shield = random.choice([5,30,31,32])
        
        self.rightHandEquipped = copy.deepcopy([i for i in self.currentMap.defaultItems if i.ID == weapon][0])
        if shieldEquipped:
            self.leftHandEquipped = copy.deepcopy([i for i in self.currentMap.defaultItems if i.ID == shield][0])
            
        # Mode 0 is inactive
        # Mode 1 is active
        # Mode 2 is on patrol
        # Mode 3 is running away
        # Mode 4 is berserk. If health is extremely low, go nuts and
        #        just rush attack. Will also berserk if all exits
        #    are blocked
         
        self.mode = random.choice([0,0,0,2])
        
        room1 = room2 = random.choice(self.currentMap.Rooms)
        while room1 == room2:
            room2 = random.choice(self.currentMap.Rooms)
        self.patrolRoute = [(round(room1.w / 2) + room1.x,(round(room1.h / 2) + room1.y)), (round(room2.w / 2) + room2.x,(round(room2.h / 2) + room2.y))]
        self.patrolRouteI = 0       
        self.currentTarget = self.patrolRoute[self.patrolRouteI]
        
        
        self.runAwayAt = (self.maxhp / 4) * random.choice([0,1,2])      
        
        self.teamMates = []
    
    def danger(self):
        return (2 + self.levelMod/2) * ((self.badass + 1) ** 2) 
    
    def update(self):           
        super().update()
        
        # Nearest enemy is naive and is simply approximate - I don't use pathfinding
        enemies = [i for i in self.currentMap.characters if i != self and i.team != self.team]
        if len(enemies)>0:
            nearestEnemy = min(enemies,
                    key = lambda i: abs(self.x - i.x) + abs(self.y - i.y))
        else:
            self.Wait()
            return
        
        # Find if any enemies in room
        # This could be an eloquent one liner, but I think that this is actually more clear
        #
        # I think this is a slow(ish) chunk of code but it's better then it used to be...
        myRooms = self.currentMap.GetRooms(self.x, self.y)
        inRoom = [i for i in self.currentMap.characters\
            if (i.team != self.team) and\
            len(self.currentMap.Map[self.x][self.y].rooms & self.currentMap.Map[i.x][i.y].rooms) > 0]
            
    
        moveTo = None
        activateTeam = False
        # This update is in two parts.
        # The first picks if a mode needs to change
        # The second is to performs its action
        
        if self.mode == 0:
            # Inactive. Do nothing unless enemy moves into room,
            # in which case go active
            if len(inRoom) > 0:
                self.mode = 1
            else:
                moveTo = None
        
        # NOTE: No elif - just if. I want to go active straight away if 
        # located
        if self.mode == 2:
            # Walk from the centre of room1 to the centre of room2.
            # If an enemy is found, blow whistle to make all teammates active
            # and go active
            
            if len(inRoom) > 0:
                self.mode = 1
                activateTeam = True
                
            else:
                if self.x == self.currentTarget[0] and self.y == self.currentTarget[1]:
                    # Swap targets
                    self.patrolRouteI += 1
                    self.currentTarget = self.patrolRoute[self.patrolRouteI % len(self.patrolRoute)]
                    
                #print (self.x, ' ', self.y, '    ', self.currentTarget)
                moveTo = self.GetRoute(self.currentTarget)
                #print (moveTo)
                if moveTo == []:
                    moveTo = None
                if moveTo != None:
                    moveTo = moveTo[1]
        
        if self.mode == 1:
            # Active. Move towards nearest enemy.
            if len(inRoom) > 0:
                nearestEnemy = min([i for i in inRoom if i != self and i.team != self.team],\
                    key = lambda i: abs(self.x - i.x) + abs(self.y - i.y))
            
            moveTo = self.GetRoute((nearestEnemy.x, nearestEnemy.y))
            if moveTo == []:
                    moveTo = None
            if moveTo != None:
                moveTo = moveTo[1]
            
            if self.hp < self.runAwayAt:
                moveTo = self.GetNearest(lambda i: (max(abs(i[0]-nearestEnemy.x),abs(i[1]-nearestEnemy.y))) > 5)
                if moveTo == []:
                    self.mode = 4
                    self.messageLog.append(Message.Message(self.name + " turns to run away but is blocked!"))
                    self.messageLog.append(Message.Message(self.name + " decides to fight for his life!"))
                else:
                    self.messageLog.append(Message.Message(self.name + " turns to run away!"))
                    self.mode = 3
                
        
        if self.mode == 3:
            # Try to run away
            if self.hp < 3:
                self.mode = 4
                self.messageLog.append(Message.Message(self.name + " decides to fight for his life!"))
            
            # This might be better as a max function rather then a find first which satisfies,
            # but I'm concerned about speed
            moveTo = self.GetNearest(lambda i: (max(abs(i[0]-nearestEnemy.x),abs(i[1]-nearestEnemy.y))) > 5)
            if moveTo == []:
                moveTo = None
            # Go nuts if can't run away
            
            if moveTo == None:
                self.mode = 4
                self.messageLog.append(Message.Message(self.name + " decides to fight for his life!"))
            else:
                moveTo = moveTo[1]
        
        if self.mode == 4:
            # Go nuts. Just try to kill.
            if len(inRoom) > 0:
                nearestEnemy = min([i for i in inRoom if i != self and i.team != self.team],\
                    key = lambda i: abs(self.x - i.x) + abs(self.y - i.y))
                
            moveTo = self.GetRoute((nearestEnemy.x, nearestEnemy.y))
            if moveTo == []:
                moveTo = None
            if moveTo != None:
                moveTo = moveTo[1]
        
        if moveTo == None:
            self.Wait()
        else:
            if len(moveTo) > 0:
                self.tryMove(moveTo[0], moveTo[1])
            else:
                self.Wait()
        
        if activateTeam:
            activateTeam = False
            self.messageLog.append(Message.Message(self.name + " loudly blows a tiny whistle!"))
            for i in self.teamMates:
                i.mode = 1
                    

