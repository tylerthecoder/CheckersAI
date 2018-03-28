#================================
# Name: Checking Simulator
# Author: Tyler Tracy
# Purpose: To simulate the game of checkers and to make it easier for an AI to play
#================================
import sys
import drawing
from board import Board, Move

sys.path.insert(0, '/AI')
import AI.tgt_AI, AI.rand_AI

mainWindow = drawing.Window((600,600))
grid = Board("Standard")

#==============================================
#            Player Function
#==============================================

selected = (-1,-1) #this stores the value of the grid square that is currently selected
def HumanPlayer(grid):
    global selected

    if not mainWindow.isClick():
        #user didn't click anything 
        return False

    click = mainWindow.getClickedSquare()

    #if you click the piece that you already selected, then unselect
    if selected == click:
        selected = (-1,-1)

    #if you click your piece, then select it
    elif grid.board[click].color == grid.turn:
        selected = click
    
    #try to play
    else:
        move = Move(selected,click,grid)
        res = grid.checkMove(move)
        if res["valid"]: #if the move was sucsessful
            return move
        else:
            print(res["error"])
            return False
    

#=============================================
#           Main Program Loop
#=============================================
done = False
while not done:
    done = mainWindow.isQuit() #did they click the exit button?


    move = False

    if grid.turn == "r":
        # move = AI.rand_AI.AIPlayer(grid,"r")
        move = HumanPlayer(grid)  

    elif grid.turn == "b":
        move = AI.tgt_AI.AIPlayer(grid,"b")
    
    #Make the move
    if move:
        result = grid.applyMove(move)
        if result:
            #reset the player selection
            selected = (-1,-1)
    


    mainWindow.draw(grid,selected)
 
    mainWindow.tick() #Go to the next frame
 
# Close the window and quit.
mainWindow.QuitGame()