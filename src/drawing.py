import pygame
import math

pygame.init()
pygame.display.set_caption("Checkers")

class Window():
    #Define some colors
    black = (10, 10, 10)
    yellow = (255, 255, 0)
    green = (0, 255, 20)
    red = (255, 0, 0)
    white = (255,255,255)
    brown1 = (139,69,19)
    brown2 = (244,164,96)


    clock = pygame.time.Clock() # Used to manage how fast the screen updates
    mousePressed = True #variable to make the mouse click only happen when mouse is clicked up and then down

    def __init__(self,size):
        self.squareLength = math.floor(size[0]/8)
        self.size = (self.squareLength*8,self.squareLength*8)
        self.screen = pygame.display.set_mode(self.size)

    def isQuit (self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
        return False

    def waitForClick(self):
        while not self.isQuit():
            if self.isClick():
                return self.getClickedSquare()

            self.tick()

    def QuitGame (self):
        pygame.quit()

    def tick(self):
        self.clock.tick(60)

    def isClick (self):
        if pygame.mouse.get_pressed()[0] and not self.mousePressed: #mouse is down, for the first time
            self.mousePressed = True
            return True
        elif pygame.mouse.get_pressed()[0] == 0: #mouse is up
            self.mousePressed = False
            return False
        return False

    def getClickedSquare (self):
        pos = pygame.mouse.get_pos()
        return (math.floor(pos[0]/(self.size[0]/8)),math.floor(pos[1]/(self.size[1]/8)))

    def draw (self,grid):
        #clear the screen
        self.screen.fill(self.white)
            
        #draw the grid
        for i in range(0,8):
            for j in range(0,8):
                spot = (i,j)

                squareX = i*self.squareLength
                squareY = j*self.squareLength

                if grid.selected == (i,j):
                    squareColor = self.green
                elif (i+j)%2 == 0:
                    squareColor = self.brown2
                else:
                    squareColor = self.brown1
                
                pygame.draw.rect(self.screen,squareColor,[squareX,squareY,self.squareLength,self.squareLength])

                circleX = math.floor(i*self.squareLength+self.squareLength/2)
                circleY = math.floor(j*self.squareLength+self.squareLength/2)
                radius = math.floor(self.size[0]/32)
                
                if grid.board[(i,j)].color == "r":
                    pygame.draw.circle(self.screen, self.red, [circleX, circleY], radius)
                elif grid.board[(i,j)].color == "b":
                    pygame.draw.circle(self.screen, self.black, [circleX, circleY], radius)
                
                #draw if it is a king
                if grid.board[spot].king:
                    pygame.draw.circle(self.screen,self.yellow,[circleX,circleY],math.floor(radius/4))

         #draw the lines
        for i in range(0,9):
            pygame.draw.line(self.screen, self.black, [i*self.size[0]/8, 0], [i*self.size[0]/8, self.size[1]], 4)
            pygame.draw.line(self.screen, self.black, [0, i*self.size[0]/8], [self.size[1],i*self.size[0]/8], 4)
        
        #Go ahead and update the screen with what we've drawn.
        pygame.display.flip()