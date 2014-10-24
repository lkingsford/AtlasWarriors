import pygame

from pygame.locals import *

class BasicGui:	
	def __init__(self):
		self.elements = []
		
	def ProcessEvent(self, event):	
		if (event.type == MOUSEDOWN):
			element = next(i for i in self.elements if ((i.x >= self.x) and (i.x + i.w <= self.x + self.w)  and (i.y >= self.y) and (i.y + i.h <= self.y + self.h)))
			if (element.OnClick != None):
				element.OnClick()
	
	def Paint(self, target):
		for i in self.elements:
			i.Paint(target)
		
class GuiElement:
	def __init__(self, x, y, w, h, OnClick = None, OnMouseDown = None, OnMouseUp = None):
		self.x = x
		self.y = y
		self.w = w
		self.h = h
		self.OnClick = OnClick
		self.hotkey = None
		
	def Paint(self, target):
		raise NotImplementedError
		
class Button(GuiElement):
	def __init__(self, x, y, w, h, OnClick = None):
		super().__init__(x,y,w,h,OnClick)
		self.caption = ""
		self.foreColor = Color(255, 255, 255, 255)
		self.backColor = Color(64, 64, 64, 255)
		self.borderColor = Color(128, 128, 128, 255)
		self.font = pygame.font.Font("DejaVuSans.ttf", 12)
		
	def Paint(self, target):
		pygame.draw.rect(target, self.backColor, Rect(self.x,self.y,self.w,self.h), 0)
		pygame.draw.rect(target, self.borderColor, Rect(self.x,self.y,self.w,self.h), 1)
		size = self.font.size(self.caption)
		
