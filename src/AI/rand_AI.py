import random

def play (board):
    allMoves = board.getAllMoves(board.turn)
    goodMoves = []
    for move in allMoves:
        if board.checkMove(move)["valid"]: goodMoves.append(move)
    return random.choice(allMoves)