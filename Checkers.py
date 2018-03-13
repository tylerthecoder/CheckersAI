#================================
# Name: Checking Simulator
# Author: Tyler Tracy
# Purpose: To simulate the game of checkers and to make it easier for an AI to play
#================================

import pygame
import math
 
#Define some colors
black = (0, 0, 0)
yellow = (255, 255, 0)
green = (0, 255, 0)
red = (255, 0, 0)
white = (255,255,255)

pygame.init()
    
# Set the width and height of the screen [width, height]
size = (700, 700)
squareLength = math.floor(size[0]/8)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Checkers")    

#creating the grid array

grid = {}
for col in range(8):
    for row in range(8):
        if col < 3 and (row+col)%2 == 0: #check if (row,col) is in the checker diagonal
            char = "R" #set the square to be red
        elif col > 4 and (row+col)%2 == 0:
            char = "b" #set the square to be black
        else:
            char = "N" #set the square to be empty
        
        grid[(row,col)] = char
        # grid[(row,col)] = "N"

# grid[(4,4)] = "R"
# grid[(0,0)] = "R"
# grid[(3,3)] = "b"

clock = pygame.time.Clock() # Used to manage how fast the screen updates
selected = (-1,-1) #this stores the value of the grid square that is currently selected
mousePressed = True #variable to make the mouse click only happen when mouse is clicked up and then down
turn = "r"
done = False

#==============================================
#            Helper Functions
#==============================================

def otherColor(color):
    if color == "r":
        return "b"
    if color == "b":
        return "r"

def isRealSpot(spot):
    if (spot[0] < 0 or spot[0] > 7):
        return False
    elif (spot[1] < 0 or spot[1] > 7):
        return False
    return True
        
#This function was written to not modify any data. 
#This way, when the AI if checking possible moves, it can use this to see the state of the board without altering it
def makeTurn(start,end):
    result = {
        "valid":True,
        "changeTurn":True,
        "error":""
    }
    if grid[start].lower() != turn: #wrong player
        result["valid"] = False
        result["error"] = "Wrong Player"
        return result
    
    #if a jump is aviliable, then you must make it
    #check if there is a jump avaliable
    moves = allPosibleMoves(turn)
    jump = False
    myMove = False
    for move in moves:
        if move["start"] == start and move["end"] == end:
            myMove = move
        if move["jump"]:
            jump = True

    if not myMove:
        return checkMove(start,end)

    if jump and not myMove["jump"]:
        result["valid"] = False
        result["error"] = "You need to jump"
    
    result["spotsToRemove"] = myMove["spotsToRemove"]
    result["drop"] = myMove["drop"]


    #check for double jump
    if myMove["jump"]:
        king = grid[start] == grid[start].upper()
        moves = checkForJump(turn,myMove["drop"],king)
        dj = False
        for move in moves:
            if move["jump"]:
                dj = True
        if dj:
            result["changeTurn"] = False

    return result

def allPosibleMoves (color,onlyJump=False):
    allMoves = []
    jumps = []
    for row in range(8):
        for col in range(8):
            if (grid[(row,col)].lower() == color):
                king = grid[(row,col)] == grid[(row,col)].upper()
                moves = checkForJump(color,(row,col),king)
                for i in moves:
                    allMoves.append(i)
            
    return allMoves

def checkForJump(color,spot,king):
    allMoves = []
    rngi = [-1,1]
    if king:
        rngj = [-1,1]
    elif color == "r":
        rngj = [1]
    elif color == "b":
        rngj = [-1]
    
    for i in rngi:
        for j in rngj:
            check = (spot[0]+i,spot[1]+j)
            oc = otherColor(color)
            #compare spot and check
            res = checkMove(spot,check)
            if res["valid"]:
                allMoves.append(res)
    return allMoves

