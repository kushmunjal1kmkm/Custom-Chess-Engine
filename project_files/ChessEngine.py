'''
This class is responsible for storing all the information about the current state of a chess game. It will also be responsible for determining the valid moves.and also keep a log of all the moves. and in the future castling and other moves also
'''

class GameState():
    def __init__(self):
        # this is the 8x8 2d list representing the board and -- represents an empty space
        self.board = [["black-rook", "black-knight", "black-bishop", "black-queen", "black-king", "black-bishop", "black-knight", "black-rook"],
                      ["black-pawn", "black-pawn", "black-pawn", "black-pawn", "black-pawn", "black-pawn", "black-pawn", "black-pawn"],
                      ["--", "--", "--", "--", "--", "--", "--", "--"],
                      ["--", "--", "--", "--", "--", "--", "--", "--"],
                      ["--", "--", "--", "--", "--", "--", "--", "--"],
                      ["--", "--", "--", "--", "--", "--", "--", "--"],
                      ["white-pawn", "white-pawn", "white-pawn", "white-pawn", "white-pawn", "white-pawn", "white-pawn", "white-pawn"],
                      ["white-rook", "white-knight", "white-bishop", "white-queen", "white-king", "white-bishop", "white-knight", "white-rook"]]
        self.whiteToMove = True
        self.moveLog = []
        self.Movefunction = {"pawn":self.getPawnMoves,"rook":self.getRookMoves,"knight":self.getKnightMoves,"bishop":self.getBishopMoves,"queen":self.getQueenMoves,"king":self.getKingMoves}
        self.whiteKingLocation = (7,4)
        self.blackKingLocation = (0,4)
        self.isCheck = False
        self.checkMate = False
        self.staleMate = False
        self.pins = []
        self.check = []
        self.empassantpossible = ()
        self.currentCastlingRights = CastleRights(True,True,True,True)
        self.castlerightlogs = [CastleRights(self.currentCastlingRights.wksLeft,self.currentCastlingRights.wqsLeft,self.currentCastlingRights.bksLeft,self.currentCastlingRights.bqsLeft)]


    def makeMove(self,move):
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.board[move.startRow][move.startCol] = "--"
        self.whiteToMove = not self.whiteToMove
        self.moveLog.append(move)
        
        
        if move.pieceMoved == 'white-king':
            self.whiteKingLocation = (move.endRow,move.endCol)
        
        elif move.pieceMoved == 'black-king':
            self.blackKingLocation = (move.endRow,move.endCol)
        


        #updating empassant possible variable with each move update the empassant possible variable
        if move.pieceMoved.endswith("pawn") and abs(move.startRow - move.endRow) == 2: # empassant only possible when pawn move first 2 moves
            self.empassantpossible = ((move.startRow + move.endRow)//2,move.endCol) # this is calculating the one row behind the pawn that moved keeping the column same we are getting the square that is the empassant square and / gives 5.0 but // give 5 as the result
        else:
            self.empassantpossible = () 

        if move.isEmpassantMove:
            self.board[move.startRow][move.endCol] = '--' # this is the empassant move so we are removing the enemy pawn from the board

        if move.isPawnPromotion:
            promototedPiece = input("enter the piece you want to promote to (queen,rook,bishop,knight): ")
            while promototedPiece not in ["queen", "rook", "bishop", "knight"]:
                print("invalid piece")
                promototedPiece = input("enter the piece you want to promote to (queen,rook,bishop,knight): ")
            self.board[move.endRow][move.endCol] = move.pieceMoved.split("-")[0] + "-" + promototedPiece

        if move.isCastleMove:
            if move.endCol - move.startCol == 2:
                self.board[move.endRow][move.endCol-1] = self.board[move.endRow][move.endCol+1]
                self.board[move.endRow][move.endCol+1] = "--"
            else:
                self.board[move.endRow][move.endCol+1] = self.board[move.endRow][move.endCol-2]
                self.board[move.endRow][move.endCol-2] = "--"


        self.updateCastleRights(move)
        self.castlerightlogs.append(CastleRights(self.currentCastlingRights.wksLeft,self.currentCastlingRights.bksLeft,self.currentCastlingRights.wksLeft,self.currentCastlingRights.bqsLeft))


    '''
    unde the last move
    '''
    def undoMove(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove
            if move.pieceMoved == 'white-king':
                self.whiteKingLocation = (move.startRow,move.startCol)
            elif move.pieceMoved == 'black-king': 
                self.blackKingLocation = (move.startRow,move.startCol)

            if move.isEmpassantMove:
                self.board[move.endRow][move.endCol] = '--'
                self.board[move.startRow][move.endCol] = move.pieceCaptured # restore enemy pawn to its actual square
                self.empassantpossible = (move.endRow,move.endCol)
            
            self.castlerightlogs.pop()
            newRights = self.castlerightlogs[-1]
            self.currentCastlingRights = CastleRights(newRights.wksLeft,newRights.bksLeft,newRights.wqsLeft,newRights.bqsLeft)

            
            if move.isCastleMove:
                if move.endCol - move.startCol == 2:
                    self.board[move.endRow][move.endCol+1] = self.board[move.endRow][move.endCol-1]
                    self.board[move.endRow][move.endCol-1] = "--"
                else:
                    self.board[move.endRow][move.endCol-2] = self.board[move.endRow][move.endCol+1]
                    self.board[move.endRow][move.endCol+1] = "--"

        
    def updateCastleRights(self,move):
        if move.pieceMoved == 'white-king':
            self.currentCastlingRights.wksLeft = False
            self.currentCastlingRights.wqsLeft = False
        elif move.pieceMoved == 'black-king':
            self.currentCastlingRights.bksLeft = False
            self.currentCastlingRights.bqsLeft = False
        elif move.pieceMoved == 'white-rook':
            if move.startRow == 7 and move.startCol == 0: 
                self.currentCastlingRights.wksLeft = False
            elif move.startRow == 7 and move.startCol == 7:
                self.currentCastlingRights.wqsLeft = False
        elif move.pieceMoved == 'black-rook':
            if move.startRow == 0 and move.startCol == 0:
                self.currentCastlingRights.bksLeft = False
            elif move.startRow == 0 and move.startCol == 7:
                self.currentCastlingRights.bqsLeft = False

    '''
    all moves considering checks
    '''
    def getValidMoves(self):
        moves = []
        
        self.isCheck, self.pins, self.check = self.getPinAndCheck() # gets all the pin that are coming in front of the enemy piece and 

        if self.whiteToMove:
            kingRow = self.whiteKingLocation[0]
            kingCol = self.whiteKingLocation[1]
        else:
            kingRow = self.blackKingLocation[0]
            kingCol = self.blackKingLocation[1]

        if self.isCheck: 
            if len(self.check) == 1: # if there is only one check
                moves = self.getAllPosibleMoves()
                check = self.check[0]
                checkRow = check[0]
                checkCol = check[1]
                validSquares = []
                piecechecking = self.board[checkRow][checkCol]
                typeof_piece = piecechecking.split("-")[1]
                if typeof_piece == "knight": # if the enemy piece is a knight then we can only block the check by capturing the knight
                    validSquares = [(checkRow,checkCol)]
                else:
                    checkDirRow = check[2]
                    checkDirCol = check[3]
                    for i in range(1,8):
                        validSquare = (kingRow + checkDirRow*i, kingCol + checkDirCol*i)
                        validSquares.append(validSquare)
                        if validSquare[0] == checkRow and validSquare[1] == checkCol:
                            break
                for i in range(len(moves)-1,-1,-1):
                    if moves[i].pieceMoved.split("-")[1] != "king":
                        if not (moves[i].endRow,moves[i].endCol) in validSquares:
                            moves.pop(i)
            else: # this is if there is a double check then the king has to move
                self.getKingMoves(kingRow,kingCol,moves)
        else: # king is not in check
            moves = self.getAllPosibleMoves()
            self.getCastlingMoves(kingRow, kingCol, moves)

# Prevent infinite recursion during attack checking:
# isSquareAttacked() calls getAllPossibleMoves(), which calls getKingMoves().
# If castling moves are generated inside getKingMoves(), getCastlingMoves()
# again calls isSquareAttacked(), creating a recursive loop.
#
# Solution:
# Castling moves are generated separately inside getValidMoves() only for
# actual legal move generation, while getAllPossibleMoves() generates only
# normal king moves for attack detection.
        
        if len(moves) == 0:
            if self.isCheck:
                self.checkMate = True
            else:
                self.staleMate = True
        else:
            self.checkMate = False
            self.staleMate = False

        return moves
    '''
    all moves without considering checks
    '''

    def getPinAndCheck(self):
        pins=[]
        check=[]
        inCheck=False
        if self.whiteToMove:
            enemycolor = "b"
            allycolor = "w"
            startRow = self.whiteKingLocation[0]
            startCol = self.whiteKingLocation[1]
        else:
            enemycolor = "w"
            allycolor = "b"
            startRow = self.blackKingLocation[0]
            startCol = self.blackKingLocation[1]
        direction = ((-1,0),(0,-1),(1,0),(0,1),(-1,-1),(-1,1),(1,-1),(1,1)) # up,down,left,right,up-left,up-right,down-left,down-right
        # these directions are set in a specific way because we have to check for pins and check along specific direction and also check is based on the direction and the enemypiece that is there
        for j, d in enumerate(direction):
            possiblePin = () # reset possible pins
            for i in range(1,8):
                r = startRow + d[0] * i
                c = startCol + d[1] * i
                if 0 <= r < 8 and 0 <= c < 8:
                    endPiece = self.board[r][c]
                    if endPiece.startswith(allycolor) : # if we find a pin we add it to the possible pin 
                        if possiblePin == (): # if there is no possible pin then we add it it is the first pin
                            possiblePin = (r,c,d[0],d[1])
                        else: # if there is already there then we dont add it we break because if there is 2 ally piece in 1 direction then there is no need to check further
                            break
                    elif endPiece.startswith(enemycolor): # if we find an enemy piece
                        typeofPiece = endPiece.split("-")[1] # get the type of enemy piece
                        # check if the enemy piece can attack the king from this direction

                        # if rook we check the left right up and down
                        # if bishop we check the 4 diagonals
                        # if queen we check all 8 directions
                        # if king we check the 8 directions but only 1 step
                        # if pawn we check 1 step diagonally and based on if enemy is white or black because white move forward and black move down as seen from perspective
                        if (typeofPiece == "rook" and 0 <= j <= 3) or \
                           (typeofPiece == "bishop" and 4 <= j <= 7) or \
                           (typeofPiece == "queen") or \
                           (typeofPiece == "king" and i == 1) or \
                           (typeofPiece == "pawn" and i == 1 and (
                               (enemycolor == "w" and 6 <= j <= 7) or
                               (enemycolor == "b" and 4 <= j <= 5))):
                            if possiblePin == (): # no ally piece blocking so it is a check
                                inCheck = True
                                check.append((r, c, d[0], d[1])) # one thing to note is it does not add the piece as check which has a pin in front of it that
                            else: # ally piece blocking so it is a pin if there is a ally piece between the king and the enemy piece so we move the pin from possible pin to make it a pins
                                pins.append(possiblePin)
                            break
                        else: # enemy piece but not applying check in this direction
                            break
                    else:
                        pass
                else:
                    break
        # check for knight attacks
        knightMoves = ((1,2),(2,1),(2,-1),(1,-2),(-1,-2),(-2,-1),(-2,1),(-1,2)) # checking for checks from outwards of king place 
        for m in knightMoves:
            r = startRow + m[0]
            c = startCol + m[1]
            if 0 <= r < 8 and 0 <= c < 8:
                endPiece = self.board[r][c]
                if endPiece.startswith(enemycolor) and endPiece.split("-")[1] == "knight":
                    inCheck = True
                    check.append((r, c, m[0], m[1]))
        return inCheck, pins, check

    def inCheck(self):
        if self.whiteToMove:
            return self.isSquareAttacked(self.whiteKingLocation[0],self.whiteKingLocation[1])
        else:
            return self.isSquareAttacked(self.blackKingLocation[0],self.blackKingLocation[1])

    def isSquareAttacked(self,r,c):
        self.whiteToMove = not self.whiteToMove
        oppmoves = self.getAllPosibleMoves()
        self.whiteToMove = not self.whiteToMove
        for move in oppmoves:
            if move.endRow == r and move.endCol == c:
                return True
        return False


    def getAllPosibleMoves(self):
        moves =[]
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                
                if self.board[r][c] == "--": # if the space is empty then continue otherwise it would split it into 3 values not 2
                    continue
                color,piece = self.board[r][c].split("-")
                if (color == "white" and self.whiteToMove) or (color == "black" and not self.whiteToMove):
                    self.Movefunction[piece](r,c,moves)
        return moves

    
    '''
    fucntion for getting all the moves for pawn located at the rth cth row and column and move them to the moves list
    '''
    def  getPawnMoves(self,r,c,moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins)-1,-1,-1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = self.pins[i][2:]
                self.pins.remove(self.pins[i])
                break

        if self.whiteToMove:
            moveAmmount = -1
            startRow = 6
            endRow = 0
            enemyColor = "black"
        else:
            moveAmmount = 1
            startRow = 1
            endRow = 7
            enemyColor = "white"
        pawnPromotion = False

        if self.board[r+moveAmmount][c] == "--": # pawn forward move
            if not piecePinned or pinDirection == (moveAmmount, 0):
                pawnPromotion = (r + moveAmmount == endRow)
                moves.append(Move((r, c), (r+moveAmmount, c), self.board, isPawnPromotion=pawnPromotion))
                if r == startRow and self.board[r+2*moveAmmount][c] == "--": # 2 square pawn advance
                    moves.append(Move((r, c), (r+2*moveAmmount, c), self.board))
        if c-1 >= 0: # capture to the left
            if self.board[r+moveAmmount][c-1].startswith(enemyColor):
                if not piecePinned or pinDirection == (moveAmmount, -1):
                    pawnPromotion = (r + moveAmmount == endRow)
                    moves.append(Move((r, c), (r+moveAmmount, c-1), self.board, isPawnPromotion=pawnPromotion))
            elif (r+moveAmmount, c-1) == self.empassantpossible:
                if not piecePinned or pinDirection == (moveAmmount, -1):
                    moves.append(Move((r, c), (r+moveAmmount, c-1), self.board, empassantpossible=True))
        if c+1 <= 7: # capture to the right
            if self.board[r+moveAmmount][c+1].startswith(enemyColor):
                if not piecePinned or pinDirection == (moveAmmount, 1):
                    pawnPromotion = (r + moveAmmount == endRow)
                    moves.append(Move((r, c), (r+moveAmmount, c+1), self.board, isPawnPromotion=pawnPromotion))
            elif (r+moveAmmount, c+1) == self.empassantpossible:
                if not piecePinned or pinDirection == (moveAmmount, 1):
                    moves.append(Move((r, c), (r+moveAmmount, c+1), self.board, empassantpossible=True))

    '''
    function for getting all moves for rook located at the rth cth row and column and move them to the moves list
    '''
    def getRookMoves(self,r,c,moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins)-1,-1,-1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = self.pins[i][2:]
                if self.board[r][c].split("-")[1] != "queen": # we are using the same function to get queen moves so we add a check to make sure we are not removing the pin of a queen
                    self.pins.remove(self.pins[i])
                break
        directions = ((0,1),(0,-1),(1,0),(-1,0))
        enemycolor = "black" if self.whiteToMove else "white"
        for d in directions:
            for i in range(1,8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    if not piecePinned or pinDirection == d or pinDirection == (-d[0],-d[1]): # this is the code for white and black rook moves we are flipping the pin direction to make sure we are not removing the pin of a queen
                        endPiece = self.board[endRow][endCol]
                        if endPiece == "--":
                            moves.append(Move((r,c),(endRow,endCol),self.board))
                        elif endPiece.startswith(enemycolor):
                            moves.append(Move((r,c),(endRow,endCol),self.board))
                            break
                        else:  # ally piece
                            break
                    else:
                        break
                else:
                    break
    '''
    fucntion for getting all moves for knight located at the rth cth row and column and move them to the moves list
    '''
    def getKnightMoves(self,r,c,moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins)-1,-1,-1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = self.pins[i][2:]
                self.pins.remove(self.pins[i])
                break
        knightMoves = ((1,2),(2,1),(2,-1),(1,-2),(-1,-2),(-2,-1),(-2,1),(-1,2))
        enemycolor = "black" if self.whiteToMove else "white"
        for m in knightMoves:
            endRow = r + m[0]
            endCol = c + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                if not piecePinned:
                    if self.board[endRow][endCol] == "--":
                        moves.append(Move((r,c),(endRow,endCol),self.board))
                    elif self.board[endRow][endCol].startswith(enemycolor):
                        moves.append(Move((r,c),(endRow,endCol),self.board))
                else:
                    break
            else: # if it goes out of bounds then we continue not break because we check all direction not like bishop or queen etc we have to check all in case of knight
                continue

    def getBishopMoves(self,r,c,moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins)-1,-1,-1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = self.pins[i][2:]
                self.pins.remove(self.pins[i]) # also removes the queens pins also because its not removed in the queen moves so we remove it here
                break
        direction = ((-1,-1),(-1,1),(1,-1),(1,1))
        enemycolor = "black" if self.whiteToMove else "white"
        for d in direction:
            for i in range(1,8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    if not piecePinned or pinDirection == d or pinDirection == (-d[0],-d[1]):
                        endPiece = self.board[endRow][endCol]
                        if endPiece == "--":
                            moves.append(Move((r,c),(endRow,endCol),self.board))
                        elif endPiece.startswith(enemycolor): # capturing enemy piece
                            moves.append(Move((r,c),(endRow,endCol),self.board))
                            break
                        else:  # ally piece we can have moves up to it not capture our ally piece
                            break
                    else:
                        break
                else:
                    break
                
    def getQueenMoves(self,r,c,moves):
        self.getRookMoves(r,c,moves)
        self.getBishopMoves(r,c,moves)

    def getKingMoves(self,r,c,moves):
        direction = ((0,1),(1,1),(1,0),(1,-1),(0,-1),(-1,-1),(-1,0),(-1,1))
        allycolor = "white" if self.whiteToMove else "black"
        for d in direction:
            endRow = r + d[0]
            endCol = c + d[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if not endPiece.startswith(allycolor):  # can't land on ally piece
                    if allycolor == "white":
                        self.whiteKingLocation = (endRow,endCol)
                    else:
                        self.blackKingLocation = (endRow,endCol)
                    # temporarily remove king from old square so getPinAndCheck
                    # doesn't treat it as a blocker when scanning back through it
                    self.board[r][c] = "--"
                    isCheck, pins , checks= self.getPinAndCheck()
                    # restore the king on the board before creating the Move object
                    self.board[r][c] = allycolor + "-king" # adding the king back to the board and switching back the location of the king
                    if not isCheck:
                        moves.append(Move((r,c),(endRow,endCol),self.board))
                    if  allycolor == "white":
                        self.whiteKingLocation = (r,c)
                    else:
                        self.blackKingLocation = (r,c)

    def getCastlingMoves(self,r,c,moves):
        if self.isSquareAttacked(r,c):
            return
        if (self.whiteToMove and self.currentCastlingRights.wksLeft) or (not self.whiteToMove and self.currentCastlingRights.bksLeft):
            self.getkingsidecastlingmoves(r,c,moves)
        if (self.whiteToMove and self.currentCastlingRights.wqsLeft) or (not self.whiteToMove and self.currentCastlingRights.bqsLeft):
            self.getqueensidecastlingmoves(r,c,moves)
    
    def getkingsidecastlingmoves(self,r,c,moves):
        if self.board[r][c+1] == "--" and self.board[r][c+2] == "--":
            if not self.isSquareAttacked(r,c+1) and not self.isSquareAttacked(r,c+2):
                moves.append(Move((r,c),(r,c+2),self.board,isCastleMove=True))
    def getqueensidecastlingmoves(self,r,c,moves):
        if self.board[r][c-1] == "--" and self.board[r][c-2] == "--" and self.board[r][c-3] == "--":
            if not self.isSquareAttacked(r,c-1) and not self.isSquareAttacked(r,c-2):
                moves.append(Move((r,c),(r,c-2),self.board,isCastleMove=True))
    
    

class CastleRights():
    def __init__(self,wks,bks,wqs,bqs):
        self.wksLeft = wks
        self.bksLeft = bks
        self.wqsLeft = wqs
        self.bqsLeft = bqs

class Move():
    #maps key to value
    #key: value
    ranksToRows = {"1":7, "2":6, "3":5, "4":4, "5":3, "6":2, "7":1, "8":0}
    filesToCols = {"a":0, "b":1, "c":2, "d":3, "e":4, "f":5, "g":6, "h":7}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board , empassantpossible =False ,isPawnPromotion = False,isCastleMove = False):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.board = board
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        if empassantpossible: # the real captured pawn is NOT on endRow/endCol (that square is empty), it's behind the destination
            self.pieceCaptured = board[self.startRow][self.endCol]

        self.isPawnPromotion = isPawnPromotion

        self.isEmpassantMove = empassantpossible

        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol

        self.isCastleMove = isCastleMove

    # now why are we overiding this eq function in the move class
    # -- this is because when the user makes the move it is an different object of the move class and when we are comparing the it in the moves list it is an different object of the move class so we need to compare them based on their attributes
    # -- we can make a move id to uniquely identify the move
    
    # def __eq__(self,other):
    #     return self.moveID == other.moveID

    def __eq__(self,other):
        if isinstance(other,Move):
            return self.moveID == other.moveID
        return False
    # in python the default __eq__ simply checks for identity whether two variables point to the exact same object in memory
    '''
    def __eq__(self,other):
        return self is other
    
    so it is true if a == b and a and b are exact same object in memory id(a) == id(b)
    it also has another thing which is called hash it is a special method in python that returns a integer for an object used when to put into a hash-based data structure like a set or use it as a dict key
    
    a= "hello"
    print(hash(a))

    --python uses this integer for quick look up objects in sets/dicts

    class Foo:
        def __init__(self, x):
            self.x = x

    a = Foo(5)
    b = Foo(5)

    print(hash(a))  # e.g., 8771234567
    print(hash(b))  # e.g., 8771234999 — different, because different objects

    it is a fundamental rule in python
    if a == b then hash(a) must equal hash(b)
    but overiding eq so hash is equal so python sets hash to null making your object unhashable but if you want to use it then

    def __hash__(self):
        return hash(self.moveID)
    '''
    
    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, row, col):
        return self.colsToFiles[col] + self.rowsToRanks[row]

    def __str__(self):
        return self.getChessNotation()