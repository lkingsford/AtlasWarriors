import dialog
import pygame
from pygame.locals import *
class MessagesDialog(dialog.Dialog):
	def __init__(self):
		self.toClose = False
		TitleFont = pygame.font.Font("DejaVuSerif.ttf", 20) 
		BodyFont = pygame.font.Font("DejaVuSerif.ttf", 12)	
		self.Box = pygame.Rect(0,0,0,0)
	
	def draw(self, win):
		pygame.draw.rect(win, (32,32,32,255), pygame.Rect(50, 50, win.get_width() - 100, win.get_height() - 100), 0)
		pygame.draw.rect(win, (128,128,128,255), pygame.Rect(50, 50, win.get_width() - 100, win.get_height() - 100 ), 1)
		self.Box = pygame.Rect(50, 50, win.get_width() - 100, win.get_height() - 100)	
	
	def process(self, event):
		if event.type == KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				self.toClose = True
		
		if event.type == MOUSEBUTTONDOWN:
			if not self.Box.collidepoint(event.pos):
				self.toClose = True
