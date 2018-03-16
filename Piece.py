class Piece:
    pieces = {('r','R') : [],                                                   # it may be helpful to store pieces in a dictionary (e.g. {('r','R') : [pieces], ('b','B') : [pieces]} ), as this would allow direct access using OtherColor().
              ('b','B') : []}                                                   # These dictionaries may also be able to have keys of just one character.

    # Moves
    NK_MOVES_R = ((-1, 1), (-1, -1))                                            # Moves for non-king red pieces
    NK_MOVES_B = ((1, 1), (1, -1))                                              # Moves for non-king black pieces
    K_MOVES = ((-1, 1), (-1, -1), (1, 1), (1, -1))                              # Moves for all kinged pieces
    

    def __init__(self, color, pos):
        self.color = color
        self.pos = pos
        self.jumped = False

        if self.color == 'r':                                                   #A Normal Red Piece
            self.moves = Piece.NK_MOVES_R
            Piece.pieces[('r','R')].append(self)

        elif self.color == 'b':                                                 #A Normal Black Piece
            self.moves = Piece.NK_MOVES_B
            Piece.pieces[('b','B')].append(self)

        else: print("Not a valid color for a piece.")

    def RemovePiece(self, board):
        """Deletes a piece from the board and list of pieces."""

        board[self.pos[0]][self.pos[1]] = 'N'
        self.jumped = True                                                      # Don't actually delete the object, because it may be needed in the UndoJump() function.
                                                                                # Instead, it is tagged as 'jumped', which will be checked by Done().
        return board

    def OtherColor(self):
        """This Function returns a tuple containing the opposite colors of the piece passed as an argument."""

        if self.color in ('r', 'R'):
            return ('b','B')
        elif self.color in ('b','B'):
            return ('r','R')

    def IsJump(self, board):
        """This Function recieves a piece on the board as an argument, and checks for possible jumps."""

        valid_jumps = []
        for move in self.moves:                                                # TODO: does not check if next square is open for the piece to move to after jumping.
            jumped_pos = (self.pos[0] + move[0], self.pos[1] + move[1])
            new_pos = (self.pos[0] + 2 * move[0], self.pos[1] + 2 * move[1])

            if board[jumped_pos[0]][jumped_pos[1]] in ('X','N'):
                continue
            elif (board[jumped_pos[0]][jumped_pos[1]].color in Piece.OtherColor(self)) and (board[new_pos[0]][new_pos[1]] == 'N'):
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
        for move in self.moves:                                                #TODO: Create function for this part? Will be repeated many times.
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


    def King(self):
        """This function changes a normal piece into a kinged piece, updating its color label and moves."""

        self.color = self.color.upper()
        self.moves = Piece.K_MOVES
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
