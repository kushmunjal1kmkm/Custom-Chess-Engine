'''
This is the main file for the chess engine. It will be responsible for handling user input and displaying the current gamestate object
'''
import os
import pygame as p
import ChessEngine

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

    p.display.set_caption("Chess")
    LoadImages()
    
    running = True

    sqSelected = () # no square selected initially keep track of the last click of the user (tuple : (row, col))
    playerClicks = [] # store (row, col) of clicks (two clicks) (two tuples: [(6,4),(4,4)])

    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            # mouse handlers
            elif e.type == p.MOUSEBUTTONDOWN:
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
                            sqSelected = ()
                            playerClicks = []
                    if not moveMade:
                        playerClicks = [sqSelected]
            # key handlers 
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z: # undo move 
                    gs.undoMove()
                    sqSelected = ()
                    playerClicks = []
                    moveMade = True
        
        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False

        drawGameState(screen, gs)
        p.display.flip()
    p.quit()

def drawGameState(screen,gs):
    drawBoard(screen)
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

if __name__ == "__main__":
    main()