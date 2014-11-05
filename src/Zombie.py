from enemy import *
import random
import Message

class Zombie(Enemy):
    def __init__(self,messageLog,  currentMap = None):
        super().__init__(messageLog, currentMap)
        self.name = "Zombie"
        self.levelMod = random.choice([-2,-1,0,0,0,0,0,1,1,2])
        self.level = currentMap.level + self.levelMod               
        self.character = "z"        
        self.speed = 7
        self.hp = self.maxhp = round(4 * (max(1,self.level - 4) ** 0.4))
        self.baseDamage =  round(6 * (max(1,self.level - 4) ** 0.2))
        self.baseToHit =  round(4 * (max(1,self.level - 4) ** 0.2))
        self.baseToDefend = 1
        self.color = random.choice(["silver", "maroon", "teal"])                
        self.chartype = "Zombie"
        self.team = 3
    
    def ToDefend(self):
        # Differnt so doesn't get zombie DV drain
        toDefend = self.baseToDefend +\
            ((self.leftHandEquipped.ToDefend + self.ToDefMod(self.leftHandEquipped.ItemClass)) if self.leftHandEquipped != None else 0) +\
            ((self.rightHandEquipped.ToDefend + self.ToDefMod(self.rightHandEquipped.ItemClass)) if self.rightHandEquipped !=None else 0) +\
            ((self.ToDefMod(7) if (self.leftHandEquipped != None and self.leftHandEquipped.ItemClass < 6 and self.rightHandEquipped != None and self.rightHandEquipped.ItemClass < 6) else 0)) +\
            ((self.ToDefMod(0) if (self.leftHandEquipped == None) and (self.rightHandEquipped == None) else 0))
        
        return toDefend
    
    def danger(self):
        return (5 + self.levelMod/2)
    
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
        
        
        # Update nearby DVs
        for j in [i for i in self.currentMap.characters if i.chartype != "Zombie" and i.chartype != "Necromancer"]:
            # Check for adjacent zombies
            zombies = [i for i in self.currentMap.characters if (i.chartype == "Zombie")\
                and (abs(i.x - j.x) < 2)\
                and (abs(i.y - j.y) < 2)]
            if len(zombies) > 0:
                closedCount = len(zombies)
                for x in range(j.x-1,j.x+2):
                    for y in range(self.y-1,self.y+2):
                        if self.currentMap.Map[x][y].walkable == False:                         
                            closedCount += 1
            else:
                closedCount = 0
            j.ZombieMod = closedCount
            if j.ZombieMod > 4 and j.ZombieMod < 8:             
                self.messageLog.append(Message.Message(j.name + " is almost surrounded by the undead!"))
            if j.ZombieMod == 8:
                self.messageLog.append(Message.Message(j.name + " has been overrun by the undead!"))