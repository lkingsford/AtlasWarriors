import pygcurse
import pygame
import version
import sys
import webbrowser
from pygame.locals import *


# This is quick, and dirty, but will do the job for now
def MainMenu(win, screen, surface):
    action = -1

    selected = 0
    
    while action == -1:        
        win.putchars('A T L A S    W A R R I O R S', 6, 5)
        win.putchars(version.Version(), 2, 20)
        win.putchars('Lachlan Kingsford 2014',2,21)
        win.fgcolor = 'red'
        win.putchars('WORK IN PROGRESS!',2,22, 'red')
        
        win.update() # THIS IS THE NEW CALL TO THE UPDATE() METHOD
        screen.blit(surface,(0,0))
        pygame.display.flip()
        win.setscreencolors('gray', 'black', clear=True)
        
        selected = selected
        

        win.putchars('Start Easiest Game', 2, 10, 'red' if selected == 0 else 'silver')
        win.putchars('Start Normal Game', 2, 11, 'red' if selected == 1 else 'silver')
        win.putchars('Start Difficult Game', 2, 12, 'red' if selected == 2 else 'silver')
        win.putchars('Start Hardest Game', 2, 13, 'red' if selected == 3 else 'silver')
        win.putchars('Visit Website', 2, 14, 'red' if selected == 4 else 'silver')
        win.putchars('Exit', 2, 15, 'red' if selected == 5 else 'silver')
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_8 or event.key == pygame.K_KP8:
                        selected -= 1
                        if selected == -1:
                            selected = 5
                        
                if event.key == pygame.K_DOWN or event.key == pygame.K_2 or event.key == pygame.K_KP2:
                    selected += 1
                    if selected == 6:
                        selected = 0
                
                if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    action = selected
                    
        if action == 4:
            # I want this to point to a donate page
            webbrowser.open_new_tab("http://www.nerdygentleman.com")
            action = -1
                
    win.erase()
    return action
        
        
