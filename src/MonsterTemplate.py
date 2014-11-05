from enemy import *

class Healer(Enemy):
    def __init__(self, currentMap = None):
        super().__init__(currentMap)
        
    def update(self):
        super().update()
