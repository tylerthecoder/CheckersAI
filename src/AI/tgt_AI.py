import random
import sys
sys.path.append("../")
from board import Board,Move


def AIPlayer (board,turn):
    allMoves = board.getAllMoves(turn)
    best = -10000000
    bestMove = [allMoves[0]]
    for move in allMoves:
        if board.checkMove(move)["valid"]:
            #calculate the average of all the boardValues two turns in
            # spdb.set_trace()
            newBoard = Board("Copy",board)
            newBoard.applyMove(move)
            avg = recursiveMoveFinder(newBoard,3,turn)
            print(move.start,move.end,avg)
            if avg > best:
                best = avg
                bestMove = [move]
            elif avg == best:
                bestMove.append(move)
        
    print("============================================current score:", boardValue(board,turn,1))
    return random.choice(bestMove)


def recursiveMoveFinder (board,depth,turn):
    avg = 0
    allMoves = board.getAllMoves(board.turn)
    for move in allMoves:
        if board.checkMove(move)["valid"]:
            newBoard = Board("Copy",board)
            newBoard.applyMove(move)
            avg += boardValue(newBoard,turn,depth+1)
            if depth > 0:
                data = recursiveMoveFinder(newBoard,depth-1,turn)
                avg += data
    return avg


def boardValue(grid,color,weight):
    count = 0
    for spot in grid.indices:
        pie = grid.board[spot]
        amount = 1
        if pie.isPlayer:
            if pie.king:
                amount = 4
            if pie.color == color:
                count += amount * weight
            else:
                count -= amount * weight
    return count

