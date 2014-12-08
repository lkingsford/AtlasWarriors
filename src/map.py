import random
import enemy
import bisect
import itertools
import copy
import pygame
import Bandit
import Goliath
import Necromancer
import Critter
import Assassin
import Orc
import Dragon
import Drake
import Healer
import Zombie
import Warlord
import Message

# The cells of the map
class Cell:
    def __init__ (self, character = '.',
        walkable = True,
        forecolor = 'silver',
        backcolor = None,
        walkbehavior = 'none'):
        self.walkable = walkable
        self.character = character
        self.forecolor = forecolor
        self.backcolor = backcolor
        self.walkbehavior = walkbehavior
        self.rooms = set([])
    
    def OnWalk(self, character):
        pass
    
class CloseDoorCell(Cell):
    def __init__(self, target, character = '.',
        walkable = True,
        forecolor = 'silver',
        backcolor = None,
        walkbehavior = 'none'):
        super().__init__(character, walkable, forecolor, backcolor, walkbehavior)
        self.target = target

    def OnWalk(self, character):
        if character.chartype == "PC":
            self.target.walkable = False
            self.target.character = "#"

class Room:
#  BuildDir Reference:
#
#     1         2         3        4   
#
#                         X  
#   #####      #####    #####    #####
#   #####     X#####    #####    #####X
#   #####      #####    #####    #####
#     X
#
    
    def __init__(self, x, y, w, h, buildDir = 0, shape = 0):
        self.w = w
        self.h = h
        self.shape = shape
        
        if shape == 0: # shape can be random
            self.shape = 1 # There's only one shape at the moment
        
        self.Contains = [] # All of the cells in the room. 
        
        # Some monsters care if it is occupied
        # Some don't. It effects placement.
        self.occupied = False
        
        if self.shape == 1:
            if (buildDir == 0):
                self.x = x
                self.y = y
            elif buildDir == 1:     
                self.x = x - round(w/2)
                self.y = y - h
            elif buildDir == 3: 
                self.x = x - round(w/2)
                self.y = y + 1
            elif buildDir == 2:
                self.x = x + 1
                self.y = y - round(h/2)
            elif buildDir == 4:
                self.x = x - w
                self.y = y - round(h/2)
            
            self.exits = []
            if (self.w // 2) < 2: 
                self.exits.append((self.x + round(w/2), self.y - 1, 1, self))
                self.exits.append((self.x + round(w/2), self.y + h, 3, self))
            else:
                for i in range(self.x, self.x + self.w - 1, 2):
                    self.exits.append((i, self.y - 1, 1, self))
                    self.exits.append((i, self.y + h, 3, self))
            if (self.h // 2) < 2:
                self.exits.append((self.x - 1, self.y + round(h/2), 4, self))
                self.exits.append((self.x + w, self.y + round(h/2), 2, self))
            else:
                for i in range(self.y, self.y + self.h - 1, 2):
                    self.exits.append((self.x - 1, i, 4, self))
                    self.exits.append((self.x + w, i, 2, self))
                
                
            #0 is unseen
            #1 is seen (but not in sight)
            #2 is seen
            self.seenStatus = 0
    
            for x in range(self.x-1, self.x+self.w+1):
                for y in range(self.y-1, self.y+self.h+1):
                    self.Contains.append((x,y))
        

    def Dig(self, map):
        raise NotImplemented
        
    def InRoom(self, x, y):
        # If rectangle
        if self.shape == 1:
            return x > self.x - 1 and x < self.x + self.w +1  and y > self.y - 1 and y < self.y + self.h + 1
        
    # This is to enable the Zombie level
    # The room only has exits in the 4 cardinal directions, in the middle
    def LimitToMiddleExits(self):
        self.exits = []
        self.exits.append((self.x + round(self.w/2), self.y - 1, 1, self))
        self.exits.append((self.x + round(self.w/2), self.y + self.h, 3, self))
        self.exits.append((self.x - 1, self.y + round(self.h/2), 4, self))
        self.exits.append((self.x + self.w, self.y + round(self.h/2), 2, self))

# Things like doors - anything that needs you to see both sides when standing
# there
class Gateway:
    def __init__(self, x, y, connectedRooms = []):
        self.connectedRooms = connectedRooms
        self.x = x
        self.y = y

class Map:
    # Generate a new map
    def __init__(self, level, messageLog, defaultItems, difficulty):
        
        self.Turn = 0
        
        self.difficulty = difficulty
        
        # This is used for the scores
        self.RestockDangerPoints = 0
        
        self.NextTurn = None
        
        self.BuildExtraDoorChance = .3  # Chance of building another door if exits align
        
        self.messageLog = messageLog
        
        #Initialise Map
        self.Map = [[0 for y in range(20)] for x in range(40)]

        self.VisibilityMap = [[0 for y in range(20)] for x in range(40)]
        for x in range(40):
            for y in range(20):
                self.VisibilityMap[x][y] = 0
        
        # These are for speeding up the zombie DV modifiers
        # They are effected and altered by the AddZombie and RemoveZombie
        # procedures
        self.ZombieLocations = [[0 for y in range(20)] for x in range(40)]
        for x in range(40):
            for y in range(20):
                self.ZombieLocations[x][y] = False
        
        self.ZombieMod = [[0 for y in range(20)] for x in range(40)]
        for x in range(40):
            for y in range(20):
                self.ZombieMod[x][y] = 0
        
        
        #Build outside walls 
        for x in range(40):
            self.Map[x][0] = Cell('#', False, 'red')
            self.Map[x][19] = Cell('#', False, 'red')
    
        for y in range(19):
            self.Map[0][y] = Cell('#', False, 'red')
            self.Map[39][y] = Cell('#', False, 'red')
        
        # Level is the current level number
        self.level = level      
        # Danger level is the current monsters level generated.
        # Increases over time
        self.dangerLevel = level
    
        self.Items = [] 
        if level == 7:
            self.NecromancerLevelGenerator()
        elif level == 8:
            #needs at least 1 hugeass room          
            self.DragonLevelGenerator()
        elif level == 9:
            self.CourtGenerator()

        else:
            self.HackAwayGenerator()    
        
                
        #Up/Start and Down
        self.startX = self.Rooms[0].x + round(self.Rooms[0].w / 2)
        self.startY = self.Rooms[0].y + round(self.Rooms[0].h / 2)
        
        self.endRoom = self.Rooms[0]
        while (self.endRoom == self.Rooms[0]):
            self.endRoom = random.choice(self.Rooms)
            
        self.endX = self.endRoom.x + round(self.endRoom.w / 2)
        self.endY = self.endRoom.y + round(self.endRoom.h / 2)
        
        #add some enemies               
        
        self.defaultItems = defaultItems
        
        self.characters = []
        
        # This is WAY to specific. This should be generalised one day.
       
    
        if level == 0:
            while sum([i.danger() for i in self.characters]) < 20:
                random.choice([self.AddCritters,
                    self.AddBandits])()
        if level == 1:
            while sum([i.danger() for i in self.characters]) < 30:
                random.choice([self.AddCritters,
                    self.AddBandits,
                    self.AddOrcs])()    
        if level == 2:
            while sum([i.danger() for i in self.characters]) < 40:
                random.choice([self.AddCritters,
                    self.AddBandits,
                    self.AddOrcs,
                    self.AddGoliath])()
        if level == 3:
            while sum([i.danger() for i in self.characters]) < 50:
                random.choice([self.AddCritters,
                    self.AddBandits,
                    self.AddOrcs,
                    self.AddGoliath,
                    self.AddHealers])()
                    
        if level == 4:
            while sum([i.danger() for i in self.characters]) < 60:
                random.choice([self.AddCritters,
                    self.AddBandits,
                    self.AddOrcs,
                    self.AddGoliath,
                    self.AddHealers,
                    self.AddAssassins])()
                    
        if level == 5:
            while sum([i.danger() for i in self.characters]) < 70:
                random.choice([self.AddCritters,
                    self.AddBandits,
                    self.AddOrcs,
                    self.AddGoliath,
                    self.AddHealers,
                    self.AddAssassins,
                    self.AddDrake])()
                    
        if level == 6:
            while sum([i.danger() for i in self.characters]) < 70:
                random.choice([self.AddCritters,
                    self.AddBandits,
                    self.AddOrcs,
                    self.AddGoliath,
                    self.AddHealers,
                    self.AddAssassins,
                    self.AddDrake,
                    self.AddZombies])()
                    
        if level == 7:
            self.AddNecromancer()
            while sum([i.danger() for i in self.characters]) < 90:
                self.AddZombies()
                
        if level == 8:
            self.AddDragon()            
            while sum([i.danger() for i in self.characters]) < 80:
                random.choice([self.AddCritters,
                    self.AddBandits,
                    self.AddOrcs,
                    self.AddGoliath,
                    self.AddHealers,
                    self.AddAssassins,
                    self.AddDrake,
                    self.AddZombies])()
        
        if level == 9:
            # I don't know if this special case for difficulty should be
            # here on in difficulty.py
            #            
            if self.difficulty.difficulty == 0:
                for i in self.Rooms[2:14]:
                    self.AddCritters(i)
                for i in self.Rooms[14:16]:
                    self.AddBandits(i)
                for i in self.Rooms[16:18]:
                    self.AddOrcs(i)
                for i in self.Rooms[18:22]:
                    random.choice([self.AddCritters,
                    self.AddBandits,
                    #self.AddOrcs,
                    self.AddGoliath,
                    #self.AddHealers,
                    self.AddAssassins,
                    self.AddDrake,
                    self.AddZombies])(i)
                self.AddGoliath(self.Rooms[1])
                self.AddGoliath(self.Rooms[1])
            elif self.difficulty.difficulty == 1:
                for i in self.Rooms[2:10]:
                    self.AddCritters(i)
                for i in self.Rooms[10:14]:
                    self.AddBandits(i)   
                for i in self.Rooms[14:16]:
                    self.AddOrcs(i)
                for i in self.Rooms[16:22]:
                   random.choice([self.AddCritters,
                   self.AddBandits,
                   #self.AddOrcs,
                   self.AddGoliath,
                   #self.AddHealers,
                   self.AddAssassins,
                   self.AddDrake,
                   self.AddZombies])(i)
                self.AddGoliath(self.Rooms[1])
                self.AddGoliath(self.Rooms[1])
                self.AddGoliath(self.Rooms[1])
            elif self.difficulty.difficulty == 2:
                for i in self.Rooms[2:8]:
                    self.AddCritters(i)
                for i in self.Rooms[8:12]:
                    self.AddBandits(i)
                for i in self.Rooms[12:14]:
                    self.AddOrcs(i)                    
                for i in self.Rooms[14:22]:
                   random.choice([self.AddCritters,
                   self.AddBandits,
                   #self.AddOrcs,
                   self.AddGoliath,
                   #self.AddHealers,
                   self.AddAssassins,
                   self.AddDrake,
                   self.AddZombies])(i)
                self.AddGoliath(self.Rooms[1])
                self.AddGoliath(self.Rooms[1])
                self.AddGoliath(self.Rooms[1])
                self.AddGoliath(self.Rooms[1])
            elif self.difficulty.difficulty == 3:
                for i in self.Rooms[2:22]:
                    random.choice([self.AddCritters,
                    self.AddBandits,
                    self.AddOrcs,
                    self.AddGoliath,
                    #self.AddHealers,
                    self.AddAssassins,
                    self.AddDrake,
                    self.AddZombies])(i)
                self.AddGoliath(self.Rooms[1])
                self.AddGoliath(self.Rooms[1])
                self.AddGoliath(self.Rooms[1])
                self.AddGoliath(self.Rooms[1])
                self.AddGoliath(self.Rooms[1])
                self.AddGoliath(self.Rooms[1])
            
            self.AddHealers(self.Rooms[1])
            self.AddHealers(self.Rooms[1])
            self.AddWarlord(self.Rooms[1])
        
        for i in range(random.randrange(1, 3)):
            room = random.choice(self.Rooms)
            item = copy.deepcopy(self.ChooseItem(level))
            item.x = (random.randrange(room.x, room.x+room.w)) if (room.x != room.x+room.w) else (room.x)
            item.y = (random.randrange(room.y, room.y+room.h)) if (room.y != room.y+room.h) else (room.y)
            
            # LK - Fixes bug #6 (5/11/2014)            
            while (self.Map[item.x][item.y].walkbehavior != 'none'):
                item.x = (random.randrange(room.x, room.x+room.w)) if (room.x != room.x+room.w) else (room.x)
                item.y = (random.randrange(room.y, room.y+room.h)) if (room.y != room.y+room.h) else (room.y)           
            
            self.Items.append(item)
        
        if level != 0:          
            self.Map[self.startX][self.startY] = Cell('<', True, 'white', 'blue', 'go up')
        if level != 9:          
            self.Map[self.endX][self.endY] = Cell('>', True, 'white', 'green', 'go down')   
        
        self.visibilityUpdated = True   

    
    def HackAwayGenerator (self):
        for x in range(40):
            for y in range(20):
                red = (10-self.level) * 16 + 84 - random.randint(0, 64+(self.level * 4))  
                self.Map[x][y] = Cell('#', False, pygame.Color(red,0,0))
        
        self.Doors = []
        self.Rooms = [Room(             
            random.randrange(15,20),
            random.randrange(6, 10),
            random.randrange(3, 10),
            random.randrange(3, 6))]                
                    
        desiredRoomCount = random.randrange(10,20)
        maxtries = 2000
        currenttry = 0
        
        exits = []
        exits.extend(self.Rooms[0].exits)
        
        while len(self.Rooms) < desiredRoomCount and maxtries > currenttry:
            currenttry += 1
            newExit = random.choice(exits)                  
            nextX, nextY, nextDir, baseRoom = newExit
            #nextX, nextY, nextDir = random.choice(Rooms).exits[0]  
            newW, newH = random.randrange(1, 15), random.randrange(1, 10)
            #print(nextX, nextY, nextDir, newW, newH)
            newRoom = Room(nextX, nextY, newW, newH, nextDir)
            fits = True
            for j in self.Rooms:
                #print('->', (newRoom.x > j.x + j.w), (newRoom.x + newRoom.w < j.x), (newRoom.y > j.y + j.h), (newRoom.y + newRoom.h < j.h), (newRoom.x > 0), (newRoom.x + newRoom.w < 40), (newRoom.y > 0),(newRoom.y + newRoom.h < 20)) 
                fits = fits and \
                    ((newRoom.x > j.x + j.w) or \
                    (newRoom.x + newRoom.w < j.x) or \
                    (newRoom.y > j.y + j.h) or \
                    (newRoom.y + newRoom.h < j.y)) and \
                    (newRoom.x > 0) and \
                    (newRoom.x + newRoom.w < 40) and \
                    (newRoom.y > 0) and \
                    (newRoom.y + newRoom.h < 20)
            if fits == True:
                self.Rooms.append(newRoom)              
                exits.extend(newRoom.exits)
                exits.remove(newExit)
                self.Doors.append(Gateway(nextX, nextY, [baseRoom, newRoom]))   

        for i, k in itertools.permutations(self.Rooms, 2):
            for j in i.exits:
                for l in k.exits:
                    if j[0] == l[0] and j[1] == l[1]:
                        if random.random() < self.BuildExtraDoorChance:
                            self.Doors.append(Gateway(j[0], j[1], [i, k]))

        for i in self.Rooms:
            for x in range(i.x, i.x+i.w):
                for y in range(i.y, i.y+i.h):
                    brightness = random.randint(52-self.level*2,64)
                    self.Map[x][y] = Cell('.', True, pygame.Color(brightness, brightness, brightness))
                    self.Map[x][y].rooms.add(i)
        
        for i in self.Doors:
            self.Map[i.x][i.y] = Cell(',', True, 'blue')
            for j in i.connectedRooms:
                self.Map[i.x][i.y].rooms.add(j)

    def NecromancerLevelGenerator(self):
        for x in range(40):
            for y in range(20):
                brightness = random.randint(32,100)
                self.Map[x][y] = Cell('#', False, pygame.Color(brightness, brightness, brightness))
        
        self.Doors = []
        self.Rooms = []
        
        startRoom = Room(               
            random.randrange(0,7) * 5+1,
            1,
            5,
            5)
        
        startRoom.LimitToMiddleExits()
        
        self.Rooms = [startRoom]
                    
        desiredRoomCount = 20
        maxtries = 2000
        currenttry = 0
        
        exits = []
        exits.extend(self.Rooms[0].exits)
        
        while len(self.Rooms) < desiredRoomCount and maxtries > currenttry:
            currenttry += 1
            newExit = random.choice(exits)                  
            nextX, nextY, nextDir, baseRoom = newExit
            #nextX, nextY, nextDir = random.choice(Rooms).exits[0]  
            newW, newH = 5,5
            #print(nextX, nextY, nextDir, newW, newH)
            newRoom = Room(nextX, nextY, newW, newH, nextDir)
            fits = True
            for j in self.Rooms:
                #print('->', (newRoom.x > j.x + j.w), (newRoom.x + newRoom.w < j.x), (newRoom.y > j.y + j.h), (newRoom.y + newRoom.h < j.h), (newRoom.x > 0), (newRoom.x + newRoom.w < 40), (newRoom.y > 0),(newRoom.y + newRoom.h < 20)) 
                fits = fits and \
                    ((newRoom.x > j.x + j.w) or \
                    (newRoom.x + newRoom.w < j.x) or \
                    (newRoom.y > j.y + j.h) or \
                    (newRoom.y + newRoom.h < j.y)) and \
                    (newRoom.x > 0) and \
                    (newRoom.x + newRoom.w < 40) and \
                    (newRoom.y > 0) and \
                    (newRoom.y + newRoom.h < 20)
            if fits == True:
                newRoom.LimitToMiddleExits()
                self.Rooms.append(newRoom)                              
                exits.extend(newRoom.exits)
                exits.remove(newExit)
                self.Doors.append(Gateway(nextX, nextY, [baseRoom, newRoom]))   

        for i, k in itertools.permutations(self.Rooms, 2):
            for j in i.exits:
                for l in k.exits:
                    if j[0] == l[0] and j[1] == l[1]:
                        if random.random() < self.BuildExtraDoorChance:
                            self.Doors.append(Gateway(j[0], j[1], [i, k]))

        for i in self.Rooms:
            for x in range(i.x, i.x+i.w):
                for y in range(i.y, i.y+i.h):
                    brightness = random.randint(32,48)
                    self.Map[x][y] = Cell('.', True, pygame.Color(brightness, brightness, brightness))
                    self.Map[x][y].rooms.add(i)
        
        for i in self.Doors:
            self.Map[i.x][i.y] = Cell(',', True, 'blue')    
            for j in i.connectedRooms:
                self.Map[x][y].rooms.add(j)

    def DragonLevelGenerator (self):
        for x in range(40):
            for y in range(20):
                self.Map[x][y] = Cell('#', False, pygame.Color(random.randint(128,196), random.randint(32,64), random.randint(32,64)))              
                
        self.Rooms = [
            Room(8, 6, 4, 4),
            Room(13, 5, 20, 10)]
        self.Doors = [Gateway(12,7,[self.Rooms[0], self.Rooms[1]])]
                    
        desiredRoomCount = random.randrange(10,20)
        maxtries = 2000
        currenttry = 0
        
        exits = []
        exits.extend(self.Rooms[0].exits)
        
        while len(self.Rooms) < desiredRoomCount and maxtries > currenttry:
            currenttry += 1
            newExit = random.choice(exits)                  
            nextX, nextY, nextDir, baseRoom = newExit
            #nextX, nextY, nextDir = random.choice(Rooms).exits[0]  
            newW, newH = random.randrange(1, 15), random.randrange(1, 10)
            #print(nextX, nextY, nextDir, newW, newH)
            newRoom = Room(nextX, nextY, newW, newH, nextDir)
            fits = True
            for j in self.Rooms:
                #print('->', (newRoom.x > j.x + j.w), (newRoom.x + newRoom.w < j.x), (newRoom.y > j.y + j.h), (newRoom.y + newRoom.h < j.h), (newRoom.x > 0), (newRoom.x + newRoom.w < 40), (newRoom.y > 0),(newRoom.y + newRoom.h < 20)) 
                fits = fits and \
                    ((newRoom.x > j.x + j.w) or \
                    (newRoom.x + newRoom.w < j.x) or \
                    (newRoom.y > j.y + j.h) or \
                    (newRoom.y + newRoom.h < j.y)) and \
                    (newRoom.x > 0) and \
                    (newRoom.x + newRoom.w < 40) and \
                    (newRoom.y > 0) and \
                    (newRoom.y + newRoom.h < 20)
            if fits == True:
                self.Rooms.append(newRoom)              
                exits.extend(newRoom.exits)
                exits.remove(newExit)
                self.Doors.append(Gateway(nextX, nextY, [baseRoom, newRoom]))   

        for i, k in itertools.permutations(self.Rooms, 2):
            for j in i.exits:
                for l in k.exits:
                    if j[0] == l[0] and j[1] == l[1]:
                        if random.random() < self.BuildExtraDoorChance:
                            self.Doors.append(Gateway(j[0], j[1], [i, k]))

        for i in self.Rooms:
            for x in range(i.x, i.x+i.w):
                for y in range(i.y, i.y+i.h):
                    brightness = random.choice([random.randint(32,48), 16])
                    self.Map[x][y] = Cell('.', True, pygame.Color(brightness, brightness, brightness))
                    self.Map[x][y].rooms.add(i)
        
        for i in self.Doors:
            self.Map[i.x][i.y] = Cell(',', True, 'blue')    
            for j in i.connectedRooms:
                self.Map[x][y].rooms.add(j)

    def CourtGenerator (self):
        for x in range(40):
            for y in range(20):
                self.Map[x][y] = Cell('#', False, random.choice(['gray','silver','green','olive','lime','teal']))
        for x in range(5):
            for y in range(9):
                self.Map[x][y] = Cell('#', False, 'red')        
        
        self.Doors = []
        self.Rooms = [Room(             
            1,
            1,
            3,
            7)]             
                                    
        courtRoom = Room(5,5,29,10)
        self.Rooms.append(courtRoom)        

        for i in range(7):
            room = Room(5 + i * 4, 1, 3, 3)
            self.Rooms.append(room)
            self.Doors.append(Gateway(6+i*4, 4, [room, courtRoom]))
            room = Room(5 + i * 4, 16, 3, 3)
            self.Rooms.append(room)
            self.Doors.append(Gateway(6+i*4, 15, [room, courtRoom]))
        
        self.Rooms.append(Room(35, 12, 4, 3))
        self.Doors.append(Gateway(34,13, [self.Rooms[-1], courtRoom]))
        self.Rooms.append(Room(35, 5, 4, 3))
        self.Doors.append(Gateway(34,6, [self.Rooms[-1], courtRoom]))
        self.Rooms.append(Room(35, 9, 4, 2))
        self.Doors.append(Gateway(34,10, [self.Rooms[-1], courtRoom]))
        self.Rooms.append(Room(33, 1, 6, 3))        
        self.Doors.append(Gateway(33,4, [self.Rooms[-1], courtRoom]))
        self.Rooms.append(Room(33, 16, 6, 3))
        self.Doors.append(Gateway(33,15, [self.Rooms[-1], courtRoom]))

        self.Doors.append(Gateway(4, 6, [self.Rooms[0], courtRoom]))

        for i in self.Rooms:
            for x in range(i.x, i.x+i.w):
                for y in range(i.y, i.y+i.h):
                    self.Map[x][y] = Cell('.', True, 'gray' if x < 4 else random.choice(['teal','lime','aqua','green','olive','blue','navy']))
                    self.Map[x][y].rooms.add(i)
        
        for i in self.Doors:
            self.Map[i.x][i.y] = Cell(',', True, 'blue')
            for j in i.connectedRooms:
                self.Map[x][y].rooms.add(j)
    
        self.Map[5][6] = CloseDoorCell(self.Map[4][6],'.', True, random.choice(['teal','lime','aqua','green','olive','blue','navy']))
        self.Map[5][5] = CloseDoorCell(self.Map[4][6],'.', True, random.choice(['teal','lime','aqua','green','olive','blue','navy']))
        self.Map[5][4] = CloseDoorCell(self.Map[4][6],'.', True, random.choice(['teal','lime','aqua','green','olive','blue','navy']))       

    def VisibilityStatus(self, x, y):   
        #print(x, '-',y) 
        return self.VisibilityMap[x][y]
        
    def UpdateVisibility(self, pc, x, y):   
        newlySeen = 0 # This is only needed because of the new exploration grants HP mechanic
        #print('UPDATE - ', x, '-',y)   
        for i in self.Rooms:
            if i.InRoom(x,y):           
                if i.seenStatus == 0:
                    newlySeen += i.w * i.h
                i.seenStatus = 2
                self.visibilityUpdated = True
            elif i.seenStatus == 2:
                i.seenStatus = 1
                self.visibilityUpdated = True
            elif i.seenStatus == 0:             
                i.seenStatus = 0
        
        for i in self.Doors:
            if x == i.x and y == i.y:
                for j in i.connectedRooms:
                    if j.seenStatus == 0:
                        newlySeen += j.w+j.h
                    j.seenStatus = 2
                    self.visibilityUpdated = True
        
        for i in self.Rooms:
            for j in i.Contains:
                self.VisibilityMap[j[0]][j[1]] = 0  

        for i in self.Rooms:
            for j in i.Contains:
                self.VisibilityMap[j[0]][j[1]] = max(i.seenStatus, self.VisibilityMap[j[0]][j[1]])
        
        return newlySeen
                         
    def RecalculateZombieMod(self, location):
        # This performs the following calculation for each square adjacent to
        # the location:
        # The Zombie Mod = The amount of adjacent zombies + The amount of 
        # not walkable tiles, if there are any adjacent zombies
     
        for ix in range(location[0] - 1, location[0] + 2):
            for iy in range(location[1] - 1, location[1] + 2):
                workingTotal = 0
                for jx in range(max(0,ix-1), min(40, ix + 2)):
                    for jy in range(max(0,iy-1), min(20, iy + 2)):                 
                        if self.ZombieLocations[jx][jy] and not (jx == ix and jy == iy):
                            workingTotal += 1
                if workingTotal > 0:
                    for jx in range(max(0,ix-1), min(40, ix + 2)):
                            for jy in range(max(0,iy-1), min(20, iy + 2)):
                                    if not self.Map[jx][jy].walkable:
                                        workingTotal += 1
                self.ZombieMod[ix][iy] = workingTotal                   
                   
    def AddZombie(self, location):
        self.ZombieLocations[location[0]][location[1]] = True
        self.RecalculateZombieMod(location)
    
    def RemoveZombie(self, location):
        self.ZombieLocations[location[0]][location[1]] = False
        self.RecalculateZombieMod(location)  
                
    def Tick(self):
        # Measures how long since the last restock.
        self.Turn += 1
        
        if self.NextTurn == None:
            self.NextTurn = self.Turn + random.randrange(50,100)              
        
        if self.NextTurn <= self.Turn:
            self.NextTurn = self.Turn + random.randrange(50,100)
            curDanger = sum([i.danger() for i in self.characters if i.chartype != "PC"])
            self.Restock()
            self.RestockDangerPoints += sum([i.danger() for i in self.characters if i.chartype != "PC"]) - curDanger
            # print ('POINTS IS : ', self.RestockDangerPoints)
            self.dangerLevel += 1
                
        
    def Restock(self):
        level = self.level
        if level == 0:
            random.choice([self.AddCritters,
                self.AddBandits])(None, True)
        if level == 1:
            random.choice([self.AddCritters,
                self.AddBandits,
                self.AddOrcs])(None, True)  
        if level == 2:
            random.choice([self.AddCritters,
                self.AddBandits,
                self.AddOrcs,
                self.AddGoliath])(None, True)
        if level == 3:
            random.choice([self.AddCritters,
                self.AddBandits,
                self.AddOrcs,
                self.AddGoliath,
                self.AddHealers])(None, True)
                    
        if level == 4:
            random.choice([self.AddCritters,
                self.AddBandits,
                self.AddOrcs,
                self.AddGoliath,
                self.AddHealers,
                self.AddAssassins])(None, True)
                    
        if level == 5:
            random.choice([self.AddCritters,
                self.AddBandits,
                self.AddOrcs,
                self.AddGoliath,
                self.AddHealers,
                self.AddAssassins,
                self.AddDrake])(None, True)
                    
        if level == 6:
            random.choice([self.AddCritters,
                self.AddBandits,
                self.AddOrcs,
                self.AddGoliath,
                self.AddHealers,
                self.AddAssassins,
                self.AddDrake,
                self.AddZombies])(None, True)
                    
        if level == 7:
            # No restocks on 7
            pass
        
        if level == 8:
            random.choice([self.AddCritters,
                self.AddBandits,
                self.AddOrcs,
                self.AddGoliath,
                self.AddHealers,
                self.AddAssassins,
                self.AddDrake,
                self.AddZombies])(None, True)
        
        if level == 9:
            # No restocks on 9
            pass
                    
    def ChooseItem(self, level):
        maxWeight = max([abs(i.DangerLevel() - level) for i in self.defaultItems]) 
        weights = ([maxWeight - (i.DangerLevel() - level) for i in self.defaultItems if i.Artifact == False])               
        dist = list(itertools.accumulate(weights))
        newItem = self.defaultItems[bisect.bisect(dist, random.random() * dist[-1])]
        #print('Level ', level)
        #j = 0
        #for i in self.defaultItems:            
        #   print('W ', weights[j], ' D ', dist[j], ' DL ', str(i.DangerLevel()))
        #   j = j + 1
        #print('Chosen ' + newItem.Description() + ' ' + str(newItem.DangerLevel()))
        #print('-------------')
        return newItem
                
    def GetRooms(self, x, y):
        for i in self.Doors:
            if x == i.x and y == i.y:
                return i.connectedRooms
                                
        return [i for i in self.Rooms if i.InRoom(x, y)]
        
    def Walkable(self, pos, CharactersIncluded = True):
        if self.Map[pos[0]][pos[1]].walkable == False:
            return False
        else:
            if CharactersIncluded:
                monsterInSquare = [i for i in self.characters if (i.x == pos[0]) and (i.y == pos[1])]
                return len(monsterInSquare) == 0
                
            else:
                return True
                
    def AddCritters(self, forcedRoom = None, restock = False):
        space = 0
        
        # Leave if there's no space
        if max(map(lambda i: i.w * i.h - len([j for j in self.characters if i.InRoom(j.x, j.y)]), self.Rooms)) < 2:
            return False
        
        if forcedRoom == None:
            while space < 2:
                room = random.choice(self.Rooms)
                space = room.w * room.h - len([i for i in self.characters if room.InRoom(i.x,i.y)])
        else:
            room = forcedRoom
            space = room.w * room.h - len([i for i in self.characters if room.InRoom(i.x,i.y)])
        
        count = random.randint(1,min(space,6))
        
        for i in range(count):
            newCharacter = Critter.Critter(self.messageLog, self)
            newCharacter.x = random.randint(room.x, room.x+room.w-1)
            newCharacter.y = random.randint(room.y, room.y+room.h-1)
            while(len([i for i in self.characters if i.x == newCharacter.x and i.y == newCharacter.y]) > 0):            
                newCharacter.x = random.randint(room.x, room.x+room.w-1)
                newCharacter.y = random.randint(room.y, room.y+room.h-1)            
            self.characters.append(newCharacter)
        
        if restock:
            self.messageLog.append(Message.Message("You hear muffled scratching"))
        
    def AddBandits(self, forcedRoom = None, restock = False):
        space = 0
                
        # Leave if there's no space
        if max(map(lambda i: i.w * i.h - len([j for j in self.characters if i.InRoom(j.x, j.y)]), self.Rooms)) < 5:
            return False
        
        if restock:
            roomChoices = self.Rooms
        else:
            roomChoices = [i for i in self.Rooms[1:] if i.occupied == False]
        
        
        if len(roomChoices) == 0:
            return False
        
        if forcedRoom == None:
            while space < 5:
                # Prevents them in starting room
                room = random.choice(roomChoices)
                space = room.w * room.h - len([i for i in self.characters if room.InRoom(i.x,i.y)])
        else:
            room = forcedRoom
            space = room.w * room.h - len([i for i in self.characters if room.InRoom(i.x,i.y)])         
        
        room.occupied = True
        
        count = min(space,round(random.triangular(2, self.level + 5, 2 + self.level)))
        
        team = []
        
        # Add guaranteed badasses if right level
        if self.level >= 6:
            count -= 1
            newCharacter = Bandit.Bandit(self.messageLog, self, 1)
            newCharacter.x = random.randint(room.x, room.x+room.w-1)
            newCharacter.y = random.randint(room.y, room.y+room.h-1)
            while(len([i for i in self.characters if i.x == newCharacter.x and i.y == newCharacter.y]) > 0):            
                newCharacter.x = random.randint(room.x, room.x+room.w-1)
                newCharacter.y = random.randint(room.y, room.y+room.h-1)            
            self.characters.append(newCharacter)
            team.append(newCharacter)
        
        if self.level >= 8:
            count -= 1
            newCharacter = Bandit.Bandit(self.messageLog, self, 2)
            newCharacter.x = random.randint(room.x, room.x+room.w-1)
            newCharacter.y = random.randint(room.y, room.y+room.h-1)
            while(len([i for i in self.characters if i.x == newCharacter.x and i.y == newCharacter.y]) > 0):            
                newCharacter.x = random.randint(room.x, room.x+room.w-1)
                newCharacter.y = random.randint(room.y, room.y+room.h-1)            
            self.characters.append(newCharacter)
            team.append(newCharacter)
        
        for i in range(count):
            newCharacter = Bandit.Bandit(self.messageLog, self)
            newCharacter.x = random.randint(room.x, room.x+room.w-1)
            newCharacter.y = random.randint(room.y, room.y+room.h-1)
            while(len([i for i in self.characters if i.x == newCharacter.x and i.y == newCharacter.y]) > 0):            
                newCharacter.x = random.randint(room.x, room.x+room.w-1)
                newCharacter.y = random.randint(room.y, room.y+room.h-1)            
            self.characters.append(newCharacter)
            team.append(newCharacter)
            
        for i in team:
            i.teamMates = team
            
        if restock:
            self.messageLog.append(Message.Message("You hear a distant whistle"))
        
    def AddOrcs(self, forcedRoom = None, restock = False):
        space = 0
                
        # Leave if there's no space
        if max(map(lambda i: i.w * i.h - len([j for j in self.characters if i.InRoom(j.x, j.y)]), self.Rooms)) < 5:
            return False
        
        if restock:
            roomChoices = self.Rooms
        else:
            roomChoices = [i for i in self.Rooms[1:] if i.occupied == False]
        
        if len(roomChoices) == 0:
            return False
        
        if forcedRoom == None:      
            while space < 5:
                # Prevents them in starting room
                room = random.choice(roomChoices)
                space = room.w * room.h - len([i for i in self.characters if room.InRoom(i.x,i.y)])     
        else:
            room = forcedRoom
            space = room.w * room.h - len([i for i in self.characters if room.InRoom(i.x,i.y)])         
        
        room.occupied = True
        
        # There are multiple to weight each choice
        countChoices = [1,1,1,1,2,2,2,2,2,2,3,3,3,3,3,3,3,3,3,3]
        if self.level > 4:
            countChoices.extend(range(3, self.level))
        count = min(space,round(random.choice(countChoices)))
        badassGuaranteed = count >= 10
        # Add guaranteed badasses if right level, and a
        if self.level >= 6 and badassGuaranteed:
            count -= 1
            newCharacter = Orc.Orc(self.messageLog, self, 1)
            newCharacter.x = random.randint(room.x, room.x+room.w-1)
            newCharacter.y = random.randint(room.y, room.y+room.h-1)
            while(len([i for i in self.characters if i.x == newCharacter.x and i.y == newCharacter.y]) > 0):            
                newCharacter.x = random.randint(room.x, room.x+room.w-1)
                newCharacter.y = random.randint(room.y, room.y+room.h-1)            
            self.characters.append(newCharacter)
        
        if self.level >= 8 and badassGuaranteed:
            count -= 1
            newCharacter = Orc.Orc(self.messageLog, self, 2)
            newCharacter.x = random.randint(room.x, room.x+room.w-1)
            newCharacter.y = random.randint(room.y, room.y+room.h-1)
            while(len([i for i in self.characters if i.x == newCharacter.x and i.y == newCharacter.y]) > 0):            
                newCharacter.x = random.randint(room.x, room.x+room.w-1)
                newCharacter.y = random.randint(room.y, room.y+room.h-1)            
            self.characters.append(newCharacter)        
        
        for i in range(count):
            newCharacter = Orc.Orc(self.messageLog, self)
            newCharacter.x = random.randint(room.x, room.x+room.w-1)
            newCharacter.y = random.randint(room.y, room.y+room.h-1)
            while(len([i for i in self.characters if i.x == newCharacter.x and i.y == newCharacter.y]) > 0):            
                newCharacter.x = random.randint(room.x, room.x+room.w-1)
                newCharacter.y = random.randint(room.y, room.y+room.h-1)            
            self.characters.append(newCharacter)
        
        if restock:
            self.messageLog.append(Message.Message("You hear shots in the distance"))
    
    def AddGoliath(self, forcedRoom = None, restock = False):
        space = 0
                
        # Leave if there's no space
        if max(map(lambda i: i.w * i.h - len([j for j in self.characters if i.InRoom(j.x, j.y)]), self.Rooms)) < 1:
            return False

        if restock:
            roomChoices = self.Rooms
        else:
            roomChoices = self.Rooms[1:]

        if forcedRoom == None:
            while space < 1:
                room = random.choice(roomChoices)
                space = room.w * room.h - len([i for i in self.characters if room.InRoom(i.x,i.y)])
        else:
            room = forcedRoom
            space = room.w * room.h - len([i for i in self.characters if room.InRoom(i.x,i.y)])

        newCharacter = Goliath.Goliath(self.messageLog, self)
        newCharacter.x = random.randint(room.x, room.x+room.w-1)
        newCharacter.y = random.randint(room.y, room.y+room.h-1)
        while(len([i for i in self.characters if i.x == newCharacter.x and i.y == newCharacter.y]) > 0):            
            newCharacter.x = random.randint(room.x, room.x+room.w-1)
            newCharacter.y = random.randint(room.y, room.y+room.h-1)            
        self.characters.append(newCharacter)
        
        if restock:
            self.messageLog.append(Message.Message("You feel a small earthquake"))
        
    def AddHealers(self, forcedRoom = None, restock = False):
        space = 0
                
        # Leave if there's no space         
        if max(map(lambda i: i.w * i.h - len([j for j in self.characters if i.InRoom(j.x, j.y)]), self.Rooms)) < 1:
            return False
            
        # if no characters yet (ie - healer is first) then we'll make a 'hospital' of healers! Mwahahah!
        if len(self.characters) == 0 or forcedRoom != None:                         
            if forcedRoom == None:
                while space < 3:
                    room = random.choice(self.Rooms)
                    space = room.w * room.h - len([i for i in self.characters if room.InRoom(i.x,i.y)])     
            else:
                room = forcedRoom
                space = room.w * room.h - len([i for i in self.characters if room.InRoom(i.x,i.y)])
            
            count = min(space,round(random.randint(3,9)))
            
            for i in range(count):              
                newCharacter = Healer.Healer(self.messageLog, self)
                newCharacter.x = random.randint(room.x, room.x+room.w-1)
                newCharacter.y = random.randint(room.y, room.y+room.h-1)
                while(len([i for i in self.characters if i.x == newCharacter.x and i.y == newCharacter.y]) > 0):            
                    newCharacter.x = random.randint(room.x, room.x+room.w-1)
                    newCharacter.y = random.randint(room.y, room.y+room.h-1)            
                self.characters.append(newCharacter)
            
        else:
            # Healers get added to the rooms with enemies
            
            # To prevent deadlocks
            tries = 100
            curtry = 0
            while (space < 1 and curtry < tries):
                curtry += 1
                target = random.choice(self.characters)
                room = [i for i in self.Rooms if i.InRoom(target.x, target.y)][0]
                space = room.w * room.h - len([i for i in self.characters if room.InRoom(i.x,i.y)])
                #print ("Tried")
            
            if tries == curtry:
                #print ("Tried and failed")
                return False
            
            newCharacter = Healer.Healer(self.messageLog, self)
            newCharacter.x = random.randint(room.x, room.x+room.w-1)
            newCharacter.y = random.randint(room.y, room.y+room.h-1)
            while(len([i for i in self.characters if i.x == newCharacter.x and i.y == newCharacter.y]) > 0):            
                newCharacter.x = random.randint(room.x, room.x+room.w-1)
                newCharacter.y = random.randint(room.y, room.y+room.h-1)            
            self.characters.append(newCharacter)
        
        if restock:
            self.messageLog.append(Message.Message("You smell antiseptics"))

    def AddAssassins(self, forcedRoom = None, restock = False):
        space = 0
        
        # Leave if there's no space
        if max(map(lambda i: i.w * i.h - len([j for j in self.characters if i.InRoom(j.x, j.y)]), self.Rooms)) < 2:
            return False
        
        if forcedRoom == None:
            while space < 2:
                room = random.choice(self.Rooms)
                space = room.w * room.h - len([i for i in self.characters if room.InRoom(i.x,i.y)])
        else:
            room = forcedRoom
            space = room.w * room.h - len([i for i in self.characters if room.InRoom(i.x,i.y)])
        
        count = random.randint(1,min(space,2))
        
        for i in range(count):
            newCharacter = Assassin.Assassin(self.messageLog, self)
            newCharacter.x = random.randint(room.x, room.x+room.w-1)
            newCharacter.y = random.randint(room.y, room.y+room.h-1)
            while(len([i for i in self.characters if i.x == newCharacter.x and i.y == newCharacter.y]) > 0):            
                newCharacter.x = random.randint(room.x, room.x+room.w-1)
                newCharacter.y = random.randint(room.y, room.y+room.h-1)            
            self.characters.append(newCharacter)
            
        if restock:    
            self.messageLog.append(Message.Message("You hear nothing"))            
        
    def AddDrake(self, forcedRoom = None, restock = False):
        space = 0
                
        # Leave if there's no space
        if max(map(lambda i: i.w * i.h - len([j for j in self.characters if i.InRoom(j.x, j.y)]), self.Rooms)) < 1:
            return False
        
        if forcedRoom == None:
            while space < 1:
                room = random.choice(self.Rooms)
                space = room.w * room.h - len([i for i in self.characters if room.InRoom(i.x,i.y)])
        else:
            room = forcedRoom
            space = room.w * room.h - len([i for i in self.characters if room.InRoom(i.x,i.y)])

        newCharacter = Drake.Drake(self.messageLog, self)
        newCharacter.x = random.randint(room.x, room.x+room.w-1)
        newCharacter.y = random.randint(room.y, room.y+room.h-1)
        while(len([i for i in self.characters if i.x == newCharacter.x and i.y == newCharacter.y]) > 0):            
            newCharacter.x = random.randint(room.x, room.x+room.w-1)
            newCharacter.y = random.randint(room.y, room.y+room.h-1)            
        self.characters.append(newCharacter)
        
        if restock:    
            self.messageLog.append(Message.Message("You smell sulpher"))
        
    def AddZombies(self, forcedRoom = None, restock = False):
        space = 0       
        
        # Leave if there's no space
        if max(map(lambda i: i.w * i.h - len([j for j in self.characters if i.InRoom(j.x, j.y)]), self.Rooms)) < 2:
            return False
        
        if forcedRoom == None:
            while space < 3:
                room = random.choice(self.Rooms)
                space = room.w * room.h - len([i for i in self.characters if room.InRoom(i.x,i.y)])
        else:
            room = forcedRoom
            space = room.w * room.h - len([i for i in self.characters if room.InRoom(i.x,i.y)])
        
        count = random.randint(3,min(space,12))
        
        for i in range(count):
            newCharacter = Zombie.Zombie(self.messageLog, self)
            newCharacter.x = random.randint(room.x, room.x+room.w-1)
            newCharacter.y = random.randint(room.y, room.y+room.h-1)
            while(len([i for i in self.characters if i.x == newCharacter.x and i.y == newCharacter.y]) > 0):            
                newCharacter.x = random.randint(room.x, room.x+room.w-1)
                newCharacter.y = random.randint(room.y, room.y+room.h-1)          
            self.AddZombie((newCharacter.x, newCharacter.y))
            self.characters.append(newCharacter)
            
        if restock:    
            self.messageLog.append(Message.Message("You smell rotting flesh"))
    
    def AddNecromancer(self):
        space = 0
                
        # Leave if there's no space
                    
        room = self.endRoom
        space = room.w * room.h - len([i for i in self.characters if room.InRoom(i.x,i.y)])     

        newCharacter = Necromancer.Necromancer(self.messageLog, self)
        newCharacter.x = random.randint(room.x, room.x+room.w-1)
        newCharacter.y = random.randint(room.y, room.y+room.h-1)
        while(len([i for i in self.characters if i.x == newCharacter.x and i.y == newCharacter.y]) > 0):            
            newCharacter.x = random.randint(room.x, room.x+room.w-1)
            newCharacter.y = random.randint(room.y, room.y+room.h-1)            
        self.characters.append(newCharacter)
        
        # Give the neccy some zombie friendsies
        for i in range(4):
            newCharacter = Zombie.Zombie(self.messageLog, self)
            newCharacter.x = random.randint(room.x, room.x+room.w-1)
            newCharacter.y = random.randint(room.y, room.y+room.h-1)
            while(len([i for i in self.characters if i.x == newCharacter.x and i.y == newCharacter.y]) > 0):            
                newCharacter.x = random.randint(room.x, room.x+room.w-1)
                newCharacter.y = random.randint(room.y, room.y+room.h-1)  
            self.AddZombie((newCharacter.x, newCharacter.y))
            self.characters.append(newCharacter)

    def AddDragon(self):
        space = 0
                
        # Leave if there's no space
        room = self.Rooms[1]
        space = room.w * room.h     

        newCharacter = Dragon.Dragon(self.messageLog, self)
        newCharacter.x = random.randint(room.x, room.x+room.w-1)
        newCharacter.y = random.randint(room.y, room.y+room.h-1)
        while(len([i for i in self.characters if i.x == newCharacter.x and i.y == newCharacter.y]) > 0):            
            newCharacter.x = random.randint(room.x, room.x+room.w-1)
            newCharacter.y = random.randint(room.y, room.y+room.h-1)            
        self.characters.append(newCharacter)
        
        # Give the dragon some healer friendsies
        for i in range(4):
            newCharacter = Healer.Healer(self.messageLog, self)
            newCharacter.x = random.randint(room.x, room.x+room.w-1)
            newCharacter.y = random.randint(room.y, room.y+room.h-1)
            while(len([i for i in self.characters if i.x == newCharacter.x and i.y == newCharacter.y]) > 0):            
                newCharacter.x = random.randint(room.x, room.x+room.w-1)
                newCharacter.y = random.randint(room.y, room.y+room.h-1)            
            self.characters.append(newCharacter)
    
    def AddWarlord(self, forcedRoom):
        space = 0
                
        # Leave if there's no space
        if max(map(lambda i: i.w * i.h - len([j for j in self.characters if i.InRoom(j.x, j.y)]), self.Rooms)) < 1:
            return False
        
        if forcedRoom == None:
            while space < 1:
                room = random.choice(self.Rooms)
                space = room.w * room.h - len([i for i in self.characters if room.InRoom(i.x,i.y)])
        else:
            room = forcedRoom
            space = room.w * room.h - len([i for i in self.characters if room.InRoom(i.x,i.y)])

        newCharacter = Warlord.Warlord(self.messageLog, self)
        newCharacter.x = random.randint(room.x, room.x+room.w-1)
        newCharacter.y = random.randint(room.y, room.y+room.h-1)
        while(len([i for i in self.characters if i.x == newCharacter.x and i.y == newCharacter.y]) > 0):            
            newCharacter.x = random.randint(room.x, room.x+room.w-1)
            newCharacter.y = random.randint(room.y, room.y+room.h-1)            
        self.characters.append(newCharacter)


