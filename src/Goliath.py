from enemy import *
import random
import Message
import animation

class Goliath(Enemy):
    def __init__(self, messageLog, currentMap = None, badass = -1):
        super().__init__(messageLog, currentMap)
        self.name = "Goliath"
        self.levelMod = random.choice([-2,-1,0,0,0,0,0,1,1,2])
        self.level = currentMap.dangerLevel + self.levelMod               
        self.character = "g"        
        self.speed = 7
        self.hp = self.maxhp = self.starthp = round(20 * (max(1,self.level - 2) ** 0.4))
        self.baseDamage = self.startDamage = round(6 * (max(1,self.level - 2) ** 0.2))
        self.baseToHit =  round(9 * (max(1,self.level - 3)  ** 0.2))
        self.baseToDefend = round(7 * (max(1,self.level - 3) ** 0.2))
        self.color = "silver"
        self.baseXPToLevel = 8
        if badass != -1:
            self.badass = badass 
        else:
            self.badass = 0
            if currentMap.dangerLevel  <= 5:
                self.badass = badass if badass != -1 else 0
            if currentMap.dangerLevel > 5:
                if random.random() < 0.3:
                    self.LevelUp(True)
            if currentMap.dangerLevel > 6:
                if random.random() < 0.3:
                    self.LevelUp(True)
            if currentMap.dangerLevel > 7:
                if random.random() < 0.3:
                    self.LevelUp(True)
            if currentMap.dangerLevel > 8:
                if random.random() < 0.3:
                    self.LevelUp(True)
        
        self.team = 2
        self.chartype = "Goliath"
        self.charging = False
        
    def danger(self):
        return (1 + self.levelMod/2) * ((self.badass + 1) ** 2) 
    
    def SuperPunch(self, target):
        # Firstly, this (like an ordinary attack) needs to either hit, crit or miss
        # with the same consequences. This is basically an ordinary attack with
        # forceful consequences
        
        #Calculate odds to hit
        chanceToHit = self.ChanceToHit(self.baseToHit, target.ToDefend())
        chanceToCrit = self.ChanceToCrit(self.baseToHit, target.ToDefend()) 
        hit = random.random() < chanceToHit
        crit = random.random() < chanceToCrit       
        if hit:
            damage = self.Damage() * self.GetDamageMultiplier(self.level - target.level) * (self.CritMult() if crit else 1)                 
            dead = target.Attacked(damage, self)
            route = [(target.x, target.y)]
            if crit:
                self.messageLog.append(Message.Message(self.name + " crits " + target.name + " (" + str(target.hp) + ")"));
            else:
                self.messageLog.append(Message.Message(self.name + " attacks " + target.name+ " (" + str(target.hp) + ")"));

            if dead:
                self.Killed(target)
                self.messageLog.append(Message.Message(self.name + " was killed by the blow"))
            # This dx/dy is opposite the update() version - dx and dy are the direction the target
            # is being punched in
            dx = 0 if target.x == self.x else (1 if target.x > self.x else -1)
            dy = 0 if target.y == self.y else (1 if target.y > self.y else -1)
            # print(dx,' ', dy)
            force = self.badass + 3
            while force > 0:
                newX = target.x + dx
                newY = target.y + dy
                if self.currentMap.Walkable((newX, newY)):
                    target.x = newX
                    target.y = newY
                    force -= 1
                    route.append([newX, newY])
                    self.currentMap.Map[newX][newY].OnWalk(target)
                    target.UpdateVisibility();
                else:
                    # Find if collided with wall or enemy
                    enemiesInSquare = [i for i in self.currentMap.characters if (i.x == newX and i.y == newY)]
                    if len(enemiesInSquare) > 0:
                        # Collided with enemy
                        for i in enemiesInSquare:
                            self.messageLog.append(Message.Message(target.name + " crashes into " + i.name));
                            dead = i.Attacked(force, self, False)  
                            if dead:
                                self.messageLog.append(Message.Message(i.name + " was killed by the impact"));
                                self.Killed(i)
                        if not(dead):
                            dead = target.Attacked(force, self, False)
                            if dead:
                                self.Killed(target) 
                                self.messageLog.append(Message.Message(target.name + " was killed by the impact"));
                            
                    else:
                        # Collided with wall
                        self.messageLog.append(Message.Message(target.name + " crashes into the wall"));
                        dead = target.Attacked(force, self, False) 
                        if dead:
                            self.Killed(target)
                            self.messageLog.append(Message.Message(target.name + " was killed by the impact"));
                    force = 0
            self.animations.append(animation.BigPunchAnimation(route, target))
            
        else:
            target.Missed(self.baseToHit, self)
            
    def GetNearest(self, destLogic, startingPointAllowed = False):
        # Performs Dijkstra's algorithm to find nearest square resulting in destLogic = True
        # destLogic has to take a tuplet of (x,y) as input and return a boolean as output
        #
        # Starting Point Allowed allows the alogithm to recognise the initial x y as a valid answer
        
        # As above in GetRoute
        ORTH_DISTANCE = 10
        DIAG_DISTANCE = 10
        
        Found = None
            
        # Check starting point. If it is, then return it and skip the rest
        if startingPointAllowed:
            if destLogic((self.x, self.y)):
                return [(self.x, self.y)]               
                
        # OpenLists consists of tuplets with (
        #   [0]: Position.x, 
        #   [1]: Position.y,
        #   [2]: ParentPosition.x, 
        #   [3]: ParentPosition.y,
        #   [4]: g (distance to get here from parent)
        
        OpenList = [(self.x, self.y, self.x, self.y, 0)]        
        ClosedList = []
        while (len(OpenList) > 0 and Found == None):                
            # Find entry in OpenList with lowest G score
            Current = min(OpenList, key=lambda i:i[4])          
            OpenList.remove(Current)
            ClosedList.append(Current)
            Active = [(Current[0] - 1,  Current[1],     Current[0], Current[1], Current[4] + ORTH_DISTANCE),
                (Current[0] + 1,    Current[1],     Current[0], Current[1], Current[4] + ORTH_DISTANCE),
                (Current[0] - 1,    Current[1] - 1, Current[0], Current[1], Current[4] + DIAG_DISTANCE),
                (Current[0] + 1,    Current[1] - 1, Current[0], Current[1], Current[4] + DIAG_DISTANCE),
                (Current[0] - 1,    Current[1] + 1, Current[0], Current[1], Current[4] + DIAG_DISTANCE),
                (Current[0] + 1,    Current[1] + 1, Current[0], Current[1], Current[4] + DIAG_DISTANCE),
                (Current[0],        Current[1] - 1, Current[0], Current[1], Current[4] + ORTH_DISTANCE),
                (Current[0],        Current[1] + 1, Current[0], Current[1], Current[4] + ORTH_DISTANCE)]
            for i in Active:
                # If point not in closed list and is walkable
                if (len([j for j in ClosedList if j[0] == i[0] and j[1] == i[1]]) == 0) and self.currentMap.Walkable(i, True):
                    # Look for point in open List
                    Candidate = [j for j in OpenList if j[0] == i[0] and j[1] == i[1]]
                    # If point not in open list                 
                    if(len(Candidate) == 0):
                        # Add point to the open list
                        OpenList.append(i)
                        #print ("Check ", i)
                        #print (destLogic(i))
                        #print ([j for j in self.currentMap.characters if (j.x == i[0]) and (j.y == i[1])])
                        if destLogic(i):
                            Found = i
                            #print("Found")                         
                    else:
                        # Otherwise, check to see if this path to the square is shorter, using G. If so, replace square with current route (changing parent and g) 
                        if Candidate[0][4] > i[4]:
                            OpenList.remove(Candidate[0])
                            OpenList.append(i)
            

                
        # If no path found, return empty route
        if Found == None:
            return []
        else:
            # Add path to route             
            CurSquare = Found
            Route = [CurSquare]
            # Iterate until we reach the starting point
            while (not(CurSquare[0] == CurSquare[2] and CurSquare[1] == CurSquare[3])):                 
                CurSquare = [j for j in (OpenList+ClosedList) if j[0] == CurSquare[2] and j[1] == CurSquare[3]][0]
                Route.insert(0, CurSquare)
            return Route    
    
    def update(self):           
        super().update()
        try:
            nearestEnemy = min([i for i in self.currentMap.characters if i != self and i.team != self.team],
                key = lambda i: abs(self.x - i.x) + abs(self.y - i.y))
            dx = 0 if nearestEnemy.x == self.x else (-1 if nearestEnemy.x < self.x else 1)
            dy = 0 if nearestEnemy.y == self.y else (-1 if nearestEnemy.y < self.y else 1)
            #print (nearestEnemy)               
            if max(abs(nearestEnemy.x - self.x), abs(nearestEnemy.y - self.y)) == 1:
                self.SuperPunch(nearestEnemy)
            else:
                if self.currentMap.Walkable((self.x + dx, self.y + dy)):
                    self.tryMove(self.x + dx, self.y + dy)
                elif self.currentMap.Walkable((self.x + dx, self.y)) and dx != 0:
                    self.tryMove(self.x + dx, self.y)
                elif self.currentMap.Walkable((self.x, self.y+dy)) and dy != 0:
                    self.tryMove(self.x, self.y + dy)
                else:
                    self.Wait()
                
        except ValueError:
            self.Wait()
            return
            
        #self.Wait()    

    def LevelUp(self, suppress = False):
        super().LevelUp(suppress)
        if self.badass == 0:
            self.badass += 1
            self.name = "Enraged Goliath"
            self.color = "yellow"
            self.speed = 6
        elif self.badass == 1:
            self.badass += 1
            self.name = "Badass Goliath"
            self.color = "yellow"
            self.character = "G"
            self.speed = 7
        elif self.badass == 2:
            self.badass += 1
            self.name = "Super Badass Goliath"
            self.color = "red"
            self.character = "G"
            self.speed = 8
        elif self.badass == 3:
            self.badass += 1
            self.name = "Ultimate Badass Goliath"
            self.color = "fuchsia"
            self.speed = 9
        elif self.badass == 4:
            self.badass += 1
            self.name = "Godliath"
            self.color = "green"
            self.speed = 10
        elif self.badass == 5:
            self.badass += 1
            self.name = "Unholy Godliath"
            self.color = "lime"
            self.speed = 11
        elif self.badass == 6:
            self.badass += 1
            self.name = "Most Unholy Godliath"
            self.color = "navy"
            self.speed = 12         
        elif self.badass == 8:
            self.badass += 1
            self.name = "Demonic Godliath"
            self.color = "blue"
            self.speed = 13
        elif self.badass == 9:
            self.badass += 1
            self.name = "Apocolyptic Godliath"
            self.color = "white"
            self.messageLog.append(Message.Message("The Godliath seems to have ascended"))
            self.messageLog.append(Message.Message("You suddenly realise this is tremendously bad"))
            self.speed = 15                        
            
        self.hp = self.maxhp = self.starthp * (1.1 ** self.badass)
        self.baseDamage = self.startDamage * (1.3 ** self.badass)
