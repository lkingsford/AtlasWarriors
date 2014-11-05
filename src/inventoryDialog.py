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
		self.FloorItems = [i for i in PC.currentMap.Items if i.x == PC.x and i.y == PC.y]
	
	def draw(self, win):	    
		self.Box = pygame.Rect(5, 50, win.get_width() - 10, 408)
		self.LeftHandBox = pygame.Rect(120, 118, win.get_width() - 153, 20)
		self.RightHandBox = pygame.Rect(120, 98, win.get_width() - 153, 20)	
		self.BackpackBox = pygame.Rect(28, 168, win.get_width() - 60, 124)
		self.FloorBox = pygame.Rect(28, 318, win.get_width() - 60, 124)
		
		pygame.draw.rect(win, (32,32,32,255), self.Box, 0)
		pygame.draw.rect(win, (128,128,128,255), self.Box, 1)
		pygame.draw.rect(win, (0,0,0,255), self.LeftHandBox, 0)
		pygame.draw.rect(win, (128,128,128,255), self.LeftHandBox, 1)
		pygame.draw.rect(win, (0,0,0,255), self.RightHandBox, 0)
		pygame.draw.rect(win, (128,128,128,255), self.RightHandBox, 1)
		pygame.draw.rect(win, (0,0,0,255), self.BackpackBox, 0)
		pygame.draw.rect(win, (128,128,128,255), self.BackpackBox, 1)
		titleSize = self.TitleFont.size('Load Out')
		win.blit(self.TitleFont.render('Load Out', True, (255, 255, 255, 255)), (round((win.get_width() - titleSize[0])/2), 60))
		win.blit(self.BodyFont.render('Equipped:', True, (255, 255, 255, 255)), (30, 80))
		win.blit(self.BodyFont.render('Right Hand:', True, (255, 255, 255, 255)), (30, 100))		
		win.blit(self.BodyFont.render('Left Hand:', True, (255, 255, 255, 255)), (30, 120))
		
		win.blit(self.BodyFont.render(self.PC.rightHandEquipped.Description() if self.PC.rightHandEquipped != None else (('(' + self.PC.leftHandEquipped.Description() + ')') if self.PC.leftHandEquipped != None and self.PC.leftHandEquipped.TwoHanded  else 'Empty'), True, (255, 255, 255, 255)), (122, 100))		
		win.blit(self.BodyFont.render(self.PC.leftHandEquipped.Description() if self.PC.leftHandEquipped != None else (('(' + self.PC.rightHandEquipped.Description() + ')') if self.PC.rightHandEquipped != None and self.PC.rightHandEquipped.TwoHanded  else 'Empty'), True, (255, 255, 255, 255)), (122, 120))
		
		win.blit(self.BodyFont.render('Backpack:', True, (255, 255, 255, 255)), (30, 150))
		
		win.blit(self.BodyFont.render('On Floor:', True, (255, 255, 255, 255)), (30, 300))
		
		for i in enumerate(self.PC.backpack):			
			win.blit(self.BodyFont.render(i[1].Description(), True, (255, 255, 255, 255)), (30, 170 + i[0] * 20))
			
		for i in enumerate(self.FloorItems):			
			win.blit(self.BodyFont.render(i[1].Description(), True, (255, 255, 255, 255)), (30, 320 + i[0] * 20))
		
		if self.Context != None:
			self.Context.draw(win)
	
	def process(self, event):
		if self.Context == None:
			if event.type == KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					self.toClose = True
			
			if event.type == MOUSEBUTTONDOWN:
				if not self.Box.collidepoint(event.pos):
					self.toClose = True
				
				else:
					if self.BackpackBox.collidepoint(event.pos):
						index = (event.pos[1] - 160)// 20 						
						if len(self.PC.backpack) > index:
							item = self.PC.backpack[index]
							self.Context = context.Context(event.pos[0], event.pos[1])
							self.Context.AddItem(('Equip in Right Hand', lambda: self.PC.Equip(item, 0)))
							self.Context.AddItem(('Equip in Left Hand', lambda: self.PC.Equip(item, 1)))
							self.Context.AddItem(('Drop', lambda: self.PC.Drop(item)))
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
			if self.Context.toClose == True:
				self.Context = None
		
