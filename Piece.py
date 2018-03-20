import random

class Piece:
    pieces = {('r', 'R') : [],
              ('b', 'B') : []}

    # Moves
    MOVE_LIST = {'r' : ((-1, 1), (-1, -1)),
                 'b' : ((1, 1), (1, -1)),
                 'R' : ((-1, 1), (-1, -1), (1, 1), (1, -1)),
                 'B' : ((-1, 1), (-1, -1), (1, 1), (1, -1))}


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

    #Score Weights
    EASY = (1, 1, 1, 1)                                                         # These weights may be used to further weight the decision-making process to favor better moves over worse ones, if deemed necessary.
    MEDIUM = (1.5, 1.0, 0.75, 0.5)
    HARD = (2.5, 1.5, 1.0, 0.5)

                                                    
    def __init__(self, color, pos):
        self.color = color
        self.pos = pos
        self.jumped = False

        if self.color == 'r':                                                   #A Normal Red Piece
            self.moves = Piece.MOVE_LIST[self.color]
            Piece.pieces[('r','R')].append(self)

        elif self.color == 'b':                                                 #A Normal Black Piece
            self.moves = Piece.MOVE_LIST[self.color]
            Piece.pieces[('b','B')].append(self)

        else: print("Not a valid color for a piece.")

    def RemovePiece(self, board):
        """Deletes a piece from the board and list of pieces."""

        board[self.pos[0]][self.pos[1]] = 'N'
        self.jumped = True                                                      # Don't actually delete the object, because it may be needed in the UndoJump() function.
                                                                                # Instead, it is tagged as 'jumped', which will be checked by Done().
        return board

    def SameColor(color):
        """This function returns a tuple containing the same colors of the piece passed as an argument."""

        if color in ('r', 'R'):
            return ('r', 'R')
        elif color in ('b','B'):
            return ('b','B')

    def OtherColor(color):
        """This Function returns a tuple containing the opposite colors of the piece passed as an argument."""

        if color in ('r', 'R'):
            return ('b', 'B')
        elif color in ('b','B'):
            return ('r','R')

    def IsJump(self, board):
        """This Function recieves a piece on the board as an argument, and checks for possible jumps."""

        valid_jumps = []
        for move in self.moves:
            jumped_pos = (self.pos[0] + move[0], self.pos[1] + move[1])
            new_pos = (self.pos[0] + 2 * move[0], self.pos[1] + 2 * move[1])

            if board[jumped_pos[0]][jumped_pos[1]] in ('X','N'):
                continue
            elif (board[jumped_pos[0]][jumped_pos[1]].color in Piece.OtherColor(self.color)) and (board[new_pos[0]][new_pos[1]] == 'N'):
                valid_jumps.append(move)


        return (self, valid_jumps)

    def GetAllJumps(piece_list, board):
        """This function tests each piece on the board of a given color for available jumps.

         Returns a list of pieces with available jumps, and which direction(s) they can jump."""

        all_jumps = []
        for piece in piece_list:
            jumps = Piece.IsJump(piece, board)
            if jumps[1] != []:
                for jump in jumps[1]:
                    all_jumps.append( (piece, jump) )

        return all_jumps

    def DoJump(self, jump, board):
        """ This Function is used to perform a jump.

        It moves the jumping piece to its new position, and deletes the jumped piece.
        The jump is passed as a 1-square diagonal move, but is performed as a 2-square move in the same direction.
        This function should only be used on jumps identified by IsJump, as it does not do any checking to see if a jump is valid."""

        board[self.pos[0]][self.pos[1]] = 'N'                                   # Free spot left by jumping piece
        jumped_piece = board[self.pos[0] + jump[0]][self.pos[1] + jump[1]]      # Identify piece being jumped

        Piece.RemovePiece(jumped_piece, board)

        self.pos[0] += 2 * jump[0]                                              # Set new position for jumping piece.
        self.pos[1] += 2 * jump[1]
        board[self.pos[0]][self.pos[1]] = self

        return board

    def UndoJump(self, jump, board):                                            # Right now, this and the UndoMove function are necessary to test moves. Ideally, we should be able to test moves/jumps without modifying and undoing changes to the board.
        """This function does the opposite of the DoJump function.

        It returns the board to its original state, before the given jump was performed."""

        board[self.pos[0]][self.pos[1]] = 'N'
        self.pos[0] += 2 * jump[0]                                              # Set new position for jumping piece.
        self.pos[1] += 2 * jump[1]
        board[self.pos[0]][self.pos[1]] = self

        jumped_pos = [self.pos[0] + jump[0], self.pos[1] + jump[1]]
        for piece in pieces[OtherColor(self.color)]:
            if piece.pos == jumped_pos:
                board[jumped_pos[0]][jumped_pos[1]] = piece
                piece.jumped = False

        return board

    def IsMove(self, board):
        """
        This Function recieves a piece on the board as an argument, and checks for possible moves.

        This should be run AFTER IsJump, and only if IsJump[1] returns [] for all pieces, since players must jump if possible.
        """

        valid_moves = []
        for move in self.moves:                                                 # TODO: Create function for this part? Will be repeated many times.
            new_pos = (self.pos[0] + move[0], self.pos[1] + move[1])
            if board[new_pos[0]][new_pos[1]] == 'N':
                valid_moves.append(move)

        return (self,valid_moves)

    def GetAllMoves(piece_list, board):
        """This function tests each piece on the board of a given color for available moves.

        Returns a list of pieces with available moves, and which direction(s) they can move."""

        all_moves = []
        for piece in piece_list:
            moves = Piece.IsMove(piece, board)
            if moves[1] != []:
                for move in moves[1]:
                    all_moves.append( (piece, move) )

        return all_moves

    def DoMove(self, move, board):
        """This Function is used to move a piece to an empty square.

        It moves the piece on the board, then replaces the old location with an empty space, 'N'.
        This function should only be used for moves identified with IsMove, as it does not check to see if a move is valid."""

        board[self.pos[0]][self.pos[1]] = 'N'                                   # Clear old board position
        self.pos[0] += move[0]                                                  # Reassign piece positions
        self.pos[1] += move[1]
        board[self.pos[0]][self.pos[1]] = self                                  # Move piece to new position on board

        return board

    def UndoMove(self, move, board):
        """This function does the opposite of the DoMove function.

        It returns the board to its original state, before the given move was performed."""

        board[self.pos[0]][self.pos[1]] = 'N'
        self.pos[0] -= move[0]
        self.pos[1] -= move[1]
        board[self.pos[0]][self.pos[1]] = self

        return board

    def Jumpable(self, board):                                                  # TODO: Modify to check if a king can jump the piece.
        """This function tests to see if a given piece can be jumped by another piece.

        While technically a part of the AI, this function is placed here because it requires easy access to variables in Piece."""

        for move in Piece.MOVE_LIST['R']:                                       # Just checking all diagonals, could use either king color.
            diagonal_piece = board[self.pos[0] - move[0]][self.pos[1] - move[1]]
            if diagonal_piece in Piece.pieces[Piece.OtherColor(self.color)]:
                if move in Piece.MOVE_LIST[diagonal_piece.color]:
                    return True

        return False

    def King(self):
        """This function changes a normal piece into a kinged piece, updating its color label and moves."""

        self.color = self.color.upper()
        self.moves = Piece.MOVE_LIST[self.color]
        return self

    def CreateKings(board):
        """This function checks each end of the board for pieces of the opposite color.

        If a piece is at the opposing color's end and is not already a king, they are kinged.
        This function should be run at the end of every turn."""

        for p in board[1][1:9]:
            if p == 'N':
                continue
            elif p.color == 'r':
                Piece.King(p)

        for p in board[8][1:9]:
            if p == 'N':
                continue
            elif p.color == 'b':
                Piece.King(p)

        return board

    def Done(max_moves = 50):
        """
        This Function checks the number of remaining pieces for each team.

        It also checks the number of moves made total by both players.
        If either player runs out of pieces, or more than 50 moves are made, the game ends.
        """
        move_count = 0
        done = False

        while not done:
            move_count += 1
            if all(Piece.pieces[('r','R')].jumped):
                done = True
                print('Black Team Wins!')
            elif all(Piece.pieces[('b','B')].jumped):
                done = True
                print('Red Team Wins!')
            elif move_count >= max_moves:
                done = True
                print('Too many moves! The game is a draw!')

            yield done

