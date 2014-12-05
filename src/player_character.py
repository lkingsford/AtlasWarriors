import character
import item
import math
import animation
import Message
import random
import tutorial

from item import  ItemClass 

#PC Specific stuff
class PlayerCharacter(character.Character):
    def __init__(self, messageLog, currentMap, defaultItems, difficulty, tutorial):
        super(PlayerCharacter, self).__init__(messageLog, currentMap)
        self.nextMove = "none"; 
        self.team = 0
        self.name = "Hunter"
        self.baseDamage = 4
        self.baseToHit = 3
        self.baseToDefend = 3
        self.level = 1
        self.hp = 10
        self.maxhp = 10
        self.baseDanger = 20
        self.difficulty = difficulty
        self.backpack = [defaultItems[0], defaultItems[1], defaultItems[2], defaultItems[3], defaultItems[4], defaultItems[5]]
        self.hpHealRate = self.difficulty.hpHealRate
        self.hpAccumulated = 0
        self.secondWind = False
        self.secondWindTime = self.difficulty.secondWindTime
        self.secondWindHealAmount = self.difficulty.secondWindHealAmount
        self.secondWindTimeLeft = 0     
        self.chartype = "PC"    
        self.difficulty = difficulty
        self.tutorial = tutorial
        self.autopickup = True
        
    def update(self):
        super().update();
        
        if self.burning:
            self.messageLog.append(Message.Message("YOU ARE ON FIRE! Stand still for " + str(self.burnWaitTurns) + " to be extinguished"))
        
        self.secondWindTimeLeft -= 1
        if self.secondWind:
            self.messageLog.append(Message.Message("KILL OR BE KILLED! - " + str(self.secondWindTimeLeft) + " turns left"))
        
        if self.nextMove == "move_e":
            self.tryMove(self.x - 1, self.y)
            self.nextMove = "none"
            
        if self.nextMove == "move_w":
            self.tryMove(self.x + 1, self.y)
            self.nextMove = "none"
            
        if self.nextMove == "move_n":
            self.tryMove(self.x, self.y - 1)
            self.nextMove = "none"
            
        if self.nextMove == "move_s":
            self.tryMove(self.x, self.y + 1)
            self.nextMove = "none"
            
        if self.nextMove == "move_ne":
            self.tryMove(self.x - 1, self.y - 1)
            self.nextMove = "none"
            
        if self.nextMove == "move_nw":
            self.tryMove(self.x + 1, self.y - 1)
            self.nextMove = "none"
            
        if self.nextMove == "move_se":
            self.tryMove(self.x - 1, self.y + 1)
            self.nextMove = "none"
            
        if self.nextMove == "move_sw":
            self.tryMove(self.x + 1, self.y + 1)
            self.nextMove = "none"
            
        if self.nextMove == "wait":
            self.Wait()
            self.nextMove = "none"

    
    def tryMove(self, newX, newY):
        super().tryMove(newX, newY)
        if (self.x == newX) and (self.y == newY):
            for i in self.currentMap.Items:
                if i.x == self.x and i.y == self.y:
                    if self.Pickup(i) == True and self.autopickup:
                        self.messageLog.append(Message.Message("You picked up a " + i.Description()))
                    elif self.autopickup:
                        self.messageLog.append(Message.Message("There is a " + i.Description() + " on the ground."))
                        self.messageLog.append(Message.Message("Your backpack is full"))
                    else:
                        self.messageLog.append(Message.Message("There is a " + i.Description() + " on the ground."))
        newlySeen = self.currentMap.UpdateVisibility(self, self.x, self.y)
        
        # Heal on explore
        if newlySeen > 0 and self.hp != self.maxhp:
            self.hpAccumulated += newlySeen * self.hpHealRate * self.maxhp
            if self.hpAccumulated > 1:
                self.hp += round(self.hpAccumulated)
                self.hpAccumulated -= round(self.hpAccumulated)
                self.hp = min(self.hp, self.maxhp)  
        
            
    def Killed(self, target):               
        super().Killed(target)
        if self.secondWind:
            self.secondWind = False
            self.hp = int(self.maxhp * self.secondWindHealAmount)
            self.Extinguish()
    
    def danger(self):
        return (10 * self.level)
        
    def dead(self):
        return self.secondWind and self.secondWindTimeLeft <= 0
        
    def Stun(self):
        # This is almost cheaty, but it's easier then the alternative
        # and stops people getting knocked out in weird ways with
        # the second wind
        if not self.secondWind:
            self.ticksUntilTurn += round(200/self.speed)
        
    def Attacked(self, damage, attacker, melee = True):
        self.hp -= round(damage)
        if self.hp > 0:
            self.tutorial.TriggerMessage(tutorial.TUTORIAL_ATTACKED)            
        if not self.secondWind and self.hp <= 0:
            self.tutorial.TriggerMessage(tutorial.TUTORIAL_SECONDWIND)
            self.secondWind = True
            self.secondWindTimeLeft = self.secondWindTime
            self.messageLog.append(Message.Message("KILL OR BE KILLED! - " + str(self.secondWindTimeLeft) + " turns left"))
        
        # The dagger retalliate is replicated both here and in character.py
        if attacker != None and melee == True:
            if (self.leftHandEquipped != None) and (self.leftHandEquipped.ItemClass == ItemClass.dagger):
                # Retalliate attack if got dagger
                # Retalliate attack does 4 extra ToHit
                self.messageLog.append(Message.Message(self.name + " counterattacks " + attacker.name + " with the " + self.leftHandEquipped.Name))
                self.AttackWithWeapon(attacker, [self.RetaliateBonus + self.GetWeaponToHit(self.leftHandEquipped) + self.ToHitMod(self.leftHandEquipped.ItemClass) + 0 if not self.GetTwoHanded() else self.ToHitMod(7), self.leftHandEquipped])
                
            if (self.rightHandEquipped != None) and (self.rightHandEquipped.ItemClass == ItemClass.dagger):
                self.messageLog.append(Message.Message(self.name + " counterattacks " + attacker.name + " with the " + self.rightHandEquipped.Name))
                self.AttackWithWeapon(attacker, [self.RetaliateBonus + self.GetWeaponToHit(self.rightHandEquipped) + self.ToHitMod(self.rightHandEquipped.ItemClass) + 0 if not self.GetTwoHanded() else self.ToHitMod(7), self.rightHandEquipped])         
                
        return False
        
    # Custom version to allow tutorial
    def RegisterSkillHit(self, skill):
        oldHits, oldLevel = self.skills[skill]
        super().RegisterSkillHit(skill)
        newHits, newLevel = self.skills[skill]
        if newLevel > oldLevel:
            self.tutorial.TriggerMessage(tutorial.TUTORIAL_WEAPONLVL)  

    # Custom version to allow tutorial
    def LevelUp(self, supress = False):
        super().LevelUp(supress)
        self.tutorial.TriggerMessage(tutorial.TUTORIAL_LEVEL)
