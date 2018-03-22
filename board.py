from piece import *

class Board():
    indices = []
    for col in range(8):
        for row in range(8):
            indices.append((row,col))

    dbjIndices = (-1,-1)

    turn = "r"

    def __init__(self,boardType,copy=False):
        self.board = {}
        #if you want to make a standard board
        for spot in self.indices:
            row = spot[0]
            col = spot[1]
            if boardType == "Standard":
                if col < 3 and (row+col)%2 == 0: #check if (row,col) is in the checker diagonal
                    char = "r" #set the square to be red
                elif col > 4 and (row+col)%2 == 0:
                    char = "b" #set the square to be black
                else:
                    char = "N" #set the square to be empty
                self.board[spot] = Spot(char)
            elif boardType == "Empty":
                self.board[spot] = Spot("N")
            elif boardType == "Copy":
                self.board[spot] = Spot(copy[spot].color)
            else:
                self.board[spot] = Spot("N")
        if boardType == "dbj":
            self.board[(2,2)] = Spot("r")
            self.board[(4,4)] = Spot("r")
            self.board[(5,5)] = Spot("b")


    def isRealSpot(self,spot):
        if spot[0] < 0 or spot[0] > 7:
            return False
        elif spot[1] < 0 or spot[1] > 7:
            return False
        return True

    def movePiece(self,fromPos,toPos):
        self.board[toPos].setMe(self.board[fromPos])
        self.board[fromPos] = Spot("N")

    def kingPieces (self):
        for spot in self.indices:
            if self.board[spot].color == "r" and spot[1] == 7: #if it is red and on the bottom row
                self.board[spot].kingMe()
            elif self.board[spot].color == "b" and spot[1] == 0: #if it is black and on the top row
                self.board[spot].kingMe()

    def applyMove(self,start,end,turn):
        moveData = self.checkMove(start,end,turn)
        if not moveData["valid"]:
            return False
        
        #move the starting piece to the new location
        self.movePiece(moveData["start"],moveData["drop"])

        #loop through the spots that need deleted
        for spot in moveData["spotsToRemove"]: 
            self.board[spot].isPlayer = False
            self.board[spot].color = "N"

        #king everyone
        self.kingPieces()

        #is there a dbj on the board?

        #if we just jumpped
        dbj = False
        if moveData["jump"]:
            jumps = self.getAllMoves(turn,True)
            #if there is a jump on the new board
            if len(jumps) > 0:
                #loop through the jumps
                for jump in jumps:
                    #if the next jump starts where I landed
                    if jump["start"] == moveData["drop"]:
                        #There is a dbj
                        self.dbjIndices = moveData["drop"]
                        print("There is a dbj")
                        dbj = True
        if not dbj:
            if self.turn == "r":
                self.turn = "b"
            elif self.turn == "b":
                self.turn = "r"

        return True

    def checkMove(self,start,end,turn):
        result = {"error":""}

        moveData = self.getMoveData(start,end)

        #if the move isn't valid
        if not moveData["valid"]:
            return moveData

        #if it isn't your turn
        if self.board[start].color != turn:
            result["error"] = "Not your turn"

        #If there is a jump
        if len(self.getAllMoves(turn,True)) > 0:
            #and you are not jumping
            if not moveData["jump"]:
                result["error"] = "You must take the jump"
        
        #if there is a dbj and you didn't take it
        if self.dbjIndices != (-1,-1):
            if moveData["start"] != start:
                result["error"] = "You must take the double jump"
        if result["error"] == "":
            result["valid"] = True
            return moveData
        else:
            result["valid"] = False
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
        elif color == "r":
            rngj = [1]
        elif color == "b":
            rngj = [-1]
        
        for i in rngi:
            for j in rngj:
                check = (spot[0]+i,spot[1]+j)
                res = self.getMoveData(spot,check)
                if res["valid"]:
                    if jumps:
                        if res["jump"]:
                            allMoves.append(res)
                    else:
                        allMoves.append(res)
        return allMoves

    def getMoveData(self,start,end):
        result = {
            "start":start,
            "end":end,
            "jump":False,
            "error":"",
            "valid":False,
            "spotsToRemove":[]
        }

        if (not self.isRealSpot(start) or not self.isRealSpot(end)):
            result["error"] = "Not a real spot"
            return result

        #check if they are not diagonal
        if (start[0]+start[1])%2 != (end[0]+end[1])%2:
            result["error"] = "Not on Diagonal"

        #too far away
        if abs(end[0]-start[0]) > 1 or abs(end[1]-start[1]) > 1:
            result["error"] = "Too far away"
        
        #if it is a king, it can't go backwards
        if not self.board[start].king:
            if (end[1]-start[1] != 1 and self.board[start].color == "r"):
                result["error"] = "Can't go backwards"
            elif (end[1]-start[1] != -1 and self.board[start].color == "b"):
                result["error"] = "Can't go backwards"
        
        #The colors are the same, so you can't play there
        if self.board[start].color == self.board[end].color: 
            result["error"] = "Can't jump your own pieces"
        
        if not self.board[end].isPlayer: #not jumping a piece
            dropSpot = end
        else: #jumping over a piece
            result["jump"] = True
            result["spotsToRemove"].append(end)
            dropSpot = (2*end[0]-start[0],2*end[1]-start[1]) #jump over
            if not self.isRealSpot(dropSpot):
                result["error"] = "Can't jump off board"
                return result
            elif self.board[dropSpot].isPlayer: #Can't jump, piece on other side
                result["error"] = "That jump is blocked"

        result["spotsToRemove"].append(start)
        result["drop"] = dropSpot
        if result["error"] == "":
            result["valid"] = True
        return result



        