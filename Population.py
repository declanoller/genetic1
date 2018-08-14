import matplotlib.pyplot as plt
from time import sleep
from random import randint
from copy import deepcopy
from datetime import datetime
import numpy as np

'''
The object must have the following functions or attributes:
-fitnessFunction()
-mutate()
-isSame()
-mate()
-state (maybe change to getState()?)
'''

class Population:

    def __init__(self,individ_class,popsize,**kwargs):


        self.kwargs_str = '__'.join(['{}={}'.format(x[0],x[1]) for x in kwargs.items()])
        print(self.kwargs_str)

        self.individ_class = individ_class
        print('using',individ_class.__name__,'class')
        self.class_name = individ_class.__name__
        self.popsize = popsize
        self.population = [self.createNewIndivid(**kwargs) for i in range(self.popsize)]
        self.sorted_population = None

    def createNewIndivid(self, **kwargs):
        return(self.individ_class(**kwargs))

    def printPop(self):
        print('\nPopulation:')
        [print(individ.state) for individ in self.population]
        print('\n\n')

    def printFitnessFunctions(self):
        for individ in self.population:
            individ.printState()
            print(individ.fitnessFunction())

    def sortIndivids(self):
        individs_fitness = [(individ,individ.fitnessFunction(),'old') for individ in self.population]
        individs_fitness = sorted(individs_fitness,key=lambda x: x[1])
        #print(individs_fitness)
        self.sorted_population = individs_fitness

    def sortTupleByFitness(self,tuple_list):
        return(sorted(tuple_list,key=lambda x: x[1]))

    def getBestAndMean(self):
        if self.sorted_population is None:
            return((0,0))

        best = self.sorted_population[0][1]
        mean = sum([individfitness[1] for individfitness in self.sorted_population])/(1.0*len(self.population))
        return((best,mean))

    def deleteDupes(self,pop):
        #Might have to be careful here -- what happens if you delete so many dupes that the pop size is smaller than original?
        #Pass it just a list of individs. But remember that you have to look at individ.state
        #return(list(set(pop)))

        unique_individs = []
        no_dupes = []
        for i,ind1 in enumerate(pop):
            #if ind1.state not in unique_individs:
            is_not_unique = np.any([ind1.isSameState(other) for other in no_dupes])
            if not is_not_unique:
                unique_individs.append(ind1.state)
                no_dupes.append(ind1)

        return(no_dupes)

    def mateGrid(self):

        new_individs = []

        #Mating scheme
        for i in range(self.popsize):
            for j in range(i+1,self.popsize):
                b1,b2 = self.population[i].mate(self.population[j])
                #b1,b2 = self.mate(self.population[i],self.population[j])
                new_individs.append(b1)
                new_individs.append(b2)

        old_and_new_individs = deepcopy(self.population) + new_individs
        [individ.mutate() for individ in old_and_new_individs]
        self.population = self.deleteDupes(old_and_new_individs + self.population)

        self.sortIndivids()
        self.sorted_population = self.sorted_population[:self.popsize]
        self.population = [tuple[0] for tuple in self.sorted_population]







    def plotEvolve(self,generations = 550,state_plot_obj = None):



        if state_plot_obj is None:
            fig = plt.figure()
            axis = plt.gca()
            print('no subplot')
        else:
            fig, axes = plt.subplots(2,1,figsize=(8,10))
            axis = axes[0]

        fig.show()

        found = False
        gen = []
        best = []
        mean = []
        cur_best,cur_mean = 0,0

        method_list = [func for func in dir(self.individ_class) if callable(getattr(self.individ_class, func))]


        for i in range(generations):
            #print(i)
            self.sortIndivids()
            cur_best,cur_mean = self.getBestAndMean()

            gen.append(i)
            best.append(cur_best)
            mean.append(cur_mean)

            if 'solFound' in method_list:
                if self.sorted_population[0][0].solFound():
                    print('found solution in generation {}!\n'.format(i))
                    if 'printState' in method_list:
                        self.sorted_population[0][0].printState()
                    break

            axis.clear()
            axis.set_xlabel('# generations')
            axis.set_ylabel('fitness function')
            axis.plot(gen,best,label='best')
            axis.plot(gen,mean,label='mean')
            axis.legend()

            axis.text(.6*i,.8*max(best),'best: {:.3f}\nmean: {:.3f}'.format(cur_best,cur_mean))

            if state_plot_obj is not None:
                state_plot_obj.copyState(self.sorted_population[0][0])
                state_plot_obj.plotState(plot_axis=axes[1])


            fig.canvas.draw()

            self.mateGrid()


        date_string = datetime.now().strftime("%H-%M-%S")
        plt.savefig('evolve_' + self.class_name + '__pop=' + str(self.popsize) + '__gen=' + str(generations) + '__' + self.kwargs_str + '__' + date_string + '.png')

        print('\n\nending pop:\n')
        #[print(tuple[1],tuple[0].state) for tuple in self.sorted_population]

        print('\nending mean:',cur_mean)

        return(self.sorted_population[0][0])


    def evolve(self,generations = 550):



        #generations = 550

        gen = []
        best = []
        mean = []

        found = False

        cur_best,cur_mean = 0,0

        for i in range(generations):
            self.sortIndivids()
            cur_best,cur_mean = self.getBestAndMean()

            gen.append(i)
            best.append(cur_best)
            mean.append(cur_mean)

            if cur_best==0 and not found:
                print('found solution in generation {}!\n'.format(i))
                self.sorted_population[0][0].printState()
                found = True


            self.mateGrid()


        date_string = datetime.now().strftime("%H-%M-%S")

        print('\n\nending pop:\n')
        [print(tuple[1],tuple[0].state) for tuple in self.sorted_population]

        print('\nending mean:',cur_mean)
#

#scrap

'''





'''
