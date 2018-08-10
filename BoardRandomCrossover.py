from random import shuffle,randint,sample
from copy import deepcopy


class BoardRandomCrossover:

    def __init__(self,N=8):
        #self.state = list(range(N))
        #shuffle(self.state)
        self.board_size = N
        self.state = [randint(0,self.board_size-1) for _ in range(self.board_size)]

    def printState(self):
        board = ''
        for i in range(self.board_size):
            blank = ['0 ']*self.board_size
            blank[self.state[i]] = '█ '
            blank = ''.join(blank)+'\n'
            board += blank
        print(board)


    def mutate(self):
        row = randint(0,self.board_size-1)
        col = randint(0,self.board_size-1)
        self.state[row] = col

    def fitnessFunction(self):
        pairs = 0
        for i in range(self.board_size):
            for j in range(i+1,self.board_size):
                if self.state[j]==self.state[i]:
                    pairs += 1
                if abs((self.state[j]-self.state[i]))==(j-i):
                    pairs += 1
        return(pairs)


    def isSameBoard(self,other_board):
        return(self.state==other_board.state)


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

        return(newboard_1,newboard_2)








#
