"""
The engine stores the current game state and decides whether moves are valid or invalid.
"""
class GameState():
    def __init__(self):
        # An 8x8 two-dimensional board
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]

        self.movefunction = {'P': self.getpawnmoves, 'N': self.getknightmoves, 'Q': self.getqueenmoves,
                             'K': self.getkingmoves, 'B': self.getbishopmoves, 'R': self.getrookmoves,}
        self.whiteToMove = True
        self.movelog = []
        self.whitekinglocation = (7, 4)
        self.blackkinglocation = (0, 4)
        self.checkmate = False
        self.stalemate = False
        self.enpassantpossible = () # Coordinates where an en passant move is possible
        self.enpassantpossiblelog = [self.enpassantpossible]
        self.currentcastlingright = castlerights(True, True, True, True)
        self.castlerightslog = [castlerights(self.currentcastlingright.wks, self.currentcastlingright.bks,
                                             self.currentcastlingright.wqs, self.currentcastlingright.bqs)]

    def makemove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.movelog.append(move) # Allows us to undo the move
        self.whiteToMove = not self.whiteToMove
        if move.pieceMoved == 'wK':
            self.whitekinglocation = (move.endRow, move.endCol)  # Updates the king's location
        elif move.pieceMoved == 'bK':
            self.blackkinglocation = (move.endRow, move.endCol)
        if move.ispawnpromotion: # Promotes the pawn to a queen
            self.board[move.endRow][move.endCol] = move.pieceMoved[0] + 'Q'

        if move.isenpassantmove: # Performs the en passant move
            self.board[move.startRow][move.endCol] = '--'
        if move.pieceMoved[1] == 'P' and abs(move.startRow - move.endRow) == 2:
            self.enpassantpossible = ((move.startRow + move.endRow)//2, move.startCol)
        else:
            self.enpassantpossible = ()

        if move.iscastlemove:  # Castling move
            if move.endCol - move.startCol == 2: # Kingside move
                self.board[move.endRow][move.endCol-1] = self.board[move.endRow][move.endCol+1] # Moves the rook
                self.board[move.endRow][move.endCol+1]= '--'  # Removes the rook
            else:  # Queenside move
                self.board[move.endRow][move.endCol+1] = self.board[move.endRow][move.endCol-2]
                self.board[move.endRow][move.endCol-2] = '--'

        self.enpassantpossiblelog.append(self.enpassantpossible)

        self.updatecastlerights(move)  # Updates castling rights after every king or rook move
        self.castlerightslog.append(castlerights(self.currentcastlingright.wks, self.currentcastlingright.bks,
                                                 self.currentcastlingright.wqs, self.currentcastlingright.bqs))


    def undomove(self):  # Moves the piece back to its previous position
        if len(self.movelog) !=0:
            move=(self.movelog.pop())
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove # Restores the turn
            if move.pieceMoved == 'wK':
               self.whitekinglocation = (move.startRow, move.startCol)  # Updates the king's location
            elif move.pieceMoved == 'bK':
               self.blackkinglocation = (move.startRow, move.startCol)
            if move.isenpassantmove:
                self.board[move.endRow][move.endCol] = '--'
                self.board[move.startRow][move.endCol] = move.pieceCaptured
            self.enpassantpossiblelog.pop()
            self.enpassantpossible = self.enpassantpossiblelog[-1]

            # Undoing a castling move
            self.castlerightslog.pop() # Removes the castling right that we are undoing from the list
            newrights = self.castlerightslog[-1]
            self.currentcastlingright = castlerights(newrights.wks, newrights.bks, newrights.wqs, newrights.bqs)
            if move.iscastlemove:  # Undoing a castling move
                if move.endCol - move.startCol == 2:  # Kingside move
                    self.board[move.endRow][move.endCol + 1] = self.board[move.endRow][move.endCol - 1]  # Moves the rook
                    self.board[move.endRow][move.endCol - 1] = '--'  # Removes the rook
                else:  # Queenside move
                    self.board[move.endRow][move.endCol - 2] = self.board[move.endRow][move.endCol + 1]
                    self.board[move.endRow][move.endCol + 1] = '--'

            self.checkmate = False;
            self.stalemate = False;

    def updatecastlerights(self, move):
        if  move.pieceMoved == 'wK':
            self.currentcastlingright.wks = False
            self.currentcastlingright.wqs = False
        elif  move.pieceMoved == 'bK':
            self.currentcastlingright.bks = False
            self.currentcastlingright.bqs = False
        elif  move.pieceMoved == 'wR':
            if move.startRow == 7:
                if move.startCol == 0:  # Left rook
                    self.currentcastlingright.wqs = False
                elif  move.startCol == 7: # Right rook
                    self.currentcastlingright.wks = False
        elif  move.pieceMoved == 'bR':
            if move.startRow == 0:
                if move.startCol == 0:  # Left rook
                    self.currentcastlingright.bqs = False
                elif  move.startCol == 7: # Right rook
                    self.currentcastlingright.bks = False

        # If a rook is captured
        if move.pieceCaptured == 'wR':
            if move.endRow == 7:
                if move.endCol == 0:
                    self.currentcastlingright.wqs = False
                elif move.endCol == 7:
                    self.currentcastlingright.wks = False
        elif move.pieceCaptured == 'bR':
            if move.endRow == 0:
                if move.endCol == 0:
                    self.currentcastlingright.bqs = False
                elif move.endCol == 7:
                    self.currentcastlingright.bks = False





    def getvalidmoves(self):
        tempenpassantpossible = self.enpassantpossible
        tempcastlerights = castlerights(self.currentcastlingright.wks, self.currentcastlingright.bks,
                                       self.currentcastlingright.wqs, self.currentcastlingright.bqs)
        moves = self.getallpossiblemoves()
        if self.whiteToMove:
            self.getcastlemoves(self.whitekinglocation[0], self.whitekinglocation[1], moves)
        else:
            self.getcastlemoves(self.blackkinglocation[0], self.blackkinglocation[1], moves)

        for i in range(len(moves)-1, -1, -1): # In reverse order
            self.makemove(moves[i])
            self.whiteToMove = not self.whiteToMove
            if self.incheck():
                moves.remove(moves[i])
            self.whiteToMove = not self.whiteToMove
            self.undomove()
        if len(moves) == 0:
            if self.incheck():
                self.checkmate = True
            else:
                self.stalemate = True
        else:
            self.checkmate = False
            self.stalemate = False
        self.enpassantpossible = tempenpassantpossible
        self.currentcastlingright = tempcastlerights
        return moves

    '''
    This method checks whether the current player is in check.
    '''
    def incheck(self):
        if self.whiteToMove:
            return self.squareunderattack(self.whitekinglocation[0], self.whitekinglocation[1])
        else:
            return self.squareunderattack(self.blackkinglocation[0], self.blackkinglocation[1])
    '''
    This method checks whether the specified square can be attacked or not.
    '''
    def squareunderattack(self, r, c):
        self.whiteToMove = not self.whiteToMove # Changes the turn to get all possible opponent moves
        oppmoves = self.getallpossiblemoves()
        self.whiteToMove = not self.whiteToMove # Restores the turn to its previous state
        for move in oppmoves:
            if move.endRow == r and move.endCol == c:
                return True
        return False

    def getallpossiblemoves(self):
        moves = []
        for r in range(len(self.board)):   # Row number
            for c in range(len(self.board[r])):  # Column number
                turn = self.board[r][c][0]
                if(turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    self.movefunction[piece](r, c, moves)
        return moves
    '''
    Gets all moves for the pawn located at the specified row and column and adds them to the list.
    '''
    def getpawnmoves(self, r, c, moves):
        if self.whiteToMove:
            if self.board[r-1][c] == "--":
                moves.append(Move((r, c), (r-1, c), self.board))
                if r == 6 and self.board[r-2][c] == "--":
                   moves.append(Move((r, c), (r-2, c), self.board))
            if c-1 >= 0 :
                if self.board[r-1][c-1][0] == "b":
                    moves.append(Move((r, c), (r-1 , c-1), self.board))
                elif (r-1, c-1) == self.enpassantpossible:
                    moves.append(Move((r, c), (r-1, c-1), self.board, isenpassantmove = True))
            if c+1 <= 7 :
                if self.board[r-1][c+1][0] == "b":
                    moves.append(Move((r, c), (r-1 , c+1), self.board))
                elif (r-1, c+1) == self.enpassantpossible:
                    moves.append(Move((r, c), (r-1, c+1), self.board, isenpassantmove = True))
        else:
            if self.board[r+1][c] == "--":
                moves.append(Move((r, c), (r+1, c), self.board))
                if r == 1 and self.board[r+2][c] == "--":
                   moves.append(Move((r, c), (r+2, c), self.board))
            if c-1 >= 0 :
                if self.board[r+1][c-1][0] == "w":
                    moves.append(Move((r, c), (r+1 , c-1), self.board))
                elif (r+1, c-1) == self.enpassantpossible:
                    moves.append(Move((r, c), (r+1, c-1), self.board, isenpassantmove = True))
            if c+1 <= 7 :
                if self.board[r+1][c+1][0] == "w":
                    moves.append(Move((r, c), (r+1 , c+1), self.board))
                elif (r+1, c+1) == self.enpassantpossible:
                    moves.append(Move((r, c), (r+1, c+1), self.board, isenpassantmove = True))


    '''
    Gets all moves for the rook located at the specified row and column and adds them to the list.
    '''
    def getrookmoves(self, r, c, moves):
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))
        enemycolor = 'b' if self.whiteToMove else 'w'
        for d in directions:
            for i in range(1, 8):
                endRow =  r + d[0] * i
                endCol =  c + d[1] * i
                if 0<= endRow <8 and 0<= endCol <8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--":
                       moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemycolor:
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else:
                        break
                else:
                    break
    '''
        Gets all moves for the king located at the specified row and column and adds them to the list.
    '''
    def getkingmoves(self, r, c, moves):
        kingmoves = ((-1, -1), (-1, 1), (-1, 0), (0, 1), (0, -1), (1, -1), (1, 1), (1, 0))
        enemypiece = 'b' if self.whiteToMove else 'w'
        for i in range(8):
            endRow = r + kingmoves[i][0]
            endCol = c + kingmoves[i][1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece == "--":
                    moves.append(Move((r, c), (endRow, endCol), self.board))
                if endPiece[0] == enemypiece:
                    moves.append(Move((r, c), (endRow, endCol), self.board))

    '''
    Generates legal castling moves for the specified row and column and adds them to the list.
    '''

    def getcastlemoves(self, r, c, moves):
        if self.squareunderattack(r, c):
            return # The first castling condition is not allowed when the king is in check
        if (self.whiteToMove and self. currentcastlingright.wks) or (not self.whiteToMove and self.currentcastlingright.bks):
            self.kingsidecastlemove(r, c, moves)
        if (self.whiteToMove and self. currentcastlingright.wqs) or (not self.whiteToMove and self.currentcastlingright.bqs):
            self.queensidecastlemove(r, c, moves)

    def kingsidecastlemove(self, r, c, moves):
        if self.board[r][c+1] == '--' and self.board[r][c+2] == '--':
            if not self.squareunderattack(r, c+1) and not self.squareunderattack(r, c+2):
                moves.append(Move((r, c), (r, c+2), self.board, iscastlemove = True))


    def  queensidecastlemove(self, r, c, moves):
        if self.board[r][c-1] == '--' and self.board[r][c-2] == '--' and self.board[r][c-3] == "--":
            if not self.squareunderattack(r, c-1) and not self.squareunderattack(r, c-2):
                moves.append(Move((r, c), (r, c-2), self.board, iscastlemove = True))




    '''
        Gets all moves for the knight located at the specified row and column and adds them to the list.
    '''
    def getknightmoves(self, r, c, moves):
        knightmoves = ((-2, -1), (-2, 1), (2, -1), (2, 1), (-1, 2), (-1, -2), (1, -2), (1, 2))
        enemypiece = 'b' if self.whiteToMove else 'w'
        for m in knightmoves:
            endRow = r + m[0]
            endCol = c + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece == "--":
                    moves.append(Move((r, c), (endRow, endCol), self.board))
                if endPiece[0] == enemypiece:
                    moves.append(Move((r, c), (endRow, endCol), self.board))


    '''
        Gets all moves for the queen located at the specified row and column and adds them to the list.
    '''
    def getqueenmoves(self, r, c, moves):
        self.getrookmoves(r, c, moves)
        self.getbishopmoves(r, c, moves)

    '''
        Gets all moves for the bishop located at the specified row and column and adds them to the list.
    '''
    def getbishopmoves(self, r, c, moves):
        directions = ((-1, -1), (1, -1), (-1, 1), (1, 1))
        enemycolor = 'b' if self.whiteToMove else 'w'
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--":
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemycolor:
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else:
                        break
                else:
                    break


class castlerights():
    def __init__(self, wks, bks, wqs, bqs):
        self.wks = wks
        self.bks = bks
        self.wqs = wqs
        self.bqs = bqs



class Move():

    ranksToRows = {"1":7, "2":6, "3":5, "4":4, "5":3, "6":2, "7":1, "8":0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a":0, "b":1, "c":2, "d":3, "e":4, "f":5, "g":6, "h":7}
    colsToFiles = {v: k for k, v in filesToCols.items()}  # A common dictionary for naming the chessboard rows and columns

    def __init__(self, startSq, endSq, board, isenpassantmove = False, iscastlemove = False):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]  # Here we store the move information

        self.ispawnpromotion = False  # Pawn promotion to queen
        if (self.pieceMoved == 'wP' and self.endRow == 0) or(self.pieceMoved == 'bP' and self.endRow == 7):
            self.ispawnpromotion = True

        self.isenpassantmove = isenpassantmove  # En passant
        if self.isenpassantmove:
            self.pieceCaptured = 'wP' if self.pieceMoved == 'bP' else 'bP'

        self.iscapture = self.pieceCaptured != '--'
        self.moveID = self.startRow*1000 + self.startCol*100 + self.endRow*10 + self.endCol # Assigns each move an ID from 0 to 7777

        self.iscastlemove = iscastlemove

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    def getchessnotation(self):
        return self.getrankfile(self.startRow, self.startCol) + self.getrankfile(self.endRow, self.endCol)

    def getrankfile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]

    def __str__(self):
        if self.iscastlemove:
            return "o-o" if self.endCol == 6 else "o-o-o"

        endsquare = self.getrankfile(self.endRow, self.endCol)
        if self.pieceMoved[1] == 'P':
            if self.iscapture:
                return self.colsToFiles[self.startCol] + "x" + endsquare
            else:
                return endsquare

        movestring =  self.pieceMoved[1]
        if self.iscapture:
            movestring += 'x'
        return movestring + endsquare