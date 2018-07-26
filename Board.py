from random import shuffle,randint

class Board:

    def __init__(self,N=8):
        #self.board_state = list(range(N))
        #shuffle(self.board_state)
        self.board_size = N
        self.board_state = [randint(0,self.board_size-1) for _ in range(self.board_size)]

    def printBoard(self):
        board = ''
        for i in range(self.board_size):
            blank = ['0 ']*self.board_size
            blank[self.board_state[i]] = '█ '
            blank = ''.join(blank)+'\n'
            board += blank

        print(board)


    def mutate(self):
        row = randint(0,self.board_size-1)
        col = randint(0,self.board_size-1)
        self.board_state[row] = col


    def attackingPairs(self):

        pairs = 0
        for i in range(self.board_size):
            for j in range(i+1,self.board_size):
                if self.board_state[j]==self.board_state[i]:
                    pairs += 1
                if abs((self.board_state[j]-self.board_state[i]))==(j-i):
                    pairs += 1


        return(pairs)



    def isSameBoard(self,other_board):
        return(self.board_state==other_board.board_state)











#
