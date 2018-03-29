from piece import *
from move import *

class Board():
    def __init__(self):
        self.board = {}
        self.indices = []
        for col in range(8):
            for row in range(8):
                self.indices.append((row,col))
        self.isJumpAv = False
        self.dbjIndices = (-1,-1)
        self.selected = (-1,-1)
        self.turn = "r"

        self.pieces = {
            "r":[],
            "b":[]
        }

        for spot in self.indices:
            row = spot[0]
            col = spot[1]

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

    def copy (self):
        newBoard = Board()
        newBoard.pieces = {
            "r":[],"b":[]
        }
        for spot in newBoard.indices:
            newSpot = Spot(None,None)
            newSpot.setMe(self.board[spot])
            newBoard.board[spot] = newSpot
            if newSpot.isPlayer:
                newBoard.pieces[newSpot.color].append(newSpot)
        
        newBoard.window = self.window
        newBoard.turn = self.turn
        newBoard.dbjIndices = self.dbjIndices
        newBoard.isJumpAv = self.isJumpAv

        return newBoard

    def isRealSpot(self,spot):
        if spot[0] < 0 or spot[0] > 7:
            return False
        elif spot[1] < 0 or spot[1] > 7:
            return False
        return True

    def nextTurn (self):
        self.turn = self.otherColor(self.turn)

    def otherColor (self,color):
        return "r" if color == "b" else "b"

    def movePiece(self,fromPos,toPos):
        bufferPos = self.board[fromPos].pos
        self.board[fromPos].pos = self.board[toPos].pos
        self.board[toPos].pos = bufferPos

        bufferPie = self.board[fromPos] 
        self.board[fromPos] = self.board[toPos]
        self.board[toPos] = bufferPie

        #check if toPiece is a king
        if self.board[toPos].color == "r" and toPos[1] == 7: #if it is red and on the bottom row
            self.board[toPos].kingMe()
        elif self.board[toPos].color == "b" and toPos[1] == 0: #if it is black and on the top row
            self.board[toPos].kingMe()

    def applyMove(self,move):
        #error if the move isn't valid
        if not self.checkMove(move)["valid"]:
            return False
        
        #move the starting piece to the new location
        self.movePiece(move.start,move.drop)
        
        dbj = False #flag to see if dbj happened
        
        #did you just jump?
        if move.jump:

            #delete the piece that you jumpped over
            self.pieces[self.board[move.end].color].remove(self.board[move.end])
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
        for pie in self.pieces[player]:
            moves = self.getMovesForPiece(pie,jumps)
            allMoves += moves
        return allMoves

    def getMovesForPiece(self,spot,jumps=False):
        allMoves = []

        if spot.king:
            rngj = [-1,1]
        elif spot.color == "r":
            rngj = [1]
        elif spot.color == "b":
            rngj = [-1]

        for i in [-1,1]: #check right and left
            for j in rngj: #check up and down, depending on color and if it's a king
                check = (spot.pos[0]+i,spot.pos[1]+j)
                move = Move(spot.pos,check,self)
                if move.valid:
                    if jumps:
                        if move.jump:
                            allMoves.append(move)
                    else:
                        allMoves.append(move)
        return allMoves

    def makeMove(self,startPos,endPos):
        return Move(startPos,endPos,self)

    def isGameOver(self):
        redMoves = self.getAllMoves("r")
        blackMoves = self.getAllMoves("b")
        if len(redMoves) == 0:
            return [True,"r"]
        elif len(blackMoves) == 0:
            return [True,"b"]
        return [False]

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
            print(pie,pie.pos)
        print("Black")
        for pie in self.pieces["b"]:
            print(pie,pie.pos)
        
        print("End", len(self.pieces["r"]), len(self.pieces["b"]))