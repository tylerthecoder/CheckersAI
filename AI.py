# This File contains the AI for CheckersV2.py. The AI for this program is a
# weighted-random decision making algorithm based off an array of board-position scores.
import random
from BoardFunctions import OnBoard

class AI:

    PIECE_VALUE = 16                                                            # TODO: Subject to change -- needs balancing
    KING_VALUE = 90

    # Score array for red pieces
    SCORE_ARRAY_1 = [['X','X','X','X','X','X','X','X','X','X'],
                     ['X', 66, 67, 68, 69, 69, 68, 67, 66,'X'],                 # TODO: This array is very much subject to change -- needs balancing.
                     ['X', 52, 53, 54, 55, 55, 54, 53, 52,'X'],
                     ['X', 40, 41, 42, 43, 43, 42, 41, 40,'X'],
                     ['X', 30, 31, 32, 33, 33, 32, 31, 30,'X'],
                     ['X', 22, 23, 24, 25, 25, 24, 23, 22,'X'],
                     ['X', 16, 17, 18, 19, 19, 18, 17, 16,'X'],
                     ['X', 12, 13, 14, 15, 15, 14, 13, 12,'X'],
                     ['X', 10, 11, 12, 13, 13, 12, 11, 10,'X'],
                     ['X','X','X','X','X','X','X','X','X','X']]

    # Score array for black pieces
    SCORE_ARRAY_2 = list(reversed(SCORE_ARRAY_1))                               # score_array_1 upside down

    def ValuatePiece(color, pos):
        """This function sets the score for a single piece.

        It is passed the type (color char) and position (list) of a piece, and returns its point-value, as determined by the score array for its color."""

        try:
            if color == 'r':
                score = AI.PIECE_VALUE + AI.SCORE_ARRAY_1[pos[0]][pos[1]]
            elif color == 'b':
                score = AI.PIECE_VALUE + AI.SCORE_ARRAY_2[pos[0]][pos[1]]
            elif color == 'R':
                score = AI.KING_VALUE                                           # Board position doesn't matter as much for kings -- their job is to jump other pieces.
            elif color == 'B':
                score = AI.KING_VALUE
        except TypeError:
            print('Error: Tried to evaluate the score of a piece off the edge of the board.')
            score = 0

        return score





# DEBUG==================
#
#========================
