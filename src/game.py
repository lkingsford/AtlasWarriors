import map
import random
import character
import player_character
import item
import code
import enemy
import difficulty
import item
import xml2object

class Game:
    def __init__(
            self,
            interface,                      # RLUI object
            tutorial,                       # Tutorial object
            difficulty,                     # Difficulty object
            cheats_enabled                  # Bool describing if cheats work
            ):
        self.interface = interface
        self.tutorial = tutorial
        self.difficulty = difficulty
        self.cheats_enabled = cheats_enabled
        # Load default items - this may need moving out of game.py
        # if moving to another platform
        self.default_items = xml2object.parse('items.xml', item.Item)

        # Create maps
        self.maps = []
        for i in range(10):
            self.maps.append(map.Map(
                i,
                self.interface.message_log,
                self.default_items
                self.difficulty));
        
        # Link maps together
        for i in range(10):
            if (i != 9):
                self.maps[i].nextMap = self.maps[i + 1]
            if (i != 0):
                self.maps[i].lastMap = self.maps[i - 1]
        
        # Create player characters
        self.PC = player_character.PlayerCharacter(
            self.interface.messageLog,
            self.maps[0],
            self.default_items,
            self.difficulty,
            self.tutorial)        
        PC.x = self.maps[0].startX
        PC.y = self.maps[0].startY
        maps[0].UpdateVisibility(PC, PC.x, PC.y)        
        PC.currentMap.characters.append(PC)
        lastMap = None
        
        # Find the end boss to check for victory conditions
        AllMonsters = []
        for i in Maps: AllMonsters.extend(i.characters)
        self.end_boss = next(i for i in AllMonsters if i.chartype == "endboss")
        
        self.running = False
    
    def start(self):
        self.running = True
    
    # The tick command processes the maps and characters
    def tick(self):
        pass


    
