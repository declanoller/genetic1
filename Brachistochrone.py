from random import shuffle,randint,sample,random
from copy import deepcopy
import matplotlib.pyplot as plt
import numpy as np
from math import sqrt

class Brachistochrone:

    def __init__(self,N=20,height=1.0):
        #height is as a ratio of the width.
        #N is the number of *segments*, that is, "blocks", not points (which will be N+1).
        #The state is the height of each point, so will be length N+1.
        #To make things easy, I'll also have an xpos list.
        self.N_segments = N
        self.width = 1.0
        self.height = height
        self.state = [self.height]
        self.xpos = [0]
        self.delta_x = self.width/self.N_segments

        for i in range(self.N_segments-1):
            self.xpos.append((i+1)*self.delta_x)
            self.state.append(random()*self.height)

        self.xpos.append(1.0)
        self.state.append(0)

        '''print(self.xpos)
        print(self.state)'''


    def drawPath(self):


        plt.plot(self.xpos,self.state,'bo-')
        plt.show()

    def printState(self):
        board = []
        for i in range(self.N_segments):
            blank = ['0 ']*self.N_segments
            board.append(blank)
        for q_pos in self.state:
            board[q_pos[0]][q_pos[1]] = '█ '
        for i in range(self.N_segments):
            board[i] = ''.join(board[i])+'\n'
        board = ''.join(board)
        print(board)

    def positionFree(self,pos_tuple):
        if pos_tuple not in self.state:
            return(True)
        else:
            return(False)

    def mutate(self):
        index = randint(0,self.N_segments-1)
        while True:
            row = randint(0,self.N_segments-1)
            col = randint(0,self.N_segments-1)
            if self.positionFree((row,col)):
                self.state[index] = (row,col)
                break
        self.state = sorted(self.state)

    def fitnessFunction(self):

        g = 9.8

        time_sum = 0

        #So if the next point is lower than the previous one, d will be *positive* (i.e., the y axis is down, opposite with the plot axis.)
        d = -np.array([self.state[i+1] - self.state[i] for i in range(self.N_segments)])
        print('len d:',len(d))
        print('d:',d)

        v = sqrt(2*g)*np.sqrt([0] + [sum(d[:(i+1)]) for i in range(len(d))])
        print('len v:',len(v))
        print('v:',v)

        t = np.sqrt(v**2 + 2*g*d)/(g*d/np.sqrt(d**2 + 1))
        print('len t:',len(t))
        print('t:',t)

        vs = []

        for i in range(self.N_segments):

            d = self.state[i+1] - self.state[i]



        #for i in range(self.N_segments):
        return(0)




    def isSameBoard(self,other_board):
        return(set(self.state)==set(other_board.state))


    def mate(self,other_board):
        newboard_1 = deepcopy(self)
        newboard_2 = deepcopy(other_board)
        #exclusive, inclusive
        N_switch = randint(0,self.N_segments-1)
        switch_indices = sample(list(range(self.N_segments)),N_switch)

        for index in switch_indices:
            temp = newboard_1.state[index]
            newboard_1.state[index] = newboard_2.state[index]
            newboard_2.state[index] = temp

        newboard_1.state = sorted(newboard_1.state)
        newboard_2.state = sorted(newboard_2.state)
        return(newboard_1,newboard_2)








#
