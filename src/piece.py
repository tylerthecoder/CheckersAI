class Spot:
    def __init__(self, color, pos):
        if color != "N": #it is a piece
            self.isPlayer = True
        else:
            self.isPlayer = False
        self.color = color
        self.king = False
        self.pos = pos
    
    def kingMe(self):
        self.king = True

    def setMe (self,spot):
        self.pos = spot.pos
        self.color = spot.color
        self.isPlayer = spot.isPlayer
        self.king = spot.king
    
    def setPos(self,pos):
        print(self, self.pos, pos)
        self.pos = pos

    