def checkMove (start,end): 
    #if a jump is aviliable, then you must make it
    result = {}
    result["start"] = start
    result["end"] = end
    result["valid"] = False
    result["jump"] = False

    if (not isRealSpot(start) or not isRealSpot(end)):
        result["error"] = "Not a real spot"
        return result
    
    if (start[0]+start[1])%2 != (end[0]+end[1])%2: #check if they are not diagonal
        result["error"] = "Not on Diagonal"
        return result
    if abs(end[0]-start[0]) > 1: #too far away in the x-dir
        result["error"] = "Too far away in the X direction"
        return result
    
    if grid[start].upper() == grid[start]: #if they are a king
        if (abs(end[1]-start[1]) > 1): #too far away in the y-dir
            result["error"] = "Too far away in the Y direction"
            return result
    else: #if they are not a king
        if (end[1]-start[1] != 1 and grid[start].lower() == "r"):
            result["error"] = "Can't go backwards"
            return result
        elif (end[1]-start[1] != -1 and grid[start].lower() == "b"):
            result["error"] = "Can't go backwards"
            return result
    if grid[end] == grid[start]: #The colors are the same, so you can't play there
        result["error"] = "Can't jump your own Pieces"
        return result

    #this is an array of values that will be replaced with "N", meaning we are deleting the piece in them
    result["spotsToRemove"] = []
    
    if (grid[end] == "N"): #not jumping over piece
        dropSpot = end
    else: #juming over piece
        dropSpot = (2*end[0]-start[0],2*end[1]-start[1]) #jump over
        if not isRealSpot(dropSpot):
            result["error"] = "Can't jump off board"
            return result
        elif grid[dropSpot] != "N": #Can't jump, piece on other side
            result["error"] = "That jump is blocked"
            return result
        #jump was good
        result["jump"] = True
        result["drop"] = dropSpot
        result["spotsToRemove"].append(end)


    result["spotsToRemove"].append(start)
    result["drop"] = dropSpot
    result["valid"] = True
    return result


#=============================================
#           Main Program Loop
#=============================================
while not done:
    #check if the close button is pressed
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    
    if pygame.mouse.get_pressed()[0] and not mousePressed: #mouse is down, for the first time
        mousePressed = True
        

        pos = pygame.mouse.get_pos()
        #check where click happened;
        clickedSquare = (math.floor(pos[0]/(size[0]/8)),math.floor(pos[1]/(size[1]/8)))

        #logic for selecting thing
        if selected[0] == -1: #if nothing is selected
            
            if grid[clickedSquare].lower() == turn: #make sure it is your turn
                selected = clickedSquare
            elif grid[clickedSquare].lower() == otherColor(turn): #not your turn
                print("Not your turn")

        elif selected == clickedSquare: #if you click the same spot then deselect
            selected = (-1,-1)
        else: #Try to place the piece there


            #call the main function to see if this placement is valid
            res = makeTurn(selected,clickedSquare)
            print(res)

            if res["valid"]: #if the move was sucsessful
                
                #set the new spot equal to the correct color
                newSpot = res["drop"]
                grid[newSpot] = grid[selected]
                
                #check if the newSquare is a king
                if grid[newSpot] == "r" and newSpot[1] == 7: #if it is red and on the bottom row
                    grid[newSpot] = "R" #King Them
                elif grid[newSpot] == "b" and newSpot[1] == 0: #if it is black and on the top row
                    grid[newSpot] = "B" #King Them
                #loop through the spots that need deleted
                for spot in res["spotsToRemove"]: 
                    grid[spot] = "N"
                
                #unselect square
                selected = (-1,-1)
                
                #change the turn
                turn = otherColor(turn)
                
            else: #the move was invalid
                
                #print the error
                print(res["error"])
                
    elif pygame.mouse.get_pressed()[0] == 0: #mouse is up
        mousePressed = False
    
    #=================================================
    #              Drawing code
    #=================================================
    #clear the screen
    screen.fill(white)
    
    #draw the lines
    for i in range(0,9):
        pygame.draw.line(screen, black, [i*size[0]/8, 0], [i*size[0]/8, size[1]], 5)
        pygame.draw.line(screen, black, [0, i*size[0]/8], [size[1],i*size[0]/8], 5)
        
    #draw the grid
    for i in range(0,8):
        for j in range(0,8):
            squareX = i*squareLength
            squareY = j*squareLength
            
            if selected == (i,j):
                pygame.draw.rect(screen,green,[squareX,squareY,squareLength,squareLength])
            
            circleX = math.floor(i*squareLength+squareLength/2)
            circleY = math.floor(j*squareLength+squareLength/2)
            radius = math.floor(size[0]/32)
            
            if grid[(i,j)].lower() == "r":
                pygame.draw.circle(screen, red, [circleX, circleY], radius)
            elif grid[(i,j)].lower() == "b":
                pygame.draw.circle(screen, black, [circleX, circleY], radius)
            
            #draw if it is a king
            if grid[(i,j)] == grid[(i,j)].upper() and grid[(i,j)] != "N":
                pygame.draw.circle(screen,yellow,[circleX,circleY],math.floor(radius/4))
                
    #Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
 
    #Limit to 60 frames per second
    clock.tick(60)
 
# Close the window and quit.
pygame.quit()