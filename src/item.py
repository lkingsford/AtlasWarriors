class ItemClass:
    none = 0
    blunt = 1
    sword = 2
    polearm = 3
    dagger = 4
    axe = 5
    shield = 6

class Item:
    def __init__(self):
        self.ItemClass = ItemClass.none
        self.Name = "Weapon"
        self.ID = -1
        self.ToHit = 0
        self.Damage = 0
        self.ToDefend = 0
        self.TwoHanded = False
        self.Character = '\\'
        self.Color = 'white'
        self.x = 0
        self.y = 0
        self.Speed = 100
        self.Artifact = False # If it's an artifact, it won't be randomly generated
        
    def Description(self):
        return self.Name + " [" +\
            {ItemClass.none: "None",\
            ItemClass.blunt: "Blunt",\
            ItemClass.sword: "Sword",\
            ItemClass.polearm: "Polearm",\
            ItemClass.dagger: "Dagger",\
            ItemClass.axe: "Axe",\
            ItemClass.shield: "Shield"}[self.ItemClass] +\
            "]  (" + \
            (" 2H " if self.TwoHanded == True else "") + \
            ((" H" + str(self.ToHit)) if self.ToHit != 0 else "") + \
            ((" Dmg" + str(self.Damage)) if self.Damage != 0 else "") + \
            ((" D" + str(self.ToDefend)) if self.ToDefend != 0 else "") + \
            ") "
    
    def IsWeapon(self):
        return self.ItemClass > 0 and self.ItemClass < 6
            
    # The Danger Level represents the average level the item should be found on
    def DangerLevel(self):
        return (self.ToHit * 0.9 + self.Damage * 0.5 + self.ToDefend * 0.7) / (2.5 if self.TwoHanded else 1) * 1.2
        
