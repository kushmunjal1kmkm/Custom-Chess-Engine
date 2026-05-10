'''
This is the main file for the chess engine. It will be responsible for handling user input and displaying the current gamestate object
'''
import smartmovefinder
from pygame import color
import os
import pygame as p
import ChessEngine
import smartmovefinder

WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}

'''
This is the main file for the chess engine. It will be responsible for handling user input and displaying the current gamestate object
'''

def LoadImages():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    pieces = ["black-bishop", "black-king", "black-knight", "black-pawn", "black-queen", "black-rook",
              "white-bishop", "white-king", "white-knight", "white-pawn", "white-queen", "white-rook"]
    for piece in pieces:
        image_path = os.path.join(base_dir, "..", "pieces-png", piece + ".png")
        IMAGES[piece] = p.transform.scale(p.image.load(image_path), (SQ_SIZE, SQ_SIZE))

'''
the main driver for our code this will handler user input and updating the graphics
'''

def main():
    # this is the main loop of the game
    # these are the initial settings of the pygame module and sets the window dialog box setting
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    clock.tick(MAX_FPS)
    screen.fill(p.Color("white"))

    # this is the game state object which initialize the board and get the valid moves
    gs = ChessEngine.GameState()

    # when the user makes a move we will makes the get valid moves until then we have made the moveMade as false
    validMoves = gs.getValidMoves()
    moveMade = False
    animate = False
    gameOver = False

    p.display.set_caption("Chess")
    LoadImages()
    
    running = True

    sqSelected = () # no square selected initially keep track of the last click of the user (tuple : (row, col))
    playerClicks = [] # store (row, col) of clicks (two clicks) (two tuples: [(6,4),(4,4)])
    
    playerone =  False# if true then white plays
    playertwo = False # if true then black plays

    while running:
        humanturn = (gs.whiteToMove and playerone) or (not gs.whiteToMove and playertwo)
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            # mouse handlers
            elif e.type == p.MOUSEBUTTONDOWN:
                if not gameOver and humanturn:
                    location = p.mouse.get_pos()
                    col = location[0] // SQ_SIZE
                    row = location[1] // SQ_SIZE
                    if sqSelected == (row,col): # if the user clicks the same square twice then we undo the move
                        sqSelected = ()
                        playerClicks = []
                    else:
                        sqSelected = (row,col)
                        playerClicks.append(sqSelected) # this is the first click so we have append it to the list
                    if len(playerClicks) == 2: # this is the second click so we do the logic in this event loop
                        # here we are initializing the move class of the chessengine library you can say
                        move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                        # print(move.getChessNotation())
                        for i in range(len(validMoves)):
                            if move == validMoves[i]:
                            # here we are making the move but we are keeping a check behind this that is the move even valid 
                                gs.makeMove(validMoves[i])
                                moveMade = True
                                animate = True
                                sqSelected = ()
                                playerClicks = []
                        if not moveMade:
                            playerClicks = [sqSelected]
            # key handlers 
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z: # undo move 
                    gs.undoMove()
                    if not (playerone and playertwo): # if playing against an AI, undo the human's move as well
                        gs.undoMove()
                    sqSelected = ()
                    playerClicks = []
                    moveMade = True
                    animate = False
                    gameOver = False
                if e.key == p.K_r:
                    gs = ChessEngine.GameState()
                    validMoves = gs.getValidMoves()
                    moveMade = False
                    animate = False
                    sqSelected = ()
                    playerClicks = []
                    gameOver = False
       
        if not gameOver and not humanturn and not moveMade: 
            AIMove = smartmovefinder.findbestmoveminmax(gs,validMoves)
            if AIMove is None:
                AIMove = smartmovefinder.findrandommove(validMoves)
            if AIMove is not None:
                gs.makeMove(AIMove)
                moveMade = True
                animate = True

        if moveMade:
            if animate:
                animateMove(gs.moveLog[-1], screen, gs.board, clock)
            validMoves = gs.getValidMoves()
            moveMade = False
            animate = False

        drawGameState(screen, gs,validMoves,sqSelected)

        if gs.checkMate:
            gameOver = True
            if gs.whiteToMove:
                drawText(screen, 'Black wins by checkmate')
            else:
                drawText(screen, 'White wins by checkmate')
        elif gs.staleMate:
            gameOver = True
            drawText(screen, 'Stalemate')

        p.display.flip()
    p.quit()

def highlightsquares(screen,gs,validMoves,sqSelected):
    if sqSelected != ():
        r,c = sqSelected
        color = 'w' if gs.whiteToMove else 'b'
        if gs.board[r][c][0] == color: # white piece selected
            highlight = p.Surface((SQ_SIZE, SQ_SIZE))
            highlight.set_alpha(100)
            highlight.fill(p.Color('blue'))
            screen.blit(highlight, (c * SQ_SIZE, r * SQ_SIZE))
            highlight.fill(p.Color("yellow"))
            for move in validMoves:
                if move.startRow == r and move.startCol == c:
                    screen.blit(highlight, (move.endCol * SQ_SIZE, move.endRow * SQ_SIZE))


def drawGameState(screen,gs,validMoves,sqSelected):
    drawBoard(screen)
    highlightsquares(screen,gs,validMoves,sqSelected)
    drawPieces(screen,gs.board)

'''
draw the squares on the board IMP to note that the first square is always white so doing zero based indexing if we add row and col and modulo 2 then if the after module its 0 then it is white and if its 1 then it is black
'''

def drawBoard(screen):
    colors = [p.Color("white"), p.Color("gray")]
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            color = colors[(row + col) % 2]
            p.draw.rect(screen, color, p.Rect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))

def drawPieces(screen,board):
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            piece = board[row][col]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))

def animateMove(move,screen,board,clock):
    coords = []
    dR = move.endRow - move.startRow
    dC = move.endCol - move.startCol
    framespersquare = 10
    framecount = (abs(dR) + abs(dC)) * framespersquare
    for frame in range(framecount+1):
        r,c = (move.startRow + dR*(frame/framecount), move.startCol + dC*(frame/framecount))
        drawBoard(screen)
        drawPieces(screen,board)
        colors = [p.Color("white"), p.Color("gray")]
        color = colors[(move.endRow + move.endCol)%2]
        endSquare = p.Rect(move.endCol * SQ_SIZE, move.endRow * SQ_SIZE, SQ_SIZE, SQ_SIZE)
        p.draw.rect(screen, color, endSquare)
        
        # 1. Draw the captured piece back onto its square so it doesn't disappear early
        if move.pieceCaptured != '--':
            if move.isEmpassantMove:
                enPassantSquare = p.Rect(move.endCol * SQ_SIZE, move.startRow * SQ_SIZE, SQ_SIZE, SQ_SIZE)
                screen.blit(IMAGES[move.pieceCaptured], enPassantSquare)
            else:
                screen.blit(IMAGES[move.pieceCaptured], endSquare)
        
        # 2. Draw the actual moving piece at the flying (animated) coordinates
        screen.blit(IMAGES[move.pieceMoved], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))
        p.display.flip()
        clock.tick(60)

def drawText(screen, text):
    font = p.font.SysFont("Helvetica", 32, True, False)
    textObject = font.render(text, 0, p.Color('Gray'))
    textLocation = p.Rect(0, 0, WIDTH, HEIGHT).move(WIDTH / 2 - textObject.get_width() / 2, HEIGHT / 2 - textObject.get_height() / 2)
    screen.blit(textObject, textLocation)
    textObject = font.render(text, 0, p.Color('Black'))
    screen.blit(textObject, textLocation.move(2, 2))

if __name__ == "__main__":
    main()