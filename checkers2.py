import functions
import random
import piecelist

class Checkers:
    def __init__(self):
        self.board = [['   ' for x in range(8)] for y in range(8)]
        self.w_list = piecelist.piecelist()
        self.b_list = piecelist.piecelist()

#--------------
# Board Methods
#--------------

    def print_board(self):
        count = 0
        row = 0
        col = 0
        while count < 8:
            if count == 0:
                print('   ',count,'  ',end='')
            else:
                print('  ',count,'  ',end='')
            count += 1
        count = 0
        print('')
        while count < 8:
            print (count,end='')
            while col < 8:
                print('|',self.board[row][col],'|',end='')
                col += 1
            count += 1
            row += 1
            col = 0
            print('')
            print('---------------------------------------------------------')

    def populate(self):
        white_pieces = ['w1 ','w2 ','w3 ','w4 ','w5 ','w6 ','w7 ','w8 ','w9 ','w10','w11','w12']
        col = 0
        i = 0
        while col < 8:
            self.board[0][col] = white_pieces[i]
            i += 1
            self.board[1][col+1] = white_pieces[i]
            i += 1
            self.board[2][col] = white_pieces[i]
            i+=1
            col += 2
        black_pieces = ['b1 ','b2 ','b3 ','b4 ','b5 ','b6 ','b7 ','b8 ','b9 ','b10','b11','b12']
        col = 0
        i = 0
        while col < 8:
            self.board[5][col] = black_pieces[i]
            i += 1
            self.board[6][col+1] = black_pieces[i]
            i += 1
            self.board[7][col] = black_pieces[i]
            i += 1
            col += 2
        self.print_board()

    def fill_list(self):
        for row in range(8):
            for col in range(8):
                check = self.board[row][col]
                if check[:1] == 'w':
                    self.w_list.insert(check,check[:1],check[:1],row,col,(0,1))
                if check[:1] == 'b':
                    move = functions.find_mspace(row,col,check[:1])
                    self.b_list.insert(check,check[:1],check[:1],row,col,move)


#----------
#Game loop
#----------

    def play(self):
        self.populate()
        self.fill_list()
        self.b_list.print_list()
        self.print_board()
        win = False
        while win is False:
            self.move_player1()
            #self.move_AI()

#------------------
#Player/AI methods
#------------------

    def move_player1(self):
        check = False
        while check == False:
            piece = input("Player which piece do you want to move? ")
            while (len(piece) < 3):
                piece = piece + ' '
            search = self.b_list.m_search(piece)
            rs,cs = self.b_list.p_search(piece)
            i = 0
            for items in search:
                row,col = items
                if (self.board[row][col] == '   '):
                    check = True
        temp = self.board[rs][cs]
        print("Where would you like to move?")
        rt = eval(input("Row "))
        ct = eval(input ("Column "))
        rt,ct = functions.ply_cond(rt,ct,rs,cs,self.board)
        self.board[rt][ct] = temp
        self.board[rs][cs] = '   '
        self.print_board()
        self.b_list.delete(temp)
        move = functions.find_mspace(row,col,temp[:1])
        self.b_list.insert(temp,temp[:1],temp[:1],rt,ct,temp)

    def move_AI(self):
        row = random.randint(0,7)
        col = random.randint(0,7)
        row,col = functions.AIspace_check(row,col,self.board)
        print(row,col)
        temp = self.board[row][col]
        self.board[row][col] = '   '
        choice = random.randint(0,1)
        if col == 0:
            self.board[row+1][col+1] = temp
        elif col == 7:
            self.board[row+1][col-1] = temp
        elif choice == 0:
            self.board[row+1][col-1] = temp
        elif choice ==  1:
            self.board[row+1][col+1] = temp
        self.print_board()

#------------
#Jump Methods
#------------

    def check_jump(self,board):
        #For Player
        result,rs,cs,row,col,rt,ct = functions.ply_jump(board)
        if result == True:
            self.board[rs][cs] = ' '
            self.board[row][col] = ' '
            self.board[rt][ct] = 'b'
            return True
        else:
            return False





test = Checkers()
test.play()

# search = "w8 "
# for item in test.w_pieces:
#     if item == search:
#         print (test.w_pieces[item])
#test.play()
#
# test = {1:'w1',2:'w2',3:'w3'}
#
#
#
# for item in test:
#     print (item)
