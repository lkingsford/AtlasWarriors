import pygame
from pygame.locals import *

class Context():
    def __init__(self, x, y):
        self.options = []
        self.x = x
        self.y = y
        self.selected = None
        self.toClose = False
        self.toReturn = None
        self.font = pygame.font.Font("DejaVuSansMono.ttf", 12)
        self.Box = pygame.Rect(0,0,0,0)
        self.seperation = 14
        self.width = 0
        self.curLetter = 'a'
    
    def AddItem(self, item):
        self.options.append(
            (item, # 0
            self.font.render("(" + self.curLetter + ") " + item[0], # 1
            True, (255, 255, 255, 255)), 
            pygame.Rect(self.x, self.y + self.seperation * len(self.options),
                self.font.size("(" + self.curLetter + ") " + item[0])[0], 
                self.seperation), # 2
                self.curLetter)) # 3
        self.width = max(i[2][2] for i in self.options)
        for i in self.options:
            i[2][2] = self.width
        self.Box = pygame.Rect(self.x, self.y, self.width, self.seperation * len(self.options))
        self.curLetter = chr(ord(self.curLetter) + 1);
                
    def draw(self, win):
        pygame.draw.rect(win, (16,16,16,255), self.Box, 0)
        pygame.draw.rect(win, (48,48,48,255), self.Box, 1)
        if self.selected != None:
            pygame.draw.rect(win, (16, 16, 48, 255), self.selected, 0)
        curLetter = ord('a')        
        for i in enumerate(self.options):
            win.blit(i[1][1], (self.x, self.y + i[0] * self.seperation))
            curLetter += 1;
    
    def process(self, event):
        if event.type == MOUSEBUTTONDOWN:
            self.toClose = True
            try:
                next(i[0][1] for i in self.options if i[2].collidepoint(event.pos))()
            except StopIteration:
                self.toReturn = None
        
        if event.type == MOUSEMOTION:
            if not self.Box.collidepoint(event.pos):
                self.selected = None
            else:
                self.selected = next(i[2] for i in self.options if i[2].collidepoint(event.pos))
                
        if event.type == KEYDOWN:
            for i in self.options:
                if event.unicode == i[3]:                        
                    self.toClose = True
                    i[0][1]()
            self.toClose = True
