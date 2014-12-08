import pygcurse
import pygame
import sys
import math
import random
import map
import character
import player_character
import dialog
import inventoryDialog
import messagesDialog
import skillsDialog
import item
import xml2object
import code
import enemy
import animation
import Message
import scores
import difficulty
import mainmenu
import os
import messageBox
import sys
import logging
import traceback

from tutorial import *
from pygame.locals import *
     
# Get chance to hit
# Input is To Hit - To Defend
# Output between 0 and 1

def getToHitChance (toHit):
    return math.atan(0.6577 * toHit - 3.5 + math.pi / 2)/math.pi


# Get critical chance
# Input is To Hit
def getToCritChance (toHit):
    return math.atan(0.2124 * toHit - 3.5 + math.pi / 2)/math.pi


def LoseGame (win):
    win.setscreencolors('lime', 'black', clear=True)
    win.putchars('For you, the dream ends here.', 6, 5, 'white', 'black')
    win.putchars('You have died.', 14, 10, 'white', 'black')
    win.putchars('Well. That sucks.', 13, 15, 'white', 'black')
    score = scores.CalculateScore(Maps, PC, difficulty, 0)  
    win.putchars('Score: ' + str(score), 2, 17, 'red', 'black')
        
    win.update() 
    screen.blit(surface,(0,0))
    pygame.display.update()
    pygame.display.flip()
    pygcurse.waitforkeypress()  
    pygcurse.waitforkeypress()        
    

# Spoiler warning!
#
#
#
#
#
#
#
#
#
#
#
#
#


def WinGame (victoryCondition, win):
    if victoryCondition == 1:
        win.setscreencolors('lime', 'black', clear=True)    
        win.putchars('Congratulations!', 1, 2, 'white', 'black')
        win.putchars('The mighty warlord has been slain', 1, 3, 'white', 'black')
        win.putchars('at last!', 1, 4, 'white', 'black')
        win.putchars('It may not last, but peace is upon', 1, 5, 'white', 'black')
        win.putchars('this part of Atlas.', 1, 6, 'white', 'black')
        
    elif victoryCondition == 2:
        win.setscreencolors('lime', 'black', clear=True)    
        win.putchars('Congratulations!', 1, 2, 'white', 'black')
        win.putchars('The mighty warlord has been slain', 1, 3, 'white', 'black')
        win.putchars('It may not have been by your hand, but', 1, 4, 'white', 'black')
        win.putchars('this part of Atlas is at least for now,', 1, 5, 'white', 'black')
        win.putchars('in peace.', 1, 6, 'white', 'black')
    
    elif victoryCondition == 3:
        win.setscreencolors('lime', 'black', clear=True)    
        win.putchars('The mighty warlord has been slain', 1, 3, 'white', 'black')
        win.putchars('by the horrible demonic goliath.', 1, 4, 'white', 'black')
        win.putchars('Absorbing his vast power, the ', 1, 5, 'white', 'black')
        win.putchars('unholy beast unleashes hell upon', 1, 6, 'white', 'black')
        win.putchars('Atlas.', 1, 7, 'white', 'black')
        win.putchars('Doom awaits those who survive.', 1, 7, 'white', 'black')
    
    elif victoryCondition == 4:
        win.setscreencolors('lime', 'black', clear=True)    
        win.putchars('The mighty warlord has been slain', 1, 3, 'white', 'black')
        win.putchars('by the apocalyptic goliath.', 1, 4, 'white', 'black')
        win.putchars('Absorbing his vast power, the ', 1, 5, 'white', 'black')
        win.putchars('unholy beast unleashes a wave', 1, 6, 'white', 'black')
        win.putchars('of destruction that clouds', 1, 7, 'white', 'black')
        win.putchars('Atlas in fire and desolation', 1, 8, 'white', 'black')
        win.putchars('leaving nothing.', 1, 9, 'white', 'black')
        win.putchars('You achieved your goal of', 1, 10, 'white', 'black')
        win.putchars('bringing peace to Atlas.', 1, 11, 'white', 'black')
        win.putchars('You have done so eternally.', 1, 12, 'white', 'black')
        
    elif victoryCondition == 5:
        win.setscreencolors('lime', 'black', clear=True)    
        win.putchars('The mighty warlord has been slain', 1, 3, 'white', 'black')
        win.putchars('by the Mortreon, the True Dragon.', 1, 4, 'white', 'black')
        win.putchars('Mortreon absorbs the explosion of', 1, 5, 'white', 'black')
        win.putchars('power in its entirity and' , 1, 6, 'white', 'black')
        win.putchars('unleashes an almighty roar', 1, 7, 'white', 'black')
        win.putchars('resurrecting Eon, the God King of', 1, 8, 'white', 'black')
        win.putchars('Dragons.', 1, 9, 'white', 'black')
        win.putchars('The second age of Eon will', 1, 10, 'white', 'black')
        win.putchars('come.', 1, 11, 'white', 'black')
        win.putchars('The sons of Eon will reign.', 1, 12, 'white', 'black')     
        
    elif victoryCondition == 6:
        win.setscreencolors('lime', 'black', clear=True)    
        win.putchars('The mighty warlord has been slain', 1, 3, 'white', 'black')
        win.putchars('by the blackest of the black', 1, 4, 'white', 'black')
        win.putchars('The Necromancer grins as his ', 1, 5, 'white', 'black')
        win.putchars('flesh rots away under the', 1, 6, 'white', 'black')
        win.putchars('force of his absorbed power.', 1, 7, 'white', 'black')
        win.putchars('With the power of the warlord', 1, 8, 'white', 'black')
        win.putchars('the Necromancer enslaves', 1, 9, 'white', 'black')
        win.putchars('Atlas. And what of his body?', 1, 10, 'white', 'black')
        win.putchars('Bodies are for mortal men.', 1, 11, 'white', 'black')
    
    score = scores.CalculateScore(Maps, PC, difficulty, victoryCondition)   
    win.putchars('Score: ' + str(score), 2, 17, 'red', 'black')
    win.update();
    screen.blit(surface,(0,0))
    pygame.display.update()
    pygame.display.flip()
    
    pygcurse.waitforkeypress()
    pygcurse.waitforkeypress()       
    
    
