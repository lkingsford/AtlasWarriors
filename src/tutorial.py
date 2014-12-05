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
TUTORIAL_LASTCHANCE = 11

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
            self.tutorial_settings = dict([(i, False) for i in range(11)])
        
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
                "they are."
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

