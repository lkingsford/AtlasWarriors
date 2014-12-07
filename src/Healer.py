from enemy import *
import random
import Message

class Healer(Enemy):
    def __init__(self, messageLog, currentMap = None):
        super().__init__(messageLog, currentMap)
        self.levelMod = random.choice([-2,-1,0,0,0,0,0,1,1,2])
        self.level = currentMap.dangerLevel + self.levelMod
        self.character = "h"
        self.name = "Healer"
        self.speed = 12
        self.hp = self.maxhp = round(15 * (max(1,self.level - 2) ** 0.4))
        self.mp = self.maxmp = round(10 * (max(1,self.level - 2) ** 0.4))
        self.mpChargeRate = round(3 * (max(1,self.level - 2) ** 0.4))
        self.baseDamage =  round(4 * (max(1,self.level - 2) ** 0.3))
        self.baseToHit =  round(2 * (max(1,self.level - 2) ** 0.2))
        self.baseToDefend = round(4 * (max(1,self.level - 2) ** 0.2)) 
        self.chartype = "Healer"
        
    def danger(self):
        return 3 + (self.levelMod / 2)
    
    def update(self):       
        super().update()
        
        # Find room currently in
        inRoom = [i for i in self.currentMap.characters\
            if len(self.currentMap.Map[self.x][self.y].rooms\
            & self.currentMap.Map[i.x][i.y].rooms) > 0]
         
        enemies = [i for i in self.currentMap.characters if i != self and i.team != self.team]
        if len(enemies)>0:
            nearestEnemy = min(enemies,
                    key = lambda i: abs(self.x - i.x) + abs(self.y - i.y))
        
        # Returns allies with less then full health in room
        alliesInRoom = [i for i in inRoom if (i.team == self.team)]
        needsHealingInRoom = [i for i in alliesInRoom if (i.hp < i.maxhp)\
            and (i.team == self.team)]
        needsHealingOutsideRoom = [i for i in self.currentMap.characters\
            if (i.hp < i.maxhp) and (i.team == self.team)]
        
        # Pick who to heal. Priority is first to dragons, drakes and warlords
        # if they have less then 50% health.
        # Next priority is to anything with less then 6 health (lowest first). 
        # Next priority is to most health lost
        # The list is in priority order.
        
        targets = [i for i in needsHealingInRoom if (i.chartype ==\
            "TrueDragon" or i.chartype == "Drake" or\
            i.chartype ==  "endboss") and i.hp <= (i.maxhp / 2)]       
        inRoomLowHealthTargets = [i for i in needsHealingInRoom if \
            (i.hp < 7)]
        inRoomLowHealthTargets.sort(key = lambda i: i.hp)
        targets.extend(inRoomLowHealthTargets)
        inRoomTargets = [i for i in needsHealingInRoom if \
            (i.hp < 7)]
        inRoomTargets.sort(key = lambda i: i.hp)
        targets.extend(inRoomTargets)
        outsideRoomTargets = [i for i in needsHealingOutsideRoom if \
            (i.hp < 7)]
        outsideRoomTargets.sort(key = lambda i: i.hp)
        targets.extend(outsideRoomTargets)
   
        # Logic:
        # If we are more then 1 away from the player, and if we can heal
        # someone, or find a route to heal someone
        # If we can't do that, try to stay at least 3 away from the player.
        # If we can't do that, try to stay at least 2 away from the player.
        # If we can't do that, attack the player.
        
        # This loops through the potential healing targets as above.
        # It will 'return' out of update if successful.
        if self.mp > 2 and not (nearestEnemy != None and \
            max(abs(nearestEnemy.x - self.x), abs(nearestEnemy.y - self.y))\
            <= 2):
        
            for i in targets:
                # See if inside same room
                if (len(self.currentMap.Map[self.x][self.y].rooms &\
                    self.currentMap.Map[i.x][i.y].rooms) > 0):
                    self.CastHeal(i)
                    return
                else:
                    route = self.GetNearest(lambda j: \
                        len(self.currentMap.Map[i.x][i.y].rooms &\
                        self.currentMap.Map[j[0]][j[1]].rooms) > 0)
                    # Route [0] is always the current tile if there is a route
                    if route != None and len(route)>1:
                        self.tryMove(route[1][0], route[1][1])
                        return
                        
        # Try to stay three away
        if (nearestEnemy != None):
            route = self.GetNearest(lambda i: (max(abs(i[0]-nearestEnemy.x),
                (i[1]-nearestEnemy.y)) >= 3))
            if route != None and len(route)>1:
                self.tryMove(route[1][0], route[1][1])
                return
                
        # Try to stay two away
        if (nearestEnemy != None):
            route = self.GetNearest(lambda i: (max(abs(i[0]-nearestEnemy.x),
                (i[1]-nearestEnemy.y)) >= 2))
            if route != None and len(route)>1:
                self.tryMove(route[1][0], route[1][1])
                return
        
        # Try to attack
        route = self.GetRoute((nearestEnemy.x, nearestEnemy.y))
        if route != None and len(route)>1:
            self.tryMove(route[1][0], route[1][1])
            return
            
        # Can do nothing. Wait.
        self.Wait()
