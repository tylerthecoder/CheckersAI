# A Rewritten version (work in progress) of the Checkers game written by Tyler Tracy.
# This 'Version 2' aims to structure the code for separation into files, and allow for simpler AI integration.

import pygame
import random
from BoardFunctions import CreateBoard
from Piece import Piece


#Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

# Move counter
done = Piece.Done()




#DEBUG ============================
BOARD = CreateBoard()
moves = Piece.GetAllMoves(Piece.pieces[('r','R')], BOARD)
# for move in moves:
    # print(AI.MoveScoring(move[0], move[1], Piece.pieces[('r','R')], BOARD))

print(Piece.ValuatePiece(moves[0][0], BOARD))
Piece.DoMove(moves[0][0], moves[0][1], BOARD)

moves = Piece.GetAllMoves(Piece.pieces[('r','R')], BOARD)

# for move in moves:
#     print(AI.MoveScoring(move[0], move[1], Piece.pieces[('r','R')], BOARD))
print(Piece.ValuatePiece(moves[0][0], BOARD))
Piece.DoMove(moves[0][0], moves[0][1], BOARD)

print(Piece.Jumpable(moves[0][0], BOARD))
print(Piece.ValuatePiece(moves[0][0], BOARD))

# for row in BOARD:
#     print(row)

# SCORE = 0
# for p in Piece.pieces[('b','B')]:
#     SCORE += AI.ValuatePiece(p.color, p.pos)
# print(SCORE)

#==================================

# while not done:
#     #pygame.init()
#     next(done)                                                                  # Checks if either team has won, and increments move counter.
#