def DrawMap():
    for x in range(40):
        for y in range(20):
            DrawChar(x, y)          

def DrawChar(x, y): 
    vis = PC.currentMap.VisibilityStatus(x,y)
    darkColor = pygame.Color(32,32,32)
    if (ShowMapCheat == True): vis = 2
    if vis == 0 :
        win.putchar(' ', x, y, 'black', pygame.Color(0,0,0,0));
    elif vis == 1:
        win.putchar(PC.currentMap.Map[x][y].character, x, y, darkColor, pygame.Color(0,0,0,0));
    elif vis == 2:
        win.putchar(PC.currentMap.Map[x][y].character, x, y, PC.currentMap.Map[x][y].forecolor, PC.currentMap.Map[x][y].backcolor);

# This is here for dialogs that show during times the game loop isn't running
# to be able to be used.
#
# There is a bug that it can't be closed in this state
def DialogOnlyLoop(dialog, surface):    
    while (len(dialog) > 0):
        for event in pygame.event.get():                
            dialog[0].process(event)
        dialog[0].draw(surface)
        screen.blit(surface,(0,0))
        pygame.display.update()
        pygame.display.flip()
        if dialog[0].toClose:
            dialog.remove(dialog[0])
        
def log_uncaught_exceptions(ex_cls, ex, tb):

    logging.critical(''.join(traceback.format_tb(tb)))
    logging.critical('{0}: {1}'.format(ex_cls, ex))
    
    print(''.join(traceback.format_tb(tb)))
    print('{0}: {1}'.format(ex_cls, ex))


# This needs to be a list so it can be immutable and be passed by reference.
# This has the side effect of allowing multiple dialogs.
dialog = []
lastDialog = None

# Main function

# Init

# Store log of errors
sys.excepthook = log_uncaught_exceptions
logging.basicConfig(
    level=logging.DEBUG,
    filename='error.log',
    filemode='w')

screen = pygame.display.set_mode((520,648))
pygame.display.set_caption('Atlas Warriors')
surface = pygame.Surface((520, 648))
win = pygcurse.PygcurseSurface(width=40, height=27, windowsurface=surface)
win.font = pygame.font.Font("DejaVuSansMono.ttf", 20)
descriptFont = pygame.font.Font("DejaVuSansMono.ttf", 10)
descriptTitleFont = pygame.font.Font("DejaVuSansMono.ttf", 12)
messageFont = pygame.font.Font("DejaVuSerif.ttf", 12)
hpFont = pygame.font.Font("DejaVuSerif.ttf", 20) 
clock = pygame.time.Clock()
messageLog = []
tutorial = Tutorial(messageBox.MessageBox, dialog);
background = True

