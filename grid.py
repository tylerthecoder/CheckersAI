def otherColor(color):
    if color == "r":
        return "b"
    if color == "b":
        return "r"

def isRealSpot(spot):
    if spot[0] < 0 or spot[0] > 7:
        return False
    elif spot[1] < 0 or spot[1] > 7:
        return False
    return True

def makeTurn(start,end,turn,grd):
    result = {
        "valid":True,
        "changeTurn":True,
        "error":"",
        "jump":False
    }
    
    #find all moves that are possible
    moves = allPosibleMoves(turn,grd)
    jump = False
    myMove = False
    for move in moves:
        #check if this move in in the able moves
        if move["start"] == start and move["end"] == end:
            if move["valid"]:
                myMove = move
            else:
                return move
        if move["jump"]:
            jump = True

    #if you did a move that wasn't on the list
    if not myMove:
        return checkMove(start,end,grd)

    #if you didn't jump and there was a jump avaliable
    if jump and not myMove["jump"]:
        result["valid"] = False
        result["error"] = "You need to jump"
    
    result["spotsToRemove"] = myMove["spotsToRemove"]
    result["drop"] = myMove["drop"]
    result["start"] = myMove["start"]
    result["jump"] = myMove["jump"]

    return result


def allPosibleMoves (color,grd):
    allMoves = []
    jumps = []
    for row in range(8):
        for col in range(8):
            if (grd[(row,col)].lower() == color):
                king = grd[(row,col)] == grd[(row,col)].upper()
                moves = checkForJump(color,(row,col),king,grd)
                for i in moves:
                    allMoves.append(i)
    return allMoves

def checkForJump(color,spot,king,grd):
    allMoves = []
    rngi = [-1,1]
    if king:
        rngj = [-1,1]
    elif color == "r":
        rngj = [1]
    elif color == "b":
        rngj = [-1]
    
    for i in rngi:
        for j in rngj:
            check = (spot[0]+i,spot[1]+j)
            oc = otherColor(color)
            #compare spot and check
            res = checkMove(spot,check,grd)
            if res["valid"]:
                allMoves.append(res)

    return allMoves

def checkMove (start,end,grd): 
    #if a jump is aviliable, then you must make it
    result = {}
    result["start"] = start
    result["end"] = end
    result["valid"] = False
    result["jump"] = False

    if (not isRealSpot(start) or not isRealSpot(end)):
        result["error"] = "Not a real spot"
        return result
    
    if (start[0]+start[1])%2 != (end[0]+end[1])%2: #check if they are not diagonal
        result["error"] = "Not on Diagonal"
        return result
    if abs(end[0]-start[0]) > 1: #too far away in the x-dir
        result["error"] = "Too far away in the X direction"
        return result
    
    if grd[start].upper() == grd[start]: #if they are a king
        if (abs(end[1]-start[1]) > 1): #too far away in the y-dir
            result["error"] = "Too far away in the Y direction"
            return result
    else: #if they are not a king
        if (end[1]-start[1] != 1 and grd[start].lower() == "r"):
            result["error"] = "Can't go backwards"
            return result
        elif (end[1]-start[1] != -1 and grd[start].lower() == "b"):
            result["error"] = "Can't go backwards"
            return result
    if grd[end] == grd[start]: #The colors are the same, so you can't play there
        result["error"] = "Can't jump your own Pieces"
        return result

    #this is an array of pieces to delete
    result["spotsToRemove"] = []
    
    if (grd[end] == "N"): #not jumping over piece
        dropSpot = end
    else: #juming over piece
        dropSpot = (2*end[0]-start[0],2*end[1]-start[1]) #jump over
        if not isRealSpot(dropSpot):
            result["error"] = "Can't jump off board"
            return result
        elif grd[dropSpot] != "N": #Can't jump, piece on other side
            result["error"] = "That jump is blocked"
            return result
        #jump was good
        result["jump"] = True
        result["spotsToRemove"].append(end)

    result["spotsToRemove"].append(start)
    result["drop"] = dropSpot
    result["valid"] = True
    return result