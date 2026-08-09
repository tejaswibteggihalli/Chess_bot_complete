import random

pieceScore = {"K":0, "Q": 9, "R": 5, "B": 3.5, "N": 3, "p": 1}

knightScores = [
    [-50,-40,-30,-30,-30,-30,-40,-50],
    [-40,-20,  0,  0,  0,  0,-20,-40],
    [-30,  0, 10, 15, 15, 10,  0,-30],
    [-30,  5, 15, 20, 20, 15,  5,-30],
    [-30,  5, 15, 20, 20, 15,  5,-30],
    [-30,  0, 10, 15, 15, 10,  0,-30],
    [-40,-20,  0,  0,  0,  0,-20,-40],
    [-50,-40,-30,-30,-30,-30,-40,-50]
]

bishopScores = [
    [-20,-10,-10,-10,-10,-10,-10,-20],
    [-10,  0,  0,  0,  0,  0,  0,-10],
    [-10,  0,  5, 10, 10,  5,  0,-10],
    [-10,  5,  5, 10, 10,  5,  5,-10],
    [-10,  5,  5, 10, 10,  5,  5,-10],
    [-10,  0,  5, 10, 10,  5,  0,-10],
    [-10,  0,  0,  0,  0,  0,  0,-10],
    [-20,-10,-10,-10,-10,-10,-10,-20]
]

queenScores = [
    [-20,-10,-10, -5, -5,-10,-10,-20],
    [-10,  0,  0,  0,  0,  0,  0,-10],
    [-10,  0,  5,  5,  5,  5,  0,-10],
    [ -5,  0,  5,  5,  5,  5,  0, -5],
    [ -5,  0,  5,  5,  5,  5,  0, -5],
    [-10,  0,  5,  5,  5,  5,  0,-10],
    [-10,  0,  0,  0,  0,  0,  0,-10],
    [-20,-10,-10, -5, -5,-10,-10,-20]
]

kingMidgameScores = [
    [ 20, 30, 10,  0,  0, 10, 30, 20],
    [ 20, 20,  0,  0,  0,  0, 20, 20],
    [-10,-20,-20,-20,-20,-20,-20,-10],
    [-20,-30,-30,-40,-40,-30,-30,-20],
    [-20,-30,-30,-40,-40,-30,-30,-20],
    [-10,-20,-20,-20,-20,-20,-20,-10],
    [ 20, 20,  0,  0,  0,  0, 20, 20],
    [ 20, 30, 10,  0,  0, 10, 30, 20]
]

kingEndgameScores = [
    [-50,-40,-30,-20,-20,-30,-40,-50],
    [-30,-20,-10,  0,  0,-10,-20,-30],
    [-30,-10, 20, 30, 30, 20,-10,-30],
    [-30,-10, 30, 40, 40, 30,-10,-30],
    [-30,-10, 30, 40, 40, 30,-10,-30],
    [-30,-10, 20, 30, 30, 20,-10,-30],
    [-30,-20,-10,  0,  0,-10,-20,-30],
    [-50,-40,-30,-20,-20,-30,-40,-50]
]

whitePawnScores = [
    [ 0,  0,  0,  0,  0,  0,  0,  0],   # rank 8
    [50, 50, 50, 50, 50, 50, 50, 50],   # rank 7 — one step from promoting
    [10, 10, 20, 30, 30, 20, 10, 10],   # rank 6
    [ 5,  5, 10, 25, 25, 10,  5,  5],   # rank 5
    [ 0,  0,  0, 20, 20,  0,  0,  0],   # rank 4
    [ 5, -5,-10,  0,  0,-10, -5,  5],   # rank 3
    [ 5, 10, 10,-20,-20, 10, 10,  5],   # rank 2 — starting rank
    [ 0,  0,  0,  0,  0,  0,  0,  0]    # rank 1
]

blackPawnScores = [
    [ 0,  0,  0,  0,  0,  0,  0,  0],   # rank 8
    [ 5, 10, 10,-20,-20, 10, 10,  5],   # rank 7 — starting rank
    [ 5, -5,-10,  0,  0,-10, -5,  5],   # rank 6
    [ 0,  0,  0, 20, 20,  0,  0,  0],   # rank 5
    [ 5,  5, 10, 25, 25, 10,  5,  5],   # rank 4
    [10, 10, 20, 30, 30, 20, 10, 10],   # rank 3
    [50, 50, 50, 50, 50, 50, 50, 50],   # rank 2 — one step from promoting
    [ 0,  0,  0,  0,  0,  0,  0,  0]    # rank 1
]

rookScoresWhite = [
    [ 0,  0,  0,  0,  0,  0,  0,  0],   # rank 8
    [ 5, 10, 10, 10, 10, 10, 10,  5],   # rank 7 — the key bonus
    [-5,  0,  0,  0,  0,  0,  0, -5],   # rank 6
    [-5,  0,  0,  0,  0,  0,  0, -5],   # rank 5
    [-5,  0,  0,  0,  0,  0,  0, -5],   # rank 4
    [-5,  0,  0,  0,  0,  0,  0, -5],   # rank 3
    [-5,  0,  0,  0,  0,  0,  0, -5],   # rank 2
    [ 0,  0,  0,  5,  5,  0,  0,  0]    # rank 1 — small bonus for d/e files (post-castling)
]

rookScoresBlack = rookScoresWhite[::-1]

