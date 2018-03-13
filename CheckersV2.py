# A Rewritten version (work in progress) of the Checkers game written by Tyler Tracy.
# This 'Version 2' aims to structure the code for separation into files, and allow for simpler AI integration.

import pygame
import random
from BoardFunctions import CreateBoard, OnBoard, Done
from AI import AI
from Piece import Piece


#Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

# Move counter
game_status = Done(Piece.red_pieces, Piece.black_pieces)                       # Basically what the move counter will look like.
done = False






#DEBUG ============================
BOARD = CreateBoard()
moves = Piece.GetAllMoves(Piece.red_pieces, BOARD)
for move in moves:
    print(move)
#
for row in BOARD:
    print(row)

# SCORE = 0
# for p in Piece.black_pieces:
#     SCORE += AI.ValuatePiece(p.color, p.pos)
# print(SCORE)

# for row in BOARD:
#     print(row)
#==================================

# while not done:
#     #pygame.init()
#     if next(game_status):
#         done = True
