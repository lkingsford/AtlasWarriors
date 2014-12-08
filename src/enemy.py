#base enemy
import character
import animation
import math
import itertools
import random
import Message

class Enemy(character.Character):           
    def __init__(self,  messageLog, currentMap):
        super(Enemy, self).__init__(messageLog, currentMap)
        self.minLevel = 0
        self.baseDanger = 1
        self.minGroup = 1
        self.team = 1;
        self.character = "e"
        self.name = "Enemy" 
        self.maxmp = 0
        self.mp = 0
        self.mpChargeRate = 0
        self.mpAcc = 0
        self.ai = "Basic"
        self.FlameReady = None
        self.State = None
        self.Target = None
    
    def update(self):
        super().update()        
        if self.mp < self.maxmp:
            self.mpAcc += self.mpChargeRate
            if self.mpAcc >= 1:
                self.mp += round(self.mpAcc)
                self.mpAcc -= round(self.mpAcc)
                self.mp = min(self.mp, self.maxmp)
    
    def BasicUpdate(self):
        try:
            nearestEnemy = min([i for i in self.currentMap.characters if i != self and i.team != self.team],
                key = lambda i: abs(self.x - i.x) + abs(self.y - i.y))
            dx = 0 if nearestEnemy.x == self.x else (-1 if nearestEnemy.x < self.x else 1)
            dy = 0 if nearestEnemy.y == self.y else (-1 if nearestEnemy.y < self.y else 1)
            self.tryMove(self.x + dx, self.y + dy)
            
        except ValueError:
            self.Wait()
            
        
    # Returns something that resembles the risk of dying in this turn. Essentially, how dangerous the place it.
    def GetRoomDanger(self):
        EnemiesInRoom = [i for i in self.currentMap.characters if i.team != self.team\
            and len([j for j in self.currentMap.GetRooms(i.x, i.y)\
            if j in self.currentMap.GetRooms(self.x, self.y)]) > 0]
            
        if len(EnemiesInRoom) > 0:
            # Calculate enemies average damage per hit to dragon
            try:
                return sum(map(lambda i: i.GetAverageDamage(self.ToDefend(), 
                    self.level)/max(abs(i.x - self.x ),abs(i.y-self.y)), 
                    EnemiesInRoom))/max(1,self.hp)
            except ZeroDivisionError:
                return 1
        else:
            return 0
        
    def CastHeal(self, target):
        self.mp -= 3
        target.hp += self.level+1
        target.hp = min(target.hp, target.maxhp)
        if self != target:
            self.messageLog.append(Message.Message(self.name + " heals " + target.name, [(self.x, self.y),(target.x, target.y)]))
        else:
            self.messageLog.append(Message.Message(self.name + " heals himself", [(self.x, self.y)]))
        self.ticksUntilTurn = round(200/self.speed)
        self.animations.append(animation.HealAnimation((target.x, target.y)))
        
        
    def PrepareFlameBreath(self, target, radius, distance):
        self.ticksUntilTurn = round(200/self.speed)
        self.FlameReady = (target, radius, distance)

    def FlameBreathMPCost(self, radius, distance):
        return radius * distance // 2

    def CastFlameBreath(self, target, radius, distance):
        self.mp -= self.FlameBreathMPCost(radius, distance)
            
        #Draw animation
        self.messageLog.append(Message.Message(self.name + " breathes burning flame", [(self.x, self.y)]))
        frames = []
        for i in range(distance):
            frames.append(self.CastFlame_(self.x, self.y, target[0], target[1], radius, i))
        self.animations.append(animation.DragonsBreathAnimation((self.x, self.y), frames))
        grid = self.CastFlame_(self.x, self.y, target[0], target[1], radius, i)
        width  = len(grid)
        height = len(grid[0])
        for i in range( (width//2) * -1, width // 2):
            for j in range ( (height//2) * -1, height // 2):
                windowWidth = len(self.currentMap.Map)
                windowHeight = len(self.currentMap.Map[0])
                if (self.x + i > 0) and (self.x + i < windowWidth) and (self.y + j > 0) and (self.y + j < windowHeight):
                    x = self.x + i
                    y = self.y + j
                    #print (x, y)
                    monsterInSquare = [l for l in self.currentMap.characters if (l.x == x) and (l.y == y)]
                    for k in monsterInSquare:                       
                        if k != self:       
                            #rint ("BURN CHECK: ", x, y, grid[i][j], k.name)
                            igniteResult = \
                                k.Ignite(max(.1, grid[i][j] - \
                                (0 if (k.leftHandEquipped == None) or (k.leftHandEquipped.ItemClass != 6) else k.leftHandEquipped.ToDefend) - \
                                (0 if (k.rightHandEquipped == None) or (k.rightHandEquipped.ItemClass != 6) else k.rightHandEquipped.ToDefend)), self.burnDamage, self)
                            #print (str(max(.1, grid[i][j] - \
                            #   (0 if (k.leftHandEquipped == None) or (k.leftHandEquipped.ItemClass != 6) else k.leftHandEquipped.ToDefend) - \
                            #   (0 if (k.rightHandEquipped == None) or (k.rightHandEquipped.ItemClass != 6) else k.rightHandEquipped.ToDefend))) + "%")
                            if igniteResult[0]:
                                self.messageLog.append(Message.Message(k.name + " is ignited by the scorching flame!", [(self.x, self.y),(k.x, k.y)]))
                            if igniteResult[1]:
                                self.messageLog.append(Message.Message(k.name + " has been prematurely cremated!", [(self.x, self.y),(k.x, k.y)]))
                                self.Killed(k)
        self.ticksUntilTurn = round(100/self.speed)
        
    def CastFlame_(self, sx, sy, tx, ty, radius, distance):
        grid = [[0]*(2*round(distance)+1) for i in range(2*round(distance) + 1)]
        angle = math.atan2(ty - sy, tx - sx)
        invangle = angle + math.pi/2
        endx = math.sin(angle) * distance
        endy = math.cos(angle) * distance                                       
        
    
        angles = []
        #print ('-', angle, '-')
        for i in range(round(radius) * -1, round (radius)):
            nextEndX = endx + math.sin(invangle) * i
            nextEndY = endy + math.cos(invangle) * i
            #print ("End: ", nextEndX, nextEndY)
            angles.append(math.atan2(nextEndY, nextEndX))       
        
        for i in angles:        
            #print (i)
            for j in range(1,round(distance)):
                x = math.sin(i) * j
                y = math.cos(i) * j
                
                xpart, xint = math.modf(x - 0.5)
                ypart, yint = math.modf(y - 0.5)
                xint = int(xint)
                yint = int(yint)
                
                if (not(self.currentMap.Map[round(sx+xint)][round(sy+yint)].walkable)):
                    break;
                
                xpart = xpart + 1 if xpart < 0 else xpart
                ypart = ypart + 1 if ypart < 0 else ypart
                                
                if(self.currentMap.Map[round(sx)+xint][round(sy)+yint].walkable):
                    grid[xint][yint] = grid[xint][yint] + xpart / 8 + ypart / 8
                if(self.currentMap.Map[round(sx)+xint+1][round(sy)+yint].walkable):
                    grid[xint + 1][yint] = grid[xint + 1][yint] + (1 - xpart) / 8 + ypart / 8
                if(self.currentMap.Map[round(sx)+xint+1][round(sy)+yint+1].walkable):
                    grid[xint + 1][yint + 1] = grid[xint + 1 ][yint + 1] + (1 - xpart) / 8 + (1 - ypart) / 8
                if(self.currentMap.Map[round(sx)+xint][round(sy)+yint+1].walkable):
                    grid[xint][yint + 1] = grid[xint][yint + 1] + xpart / 8 + (1 - ypart) / 8
                                
        grid[0][0] = 0              
            
        return grid

    
