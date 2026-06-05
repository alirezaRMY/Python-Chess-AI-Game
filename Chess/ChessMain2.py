import pygame as p
from Chess import ChessEngine
import time

BOARD_WIDTH = BOARD_HEIGHT = 512
MOVE_LOG_PANEL_WIDTH = 350
MOVE_LOG_PANEL_HEIGHT = BOARD_HEIGHT
DIMENSION = 8
SQ_SIZE = BOARD_HEIGHT // DIMENSION  #64
MAX_FPS = 50
IMAGES = {}


def loadimages():
    pieces = ["wP", "wR", "wN", "wB", "wQ", "wK", "bP", "bR", "bN", "bB", "bQ", "bK"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))


def main(player1, player2):
    global white_time, black_time, move_time, first_round
    white_time = 0
    black_time = 0
    move_time = 0
    first_round = True
    p.init()
    screen = p.display.set_mode((BOARD_WIDTH + MOVE_LOG_PANEL_WIDTH, BOARD_HEIGHT))
    clock = p.time.Clock()
    p.display.set_caption("enjoy Alireza(RM)'s chess game project :)")
    screen.fill(p.Color("white"))
    movelogfont = p.font.SysFont("Arial", 14, False, False)
    gs = ChessEngine.GameState()
    validmoves = gs.getvalidmoves()
    movemade = False
    animate = False # Used when we want to animate a move
    loadimages()  # Runs only once before the loop to avoid unnecessary loading and prevent slowdown
    sqSelected = () # Stores the user's last click
    playerClicks = [] # Stores the user's clicks
    running = True
    gameover = False
    while running:   # Mouse input is handled inside the while loop
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:  # Mouse movement starts from this section
                if not gameover:
                    location = p.mouse.get_pos()  # Vertical or horizontal position
                    col = location[0] // SQ_SIZE
                    row = location[1] // SQ_SIZE
                    if sqSelected == (row, col) or col >= 8:  # If the user selects the same square again or clicks on the turn panel, the variables should be reset
                        sqSelected = ()
                        playerClicks = []
                    else:
                        sqSelected = (row, col)
                        playerClicks.append(sqSelected)
                    if len(playerClicks) == 2:# If the player has selected the destination with the second click
                        move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                        print(move.getchessnotation())
                        for i in range(len(validmoves)):
                            if move == validmoves[i]:
                                gs.makemove(validmoves[i])
                                movemade = True
                                animate = True
                                sqSelected = ()
                                playerClicks = []  # Resets the player's turn
                        if not movemade:
                            playerClicks = [sqSelected]
            # Hotkeys
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z: # Undoes the move
                    gs.undomove()
                    movemade = True
                    animate = False
                    gameover = False
                if e.key == p.K_r: # Resets the game
                    gs = ChessEngine.GameState()
                    validmoves = gs.getvalidmoves()
                    sqSelected = ()
                    playerClicks = []
                    movemade = False
                    animate = False
                    gameover = False

        if movemade:
            if animate:
                animatemove(gs.movelog[-1], screen, gs.board, clock)
                move_time = p.time.get_ticks()
                if first_round == True:
                    first_round = False
                else:
                    if gs.whiteToMove:
                        white_time += move_time - last_move_time
                    else:
                        black_time += move_time - last_move_time
            validmoves = gs.getvalidmoves()
            movemade = False
            animate = False

        last_move_time = move_time
        drawgamestate(screen, gs, validmoves, sqSelected, movelogfont, player1, player2, white_time, black_time)
        if gs.checkmate or gs.stalemate:
            gameover = True
            if gs.stalemate:
                text = 'mate'
            elif gs.whiteToMove:
                text = player2 + ' wins by Checkmate'
            else:
                text = player1 + ' wins by Checkmate'
            drawendgametext(screen, text)
        clock.tick(MAX_FPS)
        p.display.flip()

'''
Highlights the possible squares and the selected piece.
'''
def highlightsquares(screen, gs, validmoves, sqSelected):
    if sqSelected != ():
        r,c = sqSelected
        if gs.board[r][c][0] == ('w' if gs.whiteToMove else 'b'):
            # Highlights the piece
            s = p.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100)
            s.fill(p.Color('blue'))
            screen.blit(s, (c*SQ_SIZE, r*SQ_SIZE))
            # Highlights the possible moves for the piece
            s.fill(p.Color('yellow'))
            for move in validmoves:
                if move.startRow == r and move.startCol == c:
                    screen.blit(s, (move.endCol*SQ_SIZE, move.endRow*SQ_SIZE))


