# This File contains the AI for CheckersV2.py. The AI for this program is a
# weighted-random decision making algorithm based off an array of board-position scores.
import random
from Piece import Piece

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

    def GetTeamScore(piece_list):
        """This function calls the ValuatePiece function on each of a team's pieces, and returns the sum of all scores."""

        total = 0
        for piece in piece_list:
            total += AI.ValuatePiece(piece.color, piece.pos)
        return total

    def MoveScoring(moving_piece, move, current_piece_list, board):
        """This function calculates how much a team's score will change if it makes a given move.

        It returns a tuple containing (piece_moved, move_made, score_change)."""

        current_team_init_score = AI.GetTeamScore(current_piece_list)

        board_after_move = Piece.DoMove(moving_piece, move, board) # This won't work. It changes the actual board.

        current_team_final_score = AI.GetTeamScore(current_piece_list)

        score_dif = current_team_final_score - current_team_init_score

        Piece.UndoMove(moving_piece, move, board)

        return (moving_piece, move, score_dif)

    def JumpScoring(jumping_piece, jump, current_piece_list, other_piece_list, board):
        """This function calculates the total relative change in scores between both teams if a given jump is made.

        Score differential is calculated as (jumping_team_score_change) - (jumped_team_score_change).
        Returns a tuple containing (jumping_piece, jump_made, score_change)."""

        current_team_init_score = AI.GetTeamScore(current_piece_list)
        other_team_init_score = AI.GetTeamScore(other_piece_list)

        board_after_move = Piece.DoJump(jumping_piece, jump, board) # Similar to above, this changes the actual board. Not ideal.

        current_team_final_score = AI.GetTeamScore(current_piece_list)
        other_team_final_score = AI.GetTeamScore(other_piece_list)

        score_dif = (current_team_final_score - current_team_init_score) - (other_team_final_score - other_team_init_score)

        Piece.UndoJump(jumping_piece, jump, board)

        return (jumping_piece, jump, score_dif)

"""
AI Steps:
1) Get all possible jumps
    1a) if none, get all possible moves
2) Get score for each team, based on current board state
3) Try each move (by making local copy of board inside a function?) and get score difference (AI newtotal - player newtotal) if made.
    This could be challenging, as it needs to be done without altering the board, ideally.
4) store 4 best moves somewhere (best move == highest score difference after making the move)
5) choose a move (semi-random: probability based on how good the move is)
6) do the move
7) if another jump(s) can be made, do that.
8) end turn
"""

# DEBUG==================
#
#========================
