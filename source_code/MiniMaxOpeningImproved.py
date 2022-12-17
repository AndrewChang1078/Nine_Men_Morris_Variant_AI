import fileinput

class board_game:
    class node:
        def __init__(self, est, board):
            self.est=est
            self.board=board

    def __init__(self):
        self.board_position=[]
        self.static_estimation_count=0

    def get_file_input(self, file_name):
        temp=""
        for line in fileinput.input(files=file_name):
            temp=line
        self.board_position=list(line.replace('\n', ''))

    def count_number_of_morris(self, board):
        w_mills, b_mills=self.count_close_mill(board)
        return w_mills - b_mills

    def count_number_of_blocked_pieces(self, board):
        w_blocked=0
        b_blocked=0
        for i in range(len(board)):
            blocked=True
            n=self.get_neighbor(i)
            for j in n:
                if board[j]=='x':
                    blocked=False
            if blocked==True:
                if (board[i]=='W'):
                    w_blocked+=1
                elif (board[i]=='B'):
                    b_blocked+=1
        return b_blocked - w_blocked

    def count_number_of_pieces(self, board):
        num_white_pieces=0
        num_black_pieces=0
        for c in board:
            if c=='W':
                num_white_pieces=num_white_pieces+1
            elif c=='B':
                num_black_pieces=num_black_pieces+1
        return num_white_pieces-num_black_pieces

    def count_two_pieces_config(self, board):
        w_config=0
        b_config=0
        for i in range(len(board)):
            if board[i]=='x':
                temp=list(board)
                temp[i]='W'
                if self.is_close_mill(i, temp):
                    w_config+=1
                temp[i]='B'
                if self.is_close_mill(i, temp):
                    b_config+=1
        return w_config-b_config

    def check_win(self, board):
        num_white_pieces=0
        num_black_pieces=0
        for i in range(len(board)):
            if board[i]=='W':
                num_white_pieces+=1
            if board[i]=='B':
                num_black_pieces+=1

        possible_black_moves_count=len(self.generate_moves_midgame_endgame(board, 'B'))
        possible_white_moves_count=len(self.generate_moves_midgame_endgame(board, 'W'))

        if num_white_pieces==2 or possible_white_moves_count==0:
            return -1
        if num_black_pieces==2 or possible_black_moves_count==0:
            return 1
        return 0

    def static_estimation(self, board):
        self.static_estimation_count+=1
        return 26*self.count_number_of_morris(board)\
               +1*self.count_number_of_blocked_pieces(board)\
               +9*self.count_number_of_pieces(board)\
               +10*self.count_two_pieces_config(board)

    def generate_remove(self, board, L):
        add=False
        for i in range(len(board)):
            if board[i]=='B':
                if self.is_close_mill(i, board)==False:
                    board_temp=list(board)
                    board_temp[i]='x'
                    L.append(board_temp)
                    add=True
        if add==False:
            L.append(board)

    def generate_add(self, board):
        L=[]
        for i in range(len(board)):
            if board[i]=='x':
                board_temp=list(board)
                board_temp[i]='W'
                if (self.is_close_mill(i, board_temp)):
                    self.generate_remove(board_temp, L)
                else:
                    L.append(board_temp)
        return L

    def generate_moves_opening(self, board, color):
        if color=='W':
            return self.generate_add(board)
        elif color=='B':
            temp=list(board)
            self.swap_color(temp)
            ret=self.generate_add(temp)
            for l in ret:
                self.swap_color(l)
        return ret

    def swap_color(self, board):
        for c in range(len(board)):
            if board[c]=='W':
                board[c]='B'
            elif board[c]=='B':
                board[c]='W'

    def count_close_mill(self, b):
        L=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17]
        w_cnt=0
        b_cnt=0
        for j in L:
            C=b[j]
            if C=='x':
                continue
            if j==0:
                if b[2]==C and b[4]==C:
                    if C=='W':
                        w_cnt+=1
                    elif C=='B':
                        b_cnt+=1
                    if 2 in L:
                        L.remove(2)
                    if 4 in L:
                        L.remove(4)
            elif j==1:
                if b[3]==C and b[5]==C:
                    if C=='W':
                        w_cnt+=1
                    elif C=='B':
                        b_cnt+=1
                    if 3 in L:
                        L.remove(3)
                    if 5 in L:
                        L.remove(5)
                if b[8]==C and b[17]==C:
                    if C=='W':
                        w_cnt+=1
                    elif C=='B':
                        b_cnt+=1
                    if 8 in L:
                        L.remove(8)
                    if 17 in L:
                        L.remove(17)
            elif j==2:
                if b[0]==C and b[4]==C:
                    if C=='W':
                        w_cnt+=1
                    elif C=='B':
                        b_cnt+=1
                    if 0 in L:
                        L.remove(0)
                    if 4 in L:
                        L.remove(4)
            elif j==3:
                if b[7]==C and b[14]==C:
                    if C=='W':
                        w_cnt+=1
                    elif C=='B':
                        b_cnt+=1
                    if 7 in L:
                        L.remove(7)
                    if 14 in L:
                        L.remove(14)
                if b[1]==C and b[5]==C:
                    if C=='W':
                        w_cnt+=1
                    elif C=='B':
                        b_cnt+=1
                    if 1 in L:
                        L.remove(1)
                    if 5 in L:
                        L.remove(5)
            elif j==4:
                if b[0]==C and b[2]==C:
                    if C=='W':
                        w_cnt+=1
                    elif C=='B':
                        b_cnt+=1
                    if 0 in L:
                        L.remove(0)
                    if 2 in L:
                        L.remove(2)
            elif j==5:
                if b[1]==C and b[3]==C:
                    if C=='W':
                        w_cnt+=1
                    elif C=='B':
                        b_cnt+=1
                    if 1 in L:
                        L.remove(1)
                    if 3 in L:
                        L.remove(3)
                if b[6]==C and b[11]==C:
                    if C=='W':
                        w_cnt+=1
                    elif C=='B':
                        b_cnt+=1
                    if 6 in L:
                        L.remove(6)
                    if 11 in L:
                        L.remove(11)
            elif j==6:
                if b[5]==C and b[11]==C:
                    if C=='W':
                        w_cnt+=1
                    elif C=='B':
                        b_cnt+=1
                    if 5 in L:
                        L.remove(5)
                    if 11 in L:
                        L.remove(11)
                if b[7]==C and b[8]==C:
                    if C=='W':
                        w_cnt+=1
                    elif C=='B':
                        b_cnt+=1
                    if 7 in L:
                        L.remove(7)
                    if 8 in L:
                        L.remove(8)
            elif j==7:
                if b[6]==C and b[8]==C:
                    if C=='W':
                        w_cnt+=1
                    elif C=='B':
                        b_cnt+=1
                    if 6 in L:
                        L.remove(6)
                    if 8 in L:
                        L.remove(8)
                if b[3]==C and b[14]==C:
                    if C=='W':
                        w_cnt+=1
                    elif C=='B':
                        b_cnt+=1
                    if 3 in L:
                        L.remove(3)
                    if 14 in L:
                        L.remove(14)
            elif j==8:
                if b[6]==C and b[7]==C:
                    if C=='W':
                        w_cnt+=1
                    elif C=='B':
                        b_cnt+=1
                    if 6 in L:
                        L.remove(6)
                    if 7 in L:
                        L.remove(7)
                if b[1]==C and b[17]==C:
                    if C=='W':
                        w_cnt+=1
                    elif C=='B':
                        b_cnt+=1
                    if 1 in L:
                        L.remove(1)
                    if 17 in L:
                        L.remove(17)
            elif j==9:
                if b[12]==C and b[15]==C:
                    if C=='W':
                        w_cnt+=1
                    elif C=='B':
                        b_cnt+=1
                    if 12 in L:
                        L.remove(12)
                    if 15 in L:
                        L.remove(15)
                if b[10]==C and b[11]==C:
                    if C=='W':
                        w_cnt+=1
                    elif C=='B':
                        b_cnt+=1
                    if 10 in L:
                        L.remove(10)
                    if 11 in L:
                        L.remove(11)
            elif j==10:
                if b[9]==C and b[11]==C:
                    if C=='W':
                        w_cnt+=1
                    elif C=='B':
                        b_cnt+=1
                    if 9 in L:
                        L.remove(9)
                    if 11 in L:
                        L.remove(11)
                if b[13]==C and b[16]==C:
                    if C=='W':
                        w_cnt+=1
                    elif C=='B':
                        b_cnt+=1
                    if 13 in L:
                        L.remove(13)
                    if 16 in L:
                        L.remove(16)
            elif j==11:
                if b[9]==C and b[10]==C:
                    if C=='W':
                        w_cnt+=1
                    elif C=='B':
                        b_cnt+=1
                    if 9 in L:
                        L.remove(9)
                    if 10 in L:
                        L.remove(10)
                if b[14]==C and b[17]==C:
                    if C=='W':
                        w_cnt+=1
                    elif C=='B':
                        b_cnt+=1
                    if 14 in L:
                        L.remove(14)
                    if 17 in L:
                        L.remove(17)
                if b[5]==C and b[6]==C:
                    if C=='W':
                        w_cnt+=1
                    elif C=='B':
                        b_cnt+=1
                    if 5 in L:
                        L.remove(5)
                    if 6 in L:
                        L.remove(6)
            elif j==12:
                if b[9]==C and b[15]==C:
                    if C=='W':
                        w_cnt+=1
                    elif C=='B':
                        b_cnt+=1
                    if 9 in L:
                        L.remove(9)
                    if 15 in L:
                        L.remove(15)
                if b[13]==C and b[14]==C:
                    if C=='W':
                        w_cnt+=1
                    elif C=='B':
                        b_cnt+=1
                    if 13 in L:
                        L.remove(13)
                    if 14 in L:
                        L.remove(14)
            elif j==13:
                if b[12]==C and b[14]==C:
                    if C=='W':
                        w_cnt+=1
                    elif C=='B':
                        b_cnt+=1
                    if 12 in L:
                        L.remove(12)
                    if 14 in L:
                        L.remove(14)
                if b[10]==C and b[16]==C:
                    if C=='W':
                        w_cnt+=1
                    elif C=='B':
                        b_cnt+=1
                    if 10 in L:
                        L.remove(10)
                    if 16 in L:
                        L.remove(16)
            elif j==14:
                if b[12]==C and b[13]==C:
                    if C=='W':
                        w_cnt+=1
                    elif C=='B':
                        b_cnt+=1
                    if 12 in L:
                        L.remove(12)
                    if 13 in L:
                        L.remove(13)
                if b[11]==C and b[17]==C:
                    if C=='W':
                        w_cnt+=1
                    elif C=='B':
                        b_cnt+=1
                    if 11 in L:
                        L.remove(11)
                    if 17 in L:
                        L.remove(17)
                if b[3]==C and b[7]==C:
                    if C=='W':
                        w_cnt+=1
                    elif C=='B':
                        b_cnt+=1
                    if 3 in L:
                        L.remove(3)
                    if 7 in L:
                        L.remove(7)
            elif j==15:
                if b[9]==C and b[12]==C:
                    if C=='W':
                        w_cnt+=1
                    elif C=='B':
                        b_cnt+=1
                    if 9 in L:
                        L.remove(9)
                    if 12 in L:
                        L.remove(12)
                if b[16]==C and b[17]==C:
                    if C=='W':
                        w_cnt+=1
                    elif C=='B':
                        b_cnt+=1
                    if 16 in L:
                        L.remove(16)
                    if 17 in L:
                        L.remove(17)
            elif j==16:
                if b[15]==C and b[17]==C:
                    if C=='W':
                        w_cnt+=1
                    elif C=='B':
                        b_cnt+=1
                    if 15 in L:
                        L.remove(15)
                    if 17 in L:
                        L.remove(17)
                if b[10]==C and b[13]==C:
                    if C=='W':
                        w_cnt+=1
                    elif C=='B':
                        b_cnt+=1
                    if 10 in L:
                        L.remove(10)
                    if 13 in L:
                        L.remove(13)
            elif j==17:
                if b[15]==C and b[16]==C:
                    if C=='W':
                        w_cnt+=1
                    elif C=='B':
                        b_cnt+=1
                    if 15 in L:
                        L.remove(15)
                    if 16 in L:
                        L.remove(16)
                if b[1]==C and b[8]==C:
                    if C=='W':
                        w_cnt+=1
                    elif C=='B':
                        b_cnt+=1
                    if 1 in L:
                        L.remove(1)
                    if 8 in L:
                        L.remove(8)
                if b[11]==C and b[14]==C:
                    if C=='W':
                        w_cnt+=1
                    elif C=='B':
                        b_cnt+=1
                    if 11 in L:
                        L.remove(11)
                    if 14 in L:
                        L.remove(14)
        return w_cnt, b_cnt

    def is_close_mill(self, j, b):
        C=b[j]
        if (C=='x'):
            print('is_close_mill: Wrong input')
            return
        if j==0:
            return b[2]==C and b[4]==C
        elif j==1:
            return (b[3]==C and b[5]==C) or (b[8]==C and b[17]==C)
        elif j==2:
            return b[0]==C and b[4]==C
        elif j==3:
            return (b[7]==C and b[14]==C) or (b[1]==C and b[5]==C)
        elif j==4:
            return b[0]==C and b[2]==C
        elif j==5:
            return (b[1]==C and b[3]==C) or (b[6]==C and b[11]==C)
        elif j==6:
            return (b[5]==C and b[11]==C) or (b[7]==C and b[8]==C)
        elif j==7:
            return (b[6]==C and b[8]==C) or (b[3]==C and b[14]==C)
        elif j==8:
            return (b[6]==C and b[7]==C) or (b[1]==C and b[17]==C)
        elif j==9:
            return (b[12]==C and b[15]==C) or (b[10]==C and b[11]==C)
        elif j==10:
            return (b[9]==C and b[11]==C) or (b[13]==C and b[16]==C)
        elif j==11:
            return (b[9]==C and b[10]==C) or (b[14]==C and b[17]==C) or (b[5]==C and b[6]==C)
        elif j==12:
            return (b[9]==C and b[15]==C) or (b[13]==C and b[14]==C)
        elif j==13:
            return (b[12]==C and b[14]==C) or (b[10]==C and b[16]==C)
        elif j==14:
            return (b[12]==C and b[13]==C) or (b[11]==C and b[17]==C) or (b[3]==C and b[7]==C)
        elif j==15:
            return (b[9]==C and b[12]==C) or (b[16]==C and b[17]==C)
        elif j==16:
            return (b[15]==C and b[17]==C) or (b[10]==C and b[13]==C)
        elif j==17:
            return (b[15]==C and b[16]==C) or (b[1]==C and b[8]==C) or (b[11]==C and b[14]==C)
        else:
            print('Wrong input\n')

    def get_neighbor(self, j):
        if j==0:
            return [1, 2, 15]
        elif j==1:
            return [0, 3, 8]
        elif j==2:
            return [0, 3, 4, 12]
        elif j==3:
            return [1, 2, 5, 7]
        elif j==4:
            return [2, 5, 9]
        elif j==5:
            return [3, 4, 6]
        elif j==6:
            return [5, 7, 11]
        elif j==7:
            return [3, 6, 8, 14]
        elif j==8:
            return [1, 7, 17]
        elif j==9:
            return [4, 10, 12]
        elif j==10:
            return [9, 11, 13]
        elif j==11:
            return [6, 10, 14]
        elif j==12:
            return [2, 9, 13, 15]
        elif j==13:
            return [10, 12, 14, 16]
        elif j==14:
            return [7, 11, 13, 17]
        elif j==15:
            return [0, 12, 16]
        elif j==16:
            return [13, 15, 17]
        elif j==17:
            return [8, 14, 16]
        else:
            print('Wrong input')

    def minimax_opening(self, board, depth, color):
        ret=self.node(-10001, ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'])
        if color=='W':
            possible_board=self.generate_moves_opening(board, 'W')
        elif color=='B':
            possible_board=self.generate_moves_opening(board, 'B')
        if len(possible_board)==0:
            depth=0
        if depth==0:
            ret.est=self.static_estimation(board)
            ret.board=board
        elif color=='W':  #MAXMIN
            ret.est=-10000
            for b in possible_board:
                temp=self.minimax_opening(b, depth-1, 'B')
                if temp.est>ret.est:
                    ret.est=temp.est
                    ret.board=b
        elif color=='B':    #MINMAX
            ret.est=10000
            for b in possible_board:
                temp=self.minimax_opening(b, depth-1, 'W')
                if temp.est<ret.est:
                    ret.est=temp.est
                    ret.board=b
        else:
            print('Wrong input')
        return ret

if __name__ == "__main__":
    depth=input("Please enter the depth (ply):")
    input_file_name='board1.txt'
    output_file_name='board2.txt'
    g=board_game()
    g.get_file_input(input_file_name)
    opt=g.minimax_opening(g.board_position, int(depth), 'W')
    open(output_file_name, 'w').close()   #Clear file content
    f=open(output_file_name, 'a')
    for c in opt.board:
        f.write(c)
    f.close()

    print('Board position: ', g.board_position)
    print('Positions evaluated by static estimation: ', g.static_estimation_count)
    print('MINIMAX estimate:', opt.est)

