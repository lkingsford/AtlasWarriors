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

class Tutorial:
    def __init__(self, messageDialogFunction, activateDialog):
        self.message_dialog_function = messageDialogFunction
        self.activate_dialog = activateDialog
                
    def TriggerMessage (self, message):
        output = ""
        if message == TUTORIAL_FIRSTRUN:
            output = ("Welcome to Atlas Warriors")
        if message == TUTORIAL_DEATH:
            output = ("")
        self.message_dialog_function(output,
            ActiveDialog = self.activate_dialog)
