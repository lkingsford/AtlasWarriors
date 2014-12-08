import json

TUTORIAL_FIRSTRUN   = 0
# These consts match the ItemClasses. Do not change as will break
# player_character.py - Equip.
TUTORIAL_BLUNT      = 1
TUTORIAL_SWORD      = 2
TUTORIAL_POLEARM    = 3
TUTORIAL_DAGGER     = 4
TUTORIAL_AXE        = 5
TUTORIAL_SHIELD     = 6
TUTORIAL_TWOHANDED  = 7
# Further tutorials
TUTORIAL_ATTACK     = 8
TUTORIAL_DEFEND     = 9
TUTORIAL_FIRE       = 10
TUTORIAL_DEATH      = 11
TUTORIAL_SECONDWIND = 12
TUTORIAL_LEVEL      = 13
TUTORIAL_WEAPONLVL  = 14
TUTORIAL_ATTACKED   = 15
TUTORIAL_UNARMED    = 16


class Tutorial:
    def __init__(self, messageDialogFunction, activateDialog):
        
        # Whether each tutorial message has been seen
        self.tutorial_settings = {}
        
        # Set whether tutorial meessages have been seen before from
        # 'tutorial.json'.
        try:
            tutorial_settings_file = open("tutorial.json", mode='r')
            tutorial_settings_temp = json.load(tutorial_settings_file)
            tutorial_settings_file.close()
            # Needed because keys are strings from json
            self.tutorial_settings = dict([(int(i[0]),i[1]) for i in tutorial_settings_temp.items()])
        except FileNotFoundError:
            self.tutorial_settings = dict([(i, False) for i in range(17)])
        
        self.message_dialog_function = messageDialogFunction
        self.activate_dialog = activateDialog
        
    
    def close(self):
        # Saves settings to tutorial.json 
        tutorial_settings_file = open("tutorial.json", mode='w')
        json.dump(self.tutorial_settings, tutorial_settings_file);
        tutorial_settings_file.close()                             
    
    def TriggerMessage (self, message):
        output = ""
        if (message == TUTORIAL_FIRSTRUN) and\
            not(self.tutorial_settings[TUTORIAL_FIRSTRUN]):
                
            # Multiple screens must be in reverse order of appearance
            # due to a quirk of how it is programmed.
            output = (
                "That's all you should need for now. Good luck, and good "+\
                "hunting!"
                )
            self.message_dialog_function(output,
                ActiveDialog = self.activate_dialog)
            output = (
                "By default, you pick up all items you walk over. You can "+\
                "change this by pushing 'a'.\n"+\
                "You can enable the background by pushing 'b'.\n"
                )
            self.message_dialog_function(output,
                ActiveDialog = self.activate_dialog)
            output = (
                "You currently have no weapons equipped. If you click on the "+\
                "Inventory button (or push 'i'), you can equip a weapon if "+\
                "you so wish. Alternatively, you can rely on good ol' "+\
                "fisticuffs to extinguish the threats in the domain of the "+\
                "warlord. It's up to you.\n"+\
                "Each weapon has unique abilities that will aid you in your "+\
                "quest. You can review these from the inventory screen.\n"+\
                "You will gain experience with weapons (and fisticuffs) "+\
                "can be reviewed by clicking the Skills button (or push "+\
                "'s')\n"
                )
            self.message_dialog_function(output,
                ActiveDialog = self.activate_dialog)   
            output = (
                "You can move by using the arrows, or by using the numeric "+\
                "keypad.\n"+\
                "You can attack monsters by moving into them.\n"+\
                "You can move your mouse over monsters and items to see what "+\
                "they are.\n"+\
                "You can see what your health, current attack, current "+\
                "defence, XP and level are on the bottom of the screen"
                )
            self.message_dialog_function(output,
                ActiveDialog = self.activate_dialog)
            output = (
                "This game is still in Alpha and unfinished, but I really " +\
                "appreciate you playing it.\n"+\
                "Feedback is fantastic. If you think that the game could be "+\
                "improved in some way, please let me know!\n"+\
                "If the game crashes on you, I'd really appreciate you "+\
                "logging the bug on " +\
                "https://github.com/lkingsford/AtlasWarriors/issues " +\
                "with as much information as you can tell me. I can't " +\
                "fix bugs I don't know about."                
                )
            self.message_dialog_function(output,
                ActiveDialog = self.activate_dialog)            
            output = (
                "Welcome to Atlas Warriors\n"+\
                "You, Hunter, have been conscripted in the fight against the "+\
                "mighty warlord. Within you will face monsters, hordes of "+\
                "undead, and dragons taken from the pages of myth.\n"           
                )
            self.message_dialog_function(output,
                ActiveDialog = self.activate_dialog)
            self.tutorial_settings[TUTORIAL_FIRSTRUN] = True
                
        if message == TUTORIAL_DEATH and\
            not (self.tutorial_settings[TUTORIAL_DEATH]):
                
            output = (
                "Unfortunately for you, you have met your mortal end.\n"+\
                "It happens to everybody. The only thing for it is to "+\
                "restart and try again. Your next adventure will be "+\
                "randomly generated again, with new maps, monsters and "+\
                "treasure.\n"+\
                "And maybe, just maybe, if you learnt something, you might "+\
                "find and slay the Warlord!\n"+\
                "Better luck next time."
                )                
            self.message_dialog_function(output,
                ActiveDialog = self.activate_dialog)
            self.tutorial_settings[TUTORIAL_DEATH] = True

        if message == TUTORIAL_SECONDWIND and\
            not (self.tutorial_settings[TUTORIAL_SECONDWIND]):
                
            output = (
                "So - the bad news is, you have got no health left.\n"+\
                "The good news is that you have a chance to save your soul "+\
                "in KILL OR BE KILLED!\n"+\
                "KILL OR BE KILLED gives you an opportunity to find a "+\
                "second wind and come back alive, providing you kill "+\
                "something in the next few turns.\n"+\
                "If you fail, then your story will end here.\n"+\
                "On Easiest, you have 8 turns and will regain 75% of your " +\
                "health.\n"+\
                "On Normal, you have 6 turns and will regain 75% of your " +\
                "health.\n"+\
                "On Hard, you have 5 turns and will regain 50% of your " +\
                "health.\n"+\
                "On Hardest, you have 4 turns and will regain 25% of your "+\
                "health.\n"
                )                
            self.message_dialog_function(output,
                ActiveDialog = self.activate_dialog)
            self.tutorial_settings[TUTORIAL_SECONDWIND] = True
        
        if message == TUTORIAL_ATTACKED and\
            not (self.tutorial_settings[TUTORIAL_ATTACKED]):
                
            output = (
                "Ouch! That attack hit you and you've lost some health!\n"+\
                "You're not going to regain it just by standing around "+\
                "and waiting to heal.\n"+\
                "You can heal yourself by exploring places you haven't "+\
                "seen yet.\n"+\
                "You can also be fully healed by gaining a level after "+\
                "killing some enemies.\n"+\
                "Finally, you can regain some of your health by killing "+\
                "a monster in KILL OR BE KILLED whilst you're on the brink "+\
                "of death."
                )                
            self.message_dialog_function(output,
                ActiveDialog = self.activate_dialog)
            self.tutorial_settings[TUTORIAL_ATTACKED] = True
            
        if message == TUTORIAL_WEAPONLVL and\
            not (self.tutorial_settings[TUTORIAL_WEAPONLVL]):
                
            output = (
                "It's not just how big the sword is, it's how you use it.\n"+\
                "You've just gained a weapon skill! Check it out by looking "+\
                "at the Skills screen by clicking the skills button or "+\
                "pushing 's'.\n"+\
                "By using weapons or fisticuffs, you train Skills. When you "+\
                "get more skilled at using something, you'll hit harder " +\
                "(damage increase), increase you chance of hitting (hit " +\
                "increase), and decrease the chance enemies will hit you ("+\
                "defence increase).\n"
                )                
            self.message_dialog_function(output,
                ActiveDialog = self.activate_dialog)
            self.tutorial_settings[TUTORIAL_WEAPONLVL] = True
            
        if message == TUTORIAL_LEVEL and\
            not (self.tutorial_settings[TUTORIAL_LEVEL]):
            
            # See earlier comment that multiple dialogs need
            # to be in reverse order
            
            output = (
                "...RUN!"
                )                
            self.message_dialog_function(output,                
                ActiveDialog = self.activate_dialog)
            
            output = (
                "Your hard work has paid off. You've accumulated enough " +\
                "experience from slaying monsters to gain a level. This " +\
                "means you get more health, and are fully healed! \n" +\
                "You deal more damage (and take less damage from) enemies " +\
                "who are a lower level then you. You deal less damage (and "+\
                "take more damage from) enemies who are a higher " +\
                "level then you. \n"+\
                "If you find an enemy that is more then a few levels higher "+\
                "then you..."
                )                
            self.message_dialog_function(output,
                ActiveDialog = self.activate_dialog)

            self.tutorial_settings[TUTORIAL_LEVEL] = True
            
        if message == TUTORIAL_BLUNT and\
            not (self.tutorial_settings[TUTORIAL_BLUNT]):

            output = (
                "You've just equipped a blunt force trauma weapon.\n"+\
                "Blunt weapons will stun enemies when you hit them, "+\
                "preventing them from moving or attacking for a turn"
                )                
            self.message_dialog_function(output,
                ActiveDialog = self.activate_dialog)

            self.tutorial_settings[TUTORIAL_BLUNT] = True
        
        if message == TUTORIAL_SWORD and\
            not (self.tutorial_settings[TUTORIAL_SWORD]):

            output = (
                "You've just equipped a sword.\n"+\
                "When you have a sword equipped, you will sometimes parry "+\
                "attacks by enemies - preventing them from attacking you, "+\
                "and getting a free attack on them!"
                )                
            self.message_dialog_function(output,
                ActiveDialog = self.activate_dialog)

            self.tutorial_settings[TUTORIAL_SWORD] = True            

        if message == TUTORIAL_POLEARM and\
            not (self.tutorial_settings[TUTORIAL_POLEARM]):

            output = (
                "You've just equipped a polearm.\n"+\
                "When you attack with a polearm, you will also attack any "+\
                "enemies directly behind the enemy you're attacking.\n"+\
                "You also can skewer them when they walk towards you, "+\
                "or lunge at them when you walk towards them."
                )                
            self.message_dialog_function(output,
                ActiveDialog = self.activate_dialog)

            self.tutorial_settings[TUTORIAL_POLEARM] = True  

        if message == TUTORIAL_DAGGER and\
            not (self.tutorial_settings[TUTORIAL_DAGGER]):

            output = (
                "You've just equipped a dagger.\n"+\
                "If you get attacked while you're weilding a dagger, "+\
                "you get a free counterattack with a very high "+\
                "chance of hitting. It's time for revenge!"
                )                
            self.message_dialog_function(output,
                ActiveDialog = self.activate_dialog)

            self.tutorial_settings[TUTORIAL_DAGGER] = True    
                            
        if message == TUTORIAL_AXE and\
            not (self.tutorial_settings[TUTORIAL_AXE]):

            output = (
                "Axes High!\n"+\
                "You've just equipped an axe.\n"+\
                "When you attack with an axe, you'll also attack any enemies "+\
                "who are next to them in a 90 degree arc. So, if you attack "+\
                "to the North, you'll also attack to the North-East and the "+\
                "North-West."
                )                
            self.message_dialog_function(output,
                ActiveDialog = self.activate_dialog)

            self.tutorial_settings[TUTORIAL_AXE] = True

        if message == TUTORIAL_SHIELD and\
            not (self.tutorial_settings[TUTORIAL_SHIELD]):

            output = (
                "Survival ahoy!\n"+\
                "You've just equipped a shield.\n"+\
                "Shields allow you to block enemy attacks. They also can "+\
                "block you from scorching flames and prevent you being "+\
                "ignited.\n"
                "I'd put that last sentence in your memory.\n"
                "It may significantly assist you in the later levels!"
                )                
            self.message_dialog_function(output,
                ActiveDialog = self.activate_dialog)

            self.tutorial_settings[TUTORIAL_SHIELD] = True
            
        if message == TUTORIAL_TWOHANDED and\
            not (self.tutorial_settings[TUTORIAL_TWOHANDED]):

            output = (
                "So - feel like wrecking havoc with two weapons at once do "+\
                "you?\n"+\
                "When you have two weapons equipped, you attack with both at "+\
                "once. This is undoubtably awesome. \n"+\
                "But:\n"+\
                "You do get a significant penalty in your chance to hit with "+\
                "each weapon. This penalty can be reduced by practicing "+\
                "wielding two weapons at once. You can see your skill "+\
                "with two weapons in the skill screen with the weapon "+\
                "skills."
                )                
            self.message_dialog_function(output,
                ActiveDialog = self.activate_dialog)

            self.tutorial_settings[TUTORIAL_TWOHANDED] = True
            
            
        if message == TUTORIAL_FIRE and\
            not (self.tutorial_settings[TUTORIAL_FIRE]):

            output = (
                "Something smells good. Are you cooking something?\n"+\
                "Oh. It's you.\n"+\
                "So - you've caught fire. You're going to take some damage "+\
                "until you're extinguished. To extinguish yourself, you have "+\
                "to stand still (push '5') for 3 turns in a row.\n"+\
                "Piece of cake."
                )                
            self.message_dialog_function(output,
                ActiveDialog = self.activate_dialog)

            self.tutorial_settings[TUTORIAL_FIRE] = True            
            
        if message == TUTORIAL_UNARMED and\
            not (self.tutorial_settings[TUTORIAL_UNARMED]):
                
            output = (
                "Fisticuffs eh? Good for you.\n"+\
                "When you successfully hit somebody while you're unarmed, "+\
                "you can sometimes give them a pummelling! This means that "+\
                "you get a free attack on them, with a slightly higher "+\
                "chance to hit.\n"+\
                "You also gain unarmed skills a bit faster then other "+\
                "weapons, and get bigger bonuses to your attack and damage "+\
                "as you get more skilled with yours fists."
                )                
            self.message_dialog_function(output,
                ActiveDialog = self.activate_dialog)
            self.tutorial_settings[TUTORIAL_UNARMEDF] = True
        
