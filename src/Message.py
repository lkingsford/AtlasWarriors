class Message:
    def __init__(self, text, location=None):
        self.text = text
        self.location = location
        self.seen = False

class MessageLog (list):
    def __init__(self, PC):
        list.__init__(self)
        self.PC = PC
        
    def append(self, item):
        # Append message if in sight, or no location
        if (item.location == None):
            list.append(self, item)
            return
         
        if (max(map(lambda i: self.PC.currentMap.VisibilityStatus(i[0],i[1]),\
            item.location)) >= 2):
            list.append(self, item)
            return
        
