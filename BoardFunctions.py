from Piece import Piece
import pygame as pg

#Colors -- Not using all of them currently, TODO: Remove extraneous colors. Probably will move back to main program.
BLACK = (0, 0, 0)
DARK_BROWN = (140, 100, 20)
LIGHT_BROWN = (220, 190, 130)

WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)


clock = pg.time.Clock()
clock.tick(30)

size = (700,700)
screen = pg.display.set_mode(size)
pg.display.set_caption("Checkers")
pg.init()

tile_width = size[0] / 8


def CreateBoard():
    """
    This Function creates a 10x10 board for the Checkers game.

    The outside ring contains 'X's, while the interior 8x8 is tiled with
    'Piece' objects of the appropriate color, or 'N's, for empty spaces.
    """

    board = [['X' for i in range(10)] for j in range(10)]                       # TODO: Improve board creation efficiency, if possible.
                                                                                # TODO: Modify to not specifically declare 'Piece' objects as game pieces.
    for row in range(1, len(board) - 1):                                        #       Can be done with eval(), but using eval() is generally considered bad practice
        if row < 4:                                                             # Black side
            for col in range(1, len(board) - 1):
                if (col + row) % 2 == 1:
                    board[row][col] = Piece('b', [row,col])
                else: board[row][col] = 'N'

        elif row > 3 and row < 6:                                               # Middle Area
            for col in range(1, len(board) - 1):
                 board[row][col] = 'N'

        elif row > 5:                                                           # Red Side
            for col in range(1, len(board) - 1):
                    if (col + row) % 2 == 1:
                        board[row][col] = Piece('r', [row,col])
                    else: board[row][col] = 'N'

    return board

def DrawBoard(board, screen=screen, tile_width=tile_width, ground_color=DARK_BROWN, tile_color=LIGHT_BROWN, line_color=BLACK, piece1=RED, piece2=BLACK, king_color=YELLOW, piece_type=Piece):
    pg.Surface.lock(screen)
    screen.fill((ground_color))

    #Create Tiles
    for i in range(8):
        for j in range(8):
            if (i + j) % 2 == 0:
                pg.draw.rect(screen, tile_color, [j*tile_width, i*tile_width, tile_width, tile_width], 0)

    # Draw Tile Outlines
    for i in range(8):
        pg.draw.line(screen, line_color, [i*tile_width, 0], [i*tile_width, size[1]], 4)
        for j in range(8):
            pg.draw.line(screen, line_color, [0, j*tile_width], [700, j*tile_width], 4)
    pg.draw.line(screen, line_color, [size[0] - 3, 0], [size[0] - 3, size[1]], 4)
    pg.draw.line(screen, line_color, [0, size[1] - 3], [size[0], size[1] - 3], 4)

    #Draw pieces
    for i in range(8):
        for j in range(8):
            if isinstance(board[i+1][j+1], piece_type):
                if board[i+1][j+1].color in ('r','R'):
                    pg.draw.circle(screen, piece1, [int(j*tile_width + (tile_width / 2)), int(i*tile_width + (tile_width / 2))], 25)
                    if board[i+1][j+1].color == 'R':
                        pg.draw.circle(screen, king_color, [int(j*tile_width + (tile_width / 2)), int(i*tile_width + (tile_width / 2))], 10)
                elif board[i+1][j+1].color in ('b','B'):
                    pg.draw.circle(screen, piece2, [int(j*tile_width + (tile_width / 2)), int(i*tile_width + (tile_width / 2))], 25)
                    if board[i+1][j+1].color == 'B':
                        pg.draw.circle(screen, king_color, [int(j*tile_width + (tile_width / 2)), int(i*tile_width + (tile_width / 2))], 10)
    pg.Surface.unlock(screen)
    pg.display.flip()
