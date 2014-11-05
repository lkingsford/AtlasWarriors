import dialog
import pygame
from pygame.locals import *
class MessagesDialog(dialog.Dialog):
    def __init__(self, messages):
        self.toClose = False
        self.TitleFont = pygame.font.Font("DejaVuSerif.ttf", 20) 
        self.BodyFont = pygame.font.Font("DejaVuSerif.ttf", 12)  
        self.Box = pygame.Rect(0,0,0,0)
        self.messages = messages
    
    def draw(self, win):
        self.Box = pygame.Rect(5, 5, win.get_width() - 10, 416)
        self.MessagesBox = pygame.Rect(10, 45, win.get_width() - 20, 371)
        
        pygame.draw.rect(win, (32,32,32,255), self.Box, 0)
        pygame.draw.rect(win, (128,128,128,255), self.Box, 1)
        pygame.draw.rect(win, (0,0,0,255), self.MessagesBox, 0)
        pygame.draw.rect(win, (128,128,128,255), self.MessagesBox, 1)
        titleSize = self.TitleFont.size('Message Log')
        win.blit(self.TitleFont.render('Message Log', True, (255, 255, 255, 255)),\
            (round((win.get_width() - titleSize[0])/2), 15))
        
        # Martian Smiley trick from http://stackoverflow.com/questions/3705670
        # It reverses the order of the list
        # 
        # This code may need to be reviewed for speed when the program has
        # been running a while.
        # 
        for i in enumerate(self.messages[::-1]):           
            win.blit(self.BodyFont.render(i[1].text, True, (255, 255, 255, 255)), (15, 48 + i[0] * 20))
   
    def process(self, event):
        if event.type == KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.toClose = True
        
        if event.type == MOUSEBUTTONDOWN:
            if not self.Box.collidepoint(event.pos):
                self.toClose = True
