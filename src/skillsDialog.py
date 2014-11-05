import dialog
import pygame

from pygame.locals import *

class SkillsDialog(dialog.Dialog):
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
        
    def draw(self, win):
        self.Box = pygame.Rect(100, 5, win.get_width() - 200, 198)
        self.LeftHandBox = pygame.Rect(150, 118, win.get_width() - 205, 20)
        self.RightHandBox = pygame.Rect(150, 98, win.get_width() - 205, 20) 
        self.BackpackBox = pygame.Rect(55, 158, win.get_width() - 110, 124)
        
        pygame.draw.rect(win, (32,32,32,255), self.Box, 0)
        pygame.draw.rect(win, (128,128,128,255), self.Box, 1)
        
        titleSize = self.TitleFont.size('Skills')
        win.blit(self.TitleFont.render('Skills', True, (255, 255, 255, 255)), (round((win.get_width() - titleSize[0])/2), 15))
        
        win.blit(self.BodyFont.render('Category' , True, (255, 0, 0, 0)), (110, 50))
        win.blit(self.BodyFont.render('Level' , True, (255, 0, 0, 0)), (210, 50))
        win.blit(self.BodyFont.render('Next' , True, (255, 0, 0, 0)), (250, 50))
        win.blit(self.BodyFont.render('Hit+' , True, (255, 0, 0, 0)), (290, 50))
        win.blit(self.BodyFont.render('Def+' , True, (255, 0, 0, 0)), (330, 50))
        win.blit(self.BodyFont.render('Dmg+' , True, (255, 0, 0, 0)), (370, 50))
        win.blit(self.BodyFont.render('Unarmed' , True, (255, 255, 255, 255)), (110, 65))
        win.blit(self.BodyFont.render('Blunts' , True, (255, 255, 255, 255)), (110, 80))
        win.blit(self.BodyFont.render('Swords' , True, (255, 255, 255, 255)), (110, 95))
        win.blit(self.BodyFont.render('Polearms' , True, (255, 255, 255, 255)), (110, 110))
        win.blit(self.BodyFont.render('Daggers' , True, (255, 255, 255, 255)), (110, 125))
        win.blit(self.BodyFont.render('Axes' , True, (255, 255, 255, 255)), (110, 140))
        win.blit(self.BodyFont.render('Shields' , True, (255, 255, 255, 255)), (110, 155))
        win.blit(self.BodyFont.render('Duel Wielding' , True, (255, 255, 255, 255)), (110, 170))
        
        for i in enumerate(self.PC.skills):         
            # Level
            win.blit(self.BodyFont.render(str(i[1][1]), True, (255, 255, 255, 255)), (210, 65 + 15 * i[0]))
            # Hits
            win.blit(self.BodyFont.render(str(self.PC.NextLevelHitsNeeded(i[1][1], i[0]) - i[1][0]), True, (255, 255, 255, 255)), (250, 65 + 15 * i[0]))
            # To Hit
            win.blit(self.BodyFont.render(str(self.PC.ToHitMod(i[0])), True, (255, 255, 255, 255)), (290, 65 + 15 * i[0]))
            # To Def
            win.blit(self.BodyFont.render(str(self.PC.ToDefMod(i[0])), True, (255, 255, 255, 255)), (330, 65 + 15 * i[0]))
            # Dmg Mod
            win.blit(self.BodyFont.render(str(self.PC.DmgMod(i[0])), True, (255, 255, 255, 255)), (370, 65 + 15 * i[0]))
    
    def process(self, event):
        if event.type == KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.toClose = True
        
        elif event.type == MOUSEBUTTONDOWN:
            if not self.Box.collidepoint(event.pos):
                self.toClose = True         
