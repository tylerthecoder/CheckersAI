from piece import *
from move import *
import copy as cpy

class Board():
    indices = []
    for col in range(8):
        for row in range(8):
            indices.append((row,col))
    isJumpAv = False
    dbjIndices = (-1,-1)
    selected = (-1,-1)
    turn = "r"

    pieces = {
        "r":[],
        "b":[]
    }

    def __init__(self,boardType,copy=False):
        self.board = {}
        
        #the regular board
        if boardType == "Standard":
            for spot in self.indices:
                row = spot[0]
                col = spot[1]
                # if (row+col)%2 == 0:
                #     char = "r" if col < 3 elif col > 4 "b" else "N"
                # else:
                #     char = "N"

                if col < 3 and (row+col)%2 == 0: #check if (row,col) is in the checker diagonal
                    char = "r" #set the square to be red
                elif col > 4 and (row+col)%2 == 0:
                    char = "b" #set the square to be black
                else:
                    char = "N" #set the square to be empty
                newSpot = Spot(char,spot)
                self.board[spot] = newSpot
                if char != "N":
                    self.pieces[char].append(newSpot)

        #if you want to copy the board
        elif boardType == "Copy":
            print("This is the copy")
            copy.printP()
            self.pieces["r"] = []
            self.pieces["b"] = []
            for spot in self.indices:
                newSpot = Spot(None,None)
                newSpot.setMe(copy.board[spot])
                self.board[spot] = newSpot
                if newSpot.isPlayer:
                    self.pieces[newSpot.color].append(newSpot)
            
            self.window = copy.window
            self.turn = copy.turn
            self.dbjIndices = copy.dbjIndices
            self.isJumpAv = copy.isJumpAv


    def isRealSpot(self,spot):
        if spot[0] < 0 or spot[0] > 7:
            return False
        elif spot[1] < 0 or spot[1] > 7:
            return False
        return True

    def nextTurn (self):
        if self.turn == "r":
            self.turn = "b"
        elif self.turn == "b":
            self.turn = "r"

    def movePiece(self,fromPos,toPos,test):
        if test:
            bufferPos = self.board[fromPos].pos
            self.board[fromPos].pos = self.board[toPos].pos
            self.board[toPos].pos = bufferPos
        else:
            self.board[fromPos].setPos("poop")
            self.board[toPos].setPos("poop")
        
        self.board[toPos].setMe(self.board[fromPos])
        self.board[fromPos] = Spot("N",fromPos) #delete piece in spot

    def kingPieces (self):
        for spot in self.indices:
            if self.board[spot].color == "r" and spot[1] == 7: #if it is red and on the bottom row
                self.board[spot].kingMe()
            elif self.board[spot].color == "b" and spot[1] == 0: #if it is black and on the top row
                self.board[spot].kingMe()

    def applyMove(self,move, test = False):
        if not self.checkMove(move)["valid"]:
            return False
        
        #move the starting piece to the new location
        self.movePiece(move.start,move.drop,test)

        #king everyone
        self.kingPieces()
        
        dbj = False #flag to see if dbj happened
        
        #did you just jump?
        if move.jump:
            #delete the piece that you jumpped over
            self.board[move.end] = Spot("N",move.end)

            #get all jumps
            jumps = self.getAllMoves(self.turn,True)
            
            #loop through the jumps
            for jump in jumps:
                #if the next jump starts where I landed
                if jump.start == move.drop:
                    #There is a dbj
                    self.dbjIndices = move.drop
                    dbj = True

        #change the turn if there isn't a double jump
        if not dbj:
            self.nextTurn()
            self.dbjIndices = (-1,-1)

        #is there is a jump on this board, do now so the computation doesn't have to be done over and over
        self.isJumpAv = len(self.getAllMoves(self.turn,True)) > 0

        return True

    def checkMove(self,move):
        result = {"error":"","valid":False}

        #not a valid move
        if not move.valid:
            result["error"] = "Not a valid move"

        #not the correct turn
        elif self.board[move.start].color != self.turn:
            result["error"] = "Not your turn"

        #if there is a jump and you are not jummping
        elif self.isJumpAv and not move.jump:
            result["error"] = "You must take the jump"
        
        #if there is a double jump and you aren't taking it
        elif self.dbjIndices != (-1,-1) and move.start != self.dbjIndices:
            result["error"] = "You must take the double jump"
        
        #There were no errors
        else:
            result["valid"] = True

        return result


    def getAllMoves(self,player,jumps=False):
        allMoves = []
        for spot in self.indices:
            if self.board[spot].color == player:
                moves = self.getMovesForPiece(spot,jumps)
                allMoves += moves
        return allMoves

    def getMovesForPiece(self,spot,jumps=False):
        allMoves = []
        rngi = [-1,1]
        if self.board[spot]:
            rngj = [-1,1]
        elif  self.board[spot].color == "r":
            rngj = [1]
        elif  self.board[spot].color == "b":
            rngj = [-1]
        
        for i in rngi:
            for j in rngj:
                check = (spot[0]+i,spot[1]+j)
                move = Move(spot,check,self)
                if move.valid:
                    if jumps:
                        if move.jump:
                            allMoves.append(move)
                    else:
                        allMoves.append(move)
        return allMoves

    def print (self):
        for col in range(8):
            rowStr = ""
            for row in range(8):
                p = self.board[(row,col)]
                rowStr += p.color
            print(rowStr)

    def printP(self):
        print("Red")
        for pie in self.pieces["r"]:
            print(pie, pie.pos)
        print("Black")
        for pie in self.pieces["b"]:
            print(pie, pie.pos)
        
        print("End", len(self.pieces["r"]))
        



        