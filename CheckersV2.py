# A Rewritten version (work in progress) of the Checkers game written by Tyler Tracy.
# This 'Version 2' aims to structure the code for separation into files, and allow for simpler AI integration.

import BoardFunctions as bf
import Piece as p


BOARD = bf.CreateBoard()
done = p.Piece.Done()
d = next(done)

bf.DrawBoard(BOARD)


color = 'r'
while not d:
    bf.AITurn(color, BOARD)
    color = bf.SwitchColor(color)
    d = next(done)

    bf.PlayerTurn(color, BOARD)
    d = next(done)
    color = bf.SwitchColor(color)
