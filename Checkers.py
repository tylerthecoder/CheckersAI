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
grid = []
for col in range(8):
    grid.append([])
    for row in range(8):
        if row < 3 and (row+col)%2 == 0: #check if (row,col) is in the checker diagonal
            grid[col].append("r") #set the square to be red
        elif row > 4 and (row+col)%2 == 0:
            grid[col].append("b") #set the square to be black
        else:
            grid[col].append("N") #set the square to be empty

clock = pygame.time.Clock() # Used to manage how fast the screen updates
selected = (-1,-1) #this stores the value of the grid square that is currently selected
mousePressed = True #variable to make the mouse click only happen when mouse is clicked up and then down
turn = "r"
done = False

#==============================================
#            Helper FUnctions
#==============================================

def otherColor(color):
    if color == "r":
        return "b"
    if color == "b":
        return "r"

#function to save some typing
def grd(t):
    return grid[t[0]][t[1]]


def vailidJump(start,end): #check if I can jump a piece in this configuation
    c = otherColor(grd(start))

    if grd((start[0]+1,start[1]+1)) == c: #if it is next to a piece of the other color
        return True
    elif grd((start[0]-1,start[1]+1)) == c: #if it is next to a piece of the other color
        return True
    
    if grd(start) == grd(start).upper(): #it is a king
        #checking behind it
        if grd((start[0]+1,start[1]-1)) == c: #if it is next to a piece of the other color
            return True
        elif grd((start[0]-1,start[1]-1)) == c: #if it is next to a piece of the other color
            return True
    return False

        
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
   
    if grd(startSpot).lower() != turn: #wrong player
        return [False,0,"Wrong Player"]
    
    if (startSpot[0]+startSpot[1])%2 != (endSpot[0]+endSpot[1])%2: #check if they are not diagonal
        return [False,1,"Not on Diagonal"]
    if abs(endSpot[0]-startSpot[0]) > 1: #too far away in the x-dir
        return [False,2,"Too far way in x-dir"]
    
    if grd(startSpot).upper() == grd(startSpot): #if they are a king
        if (abs(endSpot[1]-startSpot[1]) > 1): #too far away in the y-dir
            return [False,3,"Too far way in y-dir"]
    else: #if they are not a king
        if (endSpot[1]-startSpot[1] != 1 and grd(startSpot).lower() == "r"):
            return [False,4,"Can't Go Backwards"]
        elif (endSpot[1]-startSpot[1] != -1 and grd(startSpot).lower() == "b"):
            return [False,4,"Can't Go Backwards"]
    
    if grd(endSpot) == grd(startSpot): #The colors are the same, so you can't play there
        return [False,5,"Can't Jump your own Pieces"]

    #this is an array of values that will be replaced with "N", meaning we are deleting the piece in them
    removeSpots = []
    
    if (grd(endSpot) == "N"): #not jumping over piece
        dropSpot = endSpot
    else: #juming over piece
        dropSpot = (2*endSpot[0]-startSpot[0],2*endSpot[1]-startSpot[1]) #jump over
        if dropSpot[0] == -1 or dropSpot[0] == 8 or dropSpot[1] == -1 or dropSpot[1] == 8:
            return [False,6,"Can't Jump off board"]
        if grd(dropSpot) != "N": #Can't jump, piece on other side
            return [False,7,"That Jump is blocked"]
        removeSpots.append(endSpot)


    removeSpots.append(startSpot)
    return [True,dropSpot,removeSpots]
        
def checkForJump():
    for row in range(8):
        for col in range(8):
            #check all the boxes and the boxes around them
            for i in range(-1,1,2):
                for j in range(-1,1,2):
                    if vailidJump((row,col),(row+i,col+j)):
                        print("Good Jump")


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


        checkForJump()
        #logic for selecting thing
        if selected[0] == -1: #if nothing is selected
            
            if grd(clickedSquare).lower() == turn: #make sure it is your turn
                selected = clickedSquare
            elif grd(clickedSquare).lower() == otherColor(turn): #not your turn
                print("Not your turn")

        elif selected == clickedSquare: #if you click the same spot then deselect
            selected = (-1,-1)
        else: #Try to place the piece there
            
            #call the main function to see if this placement is valid
            res = makeTurn(selected,clickedSquare)
            
            if res[0]: #if the move was sucsessful
                
                #set the new spot equal to the correct color
                newSpot = res[1]
                grid[newSpot[0]][newSpot[1]] = grd(selected)
                
                #check if the newSquare is a king
                if grd(newSpot) == "r" and newSpot[1] == 7: #if it is red and on the bottom row
                    grid[newSpot[0]][newSpot[1]] = "R" #King Them
                    print("kinged")
                elif grd(newSpot) == "b" and newSpot[1] == 0: #if it is black and on the top row
                    grid[newSpot[0]][newSpot[1]] = "B" #King Them
                    print("kinged")
                
                #loop through the spots that need deleted
                for spot in res[2]: 
                    grid[spot[0]][spot[1]] = "N"
                
                #unselect square
                selected = (-1,-1)
                
                #change the turn
                turn = otherColor(turn)
                
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
            
            if selected[0] == i and selected[1] == j:
                pygame.draw.rect(screen,green,[squareX,squareY,squareLength,squareLength])
            
            circleX = math.floor(i*squareLength+squareLength/2)
            circleY = math.floor(j*squareLength+squareLength/2)
            radius = math.floor(size[0]/32)
            
            if grid[i][j].lower() == "r":
                pygame.draw.circle(screen, red, [circleX, circleY], radius)
            elif grid[i][j].lower() == "b":
                pygame.draw.circle(screen, black, [circleX, circleY], radius)
            
            #draw if it is a king
            if grid[i][j] == grid[i][j].upper() and grid[i][j] != "N":
                pygame.draw.circle(screen,yellow,[circleX,circleY],math.floor(radius/4))
                
                
 
    #Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
 
    #Limit to 60 frames per second
    clock.tick(60)
 
# Close the window and quit.
pygame.quit()
