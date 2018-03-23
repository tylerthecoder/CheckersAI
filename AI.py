from board import *
import random

def AIPlayer (board):
    allMoves = board.getAllMoves("b")
    best = -10000000
    bestMove = []
    for move in allMoves:
        if board.checkMove(move)["valid"]:
            #calculate the average of all the boardValues two turns in
            newBoard = Board("Copy",board)
            newBoard.applyMove(move)
            avg = recursiveMoveFinder(newBoard,2)
            avg = avg[0]/avg[1]
            if avg > best:
                best = avg
                bestMove = [move]
            elif avg == best:
                bestMove.append(move)
        
    print("current score:", boardValue(board,"b"))
    return random.choice(bestMove)


def recursiveMoveFinder (board,depth):
    avg = [0,0]
    allMoves = board.getAllMoves(board.turn)
    for move in allMoves:

        if board.checkMove(move)["valid"]:
            newBoard = Board("Copy",board)
            newBoard.applyMove(move)
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