# This should be states or something. Add to the refactor list!
# If a difficulty is in the command line arguments, start
if len(sys.argv) > 1:
    action = int(sys.argv[1])
else:
    action = mainmenu.MainMenu(win, screen, surface)

win = pygcurse.PygcurseSurface(width=40, height=27, windowsurface=surface, shadow=True)
win.font = pygame.font.Font("DejaVuSansMono.ttf", 20)

# Can enable cheat mode by setting difficulty to 6, 7, 8 or 9 in the arguments 
if action > 6:
    action = action % 7
    cheatMode = True
else:
    cheatMode = False

if action == 0:
    difficulty = difficulty.Easiest()
elif action == 1:
    difficulty = difficulty.Normal()
elif action == 2:
    difficulty = difficulty.Hard()
elif action == 3:
    difficulty = difficulty.Hardest()
elif action == 6:
    sys.exit()


win.colors = ('red', 'gray')
cellx = 0
celly = 0
ShowMapCheat = False
mouseX = 0
mouseY = 0
# To prevent weird startup mouse bugs
mousePos = (1,1)
mouseCellX = 0
mouseCellY = 0

ssframe = 0

# Load default items
DefaultItems = xml2object.parse('items.xml', item.Item)

# Create maps
Maps = []
for i in range(10):
    Maps.append(map.Map(i, messageLog, DefaultItems, difficulty));

for i in range(10):
    if (i != 9):
        Maps[i].nextMap = Maps[i + 1]
    if (i != 0):
        Maps[i].lastMap = Maps[i - 1]
    Maps[i].background = pygame.image.load(os.path.join('assets','back_level_'+str(i % 4)+'.png'))
        
PC = player_character.PlayerCharacter(messageLog, Maps[0], DefaultItems, difficulty, tutorial)
PC.x = Maps[0].startX
PC.y = Maps[0].startY
Maps[0].UpdateVisibility(PC, PC.x, PC.y)

currentTint = (0,0,0,0)

PC.currentMap.characters.append(PC)
lastMap = None

# This is not great
AllMonsters = []
for i in Maps: AllMonsters.extend(i.characters)

EndBoss = next(i for i in AllMonsters if i.chartype == "endboss")

win.autoupdate = False # THIS DISABLES THE AUTOUPDATE FEATURE
win._autodisplayupdate = False
pygame.key.set_repeat(300,30);


ForceDraw = False

Animations = []

# Pathfinding benchmarks:
# import timeit
# print (' Get Route: ')
# times = []
# for x in range(2, 39):
    # for y in range(2, 19):        
        # #print(x,y)
        # times.append(timeit.timeit('PC.GetRoute((x, y))', 'gc.enable(); from __main__ import PC, x, y', number = 10))     
                    # 
# print ('Average ', sum(times)/float(len(times)), ' Min ', min(times), ' Max ', max(times))
# print (' Get Nearest: ')
# times = []
# for x in range(2, 39):
    # for y in range(2, 19):        
        # #print(x,y)       
        # times.append(timeit.timeit('PC.GetNearest((lambda i: i[0] == x and i[1] == y))', 'gc.enable(); from __main__ import PC, x, y', number = 10))
                    # 
# print ('Average ', sum(times)/float(len(times)), ' Min ', min(times), ' Max ', max(times))
# 

PC.ChangeMap(Maps[0])

# Show introduction tutorial message if first run
tutorial.TriggerMessage(TUTORIAL_FIRSTRUN)      

running = True

