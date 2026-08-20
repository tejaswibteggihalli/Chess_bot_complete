import random

pieceScore = {"K": 0, "Q": 9, "R": 5, "B": 3, "N": 3, "p": 1}

knightScores = [
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 2, 2, 2, 2, 2, 2, 1],
    [1, 2, 3, 3, 3, 3, 2, 1],
    [1, 2, 3, 4, 4, 3, 2, 1],
    [1, 2, 3, 4, 4, 3, 2, 1],
    [1, 2, 3, 3, 3, 3, 2, 1],
    [1, 2, 2, 2, 2, 2, 2, 1],
    [1, 1, 1, 1, 1, 1, 1, 1],
]

bishopScores = [
    [4, 3, 2, 1, 1, 2, 3, 4],
    [3, 4, 3, 2, 2, 3, 4, 3],
    [2, 4, 4, 3, 3, 4, 4, 2],
    [1, 2, 4, 4, 4, 4, 2, 1],
    [1, 2, 3, 4, 4, 3, 2, 1],
    [2, 3, 4, 3, 3, 3, 3, 2],
    [3, 4, 4, 4, 4, 4, 4, 3],
    [4, 3, 3, 4, 4, 3, 3, 4],
]

queenScores = [
    [1, 1, 1, 3, 1, 1, 1, 1],
    [1, 2, 3, 3, 3, 1, 1, 1],
    [1, 4, 3, 3, 3, 3, 2, 1],
    [1, 2, 3, 3, 4, 3, 2, 1],
    [1, 2, 3, 3, 3, 3, 2, 1],
    [1, 4, 3, 3, 3, 3, 2, 1],
    [1, 1, 2, 3, 3, 1, 1, 1],
    [1, 1, 1, 3, 1, 1, 1, 1],
]

rookScores = [
    [4, 3, 4, 4, 4, 4, 3, 4],
    [4, 4, 4, 4, 4, 4, 4, 4],
    [1, 1, 2, 3, 3, 2, 1, 1],
    [1, 2, 3, 4, 4, 3, 2, 1],
    [1, 2, 3, 4, 4, 3, 2, 1],
    [1, 1, 2, 2, 2, 2, 1, 1],
    [4, 4, 4, 4, 4, 4, 4, 4],
    [4, 3, 4, 4, 4, 4, 3, 4],
]

whitePawnScores = [
    [8, 8, 8, 8, 8, 8, 8, 8],
    [8, 8, 8, 8, 8, 8, 8, 8],
    [5, 6, 6, 7, 7, 6, 6, 5],
    [2, 3, 3, 5, 5, 3, 3, 2],
    [1, 2, 3, 4, 4, 3, 2, 1],
    [1, 1, 2, 3, 3, 2, 1, 1],
    [1, 1, 1, 0, 0, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0],
]

blackPawnScores = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 0, 0, 1, 1, 1],
    [1, 1, 2, 3, 3, 2, 1, 1],
    [1, 2, 3, 4, 4, 3, 2, 1],
    [2, 3, 3, 5, 5, 3, 3, 2],
    [5, 6, 6, 7, 7, 6, 6, 5],
    [8, 8, 8, 8, 8, 8, 8, 8],
    [8, 8, 8, 8, 8, 8, 8, 8],
]

zeroScores = [[0] * 8 for _ in range(8)]
piecePositionScores = {
    "wN": knightScores,
    "bN": knightScores[::-1],
    "wB": bishopScores,
    "bB": bishopScores[::-1],
    "wR": rookScores,
    "bR": rookScores[::-1],
    "wQ": queenScores,
    "bQ": queenScores[::-1],
    "wp": whitePawnScores,
    "bp": blackPawnScores,
    "wK": zeroScores,
    "bK": zeroScores,
}












CHECKMATE = 1000
STALEMATE = 0
DEPTH = 5
QUIESCENCE_MAX_DEPTH = 6
node_count = 0





def findRandomMove(validMoves):
    return validMoves[random.randint(0, len(validMoves)-1)]


def formatPrincipalVariation(gs, principalVariation):
    movePairs = []
    moveNumber = len(gs.moveLog) // 2 + 1
    index = 0

    if not gs.whiteToMove and principalVariation:
        movePairs.append(f"{moveNumber}. ... {principalVariation[0]}")
        moveNumber += 1
        index = 1

    while index < len(principalVariation):
        moves = " ".join(str(move) for move in principalVariation[index:index + 2])
        movePairs.append(f"{moveNumber}. {moves}")
        moveNumber += 1
        index += 2
    return "[ " + " ".join(movePairs) + " ]"


