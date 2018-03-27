#================================
# Name: Checking Simulator
# Author: Tyler Tracy
# Purpose: To simulate the game of checkers and to make it easier for an AI to play
#================================
import drawing
import tgt_AI
from board import Board, Move

mainWindow = drawing.Window()
grid = Board("Standard")

#==============================================
#            Player Function
#==============================================

selected = (-1,-1) #this stores the value of the grid square that is currently selected
def HumanPlayer(click):
    global selected
    if selected == (-1,-1):
        if grid.board[click].color == grid.turn:
            selected = click
        else:
            print("Wrong Turn")
    elif selected == click:
        selected = (-1,-1)
    else:
        move = Move(selected,clickedSquare,grid)
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

    if mainWindow.isClick(): #did they click the grid

        #check where click happened;
        clickedSquare = mainWindow.getClickedSquare()
        
        #call player functions
        if grid.turn == "r":
            move = HumanPlayer(clickedSquare)
        elif grid.turn == "b":
            move = tgt_AI.AIPlayer(grid,"b")
        
        #            Make Move
        #==================================
        if move:
            result = grid.applyMove(move)
            if result:
                selected = (-1,-1)
    
    mainWindow.draw(grid,selected)
 
    mainWindow.tick() #Go to the next frame
 
# Close the window and quit.
mainWindow.QuitGame()