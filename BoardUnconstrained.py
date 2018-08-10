from random import shuffle,randint,sample
from copy import deepcopy


class BoardUnconstrained:

    def __init__(self,N=8):
        #self.state = list(range(N))
        #shuffle(self.state)
        self.board_size = N

        self.state = []
        queens_left = N
        while queens_left>0:
            row = randint(0,self.board_size-1)
            col = randint(0,self.board_size-1)
            if (row,col) not in self.state:
                self.state.append((row,col))
                queens_left -= 1
        self.state = sorted(self.state)


    def printState(self):
        board = []
        for i in range(self.board_size):
            blank = ['0 ']*self.board_size
            board.append(blank)
        for q_pos in self.state:
            board[q_pos[0]][q_pos[1]] = '█ '
        for i in range(self.board_size):
            board[i] = ''.join(board[i])+'\n'
        board = ''.join(board)
        print(board)

    def positionFree(self,pos_tuple):
        if pos_tuple not in self.state:
            return(True)
        else:
            return(False)

    def mutate(self):
        index = randint(0,self.board_size-1)
        while True:
            row = randint(0,self.board_size-1)
            col = randint(0,self.board_size-1)
            if self.positionFree((row,col)):
                self.state[index] = (row,col)
                break
        self.state = sorted(self.state)

    def fitnessFunction(self):
        pairs = 0
        for i in range(self.board_size):
            for j in range(i+1,self.board_size):
                if (self.state[j][0]==self.state[i][0]) or (self.state[j][1]==self.state[i][1]):
                    pairs += 1
                if abs((self.state[j][0]-self.state[i][0]))==abs((self.state[j][1]-self.state[i][1])):
                    pairs += 1
        return(pairs)


    def isSameBoard(self,other_board):
        return(set(self.state)==set(other_board.state))


    def mate(self,other_board):
        newboard_1 = deepcopy(self)
        newboard_2 = deepcopy(other_board)
        #exclusive, inclusive
        N_switch = randint(0,self.board_size-1)
        switch_indices = sample(list(range(self.board_size)),N_switch)

        for index in switch_indices:
            temp = newboard_1.state[index]
            newboard_1.state[index] = newboard_2.state[index]
            newboard_2.state[index] = temp

        newboard_1.state = sorted(newboard_1.state)
        newboard_2.state = sorted(newboard_2.state)
        return(newboard_1,newboard_2)








#
