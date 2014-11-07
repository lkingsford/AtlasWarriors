from enemy import *
import random
import Message

class Healer(Enemy):
    def __init__(self, messageLog, currentMap = None):
        super().__init__(messageLog, currentMap)
        self.levelMod = random.choice([-2,-1,0,0,0,0,0,1,1,2])
        self.level = currentMap.level + self.levelMod
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
        
        # The healer has priorities:
        #    healPriority -   the priority to heal a person in the room
        #    movePriority -   the priority to get better tactical positioning,
        #                     hopefully in the same room
        #    runPriority  -   the priority to go between rooms to find another
        #                     person on the team
        #    attackPriority - nobody left but us healers. Hit away.
        
        # Find room currently in
        inRoom = [i for i in self.currentMap.characters\
            if len(self.currentMap.Map[self.x][self.y].rooms\
            & self.currentMap.Map[i.x][i.y].rooms) > 0]
            
        # Returns allies with less then full health in room
        alliesInRoom = [i for i in inRoom if (i.team == self.team)]
        needsHealingInRoom = [i for i in alliesInRoom if (i.hp < i.maxhp)]
        
        # Pick who to heal. Priority is first to dragons, drakes and warlords
        # if they have less then 50% health.
        # Next priority is to anything with less then 6 health (lowest first). 
        # Next priority is to most health lost
        
        healPriority = 0
        
        if len(needsHealingInRoom) > 0: 
        
            healTarget = None
            priority1targets = [i for i in needsHealingInRoom if (i.chartype ==\
                "TrueDragon" or i.chartype == "Drake" or\
                i.chartype ==  "endboss") and i.hp <= (i.maxhp / 2)]
            if len(priority1targets) > 0:
                healTarget = priority1targets[0]
                healPriority = 12
            
            else:
                priority2targets = [i for i in needsHealingInRoom if i.hp <= 6]
                if len(priority2targets) > 0:
                    healTarget = priority2targets[0]
                    healPriority = 8 - healTarget.maxhp + healTarget.hp
                    
                else:
                    healTarget = max(needsHealingInRoom, key=lambda i:(i.maxhp\
                        - i.hp))
                    healPriority = 8 - healTarget.maxhp + healTarget.hp
        
        enemiesInRoom = [i for i in inRoom if (i.team != self.team)]
        nearestEnemy = None
        if len(enemiesInRoom) == 0:
            movePriority = 0
        else:
            nearestEnemy = min([i for i in enemiesInRoom], key = lambda i:\
                abs(self.x - i.x) + abs(self.y - i.y))
            nearestEnemyDistance = abs(self.x - nearestEnemy.x) +\
                abs(self.y - nearestEnemy.y)
            if nearestEnemyDistance == 1:
                movePriority = 9
            elif nearestEnemyDistance == 2:
                movePriority = 6
            elif nearestEnemyDistance == 3:
                movePriority = 4
            elif nearestEnemyDistance == 4:
                movePriority = 1
            else:
                movePriority = 0
            nearestEnemyAverageDamage = nearestEnemy.GetAverageDamage(\
                self.ToDefend(), self.level)
            if nearestEnemyAverageDamage >= self.hp:
                movePriority = movePriority * 2

        runPriority = 0
        attackPriority = 0
            
        nearestAllyPos = None

        if (alliesInRoom == 0):
            # Find nearest allies
            allies = [i for i in currentMap.characters if i.team == self.team\
                and i != self]
            
            # If no allies left, or they're all healers, ATTACK!
            if len(allies) == 0 or (all([i.chartype=="Healer" for i in allies])\
                and (self.hp >= self.maxhp)):
                attackPriority  = 12
            else:
                # UGLY CODE WARNING!
                nearestAllyPos = self.GetNearest(lambda i: len([j for j in\
                    allies if len(self.currentMap.Map[i[0]][i[1]].rooms &\
                self.currentMap.Map[j.x][j.y].rooms) > 0]))
                if nearestAllyPos == None:
                    attackPriority = 10
                else:
                    runPriority = 5
                    
        # I get that this is not the best way to do this, but it will do for now
        if (runPriority == 0 and attackPriority == 0 and movePriority == 0 and\
            healPriority == 0):
            self.Wait()
        
        elif (runPriority >= attackPriority) and (runPriority >= movePriority)\
            and (runPriority >=  healPriority) and (nearestAllyPos != None):
            moveTo = nearestAllyPos[1]
            self.tryMove(moveTo[0], moveTo[1])
        
        elif (self.mp > 2) and (healPriority >= runPriority) and \
            (healPriority >= movePriority) and (healPriority >=\
            attackPriority):
            self.CastHeal(healTarget)
        
        elif (movePriority >= healPriority) and (movePriority >= runPriority)\
            and (movePriority >= attackPriority) and (nearestEnemy != None):
            moveTo = self.GetNearest(lambda i: (max(abs(i[0]-nearestEnemy.x),\
                abs(i[1]-nearestEnemy.y))) > nearestEnemyDistance)
            if moveTo == None or len(moveTo) == 0:
                # Blocked in, so move closer to enemy (possibly attacking)
                moveTo = self.GetRoute([nearestEnemy.x, nearestEnemy.y])
                if moveTo == None or len(moveTo) == 0:
                    self.Wait()
                else:
                    moveTo = moveTo[1]
                    self.tryMove(moveTo[0], moveTo[1])
            else:
                moveTo = moveTo[1]                        
                self.tryMove(moveTo[0], moveTo[1])
        
        elif (attackPriority >= runPriority) and (attackPriority >=\
            healPriority) and (attackPriorirty >= movePriorirty):
            moveTo = self.GetRoute([nearestEnemy.x, nearestEnemy.y])
            if moveTo == None or len(moveTo) == 0:
                self.Wait()
            else:
                moveTo = moveTo[1]
                self.tryMove(moveTo[0], moveTo[1])
        
        else:
            self.Wait()


# BUGS IN HEALER:
# E:\Documents\GitHub\AtlasWarriors\src>python rl.py
# Traceback (most recent call last):
  # File "rl.py", line 385, in <module>
    # character.update()
  # File "E:\Documents\GitHub\AtlasWarriors\src\Healer.py", line 124, in update
    # moveTo = nearestAllyPos[1]
# UnboundLocalError: local variable 'nearestAllyPos' referenced before assignment

 
                
