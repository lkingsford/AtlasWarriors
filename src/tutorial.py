import json

TUTORIAL_FIRSTRUN   = 0
TUTORIAL_SWORD      = 1
TUTORIAL_POLEARM    = 2
TUTORIAL_BLUNT      = 3
TUTORIAL_DAGGER     = 4
TUTORIAL_AXE        = 5
TUTORIAL_SHIELD     = 6
TUTORIAL_ATTACK     = 7
TUTORIAL_DEFEND     = 8
TUTORIAL_FIRE       = 9
TUTORIAL_DEATH      = 10
TUTORIAL_SECONDWIND = 11
TUTORIAL_LEVEL      = 12
TUTORIAL_WEAPONLVL  = 13
TUTORIAL_ATTACKED   = 14

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
            self.tutorial_settings = dict([(i, False) for i in range(15)])
        
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
                "If you find the map difficult to read, you can disable "+\
                "the background by pushing 'b'.\n"
                )
            self.message_dialog_function(output,
                ActiveDialog = self.activate_dialog)
            output = (
                "You currently have no weapons equipped. If you click on the "+\
                "Inventory button (or push 'i'), you can equip a weapon if "+\
                "you so wish. Alternatively, you can rely on good ol' "+\
                "fisticuffs to extinguish the threats in the domain of the "+\
                "warlord.\n"+\
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
                "You deal more damage to enemies who are a lower " +\
                "level then you, and less to enemies who are a higher " +\
                "level then you. Unfortunately, you also take more " +\
                "damage from enemies that are a higher level then you " +\
                "and less from enemies that are a lower level then you.\n"+\
                "If you find an enemy that is more then a few levels higher "+\
                "then you..."
                )                
            self.message_dialog_function(output,
                ActiveDialog = self.activate_dialog)

            self.tutorial_settings[TUTORIAL_LEVEL] = True
