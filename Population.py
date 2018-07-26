import matplotlib.pyplot as plt
from time import sleep
from Board import Board
from random import randint
from copy import deepcopy
from datetime import datetime


class Population:

    def __init__(self,popsize=20,boardsize=8):
        self.popsize = popsize
        self.population = [Board(boardsize) for i in range(self.popsize)]
        self.sorted_population = None

    def printPop(self):
        print('\nPopulation:')
        [print(board.board_state) for board in self.population]
        print('\n\n')

    def printAttackPairs(self):
        for board in self.population:
            board.printBoard()
            print(board.attackingPairs())


    def sortBoards(self):
        boards_fitness = [(board,board.attackingPairs(),'old') for board in self.population]
        boards_fitness = sorted(boards_fitness,key=lambda x: x[1])
        #print(boards_fitness)
        self.sorted_population = boards_fitness

    def sortTupleByFitness(self,tuple_list):
        return(sorted(tuple_list,key=lambda x: x[1]))

    def getBestAndMean(self):
        if self.sorted_population is None:
            return((0,0))

        best = self.sorted_population[0][1]
        mean = sum([boardfitness[1] for boardfitness in self.sorted_population])/(1.0*len(self.population))
        return((best,mean))

    def mate(self,board1,board2):

        board1 = deepcopy(board1)
        board2 = deepcopy(board2)

        crossover = randint(1,board1.board_size-1)

        temp = board1.board_state[:crossover]
        board1.board_state[:crossover] = board2.board_state[:crossover]
        board2.board_state[:crossover] = temp

        return(board1,board2)


    def deleteDupes(self,pop):
        #Might have to be careful here -- what happens if you delete so many dupes that the pop size is smaller than original?
        #Pass it just a list of boards. But remember that you have to look at board.board_state
        #return(list(set(pop)))

        unique_boards = []
        no_dupes = []
        for i,ind1 in enumerate(pop):
            if ind1.board_state not in unique_boards:
                unique_boards.append(ind1.board_state)
                no_dupes.append(ind1)

        return(no_dupes)

    def mateGrid(self):

        new_boards = []

        #Mating scheme
        for i in range(self.popsize):
            for j in range(i+1,self.popsize):
                b1,b2 = self.mate(self.population[i],self.population[j])
                new_boards.append(b1)
                new_boards.append(b2)

        old_and_new_boards = deepcopy(self.population) + new_boards
        [board.mutate() for board in old_and_new_boards]
        self.population = self.deleteDupes(old_and_new_boards + self.population)

        self.sortBoards()
        self.sorted_population = self.sorted_population[:self.popsize]
        self.population = [tuple[0] for tuple in self.sorted_population]







    def plotEvolve(self):



        reproduction_steps = 550

        gen = []
        best = []
        mean = []

        fig = plt.figure()
        fig.show()
        fig.canvas.draw()

        found = False

        for i in range(reproduction_steps):
            self.sortBoards()
            cur_best,cur_mean = self.getBestAndMean()

            gen.append(i)
            best.append(cur_best)
            mean.append(cur_mean)

            if cur_best==0 and not found:
                print('found solution!\n')
                self.sorted_population[0][0].printBoard()
                found = True

            fig.clear()
            plt.xlabel('# generations')
            plt.ylabel('fitness function')
            plt.plot(gen,best,label='best')
            plt.plot(gen,mean,label='mean')
            plt.legend()
            fig.canvas.draw()

            self.mateGrid()


        date_string = datetime.now().strftime("%H-%M-%S")
        plt.savefig('evolve_output_' + date_string + '.png')



        print('\n\nending pop:\n')
        [print(tuple[1],tuple[0].board_state) for tuple in self.sorted_population]

#

#scrap

'''





'''