def scoreMoveForOrdering(gs, move):
    score = 0
    attackerValue = pieceScore[move.pieceMoved[1]]

    if move.isCapture:
        victimValue = pieceScore[move.pieceCaptured[1]]
        score += 100000 + victimValue * 10 - attackerValue

    if move.isPawnPromotion:
        score += 90000

    if move.isCastleMove:
        score += 10000

    return score


def orderMoves(gs, validMoves):
    forcingMoves = []
    quietMoves = []

    for move in validMoves:
        if move.isCapture or move.isPawnPromotion or move.isCastleMove:
            forcingMoves.append(move)
        else:
            quietMoves.append(move)

    forcingMoves.sort(key=lambda move: scoreMoveForOrdering(gs, move), reverse=True)
    return forcingMoves + quietMoves




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
    global node_count
    nextMove = None
    node_count = 0
    rootTurnMultiplier = 1 if gs.whiteToMove else -1
    #findMoveMinMax(gs. validMoves, DEPTH, gs.whiteToMove)
    score, principalVariation = findMoveNegaMaxAlphaBeta(
        gs,
        validMoves,
        DEPTH,
        -CHECKMATE,
        CHECKMATE,
        rootTurnMultiplier,
    )
    if principalVariation:
        whiteScore = score * rootTurnMultiplier
        print("engine top line:", formatPrincipalVariation(gs, principalVariation))
        print(f"White: {whiteScore:.2f} STM: {score:.2f}")
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

def quiescenceSearch(gs, alpha, beta, turnMultiplier, depth=0):
    global node_count
    node_count += 1

    validMoves = gs.getValidMoves()
    if gs.checkmate or gs.stalemate or gs.fiftyMoveDraw:
        return turnMultiplier * scoreBoard(gs)

    standPat = turnMultiplier * scoreBoard(gs)
    if depth >= QUIESCENCE_MAX_DEPTH:
        return standPat
    if standPat >= beta:
        return standPat
    if standPat > alpha:
        alpha = standPat

    if gs.inCheck():
        tacticalMoves = validMoves
    else:
        tacticalMoves = [
            move for move in validMoves
            if move.isCapture or move.isPawnPromotion
        ]

    for move in orderMoves(gs, tacticalMoves):
        gs.makeMove(move)
        score = -quiescenceSearch(gs, -beta, -alpha, -turnMultiplier, depth + 1)
        gs.undoMove()

        if score >= beta:
            return score
        if score > alpha:
            alpha = score

    return alpha

def findMoveNegaMaxAlphaBeta(gs, validMoves, depth, alpha, beta, turnMultiplier):
    global nextMove
    global node_count
    node_count += 1

    if gs.checkmate or gs.stalemate or gs.fiftyMoveDraw:
        return turnMultiplier * scoreBoard(gs), []
    if depth == 0:
        return quiescenceSearch(gs, alpha, beta, turnMultiplier), []

    orderedMoves = orderMoves(gs, validMoves)
    maxScore = -CHECKMATE
    bestLine = []
    for move in orderedMoves:
        gs.makeMove(move)
        nextMoves = gs.getValidMoves()
        childScore, childLine = findMoveNegaMaxAlphaBeta(
            gs,
            nextMoves,
            depth - 1,
            -beta,
            -alpha,
            -turnMultiplier,
        )
        score = -childScore
        if score > maxScore:
            maxScore = score
            bestLine = [move] + childLine
            if depth == DEPTH:
                nextMove = move
                print(move, score)
        gs.undoMove()
        if maxScore > alpha: #pruning happens
            alpha = maxScore
        if alpha >= beta:
            break
    return maxScore, bestLine
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
    elif gs.fiftyMoveDraw:
        return STALEMATE

    score = 0
    for row in range(len(gs.board)):
        for col in range(len(gs.board[row])):
            square = gs.board[row][col]
            if square != "--":
                #score it positionally
                pstRow = 7 - row if square[0] == "b" and square[1] != "p" else row
                piecePositionScore = piecePositionScores[square][pstRow][col] * .1


                if square[0] == 'w':
                    score += pieceScore[square[1]] + piecePositionScore
                elif square[0] == 'b':
                    score -= pieceScore[square[1]] + piecePositionScore

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