while running or len(Animations) > 0: 

    if len(dialog) != 0 and dialog[0].toClose == True:
        dialog.remove(dialog[0])
        ForceDraw = True

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        if len(dialog) == 0:
            if event.type == MOUSEMOTION:
                mouseCellX, mouseCellY = win.getcoordinatesatpixel(event.pos)
                mousePos = event.pos
            if event.type == KEYDOWN and PC.nextMove == 'none':
                if event.key == pygame.K_LEFT or event.key == pygame.K_4 or event.key == pygame.K_KP4:
                    PC.nextMove = 'move_e'              
                    
                if event.key == pygame.K_UP or event.key == pygame.K_8 or event.key == pygame.K_KP8:
                    PC.nextMove = 'move_n'
                    
                if event.key == pygame.K_DOWN or event.key == pygame.K_2 or event.key == pygame.K_KP2:
                    PC.nextMove = 'move_s'
                    
                if event.key == pygame.K_RIGHT or event.key == pygame.K_6 or event.key == pygame.K_KP6:
                    PC.nextMove = 'move_w'
                    
                if event.key == pygame.K_7 or event.key == pygame.K_KP7:
                    PC.nextMove = 'move_ne'
                    
                if event.key == pygame.K_9 or event.key == pygame.K_KP9:
                    PC.nextMove = 'move_nw'
                    
                if event.key == pygame.K_1 or event.key == pygame.K_KP1:
                    PC.nextMove = 'move_se'
                    
                if event.key == pygame.K_3 or event.key == pygame.K_KP3:
                    PC.nextMove = 'move_sw'
                    
                if event.key == pygame.K_5 or event.key == pygame.K_KP5:
                    PC.nextMove = 'wait'
                    
                if event.key == pygame.K_i:
                    dialog.insert(0, inventoryDialog.InventoryDialog(PC))
                    
                if event.key == pygame.K_s:
                    dialog.insert(0, skillsDialog.SkillsDialog(PC))
                    
                if event.key == pygame.K_m:
                    dialog.insert(0, messagesDialog.MessagesDialog(messageLog))
                    
                if event.key == pygame.K_a:
                    PC.autopickup = not(PC.autopickup)
                    if PC.autopickup:
                        messageLog.append(Message.Message(\
                            "Autopickup has been enabled"))
                    else:
                        messageLog.append(Message.Message(\
                            "Autopickup has been disabled."))
                    
                if event.key == pygame.K_b:
                    background = not(background)
                    ForceDraw = True
                
                if cheatMode == True:                              
                    if event.key == pygame.K_F1:
                        ShowMapCheat = not ShowMapCheat
                        ForceDraw = True

                    if event.key == pygame.K_F2:
                        code.interact(local=locals())
                        
                    if event.key == pygame.K_F3:
                        PC.ChangeMap(Maps[PC.currentMap.level-1])
                        PC.currentMap.UpdateVisibility(PC, PC.x, PC.y)
                        ForceDraw = True
                        
                    if event.key == pygame.K_F4:
                        PC.ChangeMap(Maps[PC.currentMap.level+1])
                        PC.currentMap.UpdateVisibility(PC, PC.x, PC.y)
                        ForceDraw = True
                        
        else:
            dialog[0].process(event)
        
        if event.type == MOUSEBUTTONDOWN:           
            mouseCellX, mouseCellY = win.getcoordinatesatpixel(event.pos)
            #print(win.getcoordinatesatpixel(event.pos))
            if mouseCellY == 26:
                if mouseCellX < 9:                  
                    dialog.insert(0, messagesDialog.MessagesDialog(messageLog))
                if mouseCellX >= 9 and mouseCellX < 18:
                    dialog.insert(0, inventoryDialog.InventoryDialog(PC))
                if mouseCellX >= 18 and mouseCellX < 27:
                    dialog.insert(0, skillsDialog.SkillsDialog(PC))                           
            
