import random
import math
import item
import animation
import Message

from item import ItemClass

# Any character - monster or PC
class Character:
    def __init__(self, messageLog, currentMap):
        self.x = 1;
        self.y = 1;
        self.character = '@'
        self.color = "silver"       
        self.speed = 10
        self.team = 1;
        self.currentMap = currentMap
        self.level = 1
        self.hp = 10    
        self.maxhp = 10
        self.baseToHit = 1
        self.baseToDefend = 1
        self.baseDamage = 1
        self.baseCritMult = 4
        self.living = True
        self.name = 'Character'     
        self.xp = 0         
        # Whether can attack multiple times with fists. Only PC can.
        self.canPummel = False                      
        # This is for the score (but only used by the Player Character)
        self.totalxp = 0
        
        self.baseXPToLevel = 10
        self.ticksUntilTurn = random.randint(0,10)
        
        self.messageLog = messageLog
        
        self.lastx = 1;
        self.lasty = 1;
        self.backpackSize = 6
        self.backpack = []
        self.leftHandEquipped = None
        self.rightHandEquipped = None
        
        self.animations = []
        
        self.burning = False
        self.burnDamage = 0
        self.DEFAULT_BURN_WAIT_TURNS = 2
        
        self.RetaliateBonus = 4
        
        self.moved = False
        
        self.chartype = ""
        
        self.nextLevel =  self.baseXPToLevel * (self.level ** .5)
        
        # See comment before def RegisterHit for how this list is used
        self.skills = [(0, 0) for i in range(8)]    
    
    def dead(self):
        return self.hp <= 0
            
    
    def update(self):       
        if self.burning:            
            if self.moved:
                self.burnWaitTurns = self.DEFAULT_BURN_WAIT_TURNS
            else:
                self.burnWaitTurns -= 1
                if self.burnWaitTurns == 0:
                    self.Extinguish()
            self.messageLog.append(Message.Message(self.name + " is burning!",[(self.x, self.y)]))
            if self.Attacked(self.burnDamage, self.burnSource):
                self.messageLog.append(Message.Message(self.name + " burns to death",[(self.x, self.y)]))
                self.burnSource.Killed(self)
        self.moved = False
        
    def tryMove(self, newX, newY):
        self.moved = True
        if self.currentMap.Map[newX][newY].walkable == True:
            monsterInSquare = [i for i in self.currentMap.characters if (i.x == newX) and (i.y == newY)]
            if len(monsterInSquare) > 0:
                if (monsterInSquare[0].team != self.team):              
                    self.Attack((newX, newY))
            else:
                self.lastx = self.x
                self.lasty = self.y
                self.x = newX
                self.y = newY   
                action = self.currentMap.Map[newX][newY].walkbehavior
                if (action != 'none'):
                    if (action == 'go up'):
                        self.ChangeMap(self.currentMap.lastMap, self.currentMap.lastMap.endX, self.currentMap.lastMap.endY)
                    if (action == 'go down'):
                        self.ChangeMap(self.currentMap.nextMap,  self.currentMap.nextMap.startX, self.currentMap.nextMap.startY)
                self.currentMap.Map[newX][newY].OnWalk(self)
                self.ticksUntilTurn = round(100/self.speed)
            
                # Spear skewer if walk towards spear, or enemy if holding one
                dx = self.x - self.lastx
                dy = self.y - self.lasty
                monsterInNextSquare = [i for i in self.currentMap.characters if
                    (i.x == (self.x + dx)) and (i.y == (self.y + dy))]
                for i in monsterInNextSquare:
                    i.Skewer(i)
                    self.Lunge(i)
                    
    # Skewer if an enemy walks towards while self is holding a spear 
    def Skewer(self, enemy):
            if (self.leftHandEquipped != None) and (self.leftHandEquipped.ItemClass == ItemClass.polearm):
                self.messageLog.append(Message.Message(self.name + " skewers " + enemy.name + " with the " + self.leftHandEquipped.Name,[(self.x, self.y)]))
                self.AttackWithWeapon(enemy, [self.GetWeaponToHit(self.leftHandEquipped) + self.ToHitMod(self.leftHandEquipped.ItemClass) + 0 if not self.GetTwoHanded() else self.ToHitMod(7), self.leftHandEquipped])
                
            if (self.rightHandEquipped != None) and (self.rightHandEquipped.ItemClass == ItemClass.polearm):
                self.messageLog.append(Message.Message(self.name + " skewers " + enemy.name + " with the " + self.rightHandEquipped.Name,[(self.x, self.y)]))
                self.AttackWithWeapon(enemy, [self.GetWeaponToHit(self.rightHandEquipped) + self.ToHitMod(self.rightHandEquipped.ItemClass) + 0 if not self.GetTwoHanded() else self.ToHitMod(7), self.rightHandEquipped])         

    def Lunge(self, enemy):
            if (self.leftHandEquipped != None) and (self.leftHandEquipped.ItemClass == ItemClass.polearm):
                self.messageLog.append(Message.Message(self.name + " lunges towards " + enemy.name + " with the " + self.leftHandEquipped.Name,[(self.x, self.y)]))
                self.AttackWithWeapon(enemy, [self.GetWeaponToHit(self.leftHandEquipped) + self.ToHitMod(self.leftHandEquipped.ItemClass) + 0 if not self.GetTwoHanded() else self.ToHitMod(7), self.leftHandEquipped])
                
            if (self.rightHandEquipped != None) and (self.rightHandEquipped.ItemClass == ItemClass.polearm):
                self.messageLog.append(Message.Message(self.name + " lunges towards " + enemy.name + " with the " + self.rightHandEquipped.Name,[(self.x, self.y)]))
                self.AttackWithWeapon(enemy, [self.GetWeaponToHit(self.rightHandEquipped) + self.ToHitMod(self.rightHandEquipped.ItemClass) + 0 if not self.GetTwoHanded() else self.ToHitMod(7), self.rightHandEquipped])         
    

    def ChangeMap(self, newMap, x = 0, y = 0):
        self.currentMap.characters.remove(self)
        self.currentMap = newMap
        self.currentMap.characters.append(self)                 
        if (x != 0):
            self.x = x
            self.y = y
        else:
            self.x = newMap.startX
            self.y = newMap.startY

    def GetWeaponToHit(self, weapon):
        return self.baseToHit + weapon.ToHit        
    
    def GetTwoHanded(self):
        return (self.rightHandEquipped != None and self.rightHandEquipped.IsWeapon() == True and 
                (self.leftHandEquipped != None and self.leftHandEquipped.IsWeapon() == True ))
        
    def ToHit(self):                        
            
            # Unarmed
            if ((self.leftHandEquipped == None) or (self.leftHandEquipped != None and self.leftHandEquipped.IsWeapon() == False ))\
             and ((self.rightHandEquipped == None) or (self.rightHandEquipped != None and self.rightHandEquipped.IsWeapon() == False )):
                return [(self.baseToHit + self.ToHitMod(0) + (self.leftHandEquipped.ToHit if self.leftHandEquipped != None else 0) + (self.rightHandEquipped.ToHit if self.rightHandEquipped != None else 0) , None)]
            
            # 1 Weapon
            elif (self.leftHandEquipped != None and self.leftHandEquipped.IsWeapon() == True and not\
                (self.rightHandEquipped != None and self.rightHandEquipped.IsWeapon() == True )) and not\
                (self.rightHandEquipped != None and self.rightHandEquipped.IsWeapon() == True ):
                    return [(self.GetWeaponToHit(self.leftHandEquipped) + self.ToHitMod(self.leftHandEquipped.ItemClass) + (self.rightHandEquipped.ToHit if self.rightHandEquipped != None else 0), self.leftHandEquipped)]
            
            elif (self.rightHandEquipped != None and self.rightHandEquipped.IsWeapon() == True and not\
                (self.leftHandEquipped != None and self.leftHandEquipped.IsWeapon() == True )) and not\
                (self.leftHandEquipped != None and self.leftHandEquipped.IsWeapon() == True ):
                    return [(self.GetWeaponToHit(self.rightHandEquipped) + self.ToHitMod(self.rightHandEquipped.ItemClass) + (self.leftHandEquipped.ToHit if self.leftHandEquipped != None else 0), self.rightHandEquipped)]
            
            # 2 Weapons
            else:
                return [(self.baseToHit + self.leftHandEquipped.ToHit + self.ToHitMod(self.leftHandEquipped.ItemClass) + self.ToHitMod(7), self.leftHandEquipped), \
                    (self.baseToHit + self.rightHandEquipped.ToHit + self.ToHitMod(self.rightHandEquipped.ItemClass) + self.ToHitMod(7), self.rightHandEquipped)]
                    
    def ZombieMod(self):
        return self.currentMap.ZombieMod[self.x][self.y]
        
    def ToDefend(self):
        # This would have be changed in a different game - there is the special provision for zombie DV drain
        toDefend = self.baseToDefend +\
            ((self.leftHandEquipped.ToDefend + self.ToDefMod(self.leftHandEquipped.ItemClass)) if self.leftHandEquipped != None else 0) +\
            ((self.rightHandEquipped.ToDefend + self.ToDefMod(self.rightHandEquipped.ItemClass)) if self.rightHandEquipped !=None else 0) +\
            ((self.ToDefMod(7) if (self.leftHandEquipped != None and self.leftHandEquipped.ItemClass < 6 and self.rightHandEquipped != None and self.rightHandEquipped.ItemClass < 6) else 0)) +\
            ((self.ToDefMod(0) if (self.leftHandEquipped == None) and (self.rightHandEquipped == None) else 0))                     
        return toDefend - self.ZombieMod()
        
    def Damage(self):
        return self.baseDamage  
    
    def CritMult(self):
        return self.baseCritMult
    
    def GetDamageMultiplier(self, difference):
        levelDifferenceDamageMultipliers = {
            -6: 0.05,
            -5: 0.1,
            -4: 0.2, 
            -3: 0.4, 
            -2: 0.6,
            -1: 0.8, 
            0 : 1,
            1 : 1.1,
            2 : 1.2,
            3 : 1.3,
            4 : 1.4,
            5 : 1.6,
            6 : 2 }
        if (difference < -6):
            difference = -6
        if (difference > 6):
            difference = 6
        return levelDifferenceDamageMultipliers[difference]
    
    def Killed(self, target):
        xp = round(target.danger() * self.GetDamageMultiplier(target.level - self.level))
        self.xp += xp
        self.totalxp += xp
        if self.xp > self.nextLevel:
            self.LevelUp()                  
            self.nextLevel = round(self.baseXPToLevel * (self.level ** .69897))
    
    def Color(self):
        if not self.burning:
            return (self.color, None)
        else:
            return ('red', 'yellow')
    
            
    def LevelUp(self, suppress = False):
        self.xp = round(self.xp - int(self.baseXPToLevel * (max(0, self.level) ** .69897)), 0) 
        self.level += 1
        self.maxhp = round(10 * ((self.level) ** 0.4));
        self.hp = self.maxhp        
        self.animations.append(animation.LevelUpAnimation((self.x, self.y)))
        if not(suppress):
            self.messageLog.append(Message.Message(self.name + " levels up!",[(self.x, self.y)]));
    
    def ChanceToHit(self, toHit, toDefend):
        return (math.atan(0.6 * (toHit - toDefend) - 1) + math.pi/2) / math.pi
    
    def ChanceToCrit(self, toHit, toDefend):
        return (math.atan(0.5 * (toHit - toDefend) - 3.5) + math.pi/2) / math.pi
    
    def GetAverageDamage(self, toDefend, defenderLevel):
        damage = []
        for i in self.ToHit():
            chanceToHit = self.ChanceToHit(i[0], toDefend)
            chanceToCrit = self.ChanceToCrit(i[0], toDefend)
            normDamageChance = chanceToHit * (((self.Damage() if i[1] == None else i[1].Damage) + self.DmgMod(0 if i[1] == None else i[1].ItemClass)) * self.GetDamageMultiplier(self.level - defenderLevel)) * (1 - chanceToCrit)
            critDamageChance = chanceToHit * (((self.Damage() if i[1] == None else i[1].Damage) + self.DmgMod(0 if i[1] == None else i[1].ItemClass)) * self.GetDamageMultiplier(self.level - defenderLevel)) * (chanceToCrit) * self.CritMult()
            damage.append(normDamageChance + critDamageChance)
        return 0 if len(damage) == 0 else sum(damage)/float(len(damage))
            
    def GetShieldDV(self):
        TotalDV = 0
        if self.leftHandEquipped != None and self.leftHandEquipped.ItemClass == ItemClass.shield:
            TotalDV += self.leftHandEquipped.ToDefend
        if self.rightHandEquipped != None and self.rightHandEquipped.ItemClass == ItemClass.shield:
            TotalDV += self.rightHandEquipped.ToDefend
        return TotalDV
    
    def UpdateVisibility(self):
        pass
            
    def Attack(self, pos):
        self.moved = True
        self.ticksUntilTurn = round(100/self.speed)
        
        # Unarmed
        if ((self.leftHandEquipped == None) or (self.leftHandEquipped != None and self.leftHandEquipped.IsWeapon() == False ))\
         and ((self.rightHandEquipped == None) or (self.rightHandEquipped != None and self.rightHandEquipped.IsWeapon() == False )):
            Weapons = [(self.baseToHit + self.ToHitMod(0), None)]
        
        # 1 Weapon
        elif (self.leftHandEquipped != None and self.leftHandEquipped.IsWeapon() == True and not\
            (self.rightHandEquipped != None and self.rightHandEquipped.IsWeapon() == True )) and not\
            (self.rightHandEquipped != None and self.rightHandEquipped.IsWeapon() == True ):
                Weapons = [(self.GetWeaponToHit(self.leftHandEquipped) + self.ToHitMod(self.leftHandEquipped.ItemClass), self.leftHandEquipped)]
        
        elif (self.rightHandEquipped != None and self.rightHandEquipped.IsWeapon() == True and not\
            (self.leftHandEquipped != None and self.leftHandEquipped.IsWeapon() == True )) and not\
            (self.leftHandEquipped != None and self.leftHandEquipped.IsWeapon() == True ):
                Weapons = [(self.GetWeaponToHit(self.rightHandEquipped) + self.ToHitMod(self.rightHandEquipped.ItemClass), self.rightHandEquipped)]
        
        # 2 Weapons
        else:
            Weapons = [(self.baseToHit + self.leftHandEquipped.ToHit + self.ToHitMod(self.leftHandEquipped.ItemClass) + self.ToHitMod(7), self.leftHandEquipped), \
                (self.baseToHit + self.rightHandEquipped.ToHit + self.ToHitMod(self.rightHandEquipped.ItemClass) + self.ToHitMod(7), self.rightHandEquipped)]
                
        for i in Weapons:
            attackSquares = [pos]
            if (i[1] != None):
                if (i[1].ItemClass == ItemClass.polearm):
                    dx = pos[0] - self.x
                    dy = pos[1] - self.y
                    attackSquares = [pos, (self.x + dx * 2, self.y + dy * 2)]
                elif (i[1].ItemClass == ItemClass.axe):
                    dx = pos[0] - self.x 
                    dy = pos[1] - self.y
                    if (dx == 0 and dy == -1):
                        attackSquares = [pos, (self.x - 1, self.y - 1), (self.x + 1, self.y - 1)]
                    if (dx == 0 and dy == 1):
                        attackSquares = [pos, (self.x - 1, self.y + 1), (self.x + 1, self.y + 1)]
                    if (dx == -1 and dy == 0):
                        attackSquares = [pos, (self.x - 1, self.y - 1), (self.x - 1, self.y - 1)]
                    if (dx == 1 and dy == 0):
                        attackSquares = [pos, (self.x + 1, self.y + 1), (self.x + 1, self.y - 1)]
                    if (dx == -1 and dy == -1):
                        attackSquares = [pos, (self.x - 1, self.y), (self.x, self.y - 1)]
                    if (dx == 1 and dy == -1):
                        attackSquares = [pos, (self.x + 1, self.y), (self.x, self.y - 1)]
                    if (dx == -1 and dy == 1):
                        attackSquares = [pos, (self.x - 1, self.y), (self.x, self.y + 1)]
                    if (dx == 1 and dy == 1):
                        attackSquares = [pos, (self.x + 1, self.y), (self.x, self.y + 1)]                                
            
            for j in attackSquares:
                # self.animations.append(animation.DrawAttackAnimation(attackSquares))              
                monsterInSquare = [c for c in self.currentMap.characters if (c.x == j[0]) and (c.y == j[1])]
                if len(monsterInSquare) > 0:
                    if (monsterInSquare[0].team != self.team):          
                        result = self.AttackWithWeapon(monsterInSquare[0], i)
                        if (
                            (i[1] == None) or i[1].ItemClass == ItemClass.none)\
                            and (self.canPummel):
                            pummelMod = 0;
                            while(not(monsterInSquare[0].dead()) and\
                                result > 0):                                
                                self.messageLog.append(Message.Message(\
                                    self.name + " pummels " +\
                                    monsterInSquare[0].name + "!",\
                                    [(self.x, self.y)]))
                                pummelMod += 1
                                result = self.AttackWithWeapon(\
                                    monsterInSquare[0], (i[0]+pummelMod, i[1]))
                                
                        
        self.ticksUntilTurn = round(max(map(lambda i:100 if i[1] == None else i[1].Speed, Weapons))/self.speed)
    
    def AttackWithWeapon(self, target, ToHit):
        self.moved = True       
        #Calculate odds to hit
        chanceToHit = self.ChanceToHit(ToHit[0], target.ToDefend())
        #Calculate odds to crit
        chanceToCrit = self.ChanceToCrit(ToHit[0], target.ToDefend()) 
        
        #Did it hit?
        hit = random.random() < chanceToHit
        
        #Did it crit?
        crit = random.random() < chanceToCrit
        
        if not(target.dead()):
            if hit:
                damage = ((self.Damage() if ToHit[1] == None else ToHit[1].Damage) + self.DmgMod(0 if ToHit[1] == None else ToHit[1].ItemClass)) * self.GetDamageMultiplier(self.level - target.level) * (self.CritMult() if crit else 1)
                target.Attacked(damage, self)
                if crit:
                    self.messageLog.append(Message.Message(self.name + " crits " + target.name + " (" + str(target.hp) + ")",[(self.x, self.y)]));
                else:
                    self.messageLog.append(Message.Message(self.name + " attacks " + target.name+ " (" + str(target.hp) + ")",[(self.x, self.y)]));
                if (target.dead()):
                    self.messageLog.append(Message.Message(target.name + " has been killed!",[(self.x, self.y)]));
                    self.Killed(target)
                if (ToHit[1] != None):              
                    self.RegisterSkillHit(ToHit[1].ItemClass)
                    if (self.leftHandEquipped != None and self.leftHandEquipped.ItemClass < 6 and self.rightHandEquipped != None and self.rightHandEquipped.ItemClass < 6):
                        self.RegisterSkillHit(7)
                    stunned = False
                    if ToHit[1].ItemClass == ItemClass.blunt:
                        stunned = True
                        target.Stun();
                else:
                    self.RegisterSkillHit(0)
                    
            else:
                damage = 0
                target.Missed(ToHit[0], self)           
            
        """print (self.name, '->', target.name, ' ToHit - ToDefend = ', 
            self.ToHit() - target.ToDefend(), ' chanceToHit ', 
            chanceToHit, ' chanceToCrit ', chanceToCrit, ' hit ', 
            hit, ' crit ', crit, ' DamageMultiplyer ', 
            self.GetDamageMultiplier(self.level-target.level),
            ' damage done ', damage)"""                 
        
        if hit:
            if crit:
                return 2
            else:
                return 1
        else:
            return 0
            
    def Attacked(self, damage, attacker, melee = True):
        self.hp -= round(damage)
        # The dagger retalliate is replicated both here and in player.py
        if attacker != None and melee == True:
            if (self.leftHandEquipped != None) and (self.leftHandEquipped.ItemClass == ItemClass.dagger):
                # Retalliate attack if got dagger
                # Retalliate attack does 4 extra ToHit
                self.messageLog.append(Message.Message(self.name + " counterattacks " + attacker.name + " with the " + self.leftHandEquipped.Name,[(self.x, self.y)]))
                self.AttackWithWeapon(attacker, [self.RetaliateBonus + self.GetWeaponToHit(self.leftHandEquipped) + self.ToHitMod(self.leftHandEquipped.ItemClass) + 0 if not self.GetTwoHanded() else self.ToHitMod(7), self.leftHandEquipped])
                
            if (self.rightHandEquipped != None) and (self.rightHandEquipped.ItemClass == ItemClass.dagger):
                self.messageLog.append(Message.Message(self.name + " counterattacks " + attacker.name + " with the " + self.rightHandEquipped.Name,[(self.x, self.y)]))
                self.AttackWithWeapon(attacker, [self.RetaliateBonus + self.GetWeaponToHit(self.rightHandEquipped) + self.ToHitMod(self.rightHandEquipped.ItemClass) + 0 if not self.GetTwoHanded() else self.ToHitMod(7), self.rightHandEquipped])         
                
        if self.hp <= 0:
            return True
        else:
            return False
    
    def Missed(self, toHit, attacker):
        # Find if it hit the shield, was dodged or was parried
        
        # Get chance to miss without anything equipped (dodge chance)       
        dodgeChance = 1 - self.ChanceToHit(toHit, self.baseToDefend)
        
        shieldBlockChance = 0
        weaponBlockLeftChance = 0
        weaponBlockRightChance = 0
        
        # Get chance with left hand
        if (self.leftHandEquipped != None):
            if self.leftHandEquipped.ItemClass == ItemClass.shield:
                shieldBlockChance += 1 - self.ChanceToHit(toHit,    (self.leftHandEquipped.ToDefend + self.ToDefMod(self.leftHandEquipped.ItemClass)))
            else:
                weaponBlockLeftChance = 1 - self.ChanceToHit(toHit, (self.leftHandEquipped.ToDefend + self.ToDefMod(self.leftHandEquipped.ItemClass)))

        # Get chance with right hand
        if (self.rightHandEquipped != None):
            if self.rightHandEquipped.ItemClass == ItemClass.shield:
                shieldBlockChance += 1 - self.ChanceToHit(toHit,    (self.rightHandEquipped.ToDefend + self.ToDefMod(self.rightHandEquipped.ItemClass)))
            else:
                weaponBlockRightChance = 1 - self.ChanceToHit(toHit, (self.rightHandEquipped.ToDefend + self.ToDefMod(self.rightHandEquipped.ItemClass)))
        
        # Add shield skill points if one is weilded
        if (self.leftHandEquipped != None and self.leftHandEquipped.ItemClass == 6) or\
            (self.rightHandEquipped != None and self.rightHandEquipped.ItemClass == 6):
                self.RegisterSkillHit(6)
        
        totalChance = shieldBlockChance+weaponBlockLeftChance+weaponBlockRightChance+dodgeChance
        shieldBlockChance = shieldBlockChance / totalChance
        weaponBlockLeftChance = weaponBlockLeftChance / totalChance + shieldBlockChance
        weaponBlockRightChance = weaponBlockRightChance / totalChance + weaponBlockLeftChance
        
        # There might be a neater way to do this, but this will do
        v = random.random()
        if v < shieldBlockChance:
            # Blocked with shield
            self.messageLog.append(Message.Message(self.name + " deflects " + attacker.name + "'s attack with the shield",[(self.x, self.y),(attacker.x, attacker.y)]))
            pass
        elif v < weaponBlockLeftChance:
            # Blocked (or else) with left hand item
            if self.leftHandEquipped.ItemClass == item.ItemClass.sword:
                # Parry if a sword
                self.messageLog.append(Message.Message(self.name + " parried " + attacker.name + "'s attack with the " + self.leftHandEquipped.Name,[(self.x, self.y),(attacker.x, attacker.y)]))               
                self.AttackWithWeapon(attacker, [self.GetWeaponToHit(self.leftHandEquipped) + self.ToHitMod(self.leftHandEquipped.ItemClass) + 0 if not self.GetTwoHanded() else self.ToHitMod(7), self.leftHandEquipped])
            else:
                self.messageLog.append(Message.Message(self.name + " blocks " + attacker.name + "'s attack with the " + self.leftHandEquipped.Name,[(self.x, self.y),(attacker.x, attacker.y)]))

                
        elif v < weaponBlockRightChance:
            # Blocked (or else) with right hand item
            if self.rightHandEquipped.ItemClass == item.ItemClass.sword:
                # Parry if a sword
                self.messageLog.append(Message.Message(self.name + " parried " + attacker.name + "'s attack with the " + self.rightHandEquipped.Name,[(self.x, self.y),(attacker.x, attacker.y)]))              
                self.AttackWithWeapon(attacker, [self.GetWeaponToHit(self.rightHandEquipped) + self.ToHitMod(self.rightHandEquipped.ItemClass) + 0 if not self.GetTwoHanded() else self.ToHitMod(7), self.rightHandEquipped])
            else:
                self.messageLog.append(Message.Message(self.name + " blocks " + attacker.name+ "'s attack with the " + self.rightHandEquipped.Name,[(self.x, self.y),(attacker.x, attacker.y)]))
                
        else:
            # Dodged            
            self.messageLog.append(Message.Message(self.name + " dodges " + attacker.name + "'s attack ",[(self.x, self.y),(attacker.x, attacker.y)]))
            pass
        
        #print ("Shield Chance:", shieldBlockChance, " Weapon Block Left Chance:", weaponBlockLeftChance, " Weapon Black Right Chance:", weaponBlockRightChance)
        
    
    def Wait(self):
        self.ticksUntilTurn = round(100/self.speed)
        
    def Equip(self, item, slot):        
        if slot == 0:
            # Unequip
            if (self.rightHandEquipped != None):
                self.backpack.append(self.rightHandEquipped)

            # Unequip if two handed in other hand
            if (self.leftHandEquipped != None) and\
                (self.leftHandEquipped.TwoHanded == True):
                self.Equip(None, 1)

            self.rightHandEquipped = item
            if (item != None and item.TwoHanded):
                if (self.leftHandEquipped != None):
                    self.backpack.append(self.leftHandEquipped)
                    self.leftHandEquipped = None                    
                    
        if slot == 1:

            # Unequip
            if (self.leftHandEquipped != None):                
                self.backpack.append(self.leftHandEquipped)

            # Unequip if two handed in other hand
            if (self.rightHandEquipped != None) and\
                    (self.rightHandEquipped.TwoHanded == True):
                    self.Equip(None, 0)

            self.leftHandEquipped = item
            if (item != None and item.TwoHanded):
                if (self.rightHandEquipped != None):
                    self.backpack.append(self.rightHandEquipped)
                    self.rightHandEquipped = None
                    
        if item in self.backpack:
            self.backpack.remove(item)
        elif item in self.currentMap.Items:
            self.currentMap.Items.remove(item)
            
        # This prevents more then six items ending up in the backpack
        # when two are unequipped at the same time. One will go on the
        # floor.
        
        while (len(self.backpack) > self.backpackSize):
            # print (len(self.backpack))
            # (self.backpack[-1])
            self.Drop(self.backpack[-1])
        
    def Drop(self, item):
        if (self.rightHandEquipped == item):
            self.Equip(None, 0)
        if (self.leftHandEquipped == item):
            self.Equip(None, 1)
        if item in self.backpack:
            self.backpack.remove(item)
            item.x = self.x
            item.y = self.y
            self.currentMap.Items.append(item)
    
    def Pickup(self, item):
        if len(self.backpack) < self.backpackSize:
            self.backpack.append(item)
            self.currentMap.Items.remove(item)
            return True
        else:
            return False
            
    # se 0 through 6 are ItemClass skills
    # Skill 7 is Duel Wielding Skill
    
    def RegisterSkillHit(self, skill):
        hits, level = self.skills[skill]
        hits += 1
        
        if hits > self.NextLevelHitsNeeded(level, skill):
            hits = 0
            level += 1
            
        self.skills[skill] = hits, level        
    
    def NextLevelHitsNeeded(self, currentLevel, skill):
        if skill == 6:
            # Shields will get inflated real quick otherwise
            return round(25 * pow(1.3, currentLevel - 1))
        if skill == 0:
            # Help unarmed to be a bit beter
            return round(5 * pow(1.3, currentLevel - 1))
        else:
            return round(10 * pow(1.3, currentLevel - 1))
    
    def ToHitMod(self, skill):
        if skill == 0:
            #Unarmed
            return self.skills[skill][1]
        elif skill > 0 and skill < 6:
            # Weapon
            # I may change this to be per weapon
            return self.skills[skill][1] * 0.5
        elif skill == 6:
            # Shield
            return 0;
        elif skill == 7:
            # Duel Wielding
            return self.skills[skill][1] * 0.5 - 3
        
    def ToDefMod(self, skill):
        if skill == 0:
            #Unarmed
            return round(self.skills[skill][1] * 0.75)
            
        elif skill > 0 and skill < 6:
            return round(self.skills[skill][1] * 0.333)
        
        elif skill == 6:
            return self.skills[skill][1] * 0.5
            
        elif skill == 7:
            return round(self.skills[skill][1] * 0.166)
        
    def DmgMod(self, skill):
        if skill == 0:
            #Unarmed
            return round(self.skills[skill][1] * 1.5)
            
        elif skill > 0 and skill < 6:
            return round(self.skills[skill][1] * 0.66)
        
        elif skill == 6:
            return 0
        
        elif skill == 7:
            return 0
    
    def Ignite(self, chance, damage, source):
        if random.random() < chance*(10-max(9,self.GetShieldDV())):
            self.burning = True
            self.burnDamage = max(self.burnDamage, damage)
            self.burnSource = source
            self.burnWaitTurns = self.DEFAULT_BURN_WAIT_TURNS
            return (True, self.Attacked(damage, None))
        return (False, False)
        
    def Extinguish(self):
        if self.burning:
            self.burning = False
            self.burnDamage = 0
            self.burnSource = None
            self.burnWaitTurns = self.DEFAULT_BURN_WAIT_TURNS
            self.messageLog.append(Message.Message(self.name + " is no longer on fire",[(self.x, self.y)]))

    
    def Stun(self):
        self.ticksUntilTurn += round(200/self.speed)
    
    def GetRoute(self, dest):
        # Performs an A* search to find route to go somewhere
        # Input:
        #   x, y - from self.x and self.y
        #   self.currentMap.Walkable(x,y) - returns if can walk at x,y
        #   dest - (x, y) tuplet of destination
        #
        # Returns a list of (x, y) tuplets
        #
        # This does have a special behaviour that it will list the final square whether or not it can be 
        # walked on - so, it will attack if needed when position is fed to TryMove
        # 
        # From <http://www.policyalmanac.org/games/aStarTutorial.htm>
        # 1) Add the starting square (or node) to the open list.
        # 2) Repeat the following:
        #   a) Look for the lowest F cost square on the open list. We refer to this as the current square.
        #   b) Switch it to the closed list.
        #   c) For each of the 8 squares adjacent to this current square 
        #      If it is not walkable or if it is on the closed list, ignore it. Otherwise do the following.           
        #      If it isn't on the open list, add it to the open list. Make the current square the parent of this square. Record the F, G, and H costs of the square. 
        #      If it is on the open list already, check to see if this path to that square is better, using G cost as the measure. A lower G cost means that this is a better path. If so, change the parent of the square to the current square, and recalculate the G and F scores of the square. If you are keeping your open list sorted by F score, you may need to resort the list to account for the change.
        #   d) Stop when you:
        #      Add the target square to the closed list, in which case the path has been found (see note below), or
        #      Fail to find the target square, and the open list is empty. In this case, there is no path.   
        # 3) Save the path. Working backwards from the target square, go from each square to its parent square until you reach the starting square. That is your path.
        
        # This is to prevent bugs
        if dest == None:
            return None
        
        # ORTH_DISTANCE and DIAG_DISTANCE are for weights of travelling between the cells orthogonally
        # and diagonally respectively. If diagoanal is further in game, then DIAG_DISTANCE should be 14
        # As the distances are the same in mine, they're weighted evenly
        ORTH_DISTANCE = 10
        DIAG_DISTANCE = 10
        
        # Heuristic for calculating h is Manhattan Distance - 
        #   abs(pos.x - dest.x) + abs(pos.y - dest.y)
        
        # OpenLists consists of tuplets with (
        #   [0]: Position.x, 
        #   [1]: Position.y,
        #   [2]: ParentPosition.x, 
        #   [3]: ParentPosition.y,
        #   [4]: g (distance to get here from parent),
        #   [5]: h (heuristic distance to destination) )
        OpenList = [(self.x, self.y, self.x, self.y, 0, abs(self.x-dest[0]) + abs(self.y-dest[1]))]     
        ClosedList = []                        
        
        Found = None
        
        while (len(OpenList) > 0 and Found == None):                
            # Find entry in OpenList with lowest F score
            # F = G + H                 
            Current = min(OpenList, key=lambda i:i[4]+i[5])         
            OpenList.remove(Current)
            ClosedList.append(Current)
            Active = [(Current[0] - 1,  Current[1],     Current[0], Current[1], Current[4] + ORTH_DISTANCE, abs(Current[0] - 1 - dest[0])   + abs(Current[1] - dest[1])),
                (Current[0] + 1,    Current[1],     Current[0], Current[1], Current[4] + ORTH_DISTANCE, abs(Current[0] + 1 - dest[0])   + abs(Current[1] - dest[1])),
                (Current[0] - 1,    Current[1] - 1, Current[0], Current[1], Current[4] + DIAG_DISTANCE, abs(Current[0] - 1 - dest[0])   + abs(Current[1] - 1 - dest[1])),
                (Current[0] + 1,    Current[1] - 1, Current[0], Current[1], Current[4] + DIAG_DISTANCE, abs(Current[0] + 1 - dest[0])   + abs(Current[1] - 1 - dest[1])),
                (Current[0] - 1,    Current[1] + 1, Current[0], Current[1], Current[4] + DIAG_DISTANCE, abs(Current[0] - 1 - dest[0])   + abs(Current[1] + 1 - dest[1])),
                (Current[0] + 1,    Current[1] + 1, Current[0], Current[1], Current[4] + DIAG_DISTANCE, abs(Current[0] + 1 - dest[0])   + abs(Current[1] + 1 - dest[1])),
                (Current[0],        Current[1] - 1, Current[0], Current[1], Current[4] + ORTH_DISTANCE, abs(Current[0] - dest[0])       + abs(Current[1] - dest[1] - 1)),
                (Current[0],        Current[1] + 1, Current[0], Current[1], Current[4] + ORTH_DISTANCE, abs(Current[0] + dest[0])       + abs(Current[1] - dest[1] + 1))]
            for i in Active:
                # If point not in closed list and is walkable
                # Remove the or (i[0] == dest[0] and i[1] == dest[1] to prevent the special behaviour
                if ((len([j for j in ClosedList if j[0] == i[0] and j[1] == i[1]]) == 0)\
                    and (self.currentMap.Walkable(i, True) or (i[0] == dest[0] and i[1] == dest[1]))):
                        
                    # Look for point in open List
                    Candidate = [j for j in OpenList if j[0] == i[0] and j[1] == i[1]]
                    # If point not in open list                 
                    if(len(Candidate) == 0):
                        # Add point to the open list
                        OpenList.append(i)
                        if (i[0] == dest[0] and i[1] == dest[1]):
                            Found = i
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

        
    
                    
