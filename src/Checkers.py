#================================
# Name: Checking Simulator
# Author: Tyler Tracy
# Purpose: To simulate the game of checkers and to make it easier for an AI to play
#================================
import sys, drawing
sys.path.insert(0, '/AI')
from board import Board
import AI.tgt_AI, AI.rand_AI, AI.human, AI.tgt2

mainWindow = drawing.Window((600,600))
grid = Board()
grid.window = mainWindow

Player1 = AI.human
Player2 = AI.human


#This is my version

#main loop
while not grid.isGameOver()[0]:

    mainWindow.draw(grid)

    if grid.turn == "r":
        move = Player1.play(grid)
    elif grid.turn == "b":
        move = Player2.play(grid)

    #Make the move
    if move:
        result = grid.applyMove(move)



if grid.isGameOver()[1] == "r":
    print("Black won the game")
elif grid.isGameOver()[1] == "b":
    print("Red won the game")

# Close the window and quit.
mainWindow.QuitGame()
