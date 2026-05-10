import random

piecescore = {"king":0, "queen":10, "rook":5, "bishop":3, "knight":3, "pawn":1}
CHECKMATE = 1000
STALEMATE = 0

def findrandommove(validMoves):
    if len(validMoves) == 0:
        return None
    return random.choice(validMoves)

def findbestmoves(gs,validMoves):
    turnmultiplier = 1 if gs.whiteToMove else -1
    maxscore = -CHECKMATE - 1 
    bestmove = None
    random.shuffle(validMoves) # Shuffle so AI doesn't play the exact same game every time
    
    for move in validMoves:
        gs.makeMove(move)
        opponentmoves = gs.getValidMoves()
        
        if gs.staleMate:
            score = STALEMATE
        elif gs.checkMate:
            score = CHECKMATE # This move checkmates the opponent! Max score!
        else:
            # The opponent will try to play the move that is WORST for us.
            # So we need to find the minimum possible score the opponent can force us into.
            opponentMinScore = CHECKMATE + 1
            for opponentmove in opponentmoves:
                gs.makeMove(opponentmove)
                gs.getValidMoves() # Crucial: update flags for the new state
                
                # Evaluate the board from our perspective
                score = turnmultiplier * scorematerial(gs, gs.board)
                
                # The opponent will choose the move that minimizes our score
                if score < opponentMinScore:
                    opponentMinScore = score
                    
                gs.undoMove() # undo opponent's move
            
            # The true score of our move is the worst-case scenario the opponent can force
            score = opponentMinScore
            
        # If this worst-case scenario is better than our previous best move, we pick it
        if score > maxscore:
            maxscore = score
            bestmove = move
            
        gs.undoMove() # undo our move
        
    return bestmove

def scorematerial(gs,board):
    if gs.checkMate:
        if gs.whiteToMove:
            return -CHECKMATE
        else:
            return CHECKMATE
    elif gs.staleMate:
        return STALEMATE
    
    score = 0
    for row in board: 
        for piece in row:
            if piece != "--":
                piece_type = piece.split("-")[1]
                if piece[0] == 'w':
                    score += piecescore[piece_type]
                elif piece[0] == 'b':
                    score -= piecescore[piece_type]
    return score