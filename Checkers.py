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
            char = "r" #set the square to be red
        elif col > 4 and (row+col)%2 == 0:
            char = "b" #set the square to be black
        else:
            char = "N" #set the square to be empty
        
        grid[(row,col)] = char

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
def makeTurn(startSpot,endSpot):
    #return values
    #Array(3)
    #Index 1: True/False for if the jump is valid
    #Index 2: If True, then return new location of the piece
    #         If False, then return error number
    #Index 3: If True Array of indices to destroy
    #         If False, String Describing error
   
    result = {}
    result["valid"] = False
    if grid[startSpot].lower() != turn: #wrong player
        result["error"] = "Wrong Player"
        return [False,0,"Wrong Player"]
    
    #if a jump is aviliable, then you must make it
    jumps = allPosibleMoves(turn,True)
    if len(jumps) > 0:
        isJump = False
        for i in jumps:
            #if there is a jump for me
            if i[1] == startSpot and i[2] == endSpot:
                isJump = True
        if not isJump: 
            result["error"] = "You need to take the jump"
            return [False,8,"You need to take the jump"]

    if (startSpot[0]+startSpot[1])%2 != (endSpot[0]+endSpot[1])%2: #check if they are not diagonal
        result["error"] = "Not on Diagonal"
        return [False,1,"Not on Diagonal"]
    if abs(endSpot[0]-startSpot[0]) > 1: #too far away in the x-dir
        result["error"] = "Too far away in the X direction"
        return [False,2,"Too far way in x-dir"]
    
    if grid[startSpot].upper() == grid[startSpot]: #if they are a king
        if (abs(endSpot[1]-startSpot[1]) > 1): #too far away in the y-dir
            result["error"] = "Too far away in the Y direction"
            return [False,3,"Too far way in y-dir"]
    else: #if they are not a king
        if (endSpot[1]-startSpot[1] != 1 and grid[startSpot].lower() == "r"):
            result["error"] = "Can't go backwards"
            return [False,4,"Can't Go Backwards"]
        elif (endSpot[1]-startSpot[1] != -1 and grid[startSpot].lower() == "b"):
            result["error"] = "Can't go backwards"
            return [False,4,"Can't Go Backwards"]
    
    if grid[endSpot] == grid[startSpot]: #The colors are the same, so you can't play there
        result["error"] = "Can't jump your own Pieces"
        return [False,5,"Can't jump your own Pieces"]

    #this is an array of values that will be replaced with "N", meaning we are deleting the piece in them
    removeSpots = []
    
    if (grid[endSpot] == "N"): #not jumping over piece
        dropSpot = endSpot
    else: #juming over piece
        dropSpot = (2*endSpot[0]-startSpot[0],2*endSpot[1]-startSpot[1]) #jump over
        if dropSpot[0] == -1 or dropSpot[0] == 8 or dropSpot[1] == -1 or dropSpot[1] == 8:
            result["error"] = "Can't jump off board"
            return [False,6,"Can't Jump off board"]
        if grid[dropSpot] != "N": #Can't jump, piece on other side
            result["error"] = "That jump is blocked"
            return [False,7,"That Jump is blocked"]
        #if jump, then check for double jump
        
        removeSpots.append(endSpot)


    removeSpots.append(startSpot)
    return [True,dropSpot,removeSpots]


def possibleMoves (spot):
    #returns array of moves
    #move = (isJump(Bool),start(Tuple),stop(Tuple))
    moves = []
    jumps = []
    rngi = [-1,1]
    if grid[spot] == grid[spot].upper(): #it is a king
        rngj = [-1,1]
    elif grid[spot] == "r": 
        rngj = [1]
    elif grid[spot] == "b":
        rngj = [-1]
    for i in rngi:
        for j in rngj:
            check = (spot[0]+i,spot[1]+j)
            oc = otherColor(grid[spot])
            if isRealSpot(check):
                if grid[check] == "N": #nothing there and we aren't just checking for jumps
                    res = makeTurn(spot,check)
                    if res[0]:
                        moves.append([False,spot,check])
                elif grid[check] == oc: #a possible jump
                    #checking if the piece is jumpable
                    landing = (2*check[0]-spot[0],2*check[1]-spot[1])
                    if isRealSpot(landing) and grid[landing] == "N": #nothing in the landing square
                        #it is good, add it to the array
                        jumps.append([True,grid[spot],spot,check])
    if len(jumps) > 0:
        return jumps
    else:
        return moves


def allPosibleMoves (color,onlyJump=False):
    allMoves = []
    jumps = []
    for row in range(8):
        for col in range(8):
            start = (row,col)
            if grid[start] != color: #not on the right square
                continue
             #check all the boxes and the boxes around them
            rngi = [-1,1]
            if grid[start] == grid[start].upper(): #it is a king
                rngj = [-1,1]
            elif grid[start] == "r": 
                rngj = [1]
            elif grid[start] == "b":
                rngj = [-1]
            for i in rngi:
                for j in rngj:
                    check = (row+i,col+j)
                    oc = otherColor(grid[start])
                    if isRealSpot(check):
                        if grid[check] == "N" and not onlyJump: #nothing there and we aren't just checking for jumps
                            res = makeTurn(start,check)
                            if res[0]:
                                allMoves.append([start,check])
                        elif grid[check] == oc: #a possible jump
                            #checking if the piece is jumpable
                            landing = (2*check[0]-start[0],2*check[1]-start[1])
                            if isRealSpot(landing) and grid[landing] == "N": #nothing in the landing square
                                #it is good, add it to the array
                                jumps.append([grid[start],start,check])

    if len(jumps) > 0 or onlyJump:
        return jumps
    else:
        return allMoves
    


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
            
            if res[0]: #if the move was sucsessful
                
                #set the new spot equal to the correct color
                newSpot = res[1]
                grid[newSpot] = grid[selected]
                
                #check if the newSquare is a king
                if grid[newSpot] == "r" and newSpot[1] == 7: #if it is red and on the bottom row
                    grid[newSpot] = "R" #King Them
                    print("kinged")
                elif grid[newSpot] == "b" and newSpot[1] == 0: #if it is black and on the top row
                    grid[newSpot] = "B" #King Them
                    print("kinged")
                
                #loop through the spots that need deleted
                for spot in res[2]: 
                    grid[spot] = "N"
                
                #unselect square
                selected = (-1,-1)
                
                #change the turn
                turn = otherColor(turn)

                print("Possible Moves: ", allPosibleMoves(turn))
                
            else: #the move was invalid
                
                #print the error
                print(res[2])
                
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