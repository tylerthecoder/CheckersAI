from Piece import Piece
import pygame as pg
import time

#Colors
BLACK = (0, 0, 0)
DARK_BROWN = (140, 100, 20)
LIGHT_BROWN = (220, 190, 130)
WHITE = (255, 255, 255)
RED = (200, 0, 0)
GREEN = (100, 200, 0)
YELLOW = (230, 230, 0)


clock = pg.time.Clock()
clock.tick(30)

size = (700,700)
screen = pg.display.set_mode(size)
pg.display.set_caption("Checkers")
pg.init()
pg.event.set_allowed(pg.QUIT)
pg.event.set_allowed(pg.MOUSEBUTTONDOWN)

tile_width = size[0] / 8
piece_type = Piece

# Board surface
board_surface = pg.Surface(size)
pg.Surface.lock(board_surface)
board_surface.fill((DARK_BROWN))

    #Create Tiles
for i in range(8):
    for j in range(8):
        if (i + j) % 2 == 0:
            pg.draw.rect(board_surface, LIGHT_BROWN, [j*tile_width, i*tile_width, tile_width, tile_width], 0)

    # Draw Tile Outlines
for i in range(8):
    pg.draw.line(board_surface, BLACK, [i*tile_width, 0], [i*tile_width, size[1]], 4)
    for j in range(8):
        pg.draw.line(board_surface, BLACK, [0, j*tile_width], [700, j*tile_width], 4)
pg.draw.line(board_surface, BLACK, [size[0] - 3, 0], [size[0] - 3, size[1]], 4)
pg.draw.line(board_surface, BLACK, [0, size[1] - 3], [size[0], size[1] - 3], 4)

pg.Surface.unlock(board_surface)


# Selector Outline surface
selector_overlay = pg.Surface((tile_width, tile_width))
selector_overlay.fill(WHITE)
pg.draw.rect(selector_overlay, GREEN, [0, 0, tile_width, tile_width], 4)
selector_overlay.set_colorkey(WHITE)


# Red Piece surface
red_piece = pg.Surface((tile_width, tile_width))
red_piece.fill(WHITE)
pg.draw.circle(red_piece, RED, [int(tile_width / 2), int(tile_width / 2)], 25)
red_piece.set_colorkey(WHITE)


# Black Piece surface
black_piece = pg.Surface((tile_width, tile_width))
black_piece.fill(WHITE)
pg.draw.circle(black_piece, BLACK, [int(tile_width / 2), int(tile_width / 2)], 25)
black_piece.set_colorkey(WHITE)


# King surface
king = pg.Surface((tile_width, tile_width))
king.fill(WHITE)
pg.draw.circle(king, YELLOW, [int(tile_width / 2), int(tile_width / 2)], 10)
king.set_colorkey(WHITE)


def CreateBoard(board_piece):
    """
    This Function creates a 10x10 board for the Checkers game.

    The outside ring contains 'X's, while the interior 8x8 is tiled with
    'Piece' objects of the appropriate color, or 'N's, for empty spaces.
    """

    board = [['X' for i in range(10)] for j in range(10)]

    for row in range(1, len(board) - 1):                                        
        if row < 4:                                                             # Black side
            for col in range(1, len(board) - 1):
                if (col + row) % 2 == 1:
                    board[row][col] = board_piece(board_piece.BLACK_PIECE, [row,col])
                else: board[row][col] = 'N'

        elif row > 3 and row < 6:                                               # Middle Area
            for col in range(1, len(board) - 1):
                 board[row][col] = 'N'

        elif row > 5:                                                           # Red Side
            for col in range(1, len(board) - 1):
                    if (col + row) % 2 == 1:
                        board[row][col] = board_piece(board_piece.RED_PIECE, [row,col])
                    else: board[row][col] = 'N'

    return board

def DrawBoard(board):
    """This function draws the board surface, then populates it with pieces in the appropriate locations."""

    screen.blit(board_surface, (0,0))
    for i in range(8):
        for j in range(8):

            if isinstance(board[i+1][j+1], piece_type):
                if board[i+1][j+1].color in ('r','R'):
                    screen.blit(red_piece, (j*tile_width, i*tile_width))
                    if board[i+1][j+1].color == 'R':
                        screen.blit(king, (j*tile_width, i*tile_width))

                elif board[i+1][j+1].color in ('b','B'):
                    screen.blit(black_piece, (j*tile_width, i*tile_width))
                    if board[i+1][j+1].color == 'B':
                        screen.blit(king, (j*tile_width, i*tile_width))

    pg.display.flip()

