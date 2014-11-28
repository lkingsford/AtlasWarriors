import dialog
import pygame
import context

from pygame.locals import *
class InventoryDialog(dialog.Dialog):
    def __init__(self, PC):
        self.toClose = False
        self.TitleFont = pygame.font.Font("DejaVuSerif.ttf", 20) 
        self.BodyFont = pygame.font.Font("DejaVuSerif.ttf", 12)                 
        self.Box = pygame.Rect(0,0,0,0)
        self.LeftHandBox = pygame.Rect(0,0,0,0) 
        self.RightHandBox = pygame.Rect(0,0,0,0)
        self.BackpackBox = pygame.Rect(0,0,0,0)
        self.PC = PC
        self.Context = None
        self.refreshFloorItems()
    
    def refreshFloorItems(self):
        self.FloorItems = [i for i in self.PC.currentMap.Items if i.x == self.PC.x and i.y == self.PC.y]
    
    def draw(self, win):        
        self.Box = pygame.Rect(5, 5, win.get_width() - 10, 408)
        self.LeftHandBox = pygame.Rect(120, 73, win.get_width() - 153, 20)
        self.RightHandBox = pygame.Rect(120, 53, win.get_width() - 153, 20) 
        self.BackpackBox = pygame.Rect(28, 123, win.get_width() - 60, 124)
        self.FloorBox = pygame.Rect(28, 273, win.get_width() - 60, 124)
        
        pygame.draw.rect(win, (32,32,32,255), self.Box, 0)
        pygame.draw.rect(win, (128,128,128,255), self.Box, 1)
        pygame.draw.rect(win, (0,0,0,255), self.LeftHandBox, 0)
        pygame.draw.rect(win, (128,128,128,255), self.LeftHandBox, 1)
        pygame.draw.rect(win, (0,0,0,255), self.RightHandBox, 0)
        pygame.draw.rect(win, (128,128,128,255), self.RightHandBox, 1)
        pygame.draw.rect(win, (0,0,0,255), self.BackpackBox, 0)
        pygame.draw.rect(win, (128,128,128,255), self.BackpackBox, 1)
        pygame.draw.rect(win, (0,0,0,255), self.FloorBox, 0)
        pygame.draw.rect(win, (128,128,128,255), self.FloorBox, 1)
        titleSize = self.TitleFont.size('Load Out')
        win.blit(self.TitleFont.render('Load Out', True, (255, 255, 255, 255)), (round((win.get_width() - titleSize[0])/2), 15))
        win.blit(self.BodyFont.render('Equipped:', True, (255, 255, 255, 255)), (30, 35))
        win.blit(self.BodyFont.render('Right Hand:', True, (255, 255, 255, 255)), (30, 55))
        win.blit(self.BodyFont.render('Left Hand:', True, (255, 255, 255, 255)), (30, 75))
        
        win.blit(self.BodyFont.render('(a) ' + self.PC.rightHandEquipped.Description() if self.PC.rightHandEquipped != None else (('(' + self.PC.leftHandEquipped.Description() + ')') if self.PC.leftHandEquipped != None and self.PC.leftHandEquipped.TwoHanded  else 'Empty'), True, (255, 255, 255, 255)), (122, 55))        
        win.blit(self.BodyFont.render('(b) ' + self.PC.leftHandEquipped.Description() if self.PC.leftHandEquipped != None else (('(' + self.PC.rightHandEquipped.Description() + ')') if self.PC.rightHandEquipped != None and self.PC.rightHandEquipped.TwoHanded  else 'Empty'), True, (255, 255, 255, 255)), (122, 75))
        
        win.blit(self.BodyFont.render('Backpack:', True, (255, 255, 255, 255)), (30, 105))
        
        win.blit(self.BodyFont.render('On Floor:', True, (255, 255, 255, 255)), (30, 255))
        
        # This letter is ascii for b. It'll increment to provide shortcut keys.
        curLetter = ord('b')        
        
        for i in enumerate(self.PC.backpack):
            curLetter += 1;
            win.blit(self.BodyFont.render("(" + chr(curLetter) + ") " + i[1].Description(), True, (255, 255, 255, 255)), (30, 125 + i[0] * 20))
            
        for i in enumerate(self.FloorItems):            
            curLetter += 1;
            win.blit(self.BodyFont.render("(" + chr(curLetter) + ") " + i[1].Description(), True, (255, 255, 255, 255)), (30, 275 + i[0] * 20))
        
        if self.Context != None:
            self.Context.draw(win)
    
    # There is duplication in this procedure. It might be better served to
    # seperate some of it into their own procedures.
    def process(self, event):
        if self.Context == None:
            if event.type == KEYDOWN:
                # Close window
                if event.key == pygame.K_ESCAPE:
                    self.toClose = True                
                    
                # Change right hand equipped
                elif event.unicode == 'a':
                    if self.PC.rightHandEquipped != None:
                        self.Context = context.Context(300,55)
                        self.Context.AddItem(('Put in backpack', lambda: self.PC.Equip(None, 0)))
                        self.Context.AddItem(('Drop', lambda: self.PC.Drop(self.PC.rightHandEquipped)))
                
                # Change left hand equipped 
                elif event.unicode == 'b':
                    if self.PC.leftHandEquipped != None:
                        self.Context = context.Context(300,75)
                        self.Context.AddItem(('Put in backpack', lambda: self.PC.Equip(None, 1)))
                        self.Context.AddItem(('Drop', lambda: self.PC.Drop(self.PC.leftHandEquipped)))    

                # Change inventory or floor
                elif ord(event.unicode) > ord('b') and ord(event.unicode) < ord('z'):
                    # Iterate through backpack, then through floor
                    curLetter = ord('b')
                    curY = 125
                    for i in self.PC.backpack:
                        curLetter += 1
                        if curLetter == ord(event.unicode):
                            self.Context = context.Context(300, curY)
                            self.Context.AddItem(('Equip in Right Hand', lambda: self.PC.Equip(i, 0)))
                            self.Context.AddItem(('Equip in Left Hand', lambda: self.PC.Equip(i, 1)))
                            self.Context.AddItem(('Drop', lambda: self.PC.Drop(i)))
                        curY += 20
                    
                    curY = 275
                    for i in self.FloorItems:
                        curLetter += 1
                        if curLetter == ord(event.unicode):
                            self.Context = context.Context(300, curY)
                            self.Context.AddItem(('Equip in Right Hand', lambda: self.PC.Equip(i, 0)))
                            self.Context.AddItem(('Equip in Left Hand', lambda: self.PC.Equip(i, 1)))
                            if len(self.PC.backpack) < self.PC.backpackSize:
                                self.Context.AddItem(('Pick up', lambda: self.PC.Pickup(i)))
                        curY += 20
            
            if event.type == MOUSEBUTTONDOWN:
                if not self.Box.collidepoint(event.pos):
                    self.toClose = True
                
                else:
                    if self.BackpackBox.collidepoint(event.pos):
                        index = (event.pos[1] - 125)// 20                       
                        if len(self.PC.backpack) > index:
                            item = self.PC.backpack[index]
                            self.Context = context.Context(event.pos[0], event.pos[1])
                            self.Context.AddItem(('Equip in Right Hand', lambda: self.PC.Equip(item, 0)))
                            self.Context.AddItem(('Equip in Left Hand', lambda: self.PC.Equip(item, 1)))
                            self.Context.AddItem(('Drop', lambda: self.PC.Drop(item)))
                            
                    if self.FloorBox.collidepoint(event.pos):
                        index = (event.pos[1] - 275) // 20
                        if len(self.FloorItems) > index:
                            item = self.FloorItems[index]
                            self.Context = context.Context(event.pos[0], event.pos[1])
                            self.Context.AddItem(('Equip in Right Hand', lambda: self.PC.Equip(item, 0)))
                            self.Context.AddItem(('Equip in Left Hand', lambda: self.PC.Equip(item, 1)))
                            if len(self.PC.backpack) < self.PC.backpackSize:
                                self.Context.AddItem(('Pick up', lambda: self.PC.Pickup(item)))
                        
                    if self.RightHandBox.collidepoint(event.pos) and self.PC.rightHandEquipped != None:
                        self.Context = context.Context(event.pos[0], event.pos[1])
                        self.Context.AddItem(('Put in backpack', lambda: self.PC.Equip(None, 0)))
                        self.Context.AddItem(('Drop', lambda: self.PC.Drop(self.PC.rightHandEquipped)))
                    if self.LeftHandBox.collidepoint(event.pos) and self.PC.leftHandEquipped != None:
                        self.Context = context.Context(event.pos[0], event.pos[1])
                        self.Context.AddItem(('Put in backpack', lambda: self.PC.Equip(None, 1)))
                        self.Context.AddItem(('Drop', lambda: self.PC.Drop(self.PC.leftHandEquipped)))                  
                    
        else:
            self.Context.process(event)
            self.refreshFloorItems()
            if self.Context.toClose == True:
                self.Context = None
                
     
        
