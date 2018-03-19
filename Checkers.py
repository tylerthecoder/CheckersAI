#================================
# Name: Checking Simulator
# Author: Tyler Tracy
# Purpose: To simulate the game of checkers and to make it easier for an AI to play
#================================

import pygame
import math
import random

import grid as gr
from board import *

#Define some colors
black = (0, 0, 0)
yellow = (255, 255, 0)
green = (0, 255, 0)
red = (255, 0, 0)
white = (255,255,255)

pygame.init()

size = (700, 700) #width and height of the screen
squareLength = math.floor(size[0]/8)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Checkers")

clock = pygame.time.Clock() # Used to manage how fast the screen updates
mousePressed = True #variable to make the mouse click only happen when mouse is clicked up and then down
done = False

grid = Board("Standard")

#==============================================
#            Player Function
#==============================================

selected = (-1,-1) #this stores the value of the grid square that is currently selected
def RedPlayer(click):
    global selected
    if selected == (-1,-1):
        if grid.board[click].color == grid.turn:
            selected = click
        else:
            print("Wrong Turn")
    elif selected == click:
        selected = (-1,-1)
    else:
        res = grid.checkMove(selected,clickedSquare,grid.turn)
        print(res)
        if res["valid"]: #if the move was sucsessful
            return res
        else:
            print(res["error"])
            return False
    

def BlackPlayer():
    allMoves = grid.getAllMoves("b")
    move = random.choice(allMoves)
    res = grid.checkMove(move["start"],move["end"],"b")
    count = 0 #in case we get an infinite loop somehow
    while not res["valid"]: #keep trying until we get a valid move
        count = count + 1
        move = random.choice(allMoves)
        res = grid.checkMove(move["start"],move["end"],"b")
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
        
        #call player functions
        if grid.turn == "r":
            res = RedPlayer(clickedSquare)
            #res = BlackPlayer()
        elif grid.turn == "b":
            res = BlackPlayer()
        
        #            Make Move
        #==================================
        print(res)
        if res:
            result = grid.applyMove(res["start"],res["end"],grid.turn)
            if result:
                selected = (-1,-1)
                        
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
            if grid.board[spot] == "r" and spot[1] == 7: #if it is red and on the bottom row
                grid.board[spot].kingMe()
            elif grid.board[spot] == "b" and spot[1] == 0: #if it is black and on the top row
                grid.board[spot].kingMe()


            squareX = i*squareLength
            squareY = j*squareLength
            if selected == (i,j):
                pygame.draw.rect(screen,green,[squareX,squareY,squareLength,squareLength])
            
            circleX = math.floor(i*squareLength+squareLength/2)
            circleY = math.floor(j*squareLength+squareLength/2)
            radius = math.floor(size[0]/32)
            
            if grid.board[(i,j)].color == "r":
                pygame.draw.circle(screen, red, [circleX, circleY], radius)
            elif grid.board[(i,j)].color == "b":
                pygame.draw.circle(screen, black, [circleX, circleY], radius)
            
            #draw if it is a king
            if grid.board[(i,j)].king:
                pygame.draw.circle(screen,yellow,[circleX,circleY],math.floor(radius/4))
                
    #Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
 
    #Limit to 60 frames per second
    clock.tick(60)
 
# Close the window and quit.
pygame.quit()