def SwitchColor(color):
    """This function is used to change teams."""

    if color == 'r':
        return 'b'
    elif color == 'b':
        return 'r'

def AITurn(color, board):
    """This function performs the AI's turn, checking for and making jumps or moves, then drawing the board."""

    time.sleep(2)
    jumps = Piece.ScoreAllJumps(color, board)
    if jumps != []:
        next_move = Piece.ChooseMoveOrJump(jumps)
        Piece.DoJump(next_move[0], next_move[1], board)

        jump_again = True
        while jump_again:                                                       # This section checks for double/triple jumps. It's a bit weird, try to clean up.
            DrawBoard(board)
            time.sleep(1)
            multi_jump = Piece.MultipleJumps(next_move[0], board)
            if not multi_jump:
                jump_again = False
    else:
        moves = Piece.ScoreAllMoves(color, board)
        if moves != []:
            next_move = Piece.ChooseMoveOrJump(moves)
            Piece.DoMove(next_move[0], next_move[1], board)
    Piece.CreateKings(board)
    DrawBoard(board)

def GetTileSelection(board):
    pg.event.clear()
    while True:
        event = pg.event.wait()

        if event.type == pg.QUIT:
            pg.quit()
            quit()
        # Get Piece selection
        elif event.type == pg.MOUSEBUTTONDOWN:
            mouse_pos = pg.mouse.get_pos()
            square_pos = (int(mouse_pos[0] / tile_width) + 1, int(mouse_pos[1] / tile_width) + 1)

            selected_piece = board[square_pos[1]][square_pos[0]]
            return selected_piece, square_pos

def PlayerTurn(color, board):
    """This function handles the player's input to the game."""

    jumps = Piece.GetAllJumps(Piece.pieces[Piece.SameColor(color)], board)
    if jumps == []:
        moves = Piece.GetAllMoves(Piece.pieces[Piece.SameColor(color)], board)
    else: moves = []

    step1 = False
    while not step1:
        selected_piece1, square_pos1 = GetTileSelection(board)
        # Check if the player has selected one of their own pieces.
        if isinstance(selected_piece1, piece_type):
            if selected_piece1.color in Piece.SameColor(color):
                screen.blit(selector_overlay, [(square_pos1[0] - 1) * tile_width, (square_pos1[1] - 1) * (tile_width)])
                pg.display.flip()
                step1 = True

        if step1:

            step2 = False
            move_allowed = True

            while not step2:
                selected_piece2, square_pos2 = GetTileSelection(board)
                # If they choose another piece
                if isinstance(selected_piece2, piece_type):
                    # If they select the original piece, deselect it, and let them choose another.
                    if selected_piece2 == selected_piece1 and move_allowed:
                        DrawBoard(board)
                        step2 = True
                        step1 = False

                    # If they select an enemy piece, check if it can be jumped. If so, do it.
                    elif selected_piece2.color in Piece.OtherColor(color):
                        jump = (square_pos2[1] - square_pos1[1], square_pos2[0] - square_pos1[0])
                        jumps = list(filter(lambda x: x[0] == selected_piece1, Piece.GetAllJumps(Piece.pieces[Piece.SameColor(color)], board)))
                        for j in jumps:
                            if jump == j[1] and selected_piece1 == j[0]:
                                Piece.DoJump(selected_piece1, jump, board)
                                DrawBoard(board)
                                step2 = True
                        # Handle double jumping
                        if Piece.IsJump(selected_piece1, board)[1] != []:
                            step2 = False
                            move_allowed = False
                            square_pos1 = (selected_piece1.pos[1], selected_piece1.pos[0])
                            screen.blit(selector_overlay, [(square_pos1[0] - 1) * tile_width, (square_pos1[1] - 1) * (tile_width)])
                            pg.display.flip()

                # If they selected to move to an empty square, check if it is a valid move. If so, do it.
                elif selected_piece2 == 'N' and move_allowed:
                    move = (square_pos2[1] - square_pos1[1], square_pos2[0] - square_pos1[0])

                    for m in moves:
                        if move == m[1] and selected_piece1 == m[0]:
                            Piece.DoMove(selected_piece1, move, board)
                            DrawBoard(board)
                            step2 = True
