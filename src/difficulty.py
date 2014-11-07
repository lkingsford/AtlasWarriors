
# Difficulty class is used to adjust difficulty. Things that rely on the
# current difficulty look to it. The default settings are for Normal.
# I also wonder whether it would be worth adjusting the badass ratio
# and/or damage and maybe xp requirements
#
# Difficulty adjustments for final level are in map.py

class Difficulty():
    def __init__(self):
        self.hpHealRate = 0.002
        self.secondWindTime = 6
        # Heal amount is multiplier of max health
        self.secondWindHealAmount = 0.75
        self.difficulty = 1
    
class Easiest(Difficulty):
    def __init__(self):
        super().__init__()
        self.hpHealRate = 0.005
        self.secondWindTime = 8
        self.secondWindHealAmount = 0.75
        self.difficulty = 0

class Normal(Difficulty):
    def __init__(self):
        super().__init__()
        self.hpHealRate = 0.002
        self.secondWindTime = 6
        self.secondWindHealAmount = 0.75
        self.difficulty = 1

class Hard(Difficulty):
    def __init__(self):
        super().__init__()
        self.hpHealRate = 0.001
        self.secondWindTime = 5
        self.secondWindHealAmount = 0.50
        self.difficulty = 2
        
class Hardest(Difficulty):
    def __init__(self):
        super().__init__()
        self.hpHealRate = 0.0005
        self.secondWindTime = 4
        self.secondWindHealAmount = 0.25
        self.difficulty = 3
