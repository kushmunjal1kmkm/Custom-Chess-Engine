import random

def findrandommove(validMoves):
    if len(validMoves) == 0:
        return None
    return random.choice(validMoves)

def findbestmoves():
    return