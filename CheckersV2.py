# A Rewritten version (work in progress) of the Checkers game written by Tyler Tracy.
# This 'Version 2' aims to structure the code for separation into files, and allow for simpler AI integration.

import math
import pygame as pg
import random
import BoardFunctions as bf
from Piece import *
import time

BOARD = bf.CreateBoard()
done = Piece.Done()
d = next(done)

bf.DrawBoard(BOARD)


color = 'r'
while not d:
    time.sleep(2)
    jumps = Piece.ScoreAllJumps(color, BOARD)
    if jumps != []:
        next_move = Piece.ChooseMoveOrJump(jumps, Piece.HARD)
        Piece.DoJump(next_move[0], next_move[1], BOARD)

        jump_again = True
        while jump_again:                                                       # This section checks for double/triple jumps. It's a bit weird, try to clean up.
            bf.DrawBoard(BOARD)
            time.sleep(1)
            multi_jump = Piece.MultipleJumps(next_move[0], BOARD)
            if not multi_jump:
                jump_again = False
    else:
        moves = Piece.ScoreAllMoves(color, BOARD)
        if moves != []:
            next_move = Piece.ChooseMoveOrJump(moves, Piece.HARD)
            Piece.DoMove(next_move[0], next_move[1], BOARD)
    Piece.CreateKings(BOARD)
    bf.DrawBoard(BOARD)
    d = next(done)
    if color == 'r':
        color = 'b'
    else: color = 'r'
input()
