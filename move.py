class Move():
    valid = False
    error = ""
    jump = False
    def __init__(self,start,end,board):
        self.start = start
        self.end = end
        self.board = board
        self.spots = board.board
        
        #not a spot on the board
        if not self.board.isRealSpot(self.start) or not self.board.isRealSpot(self.end):
            self.error = "Invalid spot"

        #not on the same diagonal
        elif (self.start[0]+self.start[1])%2 != (self.end[0]+self.end[1])%2:
            self.error = "Invalid spot"

        #too far away
        elif abs(self.end[0]-self.start[0]) > 1 or abs(self.end[1]-self.start[1]) > 1:
            self.error = "Invalid landing spot"

        #same ending color
        elif self.spots[self.start].color == self.spots[self.end].color:
            self.error = "Can't jump your own pieces"

        #if it is a red pieces trying to go backwards, and it isn't a king
        elif not self.spots[self.start].king and self.end[1]-self.start[1] != 1 and self.spots[self.start].color == "r":
            self.error = "Can't go backwards"

        #if it is a black pieces trying to go backwards, and it isn't a king
        elif not self.spots[self.start].king and self.end[1]-self.start[1] != -1 and self.spots[self.start].color == "b":
            self.error = "Can't go backwards"

        #there were no errors, so we can keep testing
        else:
            #we are ending on a player, so we are trying to jump
            if self.spots[self.end].isPlayer:
                self.jump = True
                self.drop = (2*self.end[0]-self.start[0],2*self.end[1]-self.start[1])

                #check if ending spot is on the board
                if not self.board.isRealSpot(self.drop):
                    self.error = "Can't jump off board"

                #check if the jump is blocked
                elif self.spots[self.drop].isPlayer:
                    self.error = "Jump is blocked"

            #not a jump     
            else:
                self.drop = self.end
            
            if self.error == "":
                self.valid = True
    
    def print(self):
        print("Start: ", self.start, "End: ", self.end)
                
    

        

