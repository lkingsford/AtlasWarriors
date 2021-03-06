from enemy import *
import random
import Message
import animation

class Warlord(Enemy):
    def __init__(self, messageLog, currentMap = None):
        super().__init__(messageLog, currentMap)
        self.name = "High Warlord"
        self.level = 15           
        self.character = "W"        
        self.speed = 20
        self.hp = self.maxhp = 40
        self.baseDamage =  10
        self.baseToHit =  17
        self.baseToDefend = 15
        self.color = "fuchsia"      
        self.chartype = "endboss"
        # died is used to prevent healers rehealing the dead warlord back to
        # life.
        self.died = False
        
    
    def danger(self):       
        return 500
    
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
        

    def Attacked(self, damage, attacker, melee = True):
        dead = super().Attacked(damage, attacker, melee)
        
        # Big death animation explosion!
        if dead:
            self.killedBy = attacker
            self.animations.append(animation.DrawWarlordDeath((self.x,self.y)))
            self.died = True

    def dead(self):
        return self.died;

    # Special version needed because of the pumping up damage. This is not really what it was intended for, but it saves
    # a lot of programming. This returns the unarmed skill to 0 every hit.
    def RegisterSkillHit(self, skill):
        self.skills[skill] = 0,0

    def Victory(self):
        # Returns 0 if game still going
        # Returns 1 if game won normally
        # Returns 2 if killed by a normal monster (normally a goliath)
        # Returns 3 if killed by a demonic goliath
        # Returns 4 if killed by an apocolyptic goliath
        # Returns 5 if killed by the true dragon
        # Returns 6 if killed by the necromancer
        if self.died:
            if self.killedBy.chartype == "PC":
                return 1
            elif self.killedBy.chartype == "Goliath" and self.killedBy.badass == 9:
                return 3
            elif self.killedBy.chartype == "Goliath" and self.killedBy.badass == 10:
                return 4
            elif self.killedBy.chartype == "TrueDragon":
                return 5
            elif self.killedBy.chartype == "Necromancer":
                return 6
            else:
                return 2
        else:
            return 0
