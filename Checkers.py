#================================
# Name: Checking Simulator
# Author: Tyler Tracy
# Purpose: To simulate the game of checkers and to make it easier for an AI to play
#================================

import pygame
import math
import random

import grid as gr

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
mousePressed = True #variable to make the mouse click only happen when mouse is clicked up and then down
turn = "r"
done = False
djSpot = (-1,-1) #used to store if there was a dj last turn

#==============================================
#            Player Function
#==============================================

selected = (-1,-1) #this stores the value of the grid square that is currently selected
def RedPlayer(click):
    global selected
    if selected == (-1,-1):
        if grid[click].lower() == turn:
            selected = click
        else:
            print("Wrong Turn")
    elif selected == click:
        selected = (-1,-1)
    else:
        res = gr.makeTurn(selected,clickedSquare,turn,grid)
        if res["valid"]: #if the move was sucsessful
            return res
        else:
            print(res["error"])
            return False
    

def BlackPlayer():
    allMoves = gr.allPosibleMoves("b",grid)
    move = random.choice(allMoves)
    res = gr.makeTurn(move["start"],move["end"],"b",grid)
    count = 0 #in case we get an infinite loop somehow
    while not res["valid"]:
        count = count + 1
        move = random.choice(allMoves)
        res = gr.makeTurn(move["start"],move["end"],"b",grid)
        if count > 100:
            print("something went wrong")
            break
    return res



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
        
        if turn == "r":
            res = RedPlayer(clickedSquare)
        elif turn == "b":
            res = BlackPlayer()
        
        if res:
            #check if there was a dj that needed to happen
            if djSpot != (-1,-1):
                if djSpot != res["start"]:
                    print("You have to continue the jump")
                    continue
                djSpot = (-1,-1)
            
            #set the new spot equal to the correct color
            grid[res["drop"]] = grid[res["start"]]
            
            #loop through the spots that need deleted
            for spot in res["spotsToRemove"]: 
                grid[spot] = "N"
            
            #unselect square
            selected = (-1,-1)
            
            #change the turn
            #is there a dj on the board?
            
            dj = False
            moves = gr.allPosibleMoves(turn,grid)
            if res["jump"]:
                for move in moves:
                    if move["jump"] and move["start"] == res["drop"]: #there is a dj
                        dj = True
                        djSpot = res["drop"]

            if not dj:
                turn = gr.otherColor(turn)
                
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
            spot = (i,j)
            #check for kinging
            if grid[spot] == "r" and spot[1] == 7: #if it is red and on the bottom row
                grid[spot] = "R" #King Them
            elif grid[spot] == "b" and spot[1] == 0: #if it is black and on the top row
                grid[spot] = "B" #King Them


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