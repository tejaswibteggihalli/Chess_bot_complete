"This class is responsible for storing all the information about the current state of a chess game."
"It will also be responsible for determining the valid moves at the current state. It will also keep a move log."

import copy

class GameState():
    def __init__(self):
        #board is 8x8 2d list.each element of the list has 2 characters.
        #the first character represents the color of the list, 'b or 'w'
        #the second character represents the type of the piece, 'K', 'Q','R','B','N' or 'p'
        # "--" - represents an empty space with no piece.
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]
        self.moveFunctions = {'p': self.getPawnMoves, 'R': self.getRookMoves, 'N': self.getKnightMoves,
                              'B': self.getBishopMoves, 'Q': self.getQueenMoves, 'K': self.getKingMoves}

        self.whiteToMove = True
        self.moveLog = []
        self.whiteKingLocation = (7, 4)
        self.blackKingLocation = (0, 4)
        self.checkmate = False
        self.stalemate = False
        self.enpassantPossible = ()  #coords for the square where enpassant capture is possible
        self.enpassantPossibleLog = [self.enpassantPossible]
        self.currentCastlingRight = CastleRights(True, True, True, True)
        self.castleRightsLog = [CastleRights(self.currentCastlingRight.wks, self.currentCastlingRight.bks, self.currentCastlingRight.wqs, self.currentCastlingRight.bqs)]
        #3 fold repetition
        self.threefoldrepetition = False
        self.uniqueGS = {} #for storing all the gamestates
        self.uniqueGSLog = []



    '''
    Takes a Move as a parameter and executes it (this will not work for castling, pawn promotion, and en-passant)
    '''

    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)  #log the move so we can undo it later
        self.whiteToMove = not self.whiteToMove  #swap players
        #update the king's location if moved
        if move.pieceMoved == 'wK':
            self.whiteKingLocation = (move.endRow, move.endCol)
        elif move.pieceMoved == 'bK':
            self.blackKingLocation = (move.endRow, move.endCol)

            #pawn promotion
        if move.isPawnPromotion:
            self.board[move.endRow][move.endCol] = move.pieceMoved[0] + 'Q'

        #enpassant move
        if move.isEnpassantMove:
            self.board[move.startRow][move.endCol] = '--' #capturing the pawn

        #update enpassantPossible variable
        if move.pieceMoved[1] == 'p' and abs(move.startRow - move.endRow) == 2: #only on 2 square pawn advances
            self.enpassantPossible = ((move.startRow + move.endRow)//2, move.startCol)
        else:
            self.enpassantPossible = ()


        #castle move
        if move.isCastleMove:
            if move.endCol - move.startCol == 2: #king side castle move
                self.board[move.endRow][move.endCol-1] = self.board[move.endRow][move.endCol+1] #moves the rook
                self.board[move.endRow][move.endCol+1] = '--' #erase the old square
            elif move.endCol - move.startCol == -2:#queen side castle move
                self.board[move.endRow][move.endCol+1] = self.board[move.endRow][move.endCol-2] #moves the rook
                self.board[move.endRow][move.endCol-2] = '--' #erase the old square


        self.enpassantPossibleLog.append(self.enpassantPossible)
        # if a rook is captured
        if move.pieceCaptured == 'wR':
            if move.endRow == 7:
                if move.endCol == 0:
                    self.currentCastlingRight.wqs = False
                elif move.endCol == 7:
                    self.currentCastlingRight.wks = False
        else:
            if move.endRow == 0:
                if move.endCol == 0:
                    self.currentCastlingRight.bqs = False
                elif move.endCol == 7:
                    self.currentCastlingRight.bks = False

        #update castling rights - whenever it's a rook or king move
        self.updateCastleRights(move)
        self.castleRightsLog.append(CastleRights(self.currentCastlingRight.wks, self.currentCastlingRight.bks, self.currentCastlingRight.wqs,
                         self.currentCastlingRight.bqs))




    '''
    Undo the last move made
    '''

    def undoMove(self):
        if len(self.moveLog) != 0:  #make sure that there is a move to undo
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove  #switch turns back
            #update the king's position if needed
            if move.pieceMoved == 'wK':
                self.whiteKingLocation = (move.startRow, move.startCol)
            elif move.pieceMoved == 'bK':
                self.blackKingLocation = (move.startRow, move.startCol)
            #undo en passant
            if move.isEnpassantMove:
                self.board[move.endRow][move.endCol] = '--' #leave landing square blank
                self.board[move.startRow][move.endCol] = move.pieceCaptured

            self.enpassantPossibleLog.pop()
            self.enpassantPossible = self.enpassantPossibleLog[-1]

            #undo castling rights
            self.castleRightsLog.pop() #get rid of the new castle rights from the move we are undoing
            castle_rights = copy.deepcopy(self.castleRightsLog[-1])
            self.currentCastlingRight = CastleRights
            newRights = self.castleRightsLog[-1]
            self.currentCastlingRight = CastleRights(newRights.wks, newRights.bks, newRights.wqs, newRights.bqs) #set the current castle rights to the last one in the list
            #undo castle move
            if move.isCastleMove:
                if move.endCol - move.startCol == 2: #kingside
                    self.board[move.endRow][move.endCol+1] = self.board[move.endRow][move.endCol-1]
                    self.board[move.endRow][move.endCol-1] = '--'
                else: #queenside
                    self.board[move.endRow][move.endCol-2] = self.board[move.endRow][move.endCol+1]
                    self.board[move.endRow][move.endCol+1] = '--'

            self.checkmate = False
            self.stalemate = False

    '''
    Update the castle rights given the move
    '''
    def updateCastleRights(self, move):
        if move.pieceMoved == 'wK':
            self.currentCastlingRight.wks = False
            self.currentCastlingRight.wqs = False
        elif move.pieceMoved == 'bK':
            self.currentCastlingRight.bks = False
            self.currentCastlingRight.bqs = False
        elif move.pieceMoved == 'wR':
            if move.startRow == 7:
                if move.startCol == 0: #left rook
                    self.currentCastlingRight.wqs = False
                elif move.startCol == 7: #right rook
                    self.currentCastlingRight.wks = False
        elif move.pieceMoved == 'bR':
            if move.startRow == 0:
                if move.startCol == 0: #left rook
                    self.currentCastlingRight.bqs = False
                elif move.startCol == 7: #right rook
                    self.currentCastlingRight.bks = False



    '''
    All moves considering checks
    '''

    def getValidMoves(self):
        tempEnpassantPossible = self.enpassantPossible
        tempCastleRights = CastleRights(self.currentCastlingRight.wks, self.currentCastlingRight.bks, self.currentCastlingRight.wqs, self.currentCastlingRight.bqs) #copy the current castling rights
        #1.) generate all possible moves
        moves = self.getAllPossibleMoves()
        if self.whiteToMove:
            self.getCastleMoves(self.whiteKingLocation[0], self.whiteKingLocation[1], moves)
        else:
            self.getCastleMoves(self.blackKingLocation[0], self.blackKingLocation[1], moves)
        #2.) for each move, make the move
        for i in range(len(moves) - 1, -1, -1):  #when removing from a list go backwards through that list to avoid bugs as we are removing elements from that list
            self.makeMove(moves[i])
            #3.) generate all opponent's moves
            #4.) for each of your opponent's moves, see if they attack your king
            self.whiteToMove = not self.whiteToMove  #change the turn
            if self.inCheck():
                moves.remove(moves[i])  #5.) if they do attack your king, not a valid move
            self.whiteToMove = not self.whiteToMove  #switch it backk
            self.undoMove()
        if len(moves) == 0:  #either checkmate or stalemate
            if self.inCheck():
                self.checkmate = True
            else:
                self.stalemate = True


        self.enpassantPossible = tempEnpassantPossible
        self.currentCastlingRight = tempCastleRights
        return moves

    '''
    Determine if the current player is in check
    '''

    def inCheck(self):
        if self.whiteToMove:
            return self.squareUnderAttack(self.whiteKingLocation[0], self.whiteKingLocation[1])
        else:
            return self.squareUnderAttack(self.blackKingLocation[0], self.blackKingLocation[1])

    '''
    Determine if the enemy can attack the square r, c
    '''

    def squareUnderAttack(self, r, c):
        self.whiteToMove = not self.whiteToMove  #switch to the other player's turn
        oppMoves = self.getAllPossibleMoves()
        self.whiteToMove = not self.whiteToMove  # switch turns back
        for move in oppMoves:
            if move.endRow == r and move.endCol == c:  #square is under attack
                return True
        return False

    '''
    All moves without considering checks
    '''

    # noinspection PyArgumentList
    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)):  #number of rows
            for c in range(len(self.board[r])):  #number of cols in given row
                turn = self.board[r][c][0]
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r, c, moves)  #calls the appropriate move function based on piece type
        return moves

    '''
    Get all the pawn moves for the pawn located at row, col and add these moves to the list
    '''

    def getPawnMoves(self, r, c, moves):
        if self.whiteToMove:  #white pawn moves
            # white to move
            kingRow, kingCol = self.whiteKingLocation
            if r > 0:
                if self.board[r - 1][c] == "--":  # 1 square pawn advance
                    moves.append(Move((r, c), (r - 1, c), self.board))
                    if r == 6 and self.board[r - 2][c] == "--":  # 2 square pawn advance
                        moves.append(Move((r, c), (r - 2, c), self.board))
                if c - 1 >= 0:  # captures to the left
                    if self.board[r - 1][c - 1][0] == 'b':  # enemy piece to capture
                        moves.append(Move((r, c), (r - 1, c - 1), self.board))
                    elif (r-1, c-1) == self.enpassantPossible:
                        attackingPiece = blockingPiece = False
                        if kingRow == r:
                            if kingCol < c: #king is left of the pawn
                                #inside between king and pawn; outside range between pawn border
                                insideRange = range(kingCol + 1, c-1)
                                outsideRange = range(c+1, 8)
                            else: #king right of the pawn
                                insideRange = range(kingCol - 1, c, -1)
                                outsideRange = range(c-2, -1, -1)
                            for i in insideRange:
                                if self.board[r][i] != "--": #some other piece beside en-passant pawn blocks
                                    blockingPiece = True
                            for i in outsideRange:
                                square = self.board[r][i]
                                if (square[0] == 'b' and (square[1] == "R" or square[1] == "Q")): #attacking piece
                                    attackingPiece = True
                                elif square != "--":
                                    blockingPiece = True
                        if not attackingPiece or blockingPiece:
                                moves.append(Move((r, c), (r-1, c-1), self.board, enpassantPossible = True))

                if c + 1 <= 7:  # captures to the right
                    if self.board[r - 1][c + 1][0] == 'b':  # enemy piece to capture
                        moves.append(Move((r, c), (r - 1, c + 1), self.board))
                    elif (r-1, c+1) == self.enpassantPossible:
                        attackingPiece = blockingPiece = False
                        if kingRow == r:
                            if kingCol < c:  # king is left of the pawn
                                # inside between king and pawn; outside range between pawn border
                                insideRange = range(kingCol + 1, c)
                                outsideRange = range(c + 2, 8)
                            else:  # king right of the pawn
                                insideRange = range(kingCol - 1, c + 1, -1)
                                outsideRange = range(c - 1, -1, -1)
                            for i in insideRange:
                                if self.board[r][i] != "--":  # some other piece beside en-passant pawn blocks
                                    blockingPiece = True
                            for i in outsideRange:
                                square = self.board[r][i]
                                if (square[0] == 'b' and (square[1] == "R" or square[1] == "Q")):  # attacking piece
                                    attackingPiece = True
                                elif square != "--":
                                    blockingPiece = True
                        if not attackingPiece or blockingPiece:
                            moves.append(Move((r, c), (r - 1, c + 1), self.board, enpassantPossible=True))
        else:
            #black to move
            kingRow, kingCol = self.blackKingLocation
            if r < 7:
                if self.board[r + 1][c] == "--":  # 1 square pawn advance
                    moves.append(Move((r, c), (r + 1, c), self.board))
                    if r == 1 and self.board[r + 2][c] == "--":  # 2 square pawn advance
                        moves.append(Move((r, c), (r + 2, c), self.board))
                if c - 1 >= 0:  # captures to the left
                    if self.board[r + 1][c - 1][0] == 'w':  # enemy piece to capture
                        moves.append(Move((r, c), (r + 1, c - 1), self.board))

                    elif (r+1, c-1) == self.enpassantPossible:
                        moves.append(Move((r, c), (r + 1, c - 1), self.board, enpassantPossible=True))
                if c + 1 <= 7:  # captures to the right
                    if self.board[r + 1][c + 1][0] == 'w':  # enemy piece to capture
                        moves.append(Move((r, c), (r + 1, c + 1), self.board))

                    elif (r + 1, c + 1) == self.enpassantPossible:
                        moves.append(Move((r, c), (r + 1, c + 1), self.board, enpassantPossible=True))

        #add pawn promotion later

    '''
        Get all the rook moves for the rook located at row, col and add these moves to the list
    '''

    def getRookMoves(self, r, c, moves):
        if self.whiteToMove:
            # white to move

            #up
            for i in range(r, 0, -1):  #going up the board
                if self.board[i - 1][c] == "--" or self.board[i - 1][c][
                    0] == "b":  # empty square or enemy piece has been captured
                    moves.append(Move((r, c), (i - 1, c), self.board))
                if self.board[i - 1][c] != "--":  # a piece has come in between
                    break

            #down
            for i in range(r, 7):  #going down the board
                if self.board[i + 1][c] == "--" or self.board[i + 1][c][
                    0] == "b":  # empty square or enemy piece has been captured
                    moves.append(Move((r, c), (i + 1, c), self.board))
                if self.board[i + 1][c] != "--":  # a piece has come in between
                    break
            #left
            for i in range(c, 0, -1):  #going to the left of the board
                if self.board[r][i - 1] == "--" or self.board[r][i - 1][
                    0] == "b":  # empty square or enemy piece has been captured
                    moves.append(Move((r, c), (r, i - 1), self.board))
                if self.board[r][i - 1] != "--":  # a piece has come in between
                    break
            #right

            for i in range(c, 7):  #going to the right of the board
                if self.board[r][i + 1] == "--" or self.board[r][i + 1][
                    0] == "b":  # empty square or enemy piece has been captured
                    moves.append(Move((r, c), (r, i + 1), self.board))
                if self.board[r][i + 1] != "--":  # a piece has come in between
                    break
        else:

            # black to move

            # down (white pov)

            for i in range(r, 7):  # going down the board
                if self.board[i + 1][c] == "--" or self.board[i + 1][c][
                    0] == "w":  # empty square or enemy piece has been captured
                    moves.append(Move((r, c), (i + 1, c), self.board))
                if self.board[i + 1][c] != "--":  # a piece has come in between
                    break

            # up (white pov)

            for i in range(r, 0, -1):  # going up the board
                if self.board[i - 1][c] == "--" or self.board[i - 1][c][
                    0] == "w":  # empty square or enemy piece has been captured
                    moves.append(Move((r, c), (i - 1, c), self.board))
                if self.board[i - 1][c] != "--":  # a piece has come in between
                    break

            # left (white pov)
            for i in range(c, 0, -1):  # going to the left of the board
                if self.board[r][i - 1] == "--" or self.board[r][i - 1][
                    0] == "w":  # empty square or enemy piece has been captured
                    moves.append(Move((r, c), (r, i - 1), self.board))
                if self.board[r][i - 1] != "--":  # a piece has come in between
                    break
            # right (white pov)

            for i in range(c, 7):  # going to the right of the board
                if self.board[r][i + 1] == "--" or self.board[r][i + 1][
                    0] == "w":  # empty square or enemy piece has been captured
                    moves.append(Move((r, c), (r, i + 1), self.board))
                if self.board[r][i + 1] != "--":  # a piece has come in between
                    break

    '''
            Get all the knight moves for the knight located at row, col and add these moves to the list
        '''

    def getKnightMoves(self, r, c, moves):
        if self.whiteToMove:
            # I quadrant:
            #(a)
            i = r - 1
            j = c + 2
            if 0 <= i <= 7 and 0 <= j <= 7:  # if possible moves are within the board borders
                if self.board[i][j] == "--" or self.board[i][j][0] == "b":  # empty square or enemy piece
                    moves.append(Move((r, c), (i, j), self.board))
            #(b)
            i = r - 2
            j = c + 1
            if 0 <= i <= 7 and 0 <= j <= 7:  # if possible moves are within the board borders
                if self.board[i][j] == "--" or self.board[i][j][0] == "b":  # empty square or enemy piece
                    moves.append(Move((r, c), (i, j), self.board))

            # II quadrant:
            #(a)
            i = r - 2
            j = c - 1
            if 0 <= i <= 7 and 0 <= j <= 7:  # if possible moves are within the board borders
                if self.board[i][j] == "--" or self.board[i][j][0] == "b":  # empty square or enemy piece
                    moves.append(Move((r, c), (i, j), self.board))
            #(b)
            i = r - 1
            j = c - 2
            if 0 <= i <= 7 and 0 <= j <= 7:  # if possible moves are within the board borders
                if self.board[i][j] == "--" or self.board[i][j][0] == "b":  # empty square or enemy piece
                    moves.append(Move((r, c), (i, j), self.board))

            # III quadrant:
            #(a)
            i = r + 1
            j = c - 2
            if 0 <= i <= 7 and 0 <= j <= 7:  # if possible moves are within the board borders
                if self.board[i][j] == "--" or self.board[i][j][0] == "b":  # empty square or enemy piece
                    moves.append(Move((r, c), (i, j), self.board))
            #(b)
            i = r + 2
            j = c - 1
            if 0 <= i <= 7 and 0 <= j <= 7:  # if possible moves are within the board borders
                if self.board[i][j] == "--" or self.board[i][j][0] == "b":  # empty square or enemy piece
                    moves.append(Move((r, c), (i, j), self.board))

            # IV quadrant:
            #(a)
            i = r + 2
            j = c + 1
            if 0 <= i <= 7 and 0 <= j <= 7:  # if possible moves are within the board borders
                if self.board[i][j] == "--" or self.board[i][j][0] == "b":  # empty square or enemy piece
                    moves.append(Move((r, c), (i, j), self.board))
            #(b)
            i = r + 1
            j = c + 2
            if 0 <= i <= 7 and 0 <= j <= 7:  # if possible moves are within the board borders
                if self.board[i][j] == "--" or self.board[i][j][0] == "b":  # empty square or enemy piece
                    moves.append(Move((r, c), (i, j), self.board))

        else:
            # I quadrant: (WHITEPOV)
            # (a)
            i = r - 1
            j = c + 2
            if 0 <= i <= 7 and 0 <= j <= 7:  # if possible moves are within the board borders
                if self.board[i][j] == "--" or self.board[i][j][0] == "w":  # empty square or enemy piece
                    moves.append(Move((r, c), (i, j), self.board))
                    # (b)
            i = r - 2
            j = c + 1
            if 0 <= i <= 7 and 0 <= j <= 7:  # if possible moves are within the board borders
                if self.board[i][j] == "--" or self.board[i][j][0] == "w":  # empty square or enemy piece
                    moves.append(Move((r, c), (i, j), self.board))

            # II quadrant:
            # (a)
            i = r - 2
            j = c - 1
            if 0 <= i <= 7 and 0 <= j <= 7:  # if possible moves are within the board borders
                if self.board[i][j] == "--" or self.board[i][j][0] == "w":  # empty square or enemy piece
                    moves.append(Move((r, c), (i, j), self.board))
            # (b)
            i = r - 1
            j = c - 2
            if 0 <= i <= 7 and 0 <= j <= 7:  # if possible moves are within the board borders
                if self.board[i][j] == "--" or self.board[i][j][0] == "w":  # empty square or enemy piece
                    moves.append(Move((r, c), (i, j), self.board))

            # III quadrant:
            # (a)
            i = r + 1
            j = c - 2
            if 0 <= i <= 7 and 0 <= j <= 7:  # if possible moves are within the board borders
                if self.board[i][j] == "--" or self.board[i][j][0] == "w":  # empty square or enemy piece
                    moves.append(Move((r, c), (i, j), self.board))
            # (b)
            i = r + 2
            j = c - 1
            if 0 <= i <= 7 and 0 <= j <= 7:  # if possible moves are within the board borders
                if self.board[i][j] == "--" or self.board[i][j][0] == "w":  # empty square or enemy piece
                    moves.append(Move((r, c), (i, j), self.board))

            # IV quadrant:
            # (a)
            i = r + 2
            j = c + 1
            if 0 <= i <= 7 and 0 <= j <= 7:  # if possible moves are within the board borders
                if self.board[i][j] == "--" or self.board[i][j][0] == "w":  # empty square or enemy piece
                    moves.append(Move((r, c), (i, j), self.board))
            # (b)
            i = r + 1
            j = c + 2
            if 0 <= i <= 7 and 0 <= j <= 7:  # if possible moves are within the board borders
                if self.board[i][j] == "--" or self.board[i][j][0] == "w":  # empty square or enemy piece
                    moves.append(Move((r, c), (i, j), self.board))

    '''
            Get all the bishop moves for the bishop located at row, col and add these moves to the list
        '''

    def getBishopMoves(self, r, c, moves):
        if self.whiteToMove:
            #directions: Quadrants: I II III IV in anticlockwise direction (whitePOV)

            #for I:
            for i in range(0, min(r - 0, 7 - c)):
                if self.board[r - i - 1][c + i + 1] == "--" or self.board[r - i - 1][c + i + 1][0] == "b":
                    moves.append(Move((r, c), (r - i - 1, c + i + 1), self.board))
                if self.board[r - i - 1][c + i + 1] != "--":
                    break

            #for II:
            for i in range(0, min(r - 0, c - 0)):
                if self.board[r - i - 1][c - i - 1] == "--" or self.board[r - i - 1][c - i - 1][0] == "b":
                    moves.append(Move((r, c), (r - i - 1, c - i - 1), self.board))
                if self.board[r - i - 1][c - i - 1] != "--":
                    break

            #for III:
            for i in range(0, min(7 - r, c - 0)):
                if self.board[r + i + 1][c - i - 1] == "--" or self.board[r + i + 1][c - i - 1][0] == "b":
                    moves.append(Move((r, c), (r + i + 1, c - i - 1), self.board))
                if self.board[r + i + 1][c - i - 1] != "--":
                    break

            #for IV:
            for i in range(0, min(7 - r, 7 - c)):
                if self.board[r + i + 1][c + i + 1] == "--" or self.board[r + i + 1][c + i + 1][0] == "b":
                    moves.append(Move((r, c), (r + i + 1, c + i + 1), self.board))
                if self.board[r + i + 1][c + i + 1] != "--":
                    break
        else:
            # directions: Quadrants: I II III IV in anticlockwise direction (whitePOV)

            # for I:
            for i in range(0, min(r - 0, 7 - c)):
                if self.board[r - i - 1][c + i + 1] == "--" or self.board[r - i - 1][c + i + 1][0] == "w":
                    moves.append(Move((r, c), (r - i - 1, c + i + 1), self.board))
                if self.board[r - i - 1][c + i + 1] != "--":
                    break

            # for II:
            for i in range(0, min(r - 0, c - 0)):
                if self.board[r - i - 1][c - i - 1] == "--" or self.board[r - i - 1][c - i - 1][0] == "w":
                    moves.append(Move((r, c), (r - i - 1, c - i - 1), self.board))
                if self.board[r - i - 1][c - i - 1] != "--":
                    break

            # for III:
            for i in range(0, min(7 - r, c - 0)):
                if self.board[r + i + 1][c - i - 1] == "--" or self.board[r + i + 1][c - i - 1][0] == "w":
                    moves.append(Move((r, c), (r + i + 1, c - i - 1), self.board))
                if self.board[r + i + 1][c - i - 1] != "--":
                    break

            # for IV:
            for i in range(0, min(7 - r, 7 - c)):
                if self.board[r + i + 1][c + i + 1] == "--" or self.board[r + i + 1][c + i + 1][0] == "w":
                    moves.append(Move((r, c), (r + i + 1, c + i + 1), self.board))
                if self.board[r + i + 1][c + i + 1] != "--":
                    break

    '''
            Get all the king moves for the king located at row, col and add these moves to the list
        '''

    def getKingMoves(self, r, c, moves):
        if self.whiteToMove:
            allyColor = 'w'
        else:
            allyColor = 'b'
        if self.whiteToMove:
            for i in range(r - 1, r + 2):
                for j in range(c - 1, c + 2):
                    #same square selected again,skip this
                    if i == r and j == c:
                        continue
                    if 0 <= i <= 7 and 0 <= j <= 7:  # if possible moves are within the board borders
                        if self.board[i][j] == "--" or self.board[i][j][0] == "b":  #empty square or enemy piece
                            moves.append(Move((r, c), (i, j), self.board))
        else:
            for i in range(r - 1, r + 2):
                for j in range(c - 1, c + 2):
                    #same square selected again,skip this
                    if i == r and j == c:
                        continue
                    if 0 <= i <= 7 and 0 <= j <= 7:  # if possible moves are within the board borders
                        if self.board[i][j] == "--" or self.board[i][j][0] == "w":  #empty square or enemy piece
                            moves.append(Move((r, c), (i, j), self.board))



    '''
    Generate all valid castle moves for the king at (r, c) and add them to the list of moves
    '''

    def getCastleMoves(self, r, c, moves):
        if self.squareUnderAttack(r, c):
            return #can't castle while we are in check
        if (self.whiteToMove and self.currentCastlingRight.wks) or (not self.whiteToMove and self.currentCastlingRight.bks):
            self.getKingSideCastleMoves(r, c, moves)
        if (self.whiteToMove and self.currentCastlingRight.wqs) or (not self.whiteToMove and self.currentCastlingRight.bqs):
            self.getQueenSideCastleMoves(r, c, moves)


    def getKingSideCastleMoves(self, r, c, moves):
        if self.board[r][c+1] == '--' and self.board[r][c+2] == '--':
            if not self.squareUnderAttack(r, c+1) and not self.squareUnderAttack(r, c+2):
                moves.append(Move((r, c), (r, c+2), self.board, isCastleMove=True))




    def getQueenSideCastleMoves(self, r, c, moves):
        if self.board[r][c-1] == '--' and self.board[r][c-2] == '--' and self.board[r][c-3] == '--':
            if not self.squareUnderAttack(r, c-1) and not self.squareUnderAttack(r, c-2):
                moves.append(Move((r, c), (r, c-2), self.board, isCastleMove=True))





    '''
            Get all the queen moves for the queen located at row, col and add these moves to the list
        '''

    def getQueenMoves(self, r, c, moves):
        self.getRookMoves(r, c, moves)
        self.getBishopMoves(r, c, moves)
        pass

