from Piece import Piece

def OnBoard(pos, board):                                                        # TODO: Not sure how/if I want to utilize this function. It may create some strange dependencies.
    """This function returns the value of the provided position on whatever board is passed as an argument.

    The position is passed as a list or tuple."""

    return board[pos[0]][pos[1]]



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
