import random
import sys
sys.path.append("../")
from board import *

def play (board):
    turn = board.turn
    allMoves = board.getAllMoves(turn)
    best = -10000000
    bestMove = [allMoves[0]]
    for move in allMoves:
        if board.checkMove(move)["valid"]:
            #calculate the average of all the boardValues two turns in
            newBoard = Board("Copy",board)
            newBoard.applyMove(move)

            avg = recursiveMoveFinder(newBoard,3,turn)
            print(move.start,move.end,avg)
            if avg > best:
                best = avg
                bestMove = [move]
            elif avg == best:
                bestMove.append(move)
        
    print("===================End of AI Turn=========================")
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
    amount = 0
    for pie in grid.pieces[color]:
        if pie.king:
            amount += 4 * weight
        else:
            amount += weight

    for pie in grid.pieces[grid.otherColor(color)]:
        if pie.king:
            amount -= 4 * weight
        else:
            amount -= weight
    return amount