piecePositionScores = {"wN": knightScores, "bN": knightScores, "wQ": queenScores, "bQ": queenScores, "wB": bishopScores, "bB": bishopScores, "wR": rookScoresWhite, "bR": rookScoresBlack, "bp": blackPawnScores, "wp": whitePawnScores, "wK": kingMidgameScores, "bK": kingMidgameScores}












CHECKMATE = 1000
STALEMATE = 0
DEPTH = 4
node_count = 0





def findRandomMove(validMoves):
    return validMoves[random.randint(0, len(validMoves)-1)]




def findBestMoveMinMaxNoRecursion(gs, validMoves): #MinMax without recursion
    turnMultiplier = 1 if gs.whiteToMove else -1
    opponentMinMaxScore = CHECKMATE
    bestPlayerMove = None
    random.shuffle(validMoves)
    for playerMove in validMoves:
        gs.makeMove(playerMove)
        opponentsMoves = gs.getValidMoves()
        if gs.stalemate:
            opponentMaxScore = STALEMATE
        elif gs.checkmate:
            opponentMaxScore = -CHECKMATE
        else:
            opponentMaxScore = -CHECKMATE
            for opponentsMove in opponentsMoves:
                gs.makeMove(opponentsMove)
                gs.getValidMoves()
                if gs.checkmate:
                    score = CHECKMATE
                elif gs.stalemate:
                    score = STALEMATE
                else:
                    score = -turnMultiplier * scoreMaterial(gs.board)
                if score > opponentMaxScore:
                    opponentMaxScore = score
                gs.undoMove()
            if opponentMaxScore < opponentMinMaxScore:
                opponentMinMaxScore = opponentMaxScore
                bestPlayerMove = playerMove
            gs.undoMove()
        return bestPlayerMove

'''
Helper method to make the first recursive call
'''
def findBestMove(gs, validMoves, returnQueue):
    global nextMove
    nextMove = None
    random.shuffle(validMoves)
    #findMoveMinMax(gs. validMoves, DEPTH, gs.whiteToMove)
    findMoveNegaMaxAlphaBeta(gs, validMoves, DEPTH, -CHECKMATE, CHECKMATE, 1 if gs.whiteToMove else -1)
    print(f"Evaluated {node_count} nodes")
    returnQueue.put(nextMove)

def findMoveMinMax(gs, validMoves, depth, whiteToMove):
    global nextMove
    global node_count
    node_count += 1
    if depth == 0:
        return scoreMaterial(gs.board)

    if whiteToMove:
        maxScore = -CHECKMATE
        for move in validMoves:
            gs.makeMove(move)
            nextMoves = gs.getValidMoves()
            score = findMoveMinMax(gs, nextMoves, depth-1, False)
            if score > maxScore:
                maxScore = score
                if depth == DEPTH:
                    nextMove = move
            gs.undoMove()
        return maxScore
    else:
        minScore = CHECKMATE
        for move in validMoves:
            gs.makeMove(move)
            nextMoves = gs.getValidMoves()
            score = findMoveMinMax(gs, nextMoves, depth-1, True)
            if score < minScore:
                minScore = score
                if depth == DEPTH:
                    nextMove = move
            gs.undoMove()
        return minScore

def findMoveNegaMax(gs, validMoves, depth, turnMultiplier):
    global nextMove
    if depth == 0:
        return turnMultiplier * scoreBoard(gs)

    maxScore = -CHECKMATE
    for move in validMoves:
        gs.makeMove(move)
        nextMoves = gs.getValidMoves()
        score = -findMoveNegaMax(gs, nextMoves, depth-1, -turnMultiplier)
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move
        gs.undoMove()
        return maxScore

def findMoveNegaMaxAlphaBeta(gs, validMoves, depth, alpha, beta, turnMultiplier):
    global nextMove
    global node_count
    node_count += 1
    if depth == 0:
        return turnMultiplier * scoreBoard(gs)

    #move ordering - implement later
    maxScore = -CHECKMATE
    for move in validMoves:
        gs.makeMove(move)
        nextMoves = gs.getValidMoves()
        score = -findMoveNegaMaxAlphaBeta(gs, nextMoves, depth-1, -beta, -alpha, -turnMultiplier)
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move
                print(move, score)
        gs.undoMove()
        if maxScore > alpha: #pruning happens
            alpha = maxScore
        if alpha >= beta:
            break
    return maxScore
'''
A positive score is good for white, a negative score is good for black
'''
def scoreBoard(gs):
    if gs.checkmate:
        if gs.whiteToMove:
            return -CHECKMATE #black wins
        else:
            return CHECKMATE #white wins
    elif gs.stalemate:
        return STALEMATE

    score = 0
    for row in range(len(gs.board)):
        for col in range(len(gs.board[row])):
            square = gs.board[row][col]
            if square != "--":
                #score it positionally
                piecePositionScore = piecePositionScores[square][row][col] * .1


                if square[0] == 'w':
                    score += pieceScore[square[1]] + piecePositionScore*.1
                elif square[0] == 'b':
                    score -= pieceScore[square[1]] + piecePositionScore*.1

    return score




'''
Score the board based on material.
'''
def scoreMaterial(board):
    score = 0
    for row in board:
        for square in row:
            if square[0] == 'w':
                score += pieceScore[square[1]]
            elif square[0] == 'b':
                score -= pieceScore[square[1]]

    return score