#           if mouseCellX > 0 and mouseCellY > 0 and mouseCellX < 39 and mouseCellY < 19:
                #Animations.append(animation.DrawNecromancerSpell(PC.currentMap.characters[2], PC, 'red'))
                
    if len(Animations) == 0:
        
        #Update characters if no current animations 
        if (len(dialog) == 0) and not(PC.nextMove == 'none' and PC.ticksUntilTurn <= 0):          
            # Update Characters
            
            # This seems hacky, but it's to prevent the monsters
            # moving at the same time (actually, same turn but
            # beforehand) meaning that attacks didn't hit
            if PC.ticksUntilTurn <= 0:
                PC.update()
                # This needs investigation to see if this goes here. It is the
                # part that will add more monsters after an uncertain amount
                # of time
                PC.currentMap.Tick()
                # This is to prevent PC getting one tick advantage
                PC.ticksUntilTurn += 1
                
            for character in PC.currentMap.characters:
                if character.ticksUntilTurn <= 0:
                    DrawChar(character.x, character.y)  
                    character.update()              
                else:
                    character.ticksUntilTurn -= 1
                Animations.extend(character.animations)
                character.animations.clear()
    else:
        clock.tick(20)
        #pygame.image.save(win._windowsurface, "ss\\%05d" % ssframe + ".png")
        #ssframe += 1

    #Draw Screen
    
    # Draw Background
    if background:
        surface.blit(PC.currentMap.background, (0,0)) 
    else:
        surface.fill((0,0,0,255))
 
    
    #Draw Map   
    if (lastMap != PC.currentMap or PC.currentMap.visibilityUpdated == True or ForceDraw == True):
        DrawMap()
        PC.currentMap.visibilityUpdated = False
        ForceDraw = False
    
    lastMap = PC.currentMap
    
    #Draw map over characters
    for character in PC.currentMap.characters:
        DrawChar(character.x, character.y)  
        
    #Draw Items
    for item in PC.currentMap.Items:
        if (PC.currentMap.VisibilityStatus(item.x, item.y)) == 2 or ShowMapCheat:
            win.putchar(item.Character, item.x, item.y, item.Color, None)
    
    #Draw Characters
    for character in PC.currentMap.characters:
        if not character.dead():
            if (PC.currentMap.VisibilityStatus(character.x,character.y)) == 2 or ShowMapCheat:
                win.putchar(character.character,character.x, character.y, character.Color()[0], character.Color()[1])
        else:
            #Probably not where this should be
            PC.currentMap.characters.remove(character)          

    # Draw animations if there are any. 
    for i in Animations:
        if i.frame >= i.frames:
            Animations.remove(i)
            ForceDraw = True
        else:
            i.tick(win, PC.currentMap)
            #pygame.image.save(win._windowsurface, "c:\\ss\\%05d" % ssframe + ".bmp")
            #ssframe += 1
    

    # Draw redenning if in Second Wind
    if PC.secondWind:
        newTint = ((difficulty.secondWindTime + 1 - PC.secondWindTimeLeft) * 255//5,0,0)                
    else:
        newTint = (0,0,0)
        
    if newTint != currentTint:
        win.settint(newTint[0], newTint[1], newTint[2],(0,0,40,20))        
        currentTint = newTint
    
    #win.putchars('Score: ' + str(scores.CalculateScore(Maps, PC, 1, 0) ), 2, 17, 'red')
    
    if len(dialog) != 0:
        dialog[0].draw(surface)
        screen.blit(surface,(0,0))
    else:
        win.update() # THIS IS THE NEW CALL TO THE UPDATE() METHOD
     
    # Draw HUD 
    
    # Draw Messages
    toHit = PC.ToHit()
    lines = [
        hpFont.render('HP ' + str(PC.hp) + ' (' + str(PC.maxhp) + ')    Level ' + str(PC.level) +\
            '    XP ' + str(PC.xp) + ' (' + str(int(PC.nextLevel)) + ')' \
            '   Hit ' + str(toHit[0][0]) +\
            (', ' + str(toHit[1][0]) if len(toHit) > 1 else '') + '  Def ' +\
        str(PC.ToDefend()), True, (255,255 if PC.ZombieMod() == 0 else 0,255 if PC.ZombieMod() == 0 else 0, 255))]
    if len(messageLog) > 0: lines.append(messageFont.render(messageLog[len(messageLog)-1].text, True, (255, 255, 255, 255)))
    if len(messageLog) > 1: lines.append(messageFont.render(messageLog[len(messageLog)-2].text, True, (225, 225, 225, 255)))
    if len(messageLog) > 2: lines.append(messageFont.render(messageLog[len(messageLog)-3].text, True, (195, 195, 195, 255)))
    if len(messageLog) > 3: lines.append(messageFont.render(messageLog[len(messageLog)-4].text, True, (165, 165, 165, 255)))
    if len(messageLog) > 4: lines.append(messageFont.render(messageLog[len(messageLog)-5].text, True, (135, 135, 135, 255)))
    
    curY = 5 + win._cellheight * 20
    spacing = 3
    
    for i in lines:
        surface.blit(i, (3,  curY))
        curY += i.get_height() + spacing
    

    
    
    # Draw Bottom Screen Operations
    pygame.draw.rect(surface, pygcurse.colornames['black'], pygame.Rect(0, win._cellheight * 26, win._cellwidth * 9, win._pixelheight - win._cellheight * 1), 0)
    pygame.draw.rect(surface, pygcurse.colornames['blue'], pygame.Rect(0, win._cellheight * 26, win._cellwidth * 9, win._pixelheight - win._cellheight * 1), 1)
    surface.blit(win.font.render(' Messages ', True, (255, 255, 255, 255)), (0, win._cellheight * 26))
    
    pygame.draw.rect(surface, pygcurse.colornames['black'], pygame.Rect(win._cellwidth * 9, win._cellheight * 26, win._cellwidth * 9, win._pixelheight - win._cellheight * 1), 0)
    pygame.draw.rect(surface, pygcurse.colornames['blue'], pygame.Rect(win._cellwidth * 9, win._cellheight * 26, win._cellwidth * 9, win._pixelheight - win._cellheight * 1), 1)
    surface.blit(win.font.render(' Load Out ', True, (255, 255, 255, 255)), (win._cellwidth * 9, win._cellheight * 26))
    
    pygame.draw.rect(surface, pygcurse.colornames['black'], pygame.Rect(win._cellwidth * 18, win._cellheight * 26, win._cellwidth * 9, win._pixelheight - win._cellheight * 1), 0)
    pygame.draw.rect(surface, pygcurse.colornames['blue'], pygame.Rect(win._cellwidth * 18, win._cellheight * 26, win._cellwidth * 9, win._pixelheight - win._cellheight * 1), 1)
    surface.blit(win.font.render('  Skills  ', True, (255, 255, 255, 255)), (win._cellwidth * 18, win._cellheight * 26))                 
        
    if len(dialog) == 0:  
        top =  mousePos[1] 
        #Draw descriptions if mouse over monster
        for i in PC.currentMap.characters:
            if mouseCellX == i.x and mouseCellY == i.y and (PC.currentMap.VisibilityStatus(i.x,i.y)) == 2:
                lines = [descriptTitleFont.render('   ' + i.name, True, (255,0,0,255)),
                     descriptTitleFont.render(str(id(i)), True, (0,0,0,255)),
                     descriptTitleFont.render('Level ' + str(i.level), True, (0,0,0,255)),
                     descriptTitleFont.render('HP ' + str(i.hp) + '/' + str(i.maxhp), True, (0,0,0,255))]
                
                for j in i.ToHit():
                     lines.append(descriptFont.render("To hit: " + str(j[0]), True, (0,0,0,255)))
                
                lines.append(descriptFont.render("To defend: " + str(i.ToDefend()), True, (0,0,0,255)))
                
                for j in PC.ToHit():
                     lines.append(descriptFont.render(str(round(PC.ChanceToHit(j[0], i.ToDefend()) * 100)) + '% chance to hit', True, (255,0,0,255)))
                
                spacing = 3
                                        
                widthNeeded = max(l.get_width() for l in lines ) + 6
                heightNeeded = 3 * len(lines) + sum(l.get_height() for l in lines) + 12
                top = top + heightNeeded
                pygame.draw.rect(surface, pygcurse.colornames['yellow'], pygame.Rect(min(mousePos[0], surface.get_width()-widthNeeded), mousePos[1], (widthNeeded), (heightNeeded)))
                curY = 3
                for i in lines:
                    surface.blit(i, (min(mousePos[0], surface.get_width() - widthNeeded) + 3, mousePos[1] + 3 + curY))
                    curY += i.get_height() + spacing        
        
        itemLines = []
        for i in PC.currentMap.Items:
            if mouseCellX == i.x and mouseCellY == i.y and (PC.currentMap.VisibilityStatus(i.x,i.y)) == 2:
                itemLines.append(descriptFont.render(i.Description(), True, (255,255,255,255)))
        
        if (len(itemLines) > 0):
            widthNeeded = max(l.get_width() for l in itemLines) + 6         
            heightNeeded = 3 * len(itemLines) + sum(l.get_height() for l in itemLines)
            pygame.draw.rect(surface, pygcurse.colornames['green'], pygame.Rect(min(mousePos[0], surface.get_width()-widthNeeded), top, (widthNeeded), (heightNeeded)))
            curY = 0
            for i in itemLines:
                surface.blit(i, (min(mousePos[0], surface.get_width() - widthNeeded) + 3, top + curY))
                curY += i.get_height() + spacing            
        
    # Draw Screen
    screen.blit(surface,(0,0))
    pygame.display.update()
    pygame.display.flip()

    
    #If Lachlan is dead, you win
    if (EndBoss.Victory() != 0):
        running = False
    
    #If Character is dead, you lose
    if (PC.dead()):
        tutorial.TriggerMessage(TUTORIAL_DEATH)
        DialogOnlyLoop(dialog, surface)
        running = False
        
if EndBoss.Victory() != 0:
    WinGame(EndBoss.Victory(), win)
elif PC.dead():
    LoseGame(win)
    
tutorial.close()
pygame.quit()
sys.exit() 

