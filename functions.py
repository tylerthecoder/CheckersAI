import random

def find_mspace(row,col,player):
    b_check = []
    w_check = []
    if (player == 'b') and (col == 0):
        b_check.append((row-1,col+1))
    elif (player == 'b') and (col == 7):
        b_check.append((row-1,col-1))
    elif (player == 'b'):
        b_check.append((row-1,col+1))
        b_check.append((row-1,col-1))
    return b_check

# --------------------
# Player 1 functions
# --------------------

def space_check(row,col,board):
    if (board[row][col] != '  '):
        print ("That piece has no available moves, select another.")
        return False
    else:
        return True

def ply_cond(row,col,rs,cs,board):
    if (row == rs - 1) and ((col == cs + 1) or (col == cs - 1)):
        return row,col
    else:
        print ("That is not a valid move.")
        row = eval(input("Row "))
        col = eval(input("Column "))
        return ply_cond(row,col,rs,cs,board)

def ply_jump(board):
    for row in range(8):
        for col in range(8):
            if board[row][col] == 'b':
                if (col <= 1) and (board[row-1][col+1] == 'w' and board[row-2][col+2] == ' '):
                    print("You can jump a piece at",row-1,col+1,)
                    rt = eval(input("Row "))
                    ct = eval(input("Column "))
                    while (rt!= row-1) and (ct != col+1):
                        print("You must make the available jump.")
                        rt = eval(input("Row "))
                        ct = eval(input("Column "))
                    return True,row,col,row-1,col+1,row-2,col+2
                elif (col >= 6) and (board[row-1][col-1] == 'w' and board[row-2][col-2] == ' '):
                    print("You can jump a piece at",row-1,col-1,)
                    rt = eval(input("Row "))
                    ct = eval(input("Column "))
                    while (rt!= row-1) and (ct != col-1):
                        print("You must make the available jump.")
                        rt = eval(input("Row "))
                        ct = eval(input("Column "))
                    return True,row,col,row-1,col-1,row-2,col-2
                elif (col >= 2 and col <= 5 ) and (board[row-1][col-1] == 'w' and board[row-2][col-2] == ' '):
                    print("You can jump a piece at",row-1,col-1,)
                    rt = eval(input("Row "))
                    ct = eval(input("Column "))
                    while (rt!= row-1) and (ct != col-1):
                        print("You must make the available jump.")
                        rt = eval(input("Row "))
                        ct = eval(input("Column "))
                    return True,row,col,row-1,col-1,row-2,col-2
                elif (col >= 2 and col <= 5) and (board[row-1][col+1] == 'w' and board[row-2][col+2] == ' '):
                    print("You can jump a piece at",row-1,col+1,)
                    rt = eval(input("Row "))
                    ct = eval(input("Column "))
                    while (rt!= row-1) and (ct != col+1):
                        print("You must make the available jump.")
                        rt = eval(input("Row "))
                        ct = eval(input("Column "))
                    return True,row,col,row-1,col+1,row-2,col+2
    return False,0,0,0,0,0,0

# --------------
# AI functions
# --------------

def AIspace_check(row,col,board):
    check = board[row][col]
    if check[:1] == 'w' and col == 0 and board[row+1][col+1] == '   ':
        return row,col
    elif check[:1] == 'w' and col == 7 and board[row+1][col-1] == '   ':
        return row,col
    elif check[:1] == 'w' and (board[row+1][col+1] == '   ' or board[row+1][col-1] == '   '):
        return row,col
    else:
        row = random.randint(0,7)
        col = random.randint(0,7)
        return AIspace_check(row,col,board)
