from enemy import *
import random
import Message

class Orc(Enemy):
    def __init__(self, messageLog, currentMap = None, badass = -1):
        super().__init__(messageLog, currentMap)
        self.name = "Orc Archer"
        self.levelMod = random.choice([-2,-1,0,0,0,0,0,1,1,2])
        self.level = currentMap.dangerLevel + self.levelMod               
        self.character = "o"        
        self.speed = 10
        self.hp = self.maxhp = round(8 * (max(1,self.level) ** 0.4))
        self.baseDamage =  round(4 * (max(1,self.level) ** 0.2))
        self.baseToHit =  round(4 * (max(1,self.level) ** 0.2))
        self.baseToDefend = round(4 * (max(1,self.level) ** 0.2))
        self.color = "green"        
        
        room1 = room2 = random.choice(self.currentMap.Rooms)
        while room1 == room2:
            room2 = random.choice(self.currentMap.Rooms)
        self.patrolRoute = [(round(room1.w / 2) + room1.x,(round(room1.h / 2) + room1.y)), (round(room2.w / 2) + room2.x,(round(room2.h / 2) + room2.y))]
        self.patrolRouteI = 0       
        self.currentTarget = self.patrolRoute[self.patrolRouteI]
        self.mode = 2
        
        # 0 is normal, 1 is badass, 2 is super-badass
        #
        # Chance of Badass = 0.02 * level
        # Chance of Superbadass = -0.1 + 0.02 * level
        # Chance of Super^2badass = -0.2 + 0.02 * level
        self.badass = badass if badass != -1 else 1 if random.random() < (0.02 * currentMap.level) else 2 if random.random() < (-.1 + 0.02 * currentMap.level) else 3 if random.random() < (-.2 + 0.02 * currentMap.level) else 0
        if (self.badass == 1):
            self.name = "Orc Sharpshooter"
            self.hp = self.maxhp = self.hp * 2
            self.baseDamage = self.baseDamage * 2
            self.baseToHit = self.baseToHit * 2
            self.baseToDefend = self.baseToDefend * 2
            self.character = "O"
            self.color = "lime"
        elif (self.badass == 2):
            self.name = "Orc Mastershooter"
            self.character = "O"
            self.hp = self.maxhp = self.hp * 4
            self.baseDamage = round(self.baseDamage * 4)
            self.baseToHit = self.baseToHit * 4
            self.baseToDefend = self.baseToDefend * 4
            self.color = "yellow"
        elif (self.badass == 3):
            self.name = "Orcish Wararcher"
            self.character = "O"
            self.hp = self.maxhp = self.hp * 8
            self.baseDamage = round(self.baseDamage * 8)
            self.baseToHit = self.baseToHit * 8
            self.baseToDefend = self.baseToDefend * 8
            self.color = "red"
        
        self.runAwayAt = (self.maxhp / random.choice([3,4,5]))
        
    def danger(self):
        return (4 + self.levelMod/2) * ((self.badass + 1) ** 2) 
    
    # Borrowed from http://www.roguebasin.com/index.php?title=Bresenham%27s_Line_Algorithm#Python
    # If this is needed elsewhere, then I'll move it out of here

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

    # Returns the end result line, if hits a wall or obstacle
    def GetFiringLine(self, target):
        path = self.get_line(self.x, self.y, target.x, target.y)
        for i in path[1:]:
            if not self.currentMap.Walkable(i):
                path = path[:path.index(i)+1]
                break
                
        for i in path[1:]:
            if not self.currentMap.Walkable(i):
                path = path[:path.index(i)+1]
                break       
        
        return path
        
    def FireArrow(self, target):
        path = self.GetFiringLine(target)
        self.animations.append(animation.DrawArrowAnimation(path))
        
        CharacterHit = [i for i in self.currentMap.characters if (i.x == path[-1][0]) and (i.y == path[-1][1])]
        distance = len(path)
        # To be balanced
        toHit = round(self.baseToHit - distance / 2)
        toDamage = round(self.baseDamage - distance / 3)
        for i in CharacterHit:
            chanceToHit = self.ChanceToHit(toHit, i.ToDefend())
            chanceToCrit = self.ChanceToCrit(toHit, i.ToDefend()) 
            hit = random.random() < chanceToHit
            crit = random.random() < chanceToCrit
            if hit:
                damage = toDamage * (self.CritMult() if crit else 1)
                i.Attacked(damage, self, False)
                if crit:
                    self.messageLog.append(Message.Message(self.name + " fires at " + i.name + " and crits! (" + str(i.hp) + ")",[(self.x, self.y),(i.x,i.y)]));
                else:
                    self.messageLog.append(Message.Message(self.name + " fires at " + i.name+ "  and hits! (" + str(i.hp) + ")",[(self.x, self.y),(i.x,i.y)]));
                if (i.dead()):
                    self.messageLog.append(Message.Message(i.name + " has been killed!",[(i.x,i.y)]));
                    self.Killed(i)
            else:
                self.messageLog.append(Message.Message(self.name + " fires at " + i.name+ "  but misses", [(self.x, self.y),(i.x,i.y)]))
        
        # This will make firing quicker for higher level characters. Needs balancing.
        if self.badass == 0:
            timeToShoot = 100
        elif self.badass == 1:
            timeToShoot = 75
        elif self.badass == 2:
            timeToShoot = 50
        elif self.badass == 3:
            timeToShoot = 30
        self.ticksUntilTurn = round(timeToShoot/self.speed)


    def update(self):           
        # At the moment, Orcs don't seem to do any melee at all. They need
        # to be worked on, but they're OK
        
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
            
        # CanFire is if there is a firing line to an enemy      
        CanFire = False
        
        moveTo = None
        activateTeam = False
        # This update is in two parts.
        # The first picks if a mode needs to change
        # The second is to performs its action
        
        if self.mode == 0:
            #print ("self.mode == 0")
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
            #print ("self.mode == 2")
            if len(inRoom) > 0:
                self.mode = 1   
                
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
            #print ("self.mode == 1")
            # Active. We want to be in the same room as the enemy, but at least 2 away
            # Ideally, this would take into account positioning to ensure a 
            # 'shooting solution'
            # 
            if len(inRoom) > 0:
                nearestEnemy = min([i for i in inRoom if i != self and i.team != self.team],\
                    key = lambda i: abs(self.x - i.x) + abs(self.y - i.y))\
            
            moveTo = self.GetNearest(lambda i: ((max(abs(i[0]-nearestEnemy.x),abs(i[1]-nearestEnemy.y))) >= 2)\
                and (len(self.currentMap.Map[nearestEnemy.x][nearestEnemy.y].rooms & self.currentMap.Map[i[0]][i[1]].rooms) > 0), True)
            
            if moveTo == []:
                # If no suitable route, try to move towards enemy
                moveTo = self.GetRoute((nearestEnemy.x, nearestEnemy.y))
                
            if moveTo == []:                
                moveTo = None
            
            if moveTo != None and len(moveTo) == 1:             
                # == Positioning is good
                # If more then 1 away, check if there is a line to fire
                if max(abs(self.x-nearestEnemy.x),abs(self.x-nearestEnemy.y)) > 1:
                    hits = self.GetFiringLine(nearestEnemy)[-1]
                    CharacterHit = [i for i in self.currentMap.characters if (i.x == hits[0]) and (i.y == hits[1]) and i.team != self.team]
                    if len(CharacterHit) > 0:
                        CanFire = True
                        #print ("CanFire = True")
                    else:
                        # Try to reposition by moving towards enemy
                        moveTo = self.GetRoute((nearestEnemy.x, nearestEnemy.y))
                        if moveTo == []:                
                            moveTo = None
                        else:
                            moveTo = moveTo[1]
                # Otherwise, we'll hopefully get some melee action by the moveTo doing its thing
            elif moveTo != None:
                # == Positioning is not good, but moving is
                moveTo = moveTo[1]              
            
            if self.hp < self.runAwayAt:
                moveTo = self.GetNearest(lambda i: (max(abs(i[0]-nearestEnemy.x),abs(i[1]-nearestEnemy.y))) > 5)
                if moveTo == []:
                    self.messageLog.append(Message.Message(self.name + " turns to run away but is blocked!",[(self.x, self.y)]))
                else:
                    self.messageLog.append(Message.Message(self.name + " turns to run away!",[(self.x, self.y)]))
                    self.mode = 3
                
        
        if self.mode == 3:
            #print ("self.mode == 3")
            # Try to run away
            
            # This might be better as a max function rather then a find first which satisfies,
            # but I'm concerned about speed
            moveTo = self.GetNearest(lambda i: (max(abs(i[0]-nearestEnemy.x),abs(i[1]-nearestEnemy.y))) > 4)
            if moveTo == []:
                moveTo = None

            if moveTo == None:              
                # See if can fire
                # Check if there is a line to fire
                hits = self.GetFiringLine(nearestEnemy)[-1]
                CharacterHit = [i for i in self.currentMap.characters if (i.x == hits[0]) and (i.y == hits[1]) and i.team != self.team]
                if len(CharacterHit) > 0:
                    CanFire = True
            else:
                moveTo = moveTo[1]
                
            if max(abs(self.x-nearestEnemy.x),abs(self.y-nearestEnemy.y)) > 3:
                # If far enough away, try to shoot
                hits = self.GetFiringLine(nearestEnemy)[-1]
                CharacterHit = [i for i in self.currentMap.characters if (i.x == hits[0]) and (i.y == hits[1]) and i.team != self.team]
                if len(CharacterHit) > 0:
                    CanFire = True
                        
        if CanFire:
            self.FireArrow(nearestEnemy)
        elif moveTo == None:
            # Last ditch passthrough (code shouldn't be here!) - if not gonna
            # move, and enemy adjacent, melee them
            if max(abs(self.x-nearestEnemy.x),abs(self.x-nearestEnemy.y)) == 1:
                self.tryMove(nearestEnemy.x, nearestEnemy.y)
            else:
                self.Wait()
        else:
            # BUGGYBIT00
            if len(moveTo) == 1:
                moveTo = moveTo[0]
            if len(moveTo) > 1:
                #print ("mt:")
                #print (moveTo)
               #print (len(moveTo))
                self.tryMove(moveTo[0], moveTo[1])
            else:
                self.Wait()
                    