# FROM AI, KEEP HERE, OR MOVE? =================================================

    def ValuatePiece(self, board):
        """This function sets the score for a single piece.

        It is passed the piece to check, and returns its point-value, as determined by the score array for its color."""
        pos = self.pos
        color = self.color

        if color == 'r':
            score = Piece.PIECE_VALUE + Piece.SCORE_ARRAY_1[pos[0]][pos[1]]
        elif color == 'b':
            score = Piece.PIECE_VALUE + Piece.SCORE_ARRAY_2[pos[0]][pos[1]]
        elif color == 'R':
            score = Piece.KING_VALUE                                            # Board position doesn't matter as much for kings -- their job is to jump other pieces.
        elif color == 'B':
            score = Piece.KING_VALUE

        if Piece.Jumpable(self, board):                                         # TODO: Currently, this reduces the value of any piece that can be jumped.
            score = score // 2                                                  #       This is fine when one side is evaluating its own pieces, but it also reduces the value of jumping the other team's pieces.

        return score

    def GetTeamScore(piece_list):
        """This function calls the ValuatePiece function on each of a team's pieces, and returns the sum of all scores."""

        total = 0
        for piece in piece_list:
            total += Piece.ValuatePiece(piece)
        return total

    def MoveScoring(self, move, board):
        """This function calculates how much a team's score will change if it makes a given move.

        It returns a tuple containing (piece_moved, move_made, score_change)."""

        init_score = Piece.ValuatePiece(self, board)

        board_after_move = Piece.DoMove(self, move, board)

        final_score = Piece.ValuatePiece(self, board)

        score_dif = final_score - init_score

        Piece.UndoMove(self, move, board)

        return (self, move, score_dif)

    def ScoreAllMoves(color, board):
        """This function calculates a score for all possible moves, and returns a list of the 4 best."""

        move_scores = []
        move_list = Piece.GetAllMoves(Piece.pieces[Piece.SameColor(color)], board)

        for move in move_list:
            move_scores.append(Piece.MoveScoring(move[0], move[1], board))

        move_scores = sorted(move_scores, key=lambda x: x[2], reverse=True)[:4]

        return move_scores

    def JumpScoring(self, jump, other_piece_list, board):
        """This function calculates the total relative change in scores between both teams if a given jump is made.

        Score differential is calculated as (jumping_team_score_change) - (jumped_team_score_change).
        Returns a tuple containing (self, jump_made, score_change)."""

        piece_init_score = Piece.ValuatePiece(self, board)
        other_team_init_score = Piece.GetTeamScore(other_piece_list)

        board_after_move = Piece.DoJump(self, jump, board) # Similar to above, this changes the actual board. Not ideal.

        piece_final_score = Piece.ValuatePiece(self, board)
        other_team_final_score = Piece.GetTeamScore(other_piece_list)

        score_dif = (piece_final_score - piece_init_score) - (other_team_final_score - other_team_init_score)

        Piece.UndoJump(self, jump, board)

        return (self, jump, score_dif)

    def ScoreAllJumps(color, board):
        """This function calculates a score for all possible jumps, and returns a list of the 4 best."""

        jump_scores = []
        jump_list = GetAllJumps(Piece.pieces[Piece.SameColor(color)], board)
        other_piece_list = Piece.pieces[Piece.OtherColor(color)]

        for jump in jump_list:
            jump_scores.append(Piece.JumpScoring(jump[0], jump[1], other_piece_list, board))

        jump_scores = sorted(jump_scores, key=lambda x: x[2], reverse=True)[:4]

        return jump_scores

    def ChooseMoveOrJump(options, difficulty=EASY):
        weighted_scores = [m[2]*w for m, w in zip(options, difficulty)]              # m[2] is the score of the move in options.

        s = sum(weighted_scores)

        norms = list(map(lambda x: x/s, weighted_scores))

        choice = random.random()

        if choice <= norms[0]:
            move = options[0]

        elif choice <= sum(norms[:2]):
            move = options[1]

        elif choice <= sum(norms[:3]):
            move = options[2]

        elif choice <= sum(norms[:4]):
            move = options[3]

        else: move = options[0]                                                 # Just in case, default to best move.

        return move
