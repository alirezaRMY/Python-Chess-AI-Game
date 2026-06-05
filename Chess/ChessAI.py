import random

piecescore = {"K": 0, "Q": 10, "R": 5, "B": 3, "N": 3, "P": 1}

checkmate = 1000
stalemate = 0
DEPTH = 3

knightscore = [[1, 1, 1, 1, 1, 1, 1, 1],
               [1, 2, 2, 2, 2, 2, 2, 1],
               [1, 2, 3, 3, 3, 3, 2, 1],
               [1, 2, 3, 4, 4, 3, 2, 1],
               [1, 2, 3, 4, 4, 3, 2, 1],
               [1, 2, 3, 3, 3, 3, 2, 1],
               [1, 2, 2, 2, 2, 2, 2, 1],
               [1, 1, 1, 1, 1, 1, 1, 1]]


bishopscore = [[4, 3, 2, 1, 1, 2, 3, 4],
               [3, 4, 3, 2, 2, 3, 4, 3],
               [2, 3, 4, 3, 3, 4, 3, 2],
               [1, 2, 3, 4, 4, 3, 2, 1],
               [1, 2, 3, 4, 4, 3, 2, 1],
               [2, 3, 4, 3, 3, 4, 3, 2],
               [3, 4, 3, 2, 2, 3, 4, 3],
               [4, 3, 2, 1, 1, 2, 3, 4]]


queenscore =  [[1, 1, 1, 3, 1, 1, 1, 1],
               [1, 2, 3, 3, 3, 1, 1, 1],
               [1, 4, 3, 3, 3, 4, 2, 1],
               [1, 2, 3, 3, 3, 2, 2, 1],
               [1, 2, 3, 3, 3, 2, 2, 1],
               [1, 4, 3, 3, 3, 4, 2, 1],
               [1, 1, 2, 3, 3, 1, 1, 1],
               [1, 1, 1, 3, 1, 1, 1, 1]]


rookscore =   [[4, 3, 4, 4, 4, 4, 3, 4],
               [4, 4, 4, 4, 4, 4, 4, 4],
               [1, 1, 2, 2, 2, 2, 1, 1],
               [1, 2, 3, 4, 4, 3, 2, 1],
               [1, 2, 3, 4, 4, 3, 2, 1],
               [1, 1, 2, 2, 2, 2, 1, 1],
               [4, 4, 4, 4, 4, 4, 4, 4],
               [4, 3, 4, 4, 4, 4, 3, 4]]


whitePscore = [[9, 9, 9, 9, 9, 9, 9, 9],
               [8, 8, 8, 8, 8, 8, 8, 8],
               [5, 6, 6, 7, 7, 6, 6, 5],
               [2, 3, 3, 5, 5, 3, 3, 2],
               [1, 2, 3, 4, 4, 3, 2, 1],
               [1, 1, 2, 3, 3, 2, 1, 1],
               [1, 1, 1, 0, 0, 1, 1, 1],
               [0, 0, 0, 0, 0, 0, 0, 0]]


blackPscore = [[0, 0, 0, 0, 0, 0, 0, 0],
               [1, 1, 1, 0, 0, 1, 1, 1],
               [1, 1, 2, 3, 3, 2, 1, 1],
               [1, 2, 3, 4, 4, 3, 2, 1],
               [2, 3, 3, 5, 5, 3, 3, 2],
               [5, 6, 6, 7, 7, 6, 6, 5],
               [8, 8, 8, 8, 8, 8, 8, 8],
               [9, 9, 9, 9, 9, 9, 9, 9]]


pieceposiotionscores = {"N": knightscore, "Q": queenscore, "B": bishopscore, "R": rookscore, "wP": whitePscore,
                        "bP": blackPscore}


def findrandommove(validmoves):
    return validmoves[random.randint(0, len(validmoves) - 1)]


def findbestmove(gs, validmoves):
    global nextmove
    nextmove = None
    random.shuffle(validmoves)
    findmoveminmaxalphabeta(gs, validmoves, DEPTH, -checkmate, checkmate, 1 if gs.whiteToMove else -1)
    return nextmove


def findmoveminmaxalphabeta(gs, validmoves, depth, alpha, beta, turnmultiplier):
    global nextmove
    if depth == 0:
        return turnmultiplier * scoreboard(gs)

    maxscore = -checkmate
    for move in validmoves:
        gs.makemove(move)
        nextmoves = gs.getvalidmoves()
        score = -findmoveminmaxalphabeta(gs, nextmoves, depth - 1, -beta, -alpha, -turnmultiplier)
        if score > maxscore:
            maxscore = score
            if depth == DEPTH:
                nextmove = move
                print(move, score)
        gs.undomove()
        if maxscore > alpha:
            alpha = maxscore
        if alpha >= beta:
            break
    return maxscore


'''
A positive score is good for White, and a negative score is good for Black.
'''

def scoreboard(gs):
    if gs.checkmate:
        if gs.whiteToMove:
            return -checkmate  # Black wins, so the score is negative.
        else:
            return checkmate  # White wins, so the score is positive.
    elif gs.stalemate:
        return stalemate

    score = 0
    for row in range(len(gs.board)):
        for col in range(len(gs.board[row])):
            square = gs.board[row][col]
            if square != "--":
                # Adds a position-based evaluation score.
                pieceposiotionscore = 0
                if square[1] != "K":
                    if square[1] == "P":
                        pieceposiotionscore = pieceposiotionscores[square][row][col]
                    else:
                        pieceposiotionscore = pieceposiotionscores[square[1]][row][col]

                if square[0] == 'w':
                    score += piecescore[square[1]] + pieceposiotionscore * .1
                elif square[0] == 'b':
                    score -= piecescore[square[1]] + pieceposiotionscore * .1

    return score