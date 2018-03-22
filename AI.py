from board import *
import random

highestBoardVal = 2
moveSet = []

def AIPlayer (grid):
    
    bestMove = findBestMove(grid)
    print("current score:", boardValue(grid,"b"))
    print(bestMove)
    return bestMove


def findBestMove(board):
    allMoves = board.getAllMoves("b")
    best = -10000000
    bestMove = allMoves[0]
    for move in allMoves:
        #calculate the average of all the boardValues two turns in
        newBoard = Board("Copy",board)
        newBoard.applyMove(move["start"],move["end"],board.turn)
        avg = recursiveMoveFinder(newBoard,2)
        if avg[0]/avg[1] > best:
            best = avg[0]/avg[1]
            bestMove = move
    return bestMove



def recursiveMoveFinder (board,depth):
    avg = [0,0]
    allMoves = board.getAllMoves(board.turn)
    for move in allMoves:
        if move["valid"]:
            newBoard = Board("Copy",board)
            newBoard.applyMove(move["start"],move["end"],board.turn)
            # print(move["start"],move["end"],boardValue(newBoard,"b"))
            avg[0] += boardValue(newBoard,"b")
            avg[1] += 1 #increase the count
            if depth > 0:
                data = recursiveMoveFinder(newBoard,depth-1)
                avg[0] += data[0]
                avg[1] += data[1]

    return avg


def boardValue(grid,color):
    count = 0
    for spot in grid.indices:
        pie = grid.board[spot]
        amount = 1
        if pie.isPlayer:
            if pie.king:
                amount = 2
            if pie.color == color:
                count += amount
            else:
                count -= amount
    return count

