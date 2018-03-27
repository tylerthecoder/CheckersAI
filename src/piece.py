class Spot:
    def __init__(self, color):
        if color != "N": #it is a piece
            self.isPlayer = True
        else:
            self.isPlayer = False
        self.color = color
        self.king = False
        self.me = "namer"

    def kingMe(self):
        self.king = True

    def setMe (self,spot):
        self.color = spot.color
        self.isPlayer = spot.isPlayer
        self.king = spot.king
