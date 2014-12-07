from enemy import *
import random
import Message

class Critter(Enemy):
    def __init__(self, messageLog, currentMap = None):
        super().__init__(messageLog, currentMap)
        self.name = "Critter"
        self.levelMod = random.choice([-2,-1,0,0,0,0,0,1,1,2])
        self.level = currentMap.dangerLevel + self.levelMod              
        self.character = "c"        
        self.speed = 15
        self.hp = self.maxhp = round(4 * (max(1,self.level)) ** 0.4)
        self.baseDamage =  round(3 * (max(1,self.level)) ** 0.2)
        self.baseToHit =  round(2 * (max(1,self.level)) ** 0.2)
        self.baseToDefend = round(1 * (max(1,self.level)) ** 0.2)
        self.color = "silver"       
        # 0 is normal, 1 is badass, 2 is super-badass
        #
        # Chance of Badass = .10 + 0.01 * level
        # Chance of Superbadass = -0.2 + 0.01 * level
        self.badass = badass = 1 if random.random() < (.10 + 0.01 * currentMap.level) else 2 if random.random() < (-.2 + 0.04 * currentMap.level) else 0
        if (self.badass == 1):
            self.name = "Feral Critter"
            self.hp = self.maxhp = self.hp * 2
            self.baseDamage = self.baseDamage * 2
            self.baseToHit = self.baseToHit * 2
            self.baseToDefend = self.baseToDefend * 2
            self.color = "yellow"
        elif (self.badass == 2):
            self.name = "Indomitable Critter"
            self.character = "C"
            self.hp = self.maxhp = self.hp * 4
            self.baseDamage = round(self.baseDamage * 4)
            self.baseToHit = self.baseToHit * 4
            self.baseToDefend = self.baseToDefend * 4
            self.color = "red"
        self.foundEnemy = None
    
    def danger(self):       
        return (1.5 + self.levelMod/2) * ((self.badass+1) ** 2) 
    
    def update(self):           
        super().update()
        try:
            nearestEnemy = min([i for i in self.currentMap.characters if i != self and i.team != self.team],
                key = lambda i: abs(self.x - i.x) + abs(self.y - i.y))
            dx = 0 if nearestEnemy.x == self.x else (-1 if nearestEnemy.x < self.x else 1)
            dy = 0 if nearestEnemy.y == self.y else (-1 if nearestEnemy.y < self.y else 1)
            monsterInSquare = [i for i in self.currentMap.characters if (i.x == self.x+dx) and (i.y == self.y+dy) and (i.team != self.team)]
            if len(monsterInSquare) > 0:
                self.tryMove(self.x + dx, self.y + dy)
            elif self.currentMap.Walkable((self.x + dx, self.y + dy)):
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

