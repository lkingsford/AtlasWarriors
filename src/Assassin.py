from enemy import *
import random

class Assassin(Enemy):
    def __init__(self, messageLog, currentMap = None):
        super().__init__(messageLog, currentMap)
        self.name = "Assassin"
        self.levelMod = random.choice([-2,-1,0,0,0,0,0,1,1,2])
        self.level = currentMap.level + self.levelMod               
        self.character = "A"        
        self.speed = 15
        self.hp = self.maxhp = round(6 * (max(1,self.level - 3) ** 0.4))
        self.baseDamage =  round(8 * (max(1,self.level - 3) ** 0.2))
        self.baseToHit =  round(10 * (max(1,self.level - 3) ** 0.2))
        self.baseToDefend = round(2 * (max(1,self.level - 3) ** 0.2))
        self.color = "gray"     
        # 0 is normal, 1 is badass, 2 is super-badass
        #
        # Chance of Badass = .10 + 0.04 * level
        # Chance of Superbadass = -0.1 + 0.04 * level
        self.badass = badass = 1 if random.random() < (.10 + 0.04 * currentMap.level) else 2 if random.random() < (-.2 + 0.04 * currentMap.level) else 0
        if (self.badass == 1):
            self.name = "Master Assassin"
            self.hp = self.maxhp = self.hp * 2
            self.baseDamage = self.baseDamage * 2
            self.baseToHit = self.baseToHit * 2
            self.baseToDefend = self.baseToDefend * 2
            self.character = "A"
            self.color = "navy"
        elif (self.badass == 2):
            self.name = "Assassin Mortician"
            self.character = "A"
            self.hp = self.maxhp = self.hp * 4
            self.baseDamage = round(self.baseDamage * 4)
            self.baseToHit = self.baseToHit * 4
            self.baseToDefend = self.baseToDefend * 4
            self.color = "blue"
    
    def danger(self):
        return (2 + self.levelMod/2) * ((self.badass + 1) ** 2) 
    
    def update(self):           
        super().update()
        try:
            nearestEnemy = min([i for i in self.currentMap.characters if i != self and i.team != self.team],
                key = lambda i: abs(self.x - i.x) + abs(self.y - i.y))
            dx = 0 if nearestEnemy.x == self.x else (-1 if nearestEnemy.x < self.x else 1)
            dy = 0 if nearestEnemy.y == self.y else (-1 if nearestEnemy.y < self.y else 1)
            self.tryMove(self.x + dx, self.y + dy)
            
        except ValueError:
            self.Wait()
        self.Wait() 

