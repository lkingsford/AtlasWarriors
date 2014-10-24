import dialog

class MessagesDialog(dialog.Dialog):
	def __init__(self):
		self.toClose = False
		TitleFont = pygame.font.Font("DejaVuSerif.ttf", 20) 
		BodyFont = pygame.font.Font("DejaVuSerif.ttf", 12)		
	
	def draw(self, win):
		pygame.draw.rect(win._windowsurface, pygcurse.colornames['black'], pygame.Rect(50, 50, win.get_width() - 100, win.get_height() - 100 ))
		pygame.draw.rect(win._windowsurface, pygcurse.colornames['white'], pygame.Rect(50, 50, win.get_width() - 100, win.get_height() - 100 ), 0)
	
	def process(self, event):
		if event.type == KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				self.toClose = True