class CastleRights():
    def __init__(self, wks, bks, wqs, bqs):
        self.wks = wks
        self.bks = bks
        self.wqs = wqs
        self.bqs = bqs


class Move():
    # maps keys to values
    # key : value
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4,
                   "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3,
                   "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board, enpassantPossible=False, isCastleMove = False):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        #pawn promotion
        self.isPawnPromotion = False
        self.isPawnPromotion = (self.pieceMoved == 'wp' and self.endRow == 0) or (self.pieceMoved == 'bp' and self.endRow == 7)
        self.isCastleMove = isCastleMove        #en passant
        self.isEnpassantMove = enpassantPossible
        if self.isEnpassantMove:
            self.pieceCaptured = 'wp' if self.pieceMoved == 'bp' else 'bp'

        self.isCapture = self.pieceCaptured != '--'
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol

    '''
    Overriding the equals method
    '''

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    def getChessNotation(self):
        #you can add to make this real chess notation
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]


    #overriding the str() function
    def __str__(self):
        #castle move
        if self.isCastleMove:
            return "O-O" if self.endCol == 6 else "O-O-O"

        endSquare = self.getRankFile(self.endRow, self.endCol)
        #pawn moves
        if self.pieceMoved[1] =='p':
            if self.isCapture:
                return self.colsToFiles[self.startCol] + "x" + endSquare
            else:
                return endSquare

            #pawn promotions

        #two of the same type of piece moving to a square,  Nbd2 if both knights can move to d2

        #also adding + for check move, and # for checkmate move


        #piece moves
        moveString = self.pieceMoved[1]
        if self.isCapture:
            moveString += 'x'
        return moveString + endSquare

