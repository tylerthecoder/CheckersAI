#================================
# Name: Checking Simulator
# Author: Tyler Tracy
# Purpose: To simulate the game of checkers and to make it easier for an AI to play
#================================
import sys, drawing, copy
sys.path.insert(0, '/AI')
from board import Board, Move, CopyBoard
import AI.tgt_AI, AI.rand_AI, AI.human

import pdb

mainWindow = drawing.Window((600,600))
grid = Board("Standard")
grid.window = mainWindow

Player1 = AI.human
Player2 = AI.tgt_AI


gameOver = False
mainWindow.draw(grid)


grid.printP()
newBoard = CopyBoard(grid)
grid.printP()
newBoard.printP()


pdb.set_trace()

# pdb.set_trace()

while not gameOver:

    
    mainWindow.draw(grid)
    #copyBoard = Board("Copy",grid)
    if grid.turn == "r":
        move = Player1.play(grid)  
    elif grid.turn == "b":
        move = Player2.play(grid)
    
    #Make the move
    grid.printP()
    if move:
        result = grid.applyMove(move,True)

 
# Close the window and quit.
mainWindow.QuitGame()