def drawgamestate(screen, gs, validmoves, sqSelected, font, player1, player2, white_time, black_time):
    drawboard(screen)
    highlightsquares(screen, gs, validmoves, sqSelected)
    drawpieces(screen, gs.board)
    drawmovelog(screen, gs, font, player1, player2)
    player1_text = font.render(player2 + " = ", True, p.Color("white"))
    player2_text = font.render(player1 + " = ", True, p.Color("white"))
    screen.blit(player1_text, (BOARD_WIDTH + MOVE_LOG_PANEL_WIDTH - 85, 25))
    screen.blit(player2_text, (BOARD_WIDTH + MOVE_LOG_PANEL_WIDTH - 85, 45))
    white_time_str = format_time(white_time)
    black_time_str = format_time(black_time)
    white_time_text = font.render(white_time_str, True, p.Color("white"))
    black_time_text = font.render(black_time_str, True, p.Color("white"))
    screen.blit(white_time_text, (BOARD_WIDTH + MOVE_LOG_PANEL_WIDTH - 35, 25))
    screen.blit(black_time_text, (BOARD_WIDTH + MOVE_LOG_PANEL_WIDTH - 35, 45))


def format_time(milliseconds):
    seconds = milliseconds // 1000
    minutes = seconds // 60
    seconds %= 60
    return f"{minutes:02d}:{seconds:02d}"


def drawboard(screen):
    global colors
    colors = [p.Color('light gray'), p.Color('dark green')]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r+c) % 2)]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))


def drawpieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))




def drawmovelog(screen, gs, font, player1, player2):
    movelogrect = p.Rect(BOARD_WIDTH, 0, MOVE_LOG_PANEL_WIDTH, MOVE_LOG_PANEL_HEIGHT)
    p.draw.rect(screen, p.Color("black"), movelogrect)
    movelog = gs.movelog
    moves = []
    movetexts = []
    movesperrow = 4
    for i in range(0, len(movelog), 2):
        movestring = str(i // 2 + 1) + " :: "

        if i % (movesperrow * 2) == 0:
            player_names = "{} vs {}".format(player1, player2)
            player_time = "{} : ".format("StopWatch Time")
            player_names_object = font.render(player_names, True, p.Color('white'))
            player_time_object = font.render(player_time, True, p.Color('white'))
            player_names_location = movelogrect.move(110, 5)
            player_time_location = movelogrect.move(258, 5)
            if gs.whiteToMove:
                player_turn = "{}'s Turn".format(player1)
            else:
                player_turn = "{}'s Turn".format(player2)
            player_turn_object = font.render(player_turn, True, p.Color('light Green'))
            player_turn_location = movelogrect.move(5, 30)
            screen.blit(player_names_object, player_names_location)
            screen.blit(player_time_object, player_time_location)
            screen.blit(player_turn_object, player_turn_location)

        movestring += str(movelog[i]) + " "
        if i + 1 < len(movelog):
            movestring += str(movelog[i + 1]) + "   "

        movetexts.append(movestring)

    padding = 5
    movesperrow = 4
    texty = 70
    linespacing = 2
    for i in range(0, len(movetexts), movesperrow):
        text = ""
        for j in range(movesperrow):
            if i + j < len(movetexts):
                text += movetexts[i + j]
        textobject = font.render(text, True, p.Color('white'))
        textlocation = movelogrect.move(padding, texty)
        texty += textobject.get_height() + linespacing
        screen.blit(textobject, textlocation)



def animatemove(move, screen, board, clock):
    global colors
    dr = move.endRow - move.startRow
    dc = move.endCol - move.startCol
    framepersquare = 10
    framecount = (abs(dr) + abs(dc)) * framepersquare
    for frame in range(framecount + 1):
        r, c = (move.startRow + dr*frame/framecount, move.startCol + dc*frame/framecount)
        drawboard(screen)
        drawpieces(screen, board)
        color = colors[(move.endRow + move.endCol) % 2]
        endSquare = p.Rect(move.endCol*SQ_SIZE, move.endRow*SQ_SIZE, SQ_SIZE, SQ_SIZE)
        p.draw.rect(screen, color, endSquare)
        if move.pieceCaptured != '--':
            if move.isenpassantmove:
                enpassantrow = move.endRow + 1 if move.pieceCaptured[0] == 'b' else move.endRow - 1
                endSquare = p.Rect(move.endCol * SQ_SIZE, enpassantrow * SQ_SIZE, SQ_SIZE, SQ_SIZE)
            screen.blit(IMAGES[move.pieceCaptured], endSquare)
        screen.blit(IMAGES[move.pieceMoved], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
        p.display.flip()
        clock.tick(60)

def drawendgametext(screen, text):
    font = p.font.SysFont("Helvitca", 32, True, False)
    textobject = font.render(text, 0, p.Color('black'))
    textlocation = p.Rect(0, 0, BOARD_WIDTH, BOARD_HEIGHT).move(BOARD_WIDTH / 2 - textobject.get_width() / 2, BOARD_HEIGHT / 2 - textobject.get_height() / 2)
    screen.blit(textobject, textlocation)
    textobject = font.render(text, 0, p.Color('red'))
    screen.blit(textobject, textlocation.move(2, 2))

if __name__ == "__main__":
    main(player1, player2)