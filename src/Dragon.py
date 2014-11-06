from enemy import *
import Message
import copy

# The dragon is a special and unique enemy, hence these values are hardcoded

class Dragon(Enemy):
    def __init__(self, messageLog,  currentMap = None):
        super().__init__(messageLog, currentMap)
        self.name = "True Dragon"
        self.level = 10
        self.character = "D"        
        self.speed = 14
        self.hp = self.maxhp = 30
        self.mp = self.maxmp = 16
        self.mpChargeRate = 2
        self.baseDamage =  10
        self.baseToHit =  8
        self.baseToDefend = 6
        self.burnDamage = 3
        self.color = "red"      
        self.runningTo = None
        self.chartype = "TrueDragon"
        
    def danger(self):
        return 15
    
    def update(self):           
        super().update()
        
        # If flame had been breathed out, release it. Do nothing else that turn.
        if self.FlameReady != None:
            self.CastFlameBreath(*self.FlameReady)
            self.FlameReady = None
            return
        
        # Find the nearest enemy
        try:            
            nearestEnemy = min([i for i in self.currentMap.characters if i != self and i.team != self.team],
                key = lambda i: abs(self.x - i.x) + abs(self.y - i.y))
        
            nearestEnemy_dx = 0 if nearestEnemy.x == self.x else (1 if nearestEnemy.x < self.x else 1)
            nearestEnemy_dy = 0 if nearestEnemy.y == self.y else (1 if nearestEnemy.y < self.y else 1)
            
            # Find the range of the nearest enemy. If the nearest enemy is in an adjacent cell, ensure range is 1
            # (rather then sqrt 2 if diagonal for instance)
            nearestEnemy_range = math.sqrt(math.pow(abs(self.x-nearestEnemy.x),2) + math.pow(abs(self.y-nearestEnemy.y),2)) 
            if (nearestEnemy_range < 1.5):
                nearestEnemy_range = 1              
        
            # print ("nearestEnemy_range ", nearestEnemy_range, ' nearestEnemy_dx ', nearestEnemy_dx, ' nearestEnemy_dy ', nearestEnemy_dy)
        except ValueError:
            nearestEnemy = None
            nearestEnemy_range = 20
            
        # Find the nearest healer. The dragon might want to try to get healed       
        Healers = [(i.x, i.y) for i in self.currentMap.characters if i != self and i.team == self.team and i.chartype == "Healer"]
        #print (Healers)
        if len(Healers) > 0:
            # If healer in same room, no change necessary       
            if (self.currentMap.GetRooms(self.x, self.y) in itertools.chain(map(lambda i: self.currentMap.GetRooms(i[0],i[1]), Healers))):
                RouteToHealer = (self.x, self.y)
            else:
                RouteToHealer = self.GetNearest(lambda i: (i[0],i[1]) in Healers)   
        else:
            RouteToHealer = None
        
        # Three steps away. Find if there is a route to 3 steps from any enemies. 
        # 3 Steps is in fire range, out of melee range
        # 3StepRoute = self.GetNearest(lambda i: (max(abs(self.x-i[0]),abs(self.y-i[1]))>2))        
                            
        # Risk to self.                     
        Danger = self.GetRoomDanger()
        
        # Risk to target (if there is one)
        if self.Target == None or self.Target.living == False:
            self.Target = nearestEnemy
            
        if self.Target != None and self.Target.living == True:
            DangerToTargetMelee = self.GetAverageDamage(self.Target.ToDefend(), self.Target.level)/max(1,self.Target.hp)
            DangerToTargetRange = self.burnDamage * 3 / max(1,self.Target.hp)
        
        # Pick what the preferred state should be
        if Danger > 0.6:
            if self.Target == None or self.Target.living == False:
                self.Target = nearestEnemy
                if self.Target != None and self.Target.living == True:
                    DangerToTargetMelee = self.GetAverageDamage(self.Target.ToDefend(), self.Target.level)/self.Target.hp
                    DangerToTargetRange = self.burnDamage * 3 / self.Target.hp

            if DangerToTargetMelee > 0.6:
                self.State = "berserk"
            else:
                self.State = "retreat"
        
        else:
            if self.State == None:
                self.State = "idle"
            elif self.State == "idle":
                if Danger > 0:
                    self.State = "attack"
                if Danger > 0.6:
                    self.State = "retreat"
            elif self.State == "berserk":
                self.State = "attack"
            elif self.State != "retreat":
                self.State = "attack"           
            elif self.State == "retreat":
                if self.hp > (self.maxhp - 3):
                    self.State = "attack"
                if self.runningTo != None:
                    if self.runningTo[0] == self.x and self.runningTo[1] == self.y:
                        self.State = "idle"
                if RouteToHealer == None:
                    self.State = "berserk"

        if self.State == "idle":
            self.Wait()
            return
            
        if self.State == "berserk":
            # Check if can burn
            CanBurn =  self.FlameBreathMPCost(max(4,nearestEnemy_range+2),5) <= self.mp
            ShouldBurn = nearestEnemy_range > 1 and (not nearestEnemy.burning)
            
            if CanBurn and ShouldBurn:
                self.PrepareFlameBreath((nearestEnemy.x, nearestEnemy.y),max(4,nearestEnemy_range+2),5)
                return
                
            else:
                # Attack with Melee or move towards enemy
                MovePos = self.GetRoute((nearestEnemy.x, nearestEnemy.y))
                if MovePos == None or len(MovePos) == 0:
                    self.Wait()
                    return;             
                MovePos = MovePos[1]        
                self.tryMove(MovePos[0], MovePos[1])
                return
        
        if self.State == "retreat":
            
            # Even if running away, unleash some flaming breath on the way if possible.
            # Need to be a bit further away though.
            CanBurn =  self.FlameBreathMPCost(max(4,nearestEnemy_range+2),5) <= self.mp
            ShouldBurn = nearestEnemy_range > 3 and (not nearestEnemy.burning)          
            if CanBurn and ShouldBurn:
                self.PrepareFlameBreath((nearestEnemy.x, nearestEnemy.y),max(4,nearestEnemy_range+2),5)
                return
                
            else:
                MovePos = None
                
                # Otherwise, run towards the healer, if not in same room. If same room, try to stay
                # a distance from player. If no healer, pick a room and run there.
                
                if RouteToHealer == (self.x, self.y):
                # Healer in same room:
                    MovePos = self.GetNearest(lambda i: (max(abs(i[0]-nearestEnemy.x),abs(i[1]-nearestEnemy.y))>2))
                
                elif RouteToHealer != None and len(RouteToHealer) > 0:
                # Healer in different room:
                    MovePos = RouteToHealer
                
                elif self.runningTo != None:
                    MovePos = self.GetRoute(self.runningTo)
                
                else:
                    room = random.choice(self.currentMap.Rooms)
                    runningTo = (room.x + round(room.w / 2), room.y + round(room.y / 2))
                    # Not sure why this is necessary - potential bug
                    if runningTo != None:
                        MovePos = self.GetRoute(self.runningTo)         
                    
                if MovePos == None or len(MovePos) == 0:
                    self.Wait()
                    return;             
                MovePos = MovePos[1]                                            
                self.tryMove(MovePos[0], MovePos[1])
                return
        
        if self.State == "attack":
            # A dragon will avoid melee and rely on its flame breath when attacking.
            # It will try to stay 2 away to do a burn (because of the time)
            # In attack move, it's willing to blow bigger fires. This is mostly because it's cool. 
            desireRange = max(3, nearestEnemy_range + 1) + random.choice([1,1,1,2,2,2,2,3,3,3,4])
            desireRadius = random.choice([4,4,5,5,5])
            CanBurn =  self.FlameBreathMPCost(desireRange, desireRadius) <= self.mp
            ShouldBurn = (nearestEnemy_range > 1 or Danger < 0.2) and (not nearestEnemy.burning)
            #print ("Can Burn:", CanBurn, " MP Cost ", self.FlameBreathMPCost(desireRange, desireRadius), " MP ", self.mp)
            #print ("Should Burn:", ShouldBurn, " NearestEnemy_Range: ", nearestEnemy_range, " NearestEnemy.Burning: ", nearestEnemy.burning) 
            
            if CanBurn and ShouldBurn:
                self.PrepareFlameBreath((nearestEnemy.x, nearestEnemy.y), desireRange, desireRadius)
            
            if nearestEnemy_range == 1:
                if random.random() < 0.5:
                    MovePos = self.GetRoute((nearestEnemy.x, nearestEnemy.y))
                else:
                    MovePos = self.GetNearest(lambda i: (max(abs(i[0]-nearestEnemy.x),abs(i[1]-nearestEnemy.y))==2))
                    if MovePos == None:
                        MovePos = self.GetRoute((nearestEnemy.x, nearestEnemy.y))
                if MovePos == None or len(MovePos) == 0:
                    self.Wait()
                    return;             
                MovePos = MovePos[1]                            
                self.tryMove(MovePos[0], MovePos[1])
                return
            
            elif nearestEnemy_range >= 2:
                MovePos = self.GetNearest(lambda i: 2 < (max(abs(i[0]-nearestEnemy.x),abs(i[1]-nearestEnemy.y))) < 5)               
                
                if MovePos == None:
                    MovePos = self.GetNearest(lambda i: (max(abs(i[0]-nearestEnemy.x),abs(i[1]-nearestEnemy.y))>1))
                    if MovePos == None:
                        MovePos = self.GetRoute((nearestEnemy.x, nearestEnemy.y))
                if MovePos == None or len(MovePos) == 0:
                    self.Wait()
                    return;             
                MovePos = MovePos[1]
                self.tryMove(MovePos[0], MovePos[1])
                return
    

    def Attacked(self, damage, attacker):
        dead = super().Attacked(damage, attacker)
        
        # Give the player the best weapon for them
        if dead:
            # Get best weapon skill
            bestSkill = max([i for i in enumerate(attacker.skills) if i[0] < 6], key=lambda j: j[1][1])
            bestWeapon = [i for i in self.currentMap.defaultItems if i.Artifact == True and i.ItemClass == bestSkill[0]][0]
            item = copy.deepcopy(bestWeapon)
            item.x = self.x
            item.y = self.y
            self.currentMap.Items.append(item)
