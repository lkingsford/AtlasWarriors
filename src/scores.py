
def CalculateScore(Maps, PC, Difficulty, Victory):
    score = 0
    score += PC.totalxp
    # This is to ensure that you gain slightly fewer points by just hanging
    # around
    score -= sum([i.RestockDangerPoints for i in Maps]) * 1.1
    score = round(score)
    if Victory != 0:
        for i in Maps:
            if i.Turn < 20:
                score += 50
            if i.Turn < 50:
                score += 50
    
    for i in PC.skills:
        score += round(i[1]*10)

    if Victory == 2:
        # Monster killed (so down by the Warlords 1000 points)
        # Score is lower, because I don't think it's as impressive
        score += 500
    elif Victory == 3:
        # Hell on Atlas 
        # Score is higher, because difficulty
        score += 1250
    elif Victory == 4:
        # Complete destruction of Atlas
        # Score is higher, because difficulty
        # Score is higher again due to less monsters
        # killed in order to farm the Goliath
        score += 2000
    elif Victory == 5:
        # Dragon Eon Victory
        # Score is higher, because difficulty
        score += 1500
    elif Victory == 6:
        # Necromancer Victory
        # Score is higher, because difficulty
        score += 1500
    

    DifficultyMultiplier = 1            
    # Easiest
    if Difficulty.difficulty == 0:
        DifficultyMultiplier = 0.5
    # Normal
    elif Difficulty.difficulty == 1:
        DifficultyMultiplier = 1
    # Hard
    elif Difficulty.difficulty == 2:
        DifficultyMultiplier = 2
    # Nightmare
    elif Difficulty.difficulty == 3:
        DifficultyMultiplier = 4
    
    score = round(score * DifficultyMultiplier)
    
    return score
            
