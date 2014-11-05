from enemy import *
from Dragon import *
import Message

# The dragon is a special and unique enemy, hence these values are hardcoded

class Drake(Dragon):
    def __init__(self, messageLog, currentMap = None):
        super().__init__(messageLog, currentMap)
        self.name = "Drake"
        self.levelMod = random.choice([-2,-1,0,0,0,0,0,1,1,2])
        self.level = currentMap.level + self.levelMod
        self.character = "d"        
        self.speed = 10
        self.hp = self.maxhp = round(12 * (max(1,self.level - 4) ** 0.4))
        self.mp = self.maxmp = round(8 * (max(1,self.level - 4) ** 0.4))
        self.mpChargeRate = 1
        self.baseDamage =  round(6 * (max(1,self.level - 4) ** 0.2))
        self.baseToHit =  round(8 * (max(1,self.level - 4) ** 0.2))
        self.baseToDefend = round(4 * (max(1,self.level - 4) ** 0.2))
        self.burnDamage = 1
        self.color = "yellow"       
    
    def danger(self):
        return 6
    
    def update(self):           
        super().update()

