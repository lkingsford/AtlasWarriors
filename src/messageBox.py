import dialog
import pygame
from pygame.locals import *
from itertools import chain

# Borrowed from http://www.pygame.org/wiki/TextWrapping?parent=CookBook

def truncline(text, font, maxwidth):
        real=len(text)       
        stext=text           
        l=font.size(text)[0]
        cut=0
        a=0                  
        done=1
        old = None
        while l > maxwidth:
            a=a+1
            n=text.rsplit(None, a)[0]
            if stext == n:
                cut += 1
                stext= n[:-cut]
            else:
                stext = n
            l=font.size(stext)[0]
            real=len(stext)               
            done=0                        
        return real, done, stext             
        
def wrapline(text, font, maxwidth): 
    done=0                      
    wrapped=[]                  
                               
    while not done:             
        nl, done, stext=truncline(text, font, maxwidth) 
        wrapped.append(stext.strip())                  
        text=text[nl:]                                 
    return wrapped
 
 
def wrap_multi_line(text, font, maxwidth):
    """ returns text taking new lines into account.
    """
    lines = chain(*(wrapline(line, font, maxwidth) for line in
        text.splitlines()))
    return list(lines)

class MessageBox(dialog.Dialog):
    DEFAULT_MAX_WIDTH = 400
    
    def __init__(self, message, width = DEFAULT_MAX_WIDTH, ActiveDialog = None):     
        self.toClose = False
        self.TitleFont = pygame.font.Font("DejaVuSerif.ttf", 20) 
        self.BodyFont = pygame.font.Font("DejaVuSerif.ttf", 14)     
        self.width = width;        
        self.message = wrap_multi_line(message, self.BodyFont, width - 20)
        self.message_lines = list(map(lambda x: self.BodyFont.render(x, True,
            (255, 255, 255, 255)), self.message))
        self.height = 20 + len(self.message_lines) *\
            (self.BodyFont.get_linesize() + 3)
        self.line_size = self.BodyFont.get_linesize();        
        if ActiveDialog != None:
            ActiveDialog.insert(0, self)
    
    def draw(self, win):
        self.top = (win.get_height() - self.height - 100)/2
        self.left = (win.get_width() - self.width) / 2
        self.Box = pygame.Rect(self.left, self.top, self.width, self.height)
        pygame.draw.rect(win, (32,32,32,255), self.Box, 0)
        pygame.draw.rect(win, (128,128,128,255), self.Box, 1)
        for i in enumerate(self.message_lines):
            win.blit(i[1], (self.left + 10,
                10+self.top + i[0] * (self.line_size + 3)))        
            
    def process(self, event):
        if event.type == KEYDOWN:            
            self.toClose = True
        
        elif event.type == MOUSEBUTTONDOWN:
            self.toClose = True     
        
